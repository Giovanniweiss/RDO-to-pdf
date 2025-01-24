import imapclient
import pyzmail
import time
import logging
import os
import signal
import sys
import logger_tools_improved as lti
from dotenv import load_dotenv

# Load configuration from .env file
load_dotenv()

def run_email_server(email_processing_function):
    server = os.getenv('EMAIL_SERVER')
    email = os.getenv('EMAIL_ACCOUNT')
    password = os.getenv('EMAIL_PASSWORD')
    destination_folder = os.getenv('DESTINATION_FOLDER', 'Processed')
    interval = int(os.getenv('CHECK_INTERVAL', 60))
    
    def signal_handler(sig, frame):
        logging.info('Shutting down the email server...')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    while True:
        check_for_emails(email_processing_function, server, email, password, destination_folder=destination_folder)
        time.sleep(interval)


def check_for_emails(email_processing_function, server, email, password, folder='INBOX', search_criteria='UNSEEN', destination_folder='Processed'):
    try:
        with imapclient.IMAPClient(server) as client:
            client.login(email, password)
            client.select_folder(folder)
            
            messages = client.search(search_criteria)
            if not messages:
                logging.info("No new emails found.")
                return
            
            for uid in messages:
                raw_message = client.fetch([uid], ['BODY[]', 'FLAGS'])
                message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])
                
                subject = message.get_subject()
                from_address = message.get_address('from')
                to_address = message.get_address('to')
                body = message.text_part.get_payload().decode(message.text_part.charset) if message.text_part else None
                html = message.html_part.get_payload().decode(message.html_part.charset) if message.html_part else None
                
                logging.info(f"Processing email from {from_address} with subject '{subject}'")
                
                # Call your custom function here and pass the email content
                email_processing_function(subject, from_address, to_address, body, html)
                
                # Copy the email to another folder
                client.copy(uid, destination_folder)
                
                # Delete the email from the original folder
                client.delete_messages(uid)
                client.expunge()
                
                logging.info(f"Email from {from_address} with subject '{subject}' moved to {destination_folder}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

