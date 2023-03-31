import logging
from collections import defaultdict

from discord import Activity, ActivityType, Client, Guild, Intents, Member, Role

from .guild_settings import GuildSettings
from .member_tagger import MemberTagger
from .role_tagger import RoleTagger

logger = logging.getLogger(__name__)


class RollingTagsClient(Client):
    """The discord client for rolling tags"""

    def __init__(self) -> None:
        intents = Intents.default()
        intents.members = True
        self._guild_settings: dict[Guild, GuildSettings] = defaultdict(GuildSettings)
        super().__init__(intents=intents)

    def run(self, *args, **kwargs) -> None:
        kwargs["log_handler"] = None
        super().run(*args, **kwargs)

    async def _set_presence(self) -> None:
        assert self.user is not None, "Client is not logged in"
        await self.change_presence(
            activity=Activity(
                type=ActivityType.listening,
                name=f"@{self.user.display_name} in {len(self.guilds)} servers. PUT MY ROLE ON TOP!",
            )
        )

    async def on_ready(self) -> None:
        """When discord is connected"""
        from .slash_commands import command_tree

        assert self.user is not None, "Client is not logged in"
        logger.info(f"{self.user.name} has connected to Discord!")
        await self._set_presence()
        self._guild_settings.update(
            (g, GuildSettings.from_guild(g)) for g in self.guilds
        )
        await command_tree.sync()

    async def on_guild_join(self, guild: Guild) -> None:
        """When the bot joins a guild"""
        assert self.user is not None, "Client is not logged in"
        logger.info(f"{self.user.name} has joined {guild.name}")
        await self._set_presence()

    async def on_error(self, *args, **kwargs) -> None:
        """When an error occurs"""
        logger.exception(f"An unexpected error has occurred: {args} {kwargs}")

    async def on_member_update(self, before: Member, after: Member) -> None:
        if before.display_name == after.display_name and before.roles == after.roles:
            return

        logger.debug(
            f'Member changed in guild "{before.guild.name}": {before.display_name} -> {after.display_name}'
        )
        await MemberTagger(after, self._guild_settings[after.guild]).update()

    async def on_guild_role_update(self, before: Role, after: Role) -> None:
        assert self.user is not None, "Client is not logged in"
        guild = after.guild
        guild_settings = self._guild_settings[guild]

        if after.name.startswith(self.user.name):
            new_settings = GuildSettings.from_role(after)
            if guild_settings != new_settings:
                await self.on_guild_settings_update(guild, guild_settings, new_settings)

        if (
            RoleTagger(before).tag == RoleTagger(after).tag
            and before.position == after.position
        ):
            return

        logger.debug(
            f'Role "{before.name}" was renamed to "{after.name}" in guild "{after.guild.name}".'
        )
        for member in after.members:
            await MemberTagger(member, guild_settings).update()

    async def on_guild_settings_update(
        self, guild: Guild, before: GuildSettings, after: GuildSettings
    ) -> None:
        logger.debug(f"Updated params for guild {guild.name}: {before} -> {after}")
        self._guild_settings[guild] = after
        for member in guild.members:
            await MemberTagger(member, before, after).update()


client = RollingTagsClient()
