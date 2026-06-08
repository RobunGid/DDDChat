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
from logic.bus.base import ApplicationBus
from logic.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
    DeleteChatCommand,
)
from logic.init import init_container
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
    bus = container.resolve(ApplicationBus)
    chat: Chat
    chat, *_ = await bus.handle_command(CreateChatCommand(title=schema.title))
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
    cqrs_bus = container.resolve(ApplicationBus)
    message: Message
    message, *_ = await cqrs_bus.handle_command(
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
    cqrs_bus = container.resolve(ApplicationBus)
    chat: Chat = await cqrs_bus.handle_query(GetChatQuery(chat_oid=chat_oid))
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
    application_bus = container.resolve(ApplicationBus)

    messages, count = await application_bus.handle_query(
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
    application_bus = container.resolve(ApplicationBus)

    chats, count = await application_bus.handle_query(
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
    application_bus = container.resolve(ApplicationBus)

    await application_bus.handle_command(DeleteChatCommand(chat_oid=chat_oid))
