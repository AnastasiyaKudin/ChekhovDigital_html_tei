import os
from src.mata_setter import MetaSetter
from src.text_setter import TextSetter
from src.dirs import Texts_HTML_PATH, Texts_TEI_PATH, NOTES_Preform_PATH, TEI_Preform_file
from src.file_tools import create_dir, open_with_soup, save_tei

def main(your_name, volumes_lst):
    """main pipeline for processing"""
    for volume_num in volumes_lst:
        directory_html = Texts_HTML_PATH / str(volume_num)
        directory_tei = Texts_TEI_PATH / str(volume_num)
        create_dir(directory_tei)
        note_file = NOTES_Preform_PATH / f'{str(volume_num)}.html'

        print(f'Том {volume_num} обрабатывается')
        file_num = 1
        for filename in os.listdir(directory_html):
            print(filename)
            soup_html = open_with_soup(directory_html / filename, 'windows-1251')
            soup_tei = open_with_soup(TEI_Preform_file, 'utf8')
            soup_notes_html = open_with_soup(note_file, 'windows-1251')

            # заполянем мета-информацию
            meta_setter = MetaSetter(soup_html, soup_tei)
            meta_setter.fill_all_meta(your_name)

            # заполняем текст и сноски
            text_setter = TextSetter(soup_html, soup_tei, soup_notes_html)
            text_setter.fill_all_text()

            soup_tei = text_setter.soup_tei

            # сохраняем
            save_tei(soup_tei, directory_tei, volume_num, file_num)
            file_num += 1
        print('------------')


if __name__ == '__main__':
    your_name = 'Кудин Анастасией' #имя заполняющего
    volumes_lst = [1,2,3]
    main(your_name, volumes_lst)
