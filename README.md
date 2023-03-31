# Rolling Tags Discord Bot

Add tags to nicknames based on their roles!

Rolling Tags Discord Bot will allow you to easily assign tags next to the usernames of members of your server based on what roles they are in.

[![Invite to server](https://i.imgur.com/z0ywl9d.png)](https://discord.com/api/oauth2/authorize?client_id=806118748573794385&permissions=134217728&scope=bot)
[![Join support server](https://i.imgur.com/Qkdwub8.png)](https://discord.gg/6J6pbWqqmE)

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

## Bot Configuration

Customize the bot's behavior by appending `key=value` to the bot's main role's name, separating each key-value pair by a space. Use quotes to surround values that have spaces. For example to have Linus' nickname appear as `[#] Linus` you would change the rale `Rolling Tags` to `Rolling Tags fmt="[{t}] {n}"`. Or if you wanted to put a comma between each tag you would change the role to `Rolling Tags sep=,`.

The following settings are supported.

- `sep` - The separator between each tag. Defaults to a single space.
- `fmt` - The format of users' names. `{n}` and `{t}` will be replaced with each user's name and their tags respectively. Defaults to `{n} | {t}`.

## Known Issues

There is no way for the bot to have permission to change the nickname of the owner of a server, so they're the only person who the bot will not affect.
