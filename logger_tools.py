import logging, sys, os

def logger_setup(logging_filename:str):
    """Setups a simple logger and makes it log unhandled exceptions.

    Args:
        logging_filename[str]: path to the log file to be created.
    """    
    logging.basicConfig(
        filename = logging_filename,
        level = logging.DEBUG,
        format = "%(asctime)s :: %(levelno)s :: %(lineno)d :: %(message)s")
    sys.excepthook = exception_handler

def exception_handler(exc_type, exc_value, exc_traceback):
    """Handler for uncaught exceptions."""
    logging.exception("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.exit(1)

def close_log_handlers(logger_name=""):
    """Gracefully closes the log handlers."""
    logger = logging.getLogger(logger_name)
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)

