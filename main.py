import load_email as le
import transform_pdf as pp2
import logger_tools as lt
import datetime, logging, sys, os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()

    # Create strings
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Logging setup
    logging_filename = os.path.join("processing_logs", current_time + ".log")
    lt.logger_setup(logging_filename)

    css_content = pp2.load_css_format()
    data_url_list = le.process_email()
    logging.debug(data_url_list)
    registry_file = os.getenv('REGISTRY_FILE')

    for data_url in data_url_list:
        pp2.generate_pdf_file(current_time, current_date, css_content, registry_file, data_url)

    logging.debug("Código executado com sucesso. Fechando log.")
    lt.close_log_handlers

    sys.exit(0)

if __name__ == "__main__":
    main()