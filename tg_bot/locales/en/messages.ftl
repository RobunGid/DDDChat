start =
    { $name ->
        [none] Hello, employee
       *[some] Hello, { $name }
    }
    Welcome to tech support bot
    Usage:
    - <b>/help</b> - get this message
    - <b>/chats</b> - get all current chats
    - <b>/set_chat &lt;chat oid&gt;</b> - connect to certain chat

help =
    Usage:
    - <b>/help</b> - get this message
    - <b>/chats</b> - get all chats
    - <b>/set_chat &lt;chat oid&gt;</b> - connect to certain chat

chat_list_item = 
    { $number }) Title: { $title }
         OID: <code>{ $oid }</code>
         Created at: { $created_at }
		
chats_not_found = No chats were found

set_chat_need_argument =
    Usage:
    - <b>/set_chat &lt;chat oid&gt;</b> - connect to certain chat

set_chat_success = You connected to chat successfully
set_chat_already_connected_fail = You are already connected to this chat
set_chat_not_found_fail = Chat with this oid not found