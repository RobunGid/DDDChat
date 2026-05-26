from fastapi import status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException

from application.api.dependencies.containers import container
from application.api.messages.schemas import CreateChatRequestSchema, CreateChatResponseSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand
from logic.mediator import Mediator

router = APIRouter(
	tags=["Chat"],
)

@router.post("/", response_model=CreateChatResponseSchema)
async def create_chat_handler(schema: CreateChatRequestSchema):
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(statuc_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message})
    
    return CreateChatResponseSchema.from_entity(chat)