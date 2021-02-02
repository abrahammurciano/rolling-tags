# Rolling Tags Discord Bot

Add tags to nicknames based on their roles!

Rolling Tags Discord Bot will allow you to easily assign tags next to the usernames of members of your server based on what roles they are in.

[![Invite to server](https://i.imgur.com/z0ywl9d.png)](https://discord.com/api/oauth2/authorize?client_id=806118748573794385&permissions=134217728&scope=bot)

## Example

![Example](https://i.imgur.com/zpnIsnQ.png)

## Setting tags to roles

To add a tag to a role, rename the role to "Role Name | _tag_", and everyone with that role will have that _tag_ appended to their name.

You can use emojis, symbols, words, or anything you like in place of _tag_.

For example if you rename the role "Superuser" to "Superuser | #", then our buddy Linus, who is a member of that role, will have their name changed to "Linus | #" within the server.

## Multiple tags

Users belonging to multiple roles which have tags will have all the relevant tags appended to their name. (Note, there is a 32 character limit on names, so avoid long tags.)

## Changing Roles/Nicknames

Whenever a member's nickname is changed or their roles are changed, the bot automatically reapplies tags.
