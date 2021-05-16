import os
from requests.api import get
import wget
import requests
import shutil
from bs4 import BeautifulSoup
url = 'https://smartinnovates.com/uithemez/archo/'


def get_image():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_dir = ''
    file_names = []
    full_path = []
    create_in_main_dir = []
    for image in soup.find_all('img'):
        get_src = image.get('src')
        full_path.append(get_src)
        split_path = get_src.split('/')
        file_names.append(split_path[-1])
        main_dir = split_path[0]
        for i in split_path[1:-1]:
            create_in_main_dir.append(i)
    os.mkdir(main_dir)
    os.chdir(main_dir)
    for dir_in_main in set(create_in_main_dir):
        os.mkdir(dir_in_main)


get_image()





