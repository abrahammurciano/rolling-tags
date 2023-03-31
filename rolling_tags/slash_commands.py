from typing import Iterable

from discord import Colour, Embed, Interaction, app_commands

from .rolling_tags_client import client

command_tree = app_commands.CommandTree(client)


@command_tree.command(name="help")  # type: ignore
@app_commands.rename(show="show_to_everyone")
async def help_command(interaction: Interaction, show: bool = True):
    """Show instructions on how to use the bot.

    Args:
        interaction: The interaction that triggered the command.
        show: Whether to show the help message to everyone or just you.
    """
    embeds = []

    def add_section(
        title: str,
        body: str,
        *,
        subsections: Iterable[tuple[str, str]] = (),
        image: str = "",
    ):
        embed = Embed(
            title=title,
            description=body,
            colour=Colour.from_rgb(249, 142, 142),
            url=f"https://github.com/abrahammurciano/rolling-tags#{title.lower().replace(' ', '-').replace('/', '')}",
        )
        for subsection_title, subsection_body in subsections:
            embed.add_field(name=subsection_title, value=subsection_body, inline=False)
        if image:
            embed.set_image(url=image)
        embeds.append(embed)

    add_section(
        "Rolling Tags Discord Bot",
        "Add tags to members based on their roles!\nRolling Tags Discord Bot will allow you to easily assign tags next to the usernames of members of your server based on what roles they are in.",
    )

    add_section(
        "Example",
        "Here, user `Captain Jack Sparrow` who has the role of `Pirate | 💀` had their nickname automatically changed to `Captain Jack Sparrow | 💀`.",
        image="https://i.imgur.com/zpnIsnQ.png",
    )

    add_section(
        "Setting tags to roles",
        'To add a tag to a role, rename the role to "Role Name | *tag*", and everyone with that role will have that *tag* appended to their name.\n\nYou can use emojis, symbols, words, or anything you like in place of *tag*.\n\nFor example if you rename the role "Superuser" to "Superuser | #", then our buddy Linus, who is a member of that role, will have their name changed to "Linus | #" within the server.',
    )

    add_section(
        "Multiple tags",
        "Users belonging to multiple roles which have tags will have all the relevant tags appended to their name in order. (Note, there is a 32 character limit on names, so avoid long tags.)",
    )

    add_section(
        "Changing Roles/Nicknames",
        "Whenever a member's nickname is changed or their roles are changed, the bot automatically reapplies tags.",
    )

    add_section(
        "Bot Configuration",
        "Customize the bot's behavior by appending `key=value` to the bot's main role's name, separating each key-value pair by a space. Use quotes to surround values that have spaces.\n"
        'For example to have Linus\' nickname appear as `[#] Linus` you would change the rale `Rolling Tags` to `Rolling Tags fmt="[{t}] {n}"`. Or if you wanted to put a comma between each tag you would change the role to `Rolling Tags sep=,`.\n\n**The following settings are supported.**',
        subsections=(
            (
                "`sep`",
                "The separator between each tag. Default is a space.\nUse `sep=` with no value to have no separator.",
            ),
            (
                "`fmt`",
                "The format of users' names. `{n}` and `{t}` will be replaced with each user's name and their tags respectively. Default is `{n} | {t}`.\nFor best results, don't use a format that could match a user's nickname. For example `{n}.{t}` would not be a good format because it could match a user named `Linus.Torvalds`.",
            ),
        ),
    )

    add_section(
        "Known Issues",
        "",
        subsections=(
            (
                "Bot's role must be highest",
                "The bot cannot change the nickname of users who have a higher role than the bot. For the bot to work properly, **make sure the bot's role is highest**.",
            ),
            (
                "Can't change server owner's nickname",
                "There is currently no way for the bot to change the nickname of the server owner, so they are the only person who will remain unaffected by the bot.",
            ),
            (
                "Use a unique format",
                "If a nickname could possibly match the specified format, parts of the nickname may be replaced. For example if you have a user named `Linus.Torvalds` who is a member of the role `Superuser | #`, and you have the format set to `{n}.{t}`, then the bot will change their nickname to `Linus.#`. To avoid this, use more unique formats that are less likely to match a user's nickname.",
            ),
        ),
    )

    await interaction.response.send_message(ephemeral=not show, embeds=embeds)
