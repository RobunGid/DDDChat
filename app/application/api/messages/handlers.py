from fastapi import (
    Depends,
    status,
)
from fastapi.exceptions import HTTPException
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
    GetListenersQueryResponseSchema,
    GetMessagesQueryResponseSchema,
    RequestAddTelegramListenerSchema,
    ResponseAddTelegramListenerSchema,
    ResponseChatSchema,
    ResponseListenerSchema,
    ResponseMessageSchema,
)
from application.api.schemas import ErrorSchema
from domain.entities.messages import (
    Chat,
    Message,
)
from domain.exceptions.base import ApplicationException
from logic.commands.messages import (
    AddTelegramSupportListenerCommand,
    CreateChatCommand,
    CreateMessageCommand,
    DeleteChatCommand,
)
from logic.init import init_container
from logic.mediator.base import Mediator
from logic.queries.messages import (
    GetChatListenersQuery,
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
    try:
        chat: Chat
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

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
    try:
        message: Message
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_oid=chat_oid),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
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
    try:
        chat: Chat = await mediator.handle_query(GetChatQuery(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

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

    try:
        messages, count = await mediator.handle_query(
            GetMessagesQuery(chat_oid=chat_oid, filters=filters.to_infrastructure()),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
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

    try:
        chats, count = await mediator.handle_query(
            GetChatsQuery(filters=filters.to_infrastructure()),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
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

    try:
        await mediator.handle_command(DeleteChatCommand(chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )


@router.post(
    "/{chat_oid}/",
    status_code=status.HTTP_201_CREATED,
    description="Add telegram support listener to chat",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
        status.HTTP_201_CREATED: {"model": ResponseAddTelegramListenerSchema},
    },
    response_model=ResponseAddTelegramListenerSchema,
    operation_id="addTelegramListenerToChat",
)
async def add_telegram_support_listener_handler(
    chat_oid: str,
    schema: RequestAddTelegramListenerSchema,
    container: Container = Depends(init_container),
) -> ResponseAddTelegramListenerSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        chat_listener, *_ = await mediator.handle_command(
            AddTelegramSupportListenerCommand(chat_oid=chat_oid, telegram_chat_id=schema.telegram_chat_id),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return ResponseAddTelegramListenerSchema.from_entity(chat_listener)


@router.get(
    "/{chat_oid}/listeners",
    status_code=status.HTTP_200_OK,
    description="Get certain chat listeners",
    responses={
        status.HTTP_200_OK: {"model": GetListenersQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    operation_id="getChatListenersList",
)
async def get_chat_listeners_handler(
    chat_oid: str,
    container: Container = Depends(init_container),
) -> GetListenersQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        listeners = await mediator.handle_query(
            GetChatListenersQuery(
                chat_oid=chat_oid,
            ),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    # TODO: make pagination
    return GetListenersQueryResponseSchema(
        items=[ResponseListenerSchema.from_entity(listener) for listener in listeners],
        count=-1,
        limit=-1,
        offset=-1,
    )
