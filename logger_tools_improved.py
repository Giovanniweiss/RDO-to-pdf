import logging
import os
import sys
import datetime

def prepare_general_logger():
    def general_logger():
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        general_logging_path = "general_logs"
        logger_filename = "gen_log_" + current_time + ".log"
        logger_filepath = os.path.join(general_logging_path, logger_filename)
        os.makedirs(general_logging_path, exist_ok=True)

        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(lineno)d :: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        general_logger = logging.getLogger(os.getenv("GENERAL_LOGGER_NAME", "GENERAL"))
        general_logger.setLevel(logging.DEBUG)

        if general_logger.hasHandlers():
            for handler in general_logger.handlers[:]:
                general_logger.removeHandler(handler)

        hdlr = logging.FileHandler(logger_filepath)
        hdlr.setFormatter(formatter)
        general_logger.addHandler(hdlr)

    def log_unhandled_exceptions_general(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger = logging.getLogger(os.getenv("GENERAL_LOGGER_NAME", "GENERAL"))
        logger.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = log_unhandled_exceptions_general
    general_logger()
    print("this scrud is working!!")


def prepare_process_logger(pdf_generator_function):

    def process_logger():
        logger_filename = current_time + ".log"
        logger_filepath = os.path.join(process_logging_path, logger_filename)
        os.makedirs(process_logging_path, exist_ok=True)
        formatter = logging.Formatter('%(asctime)s :: %(levelno)s :: %(lineno)d :: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        function_logger = logging.getLogger(os.getenv("PROCESS_LOGGER_NAME", "PROCESS"))
        function_logger.setLevel(logging.DEBUG)

        if function_logger.hasHandlers():
            function_logger.handlers.clear()

        hdlr = logging.FileHandler(logger_filepath)
        hdlr.setFormatter(formatter)
        function_logger.addHandler(hdlr)

    def log_unhandled_exceptions_process(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        process_logger = logging.getLogger(os.getenv("PROCESS_LOGGER_NAME", "PROCESS"))
        process_logger.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

        general_logger = logging.getLogger(os.getenv("GENERAL_LOGGER_NAME", "GENERAL"))
        general_logger.error("Unhandled exception in process", exc_info=(exc_type, exc_value, exc_traceback))

    def run_process_logger(*args, **kwargs):
        process_logger()
        logger = logging.getLogger(os.getenv("PROCESS_LOGGER_NAME", "PROCESS"))
        try:
            logger.info("Starting process submodule operations")
            return pdf_generator_function(*args, **kwargs)
        except Exception as e:
            logger.error("Exception occurred in process_logger", exc_info=True)
            raise

    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    process_logging_path = "processing_logs"
    sys.excepthook = log_unhandled_exceptions_process
    return run_process_logger

def close_log_handlers(logger_name=""):
    logger = logging.getLogger(logger_name)
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)