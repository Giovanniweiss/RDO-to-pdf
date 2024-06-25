import logging, sys

def logger_setup(logging_filename):
    logging.basicConfig(
        filename = logging_filename,
        level = logging.DEBUG,
        format = "%(asctime)s :: %(levelno)s :: %(lineno)d :: %(message)s")
    sys.excepthook = exception_handler

def exception_handler(exc_type, exc_value, exc_traceback):
    """Handler for uncaught exceptions."""
    logging.exception("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def close_log_handlers():
    logger = logging.getLogger()
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)