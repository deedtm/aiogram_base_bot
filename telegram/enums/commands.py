from dataclasses import dataclass


@dataclass(frozen=True)
class Commands:
    class admin:
        desc = "admin panel"
        access = 2

    class access:
        args = "{user_id} {level}"
        desc = "edit user's access level"
        access = 3

    class users:
        desc = "list of users"
        access = 2

    class getuser:
        args = "{user_id}"
        desc = "get user by id"
        access = 2


def parse_commands(command_format: str, access_level: int) -> list[str]:
    parsed_commands = [
        command_format.format(
            command='/' + name,
            args=getattr(c, "args", "") + " ",
            description=c.desc,
        )
        for name, c in Commands.__dict__.items()
        if not name.startswith("__") and c.access <= access_level
    ]
    return parsed_commands
