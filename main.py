
import wget
import os
import requests
import shutil
from bs4 import BeautifulSoup

#Рефактор
# Разбить все на функциональные компоненты
# сократить код,DRY



BASE_DIR = os.path.join(os.path.abspath(os.curdir), 'app')
dirs = ['css', 'js', 'img', 'fonts', 'css/plugins']
url = 'https://smartinnovates.com/uithemez/archo/'

#Управление папками
#наполнение файлами wget
#функции BS4
#функции обработки кратинок
#генерация папок на основе ссылок полученных из HTML документа
#загрузка шрифтов в отдельные файлы

def created_dirs(dirs):
    """ Создание папок проекта """
    try:
        os.mkdir(BASE_DIR)
        for d in dirs:
            os.mkdir(f'{BASE_DIR}/{d}')
        os.mkdir(f'{BASE_DIR}/css/plugins')
    except FileExistsError:
        shutil.rmtree(BASE_DIR)
        os.mkdir(BASE_DIR)
        for d in dirs:
            os.mkdir(f'{BASE_DIR}/{d}')


def get_all_file_links(url):
    """ Получение ссылок на шрифты, стили, скрипты """
    all_links = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('link'):
            all_links.append(link.get('href'))
        for scripts in soup.find_all('script'):
            all_links.append(scripts.get('src'))
        
        
    except:
        print('Ошибка')
    return all_links


def get_imported_files():
    all_files = [ff for ff in os.listdir('app/css/')[1:]]
    clean_imported_path = []
    for files in all_files:
        with open(f'{BASE_DIR}/css/{files}', 'r') as f:
            lines = f.readlines()
            import_lines = [line for line in lines if '@import' in line]
            for line in import_lines:
                clean_imported_path.append(line.replace("@import url(\"", '').replace("\");", '').replace('\n', '').replace(' ', ''))
    return clean_imported_path


def download_imported_files(links, url):
    for link in links:
        wget.download(f'{url}/css/{link}', out=f'{BASE_DIR}/css/{link}')


def get_html_pages(url):
    """ Получение HTML страниц """
    try:
        all_html_links = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            if '#' not in link.get('href') and not link.get('href').startswith('htt'):
                all_html_links.append(link.get('href'))
        for html in all_html_links:
            wget.download(f'{url}/{html}', out=BASE_DIR)
    except:
        print('Ошибка')


def create_project(files_links, dirs, url):
    created_dirs(dirs)
    wget.download(url, out=f'{BASE_DIR}/index.html')
    for l in files_links:
        if not l.startswith('https'):
            wget.download(f'{url}/{l}', out=f'{BASE_DIR}/{l}')



if __name__ == '__main__':
    created_dirs(dirs)
    get_all_links = get_all_file_links(url)
    create_projects = create_project(get_all_links, dirs, url)
    get_clean_url_import = get_imported_files()
    download_other_files = download_imported_files(get_clean_url_import, url)
    get_html = get_html_pages(url)



#Рефактор
# Разбить все на функциональные компоненты
# сократить код,DRY



