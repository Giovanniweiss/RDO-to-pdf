import sys, re, os

def process_email_loop(input):

    email_data = re.sub("\n", "", input)
    email_data = re.sub("https://", "\nhttps://", email_data)
    pattern = os.getenv("URL_PATTERN")
    matches = re.findall(pattern, email_data)

    return matches