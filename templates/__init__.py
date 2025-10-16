from .__utils import get_json_content
from .types import *

COMMANDS = Commands.model_validate_json(get_json_content("commands"))
EXCEPTIONS = Exceptions.model_validate_json(get_json_content("exceptions"))
MESSAGES = Messages.model_validate_json(get_json_content("messages"))
MIDDLEWARES = Middlewares.model_validate_json(get_json_content("middlewares"))

__all__ = "COMMANDS", "EXCEPTIONS", "MESSAGES", "MIDDLEWARES"
