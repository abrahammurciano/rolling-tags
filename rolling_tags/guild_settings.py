import logging
import shlex

import parse
from discord import Guild, Role

logger = logging.getLogger(__name__)


class GuildSettings:
    __slots__ = ("_separator", "_format", "_parser")

    def __init__(self, *, sep: str = " ", fmt: str = "") -> None:
        """Represents the settings of a guild.

        Args:
            sep: The separator between each tag. Defaults to a single space.
            fmt: The format string used to format a member's nickname. Must contain "{n}" and "{{t}}". Defaults to "{n} | {t}". The "{n}" placeholder is replaced with the member's base name, and the "{t}" placeholder is replaced with the tags.
        """
        self._separator = sep
        self._format = fmt.strip() if "{n}" in fmt and "{t}" in fmt else "{n} | {t}"
        self._parser = parse.compile(self._format)

    @property
    def separator(self) -> str:
        """The separator between each tag."""
        return self._separator

    @property
    def format_string(self) -> str:
        """The format string used to format a member's nickname."""
        return self._format

    @property
    def parser(self) -> parse.Parser:
        """The parser used to extract a member's base name."""
        return self._parser

    @classmethod
    def from_guild(cls, guild: Guild) -> "GuildSettings":
        role = _find_main_role(guild)
        return cls.from_role(role) if role else cls()

    @classmethod
    def from_role(cls, role: Role) -> "GuildSettings":
        return cls(**cls._params_from_role_name(role.name, role.guild.me.name))

    @classmethod
    def _params_from_role_name(cls, role_name: str, bot_name: str) -> dict[str, str]:
        return {
            key: value
            for key, value in (
                param.split("=")
                for param in shlex.split(role_name.removeprefix(bot_name))
            )
            if key in cls.__init__.__annotations__.keys() - {"return"}
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GuildSettings):
            return NotImplemented
        return self._separator == other._separator and self._format == other._format

    def __hash__(self) -> int:
        return hash((self._separator, self._format))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(sep={self._separator!r}, fmt={self._format!r})"
        )


def _find_main_role(guild: Guild) -> Role | None:
    return next(
        (role for role in guild.roles if role.name.startswith(guild.me.name)),
        None,
    )
