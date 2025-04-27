import logging
from . import logger


def disable_loggers(*names: str):
    names_str = ", ".join(names)

    for name, _logger in logging.root.manager.loggerDict.items():
        if name.startswith(names) and isinstance(_logger, logging.Logger):
            logger.info(f"Disabled {name}")
            _logger.setLevel(logging.WARNING)

    logger.info(f"Logging was disabled for {names_str}")
