import sys
import requests
import re
from bs4 import BeautifulSoup
import csv
import os
import slack
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def page_pfsense_dhcp(url,username,password):
    
    s = requests.session()
    r = s.get(url,verify = False)

    matchme = 'csrfMagicToken = "(.*)";var'

    csrf = re.search(matchme,str(r.text))

    payload = {
        '__csrf_magic' : csrf.group(1),
        'login' : 'Login',
        'usernamefld' : username,
        'passwordfld' : password
    }
    r = s.post(url,data=payload,verify = False)
    r = s.get(url,verify = False)
    return r.text

def _parse_activities(html):
    results = []
    soup = BeautifulSoup(html, "html.parser")
    print(soup.title)
    table = soup.find_all("table", {'class' : 'table table-striped table-hover table-condensed sortable-theme-bootstrap'})
    text_list = []
    for row in table:
        table_row = row('tr')
        for table_data in table_row:
            td = table_data('td')
            lista = ''
            for td_contents in td:
                content = td_contents.contents[0]
                valor = content.strip()
                if valor:
                   lista = lista + valor + ','             
            lista = lista[:-1]
            results.append(lista)
    return results

def ajustar_arquivo():
    file = open('foo.csv','r')
    file2 = open('final.txt', 'a')

    next(file, None)
    reader = csv.reader(file)
    reader = filter(None,reader) #remover linhas em branco
    for row in reader:
        value = row[1] + ': '
        if len(row) == 4:
            value = value + row[3]
        if len(row) >= 3:
            value = value + ' ['+ row[2] +']' 
        file2.write(value+'\n')
        
    file2.close()

def main(page_list,username,password):
    pages = page_list.split(",") 

    for url in pages:
        html = page_pfsense_dhcp(url,username,password)
        lista = _parse_activities(html)

        fo = open("foo.csv", "a")
        for item in lista:
            fo.write("%s\n" % item)
        fo.close()

if __name__ == "__main__":
    if (("PF_USER" in os.environ) and ("PF_PASS" in os.environ)):
        username=os.environ["PF_USER"]
        password=os.environ["PF_PASS"]
    else:
        print("Necessario usuario e senha para acesso")
        sys.exit()

    if (("SL_TOKEN" in os.environ) and ("SL_CHANNELS" in os.environ)):
        token=os.environ["SL_TOKEN"]
        channels=os.environ["SL_CHANNELS"]
    else:
        print("Necessario token e channels para envio de resposta slack")
        sys.exit()


    if ("PAGE_LIST" in os.environ):
        page_list=os.environ["PAGE_LIST"]
    else:
        print("Necessario paginas!")
        sys.exit()

    list_file = ['foo.csv','final.txt']
    for file in list_file:
        if os.path.exists(file):
            os.remove(file)
    
    main(page_list,username,password)
    ajustar_arquivo()
    slack.send_file_to_slack(token,channels,'final.txt')

    list_file = ['foo.csv','final.txt']
    for file in list_file:
        if os.path.exists(file):
            os.remove(file)
