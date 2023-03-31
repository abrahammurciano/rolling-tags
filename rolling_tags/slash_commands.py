from discord import Colour, Embed, Interaction, app_commands

from .rolling_tags_client import client

command_tree = app_commands.CommandTree(client)


@command_tree.command(name="help", description="Show instructions for using the bot")  # type: ignore
async def help_command(interaction: Interaction):
    embed = Embed(
        title="Add tags to members based on their roles!",
        colour=Colour.from_rgb(249, 142, 142),
    )

    embed.add_field(
        name="Note:",
        value=(
            "My role must be at the very top for me to be able to do my job properly."
        ),
        inline=False,
    )

    embed.add_field(
        name="Setting tags to roles",
        value=(
            'To add a tag to a role, rename the role to "Role Name | *tag*", and everyone with that role will have that *tag* appended to their name.\n\nYou can use emojis, symbols, words, or anything you like in place of *tag*.\n\nFor example if you rename the role "Superuser" to "Superuser | #", then our buddy Linus, who is a member of that role, will have their name changed to "Linus | #" within the server.'
        ),
        inline=False,
    )

    embed.add_field(
        name="Multiple tags",
        value=(
            "Users belonging to multiple roles which have tags will have all the relevant tags appended to their name. (Note, there is a 32 character limit on names, so avoid long tags.)"
        ),
        inline=False,
    )

    embed.add_field(
        name="Changing Roles/Nicknames",
        value=(
            "Whenever a member's nickname is changed or their roles are changed, the bot automatically reapplies tags."
        ),
        inline=False,
    )

    embed.add_field(
        name="Bot Configuration",
        value=(
            "Customize the bot's behavior by appending `key=value` to the bot's main role's name, separating each key-value pair by a space. Use quotes to surround values that have spaces. For example to have Linus' nickname appear as `[#] Linus` you would change the rale `Rolling Tags` to `Rolling Tags fmt=\"[{t}] {n}\"`. Or if you wanted to put a comma between each tag you would change the role to `Rolling Tags sep=,`.\n\nThe following settings are supported.\n\n- `sep` - The separator between each tag. Defaults to a single space.\n- `fmt` - The format of users' names. `{n}` and `{t}` will be replaced with each user's name and their tags respectively. Defaults to `{n} | {t}`."
        ),
        inline=False,
    )

    embed.add_field(
        name="Note:",
        value=(
            "There is currently no way for the bot to change the nickname of the server owner, so they are the only person who will remain unaffected by the bot."
        ),
        inline=False,
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)
