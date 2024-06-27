import logger_tools_improved as lti
import load_email as le
import transform_pdf as pp2
import datetime, logging, sys, os
from dotenv import load_dotenv

@lti.prepare_process_logger
def some_process_module():
    current_date = datetime.datetime.now().strftime("%d/%m/%Y")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    css_content = pp2.load_css_format()
    data_url_list = le.process_email()
    logging.debug(data_url_list)
    registry_file = os.getenv('REGISTRY_FILE')

    for data_url in data_url_list:
        pp2.generate_pdf_file(current_time, current_date, css_content, registry_file, data_url)

    logging.debug("Código executado com sucesso. Fechando log.")
    lti.close_log_handlers(os.getenv("PROCESS_LOGGER_NAME", "PROCESS"))
    pass

def main():
    lti.prepare_general_logger()
    load_dotenv()
    some_process_module()
    pass

main()
