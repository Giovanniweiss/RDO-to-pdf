from curl_cffi import requests
import weasyprint, datetime
import re, os, sys, glob, logging
from balloontip import balloon_tip
from bs4 import BeautifulSoup
import load_email as le

# Main function
def generate_pdf_file(current_time, current_date, css_content, registry_file, data_url):
    logging.debug(data_url)
    response = request_get_from_url(data_url)
    logging.debug(f"processado {data_url}")
    html_filename, clean_html = html_cleanup(response, current_time)
    clean_html = update_html_content(clean_html, data_url)
    logging.debug(f"limpado {html_filename}")
    nome_do_arquivo = create_filename(html_filename)
    logging.debug(f"gerado nome do arquivo {html_filename}")
    sell_number = get_sell_number(nome_do_arquivo)
    logging.debug(f"obtido numero de venda {sell_number}")
    save_path = get_where_to_save(sell_number)
    logging.debug(f"determinado onde salvar: {save_path}")
    title = "Processamento de RDO"
    msg = f"Processando RDO {nome_do_arquivo}."
    try:
        balloon_tip(title, msg)
    except:
        logging.debug("did not create new balloon tip as to not bug the code.")
    export_to_pdf(css_content, clean_html, nome_do_arquivo, save_path)
    mensagem_sucesso = f"PDF salvo como {nome_do_arquivo} em {save_path}"
    logging.debug(mensagem_sucesso)
    update_registry(registry_file, current_date, save_path, nome_do_arquivo)

# 
def update_registry(text_file, current_date, save_path, save_file):
    try:
        with open(text_file, 'a') as file:
            message = f"{current_date}: Salvo '{save_file}' em '{save_path}'. \n"
            file.write(message)
        logging.debug(f"Adicionado registro de arquivo salvo em {text_file}")
        return 0
    except Exception as e:
        logging.debug(f"Não foi possível acessar o registro de RDOs. Erro registrado: {e}")
        return 1

# Get CSS formatting (this is to set the correct sheet size.)
def load_css_format(css_file_path='stylesheet.css'):
    with open(css_file_path, 'r') as file:
        css_content = file.read()
    logging.debug(f"Opened {css_file_path} for css content.")
    return css_content

# Get the data from the URL
def request_get_from_url(data_url):
    headers = {'Accept-Language': 'pt-BR',
           'Accept-Encoding': 'gzip, deflate, br, zstd'}
    response = requests.get(data_url, impersonate="chrome120", headers=headers)
    logging.debug(f"Accessed {data_url}, response status code: {response.status_code}.")
    return str(response.text)

# Get all 
def extract_variable_content(file_path, target_text):
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'lxml')
        
        # Find the <th> with the specified text
        th = soup.find('th', class_='c-table-summary__column -font-bold -size-20', text=target_text)
        if th:
            # Find the next <td> sibling of the <th> element
            td = th.find_next_sibling('td', class_='c-table-summary__column')
            if td:
                # Get the stripped text content of the <td> element
                return td.text.strip()
        return None

# HTML Cleanup (why is the source so broken??)
def html_cleanup(response, current_time):
    clean_html = response
    clean_html = re.sub(r"&lt;", "<", clean_html)
    clean_html = re.sub(r"&gt;", ">", clean_html)
    clean_html = re.sub(str(os.getenv("FILE_SERVER_PATH_TO_REPLACE")), str(os.getenv("FILE_SERVER_PATH")), clean_html)
    clean_html = re.sub("Abrir link em nova aba", "Abrir imagem", clean_html)
    hyperlink_string = "font-size: 1.2em"
    new_hyperlink_string = "font-size: 0.7em"
    clean_html = re.sub(hyperlink_string, new_hyperlink_string, clean_html)
    clean_html = re.sub(r'\n\s*\n', '\n', clean_html)
    clean_html = re.sub(r' {2,}', ' ', clean_html)


    script_path = os.path.dirname(sys.argv[0])
    html_folder_path = os.path.join(script_path, "html")
    html_file_name = current_time + ".html"
    html_file_name = os.path.join(html_folder_path, html_file_name)
    with open(html_file_name, "w") as file:
        file.write(clean_html)
    return html_file_name, clean_html

