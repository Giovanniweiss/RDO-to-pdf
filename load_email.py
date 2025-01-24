import sys, re, os

def process_email(file_path:list=sys.argv) -> list[str]:
    """Takes a text file, that could be in the cmd arguments, and extracts the URLs from it.

    Args:
        file_path (list, optional): path to the text file. Defaults to sys.argv.

    Returns:
        list[str]: List containing the URLs.
    """    

    found_mail = False
    for index, argument in enumerate(sys.argv):
        if str(argument).endswith(".txt"):
            with open(file_path[index], 'r') as file:
                email_data= file.read()
                found_mail = True
            break
    if not found_mail:
        sys.exit(1)

    email_data = re.sub("\n", "", email_data)
    email_data = re.sub("https://", "\nhttps://", email_data)
    pattern = os.getenv("URL_PATTERN", "https://[^\n]*")
    matches = [str(i) for i in re.findall(pattern, email_data)] 
    
    return matches
