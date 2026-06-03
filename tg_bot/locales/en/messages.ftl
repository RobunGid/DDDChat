start =
    { $name ->
        [none] Hello, employee
       *[some] Hello, { $name }
    }
    Welcome to tech support bot
    Usage:
    - <b>/help</b> - get this message
    - <b>/chats</b> - get all current chats
    - <b>/set_chats &lt;chat oid&gt;</b> - connect to certain chat

help =
    Usage:
    - <b>/help</b> - get this message
    - <b>/chats</b> - get all chats
    - <b>/set_chats &lt;chat oid&gt;</b> - connect to certain chat

chat_list_item = 
    { $number }) Title: { $title }
         OID: <code>{ $oid }</code>
         Created at: { $created_at }
		
chats_not_found = No chats were found