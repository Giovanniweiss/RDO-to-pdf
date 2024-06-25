import logging, os, sys, datetime

def prepare_loggers(pdf_generator_function):

    # Logger for the e-mail checker.
    def general_logger():
        logger_filename = "gen_log_" + current_time + ".log"
        logger_filepath = os.path.join(general_logging_path, logger_filename)
        os.makedirs(general_logging_path, exist_ok=True)  # Ensure directory exists
        formatter = logging.Formatter('%(asctime)s :: %(levelno)s :: %(lineno)d :: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        general_logger = logging.getLogger(os.getenv("GENERAL_LOGGER_NAME", "GENERAL"))
        general_logger.setLevel(logging.DEBUG)

        # Clear any existing handlers
        if general_logger.hasHandlers():
            general_logger.handlers.clear()

        hdlr = logging.FileHandler(logger_filepath)
        hdlr.setFormatter(formatter)
        general_logger.addHandler(hdlr)

    # Logger for PDF creator.
    def process_logger():
        logger_filename = current_time + ".log"
        logger_filepath = os.path.join(process_logging_path, logger_filename)
        os.makedirs(process_logging_path, exist_ok=True)  # Ensure directory exists
        formatter = logging.Formatter('%(asctime)s :: %(levelno)s :: %(lineno)d :: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        function_logger = logging.getLogger(os.getenv("PROCESS_LOGGER_NAME", "PROCESS"))
        function_logger.setLevel(logging.DEBUG)

        # Clear any existing handlers
        if function_logger.hasHandlers():
            function_logger.handlers.clear()

        hdlr = logging.FileHandler(logger_filepath)
        hdlr.setFormatter(formatter)
        function_logger.addHandler(hdlr)

    # This is to log unhandled exceptions.
    def log_unhandled_exceptions(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger = logging.getLogger(os.getenv("GENERAL_LOGGER_NAME", "GENERAL"))
        logger.error("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

    # This is to run the PDF creator.
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
    general_logging_path = "general_logs"
    process_logging_path = "processing_logs"
    sys.excepthook = log_unhandled_exceptions
    general_logger()
    return run_process_logger
