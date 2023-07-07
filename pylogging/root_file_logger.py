"""
In this example, we will create a file handler root logger
"""
import logging

root_logger = logging.getLogger()  # gets the root logger

root_logger.setLevel("INFO")
# print some line before setting logger
root_logger.info(
    "Info level logs are enabled at logger but will not be "
    "visible as the default `_defaultLastResort = _StderrHandler(WARNING)` "
    "has the log level set to WARNING"
)
root_logger.warning("Warining logs are enabled.")

# create File Handler for logging
handler = logging.FileHandler("file.log", "w")  # append mode
format = (
    "[%(asctime)s: %(levelname)s: %(name)s: " "%(filename)s: %(lineno)d] %(message)s"
)
# set a custom format.
handler.setFormatter(logging.Formatter(format))

# reconfigure root logger
root_logger.addHandler(handler)

# testing
root_logger.info(
    "This will be logged to the file as we have info level enabled and have a custom logger"
)
root_logger.info("This will not be logged to stderr by default now")

root_logger.setLevel("WARNING")
root_logger.info(
    "Not visible in log file as info logs are disabled for the root loger now"
)

## Creating a child logger
kernel_logger = logging.getLogger("KernelLogger")

kernel_logger.info("Info Logs from kernel not visible as the level is set to waringing")
kernel_logger.warning("warning Logs from kernel not visible")


# There are 2 check for logging level..
# 1. Top level check in the info/error/debug function itself
# 2. handler level check just before pushing in `callHandlers` func.

# enable info logs for at the child logger.  This will pass the check-1
# we have not set any log level in the filehandler, so check-2 will also pass.
kernel_logger.setLevel("INFO")
kernel_logger.info("Info Logs from kernel visible")

# disable propagating logs to parent logger.
kernel_logger.propagate = False
kernel_logger.info(
    "Stop logging to file as we disable propagation.. thhis will not go to stderr as well"
)
kernel_logger.warning(
    "This will fallback to default stderr logger as there are no "
    f" hanlder for this logger and the log level is warning."
)
