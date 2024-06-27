import sys, re, os

def process_email(file_path=sys.argv[1]):
    with open(file_path, 'r') as file:
        email_data = file.read()

    #email_data = re.sub("\n", "", email_data)
    #email_data = re.sub("https://", "\nhttps://", email_data)
    pattern = os.getenv("URL_PATTERN")
    matches = re.findall(pattern, email_data)

    return matches

