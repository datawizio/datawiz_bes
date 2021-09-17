# .-. .-.  .-.
# |(  |-   `-.
# '_' `-'  `-'


__version__ = "0.0.5"

import logging

logger = logging.getLogger(__name__)
# logger.addHandler(logging.NullHandler())


logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
