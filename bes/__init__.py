# .-. .-.  .-.
# |(  |-   `-.
# `-' `-'  `-'

__version__ = "0.0.7"

import logging
import os

logger = logging.getLogger(__name__)

if os.getenv("BES_LOGGING_LEVEL") == "DEBUG":
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # add formatter to ch
    ch.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s '))

    # add ch to logger
    logger.addHandler(ch)
else:
    logger.addHandler(logging.NullHandler())
