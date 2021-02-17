import os
from bs4 import BeautifulSoup
import re


def open_with_soup(file_path, encoding):
    """Открывает файл и возвращает объект BeautifulSoup"""
    with open(file_path,'r',encoding=encoding) as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    return soup


def create_dir(directory):
    """Создает директорию, если ее нет"""
    if not os.path.exists(directory):
        os.makedirs(directory)


dictionary = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo',
        'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
        'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'kh',
        'ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e',
        'ю':'u','я':'ya', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'YO',
        'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
        'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'KH',
        'Ц':'C','Ч':'CH','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'Y','Ь':'','Э':'E',
        'Ю':'U','Я':'YA', ' ' : '_'}


def save_tei(soup_tei, save_dir, volume_num, file_num):
    """Сохраняет файл в формате TEI"""
    title = re.sub(r'[/\:*?''<>!«»—,]', '', soup_tei.find('title').string.strip())
    for key in dictionary:
        title = title.replace(key, dictionary[key])
    title = title[:15]

    # В зависимости от номера тома поменять цифру рядом с "V"
    with open(os.path.join(save_dir, f'V{volume_num}_{file_num}_{title}.xml'), 'w', encoding='utf8') as file:
        file.write(soup_tei.prettify())


