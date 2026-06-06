start =
    { $name ->
        [none] Hello, employee
       *[some] Hello, { $name }
    }
    Welcome to tech support bot
    Usage:
    - <b>/help</b> - get this message
    - <b>/chats</b> - get all current chats
    - <b>/add_chat &lt;chat oid&gt;</b> - add connection to specific chat
    - <b>/start_dialog</b> - start dialog to reply to users

help =
    Usage:
    - <b>/help</b> - get this message
    - <b>/chats</b> - get all chats
    - <b>/add_chat &lt;chat oid&gt;</b> - add connection to certain chat
    - <b>/start_dialog</b> - start dialog to reply to users

chat_list_item = 
    { $number }) Title: { $title }
         OID: <code>{ $oid }</code>
         Created at: { $created_at }
		
chats_not_found = No chats were found

add_chat_need_argument =
    Usage:
    - <b>/add_chat &lt;chat oid&gt;</b> - add connection to certain chat

add_chat_success = You are listening to chat successfully
add_chat_already_connected_fail = You already listens to this chat
add_chat_not_found_fail = Chat with this oid not found

start_dialog_success = 
    You are connected to dialog now. 
    Reply to specific messages so the user can see replies
