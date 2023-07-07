"""
In this example, we will create a chile logger with its own handler.
"""

import logging

root_logger = logging.getLogger()

root_logger.info(
    "This will not be logged by default unless we use basic_config() to init"
)
root_logger.warning("This will be logged to stderr from default using the lastresort..")


# Child logger

kernel_logger = logging.getLogger("KernelLogger")

# create handler for the child logger.
kernel_log_handler = logging.FileHandler("child_file.log", "w")  # write mode
format = (
    "[%(asctime)s: %(levelname)s: %(name)s: " "%(filename)s: %(lineno)d] %(message)s"
)
# set a custom format.
kernel_log_handler.setFormatter(logging.Formatter(format))
kernel_log_handler.setLevel("INFO")

# add handler to child logger
kernel_logger.addHandler(kernel_log_handler)

kernel_logger.info("Logging to child logger file wil not work")
# enable info logs at the child logger.
kernel_logger.setLevel("INFO")
kernel_logger.info("Logging to child logger file wil now work")

kernel_logger.warning("This will log to file only and not propagate to root.")

# add a new logger to root logger
root_logger.addHandler(kernel_log_handler)

kernel_logger.warning("This will log to file twice as its  propagate to root logger")

# disable log propagation
kernel_logger.propagate = False

kernel_logger.warning(
    "This will log to file only once as its  propagate to parent logger is disable."
)

root_logger.warning("This will use root logger as name anf log to file")
