import logging
from logging.handlers import RotatingFileHandler
import sys
from os.path import expanduser

"""
Code was borrowed from the configure_logging code. We update it to shorten the name of the logger, and use the
RotateFileLogger class instead of the file logger as we would prefer not to fill the disk up with our logs
"""

def _log_exceptions_in_root_logger() -> None:
    """
    Configure root logger to log uncaught exceptions under log level `ERROR`.
    :returns: Nothing, only side effects.
    """
    root_logger = logging.getLogger()
    def handle_exception(exc_type, exc_value, exc_traceback):
        root_logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.excepthook = handle_exception

def logging_setup(path: str = None, log_level: str = 'INFO', append: bool = True, stdout: bool = True) -> None:
    """ 
    Configure logging such that log records of all loggers are formatted according to same format and are written
    to a file and/or printed to stdout.

    Specifically, add a stdout and/or a rotating file handler to the root logger. Both handlers format log records according to
    the template `[datetime] [logger name] [log level] MESSAGE`. Additionally, log uncaught exceptions in the root
    logger.

    The root logger receives log records emitted by all other loggers that are configured to propagate their records up
    the loggers hierarchy, which is the default when instantiating a logger.

    :param path: Path of the file where the file handler will write log records to. Defaults to `None`, in which case
    the file handler is omitted from root logger.
    :param log_level: Log level of the root logger. Defaults to `INFO`.
    :param append: Append the log records to the log file. Defaults to `True`. Is ignored if `path` for the log file
        is not set.
    :param stdout: Whether to add stdout handler to the root logger.
    :returns: Nothing, only side effects.
    """

    if not path and not stdout:
        raise ValueError('No place to send logs to: path is empty and stdout is false.')

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    if (stdout):
        root_logger.handlers.clear()
    rfh = RotatingFileHandler(path, 100000, 3)
    root_logger.addHandler(rfh)

    _log_exceptions_in_root_logger()
