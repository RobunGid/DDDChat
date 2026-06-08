from fastapi import (
    Depends,
    status,
)
from fastapi.routing import APIRouter

from punq import Container

from application.api.messages.filters import (
    GetChatsFiltersSchema,
    GetMessagesFiltersSchema,
)
from application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
    GetChatsQueryResponseSchema,
    GetMessagesQueryResponseSchema,
    ResponseChatSchema,
    ResponseMessageSchema,
)
from application.api.schemas import ErrorSchema
from domain.entities.messages import (
    Chat,
    Message,
)
from logic.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
    DeleteChatCommand,
)
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.messages import (
    GetChatQuery,
    GetChatsQuery,
    GetMessagesQuery,
)

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
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    operation_id="createChat",
)
async def create_chat_handler(
    schema: CreateChatRequestSchema,
    container: Container = Depends(init_container),
) -> CreateChatResponseSchema:
    mediator: Mediator = container.resolve(Mediator)
    chat: Chat
    chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    "/{chat_oid}/messages",
    response_model=CreateMessageResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Endpoint creates new message",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    operation_id="createMessage",
)
async def create_message_handler(
    schema: CreateMessageRequestSchema,
    chat_oid: str,
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    mediator: Mediator = container.resolve(Mediator)
    message: Message
    message, *_ = await mediator.handle_command(
        CreateMessageCommand(text=schema.text, chat_oid=chat_oid),
    )
    return CreateMessageResponseSchema.from_entity(message)


@router.get(
    "/{chat_oid}/",
    status_code=status.HTTP_200_OK,
    description="Get certain chat",
    responses={
        status.HTTP_200_OK: {"model": ResponseChatSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    operation_id="getChat",
)
async def get_chat_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> ResponseChatSchema:
    mediator: Mediator = container.resolve(Mediator)
    chat: Chat = await mediator.handle_query(GetChatQuery(chat_oid=chat_oid))
    return ResponseChatSchema.from_entity(chat)


@router.get(
    "/{chat_oid}/messages",
    status_code=status.HTTP_200_OK,
    description="Get certain chat messages",
    responses={
        status.HTTP_200_OK: {"model": GetMessagesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    operation_id="getChatMessageList",
)
async def get_chat_messages_handler(
    chat_oid: str,
    filters: GetMessagesFiltersSchema = Depends(),
    container: Container = Depends(init_container),
) -> GetMessagesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    messages, count = await mediator.handle_query(
        GetMessagesQuery(chat_oid=chat_oid, filters=filters.to_infrastructure()),
    )

    return GetMessagesQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[ResponseMessageSchema.from_entity(message) for message in messages],
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    description="Get all chats",
    responses={
        status.HTTP_200_OK: {"model": GetChatsQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    operation_id="getChatList",
)
async def get_chats_handler(
    filters: GetChatsFiltersSchema = Depends(),
    container: Container = Depends(init_container),
) -> GetChatsQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    chats, count = await mediator.handle_query(
        GetChatsQuery(filters=filters.to_infrastructure()),
    )
    return GetChatsQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        items=[ResponseChatSchema.from_entity(chat) for chat in chats],
    )


@router.delete(
    "/{chat_oid}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete certain chat",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    operation_id="deleteChat",
)
async def delete_chat_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> None:
    mediator: Mediator = container.resolve(Mediator)

    await mediator.handle_command(DeleteChatCommand(chat_oid=chat_oid))
