"""
Logging Module
"""

# Standard Library
import logging

logger = logging.getLogger("rng2doc")


def setup_logging(level):
    global logger

    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logger.addHandler(handler)
    return logger
