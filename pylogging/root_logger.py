"""
Understanding python root logger
"""

import logging

# get the root logger.
root_logger = logging.getLogger()  # root = RootLogger(WARNING) default level is waringn

# The root logger by default does not have any custom logger and
# it falls back to using `_StderrHandler` as `_defaultLastResort` handler.
# if a handler is set, the logs will not go to the stderr.
root_logger.debug("debug logsm not available by default")
root_logger.info("Into log not available by default")
root_logger.warning("warning logs available to stderr")
root_logger.critical("Critical logs available to stderr")
