# Ticket-bot-discord
Ticket message reactive discord bot using cogs

Ticket bot based on: https://github.com/ifisq/discord-ticket-system

Commands:  
-create_ticket: Creates a message in the channel where it is written, which when reacted to by users, creates a chat in the same category  
-close: It closes the ticket channel  
-addsupport <role_id> <mentionRole="true">: Adds a role to the support team. It is added to mention role by defect. (admin-level command).  
-delsupport <role_id>: Removes role from support team. (admin-level command).  
-addmentionrole <role_id>: This command adds a role to the list of mentioned roles. (admin-level command).  
-delmentionrole <role_id>: This command removes a role from the list of mentioned roles. (admin-level command).  

Features:  
-Message to create ticket that users can react to create a private chat  
-Add a support team by adding roles  
-Mention roles wen creating new tickets  
-Close tickets  
