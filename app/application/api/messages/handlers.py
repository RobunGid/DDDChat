from typing import Iterable

from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from punq import Container

from application.api.messages.schemas import (
    CreateChatRequestSchema, 
    CreateChatResponseSchema, 
    CreateMessageRequestSchema, 
    CreateMessageResponseSchema,
    ResponseChatSchema
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic.commands.messages import CreateChatCommand, CreateMessageCommand
from logic.init import init_container
from logic.mediator import Mediator
from logic.queries.messages import GetChatQuery

router = APIRouter(
	tags=["Chat"],
)

@router.post(
    "/", 
    response_model=CreateChatResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    description="Endpoint creates new chat, if chat with that title already exists returns error 400",
    responses={
		status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
		status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
	}
)
async def create_chat_handler(
    schema: CreateChatRequestSchema, 
	container: Container=Depends(init_container)
 ) -> CreateChatResponseSchema:
    ''' Creates new chat '''
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"error": exception.message}
		)
    
    return CreateChatResponseSchema.from_entity(chat)

@router.post(
    "/{chat_oid}/messages", 
    response_model=CreateMessageResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    description="Endpoint creates new message",
    responses={
		status.HTTP_201_CREATED: {"model": CreateMessageResponseSchema},
		status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
	}
)
async def create_message_handler(
    schema: CreateMessageRequestSchema, 
    chat_oid: str,
    container: Container=Depends(init_container),
) -> CreateMessageResponseSchema:
    ''' Creates new message '''
    mediator: Mediator = container.resolve(Mediator)
    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_oid=chat_oid)
		)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"error": exception.message}
		)
    
    return CreateMessageResponseSchema.from_entity(message)

@router.get(
	'/{chat_oid}/',
    status_code=status.HTTP_200_OK,
    description="Get certain chat",
    responses={
		status.HTTP_200_OK: {"model": ResponseChatSchema},
		status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}
	}
)
async def get_chat_handler(
    chat_oid: str,
    container: Container=Depends(init_container),
) -> ResponseChatSchema:
    ''' Get chat with messages '''
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat = await mediator.handle_query(GetChatQuery(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail={"error": exception.message}
		)
    
    return ResponseChatSchema.from_entity(chat)