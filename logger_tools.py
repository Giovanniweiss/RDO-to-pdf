import logging
import sys
import os

def logger_setup(logging_filename: str):
    """Setups a simple logger and makes it log unhandled exceptions.

    Args:
        logging_filename[str]: path to the log file to be created.
    """    
    logging.basicConfig(
        filename=logging_filename,
        level=logging.DEBUG,
        format="%(asctime)s :: %(levelno)s :: %(lineno)d :: %(message)s")
    sys.excepthook = exception_handler

def exception_handler(exc_type, exc_value, exc_traceback):
    """Handler for uncaught exceptions."""
    logging.exception("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.exit(1)

def close_log_handlers(logger_name=""):
    """Gracefully closes the log handlers and renames the log file."""
    logger = logging.getLogger(logger_name)
    handlers = logger.handlers[:]
    for handler in handlers:
        if isinstance(handler, logging.FileHandler):
            # Get the log file path
            log_file_path = handler.baseFilename
            handler.close()
            logger.removeHandler(handler)
            
            # Rename the log file
            if os.path.exists(log_file_path):
                directory, filename = os.path.split(log_file_path)
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_success{ext}"
                new_file_path = os.path.join(directory, new_filename)
                os.rename(log_file_path, new_file_path)
        else:
            handler.close()
            logger.removeHandler(handler)

# Example usage
if __name__ == "__main__":
    logger_setup("example.log")
    logging.info("This is a test log message.")
    close_log_handlers()