def update_html_content(html_content, url):
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Update image links
    for div in soup.find_all('div', class_='img_container'):
        img = div.find('img', class_='img_zoom maxMediaMobile')
        a = div.find('a', class_='link-open-image d-print-none')
        
        if img and a:
            # Move the <img> inside the <a>
            img_src = img['src']
            a['href'] = img_src
            img.extract()
            a.clear()  # Clear the content of the <a> tag
            a.insert(0, img)
    
    # Append the URL as a hyperlink at the end of the <html> tag
    new_link = soup.new_tag('a', href=url, target='_blank')
    new_link.string = "Clique aqui para acessar esta RDO no sistema da Evne."
    soup.html.append(new_link)
    
    return str(soup)

def create_filename(html_file):
    location = extract_variable_content(html_file, "Onde")
    if location == None:
        location = "local_indeterminado"
    elif len(location) > 25:
        location = location[:]

    execution_date = extract_variable_content(html_file, "Quando (previsto)")
    if execution_date == None:
        execution_date = "date_indeterminada"
    else:
        clean_execution_date = execution_date.replace('\n', '').strip()
        clean_execution_date = clean_execution_date.replace('\t', '_')
        clean_execution_date = clean_execution_date.replace(' ', '')
        clean_execution_date = clean_execution_date.replace('/', '-')
        clean_execution_date = clean_execution_date.replace(':', '-')
        # Data original: DD-MM-AAAA-HH-MM
        # Data nova: AAAA-MM-DD-HH-MM
        clean_execution_date = clean_execution_date.split("_")
        clean_execution_date[0] = clean_execution_date[0].split("-")
        clean_execution_date[0] = "-".join([clean_execution_date[0][2], clean_execution_date[0][1], clean_execution_date[0][0]])
        clean_execution_date = "_".join(clean_execution_date)
        
    return "_".join([location, clean_execution_date]) + ".pdf"


def get_sell_number(filename):
    pattern = r'\b\d{7}\b'
    matches = re.findall(pattern, filename)

    if len(matches) > 1:
        return matches[-1]
    elif len(matches) == 1:
        return matches[0]
    else:
        return "SEM CODIGO DE VENDA"
    

def listar_desenhos(acervo, types = (r'\*.pdf')):
    # Lista todos os arquivos na pasta escolhida dos tipos escolhidos.
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(acervo + files, recursive=True))
    return files_grabbed


def get_where_to_save(sell_number):
    current_year = int(datetime.datetime.now().strftime("%Y"))
    
    path = os.getenv("DOCS_PATH")
    limit_year = 2009 #No projects before 2009.
    if current_year < 2009:
        current_year = 2100
    while current_year > limit_year:
        current_path = os.path.join(path, str(current_year))
        try:
            subfolders = [f.path for f in os.scandir(current_path) if f.is_dir()]
            for folder in subfolders:
                pdfs_in_folder = listar_desenhos(folder)
                if any([sell_number in i for i in pdfs_in_folder]):
                    return os.path.join(folder, "Relatórios", "RDOs")
            current_year -= 1
        except FileNotFoundError:
            current_year -= 1

    return os.getenv("STD_SAVE_PATH")

def create_folder_if_none_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Pasta '{path}' criada com sucesso em '{path}'.")
    else:
        print(f"Pasta '{path}' já existe no caminho.")
    return 0

# Export the PDF file
def export_to_pdf(css_content, response, nome_do_arquivo, save_path):
    print(save_path)
    create_folder_if_none_exists(save_path)
    doc = weasyprint.HTML(string=str(response), media_type="screen")
    css = weasyprint.CSS(string=css_content)
    digit = 1
    file_to_create = os.path.join(save_path, nome_do_arquivo)
    if os.path.isfile(file_to_create):
        file_to_create_offset = file_to_create[:-4] + "_" + str(digit) + ".pdf"
        while os.path.isfile(file_to_create_offset):
            digit += 1
            file_to_create_offset = file_to_create[:-4] + "_" + str(digit) + ".pdf"
        doc.write_pdf(file_to_create_offset, optimize_images=True, jpeg_quality=95, dpi=120, stylesheets=[css], presentational_hints=True)
    else:
        doc.write_pdf(file_to_create, optimize_images=True, jpeg_quality=95, dpi=120, stylesheets=[css], presentational_hints=True)

