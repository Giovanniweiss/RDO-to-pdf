import logger_tools_improved as lti
import load_email as le
import transform_pdf as pp2

@lti.prepare_loggers
css_content = pp2.load_css_format()
data_url_list = le.process_email()
logging.debug(data_url_list)
registry_file = os.getenv('REGISTRY_FILE')

for data_url in data_url_list:
    pp2.generate_pdf_file(current_time, current_date, css_content, registry_file, data_url)