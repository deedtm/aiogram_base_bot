from .utils import init_class_template
from os import path as p

BASE_PATH = p.dirname(__file__)

middlewares_path = p.join(BASE_PATH, "middlewares.json")
_middlewares = init_class_template(middlewares_path)

messages_path = p.join(BASE_PATH, "messages.json")
_messages = init_class_template(messages_path)

commands_path = p.join(BASE_PATH, "commands.json")
_commands = init_class_template(commands_path)

exceptions_path = p.join(BASE_PATH, "exceptions.json")
_exceptions = init_class_template(exceptions_path)
