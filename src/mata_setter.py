import re

class MetaSetter():
    """Класс с методами для заполнения метаинформации о произведении"""
    def __init__(self, soup_html, soup_tei):
        self.soup_html = soup_html
        self.soup_tei = soup_tei


    def fill_title(self):
        """Заполняет название"""
        title_main_tei = self.soup_tei.find('title')
        title_tag_html = self.soup_html.find_all('meta', attrs={'name':'title'})
        title_main_tei.string = title_tag_html[0].get('content')
        if len(title_tag_html) == 2: # Если есть подзаголовок
            title_main_tei.string += f" ({title_tag_html[1].get('content')})"


    def fill_description(self):
        """Заполняет описание текста"""
        description_html = self.soup_html.find('div', class_='description')
        full_bibl = self.soup_tei.find('biblfull').find('p')
        full_bibl.string = description_html.text
        self._description_html = description_html


    def fill_transformator_name(self, transformator_name):
        """Заполняет имя того, кто преобразовал текст в TEI"""
        name_resp_stmt = self.soup_tei.find('respstmt').find('persname')
        name_resp_stmt.string = transformator_name


    def fill_size_info(self):
        """Заполняет информацию об объеме произведения"""
        extent_inf = self.soup_tei.find('extent')
        # Получаем список номеров страниц
        list_ids = []
        for tag in self.soup_html.find_all('span', class_='page') :
            tag_page=tag.get('id')
            list_ids.append(tag_page[2:])

        # Считаем объем
        volume = int(list_ids[-1]) - int(list_ids[0]) + 1
        volume_str = str(volume)

        # Формируем результирующую строку
        if volume_str[-1] in ['5', '6', '7', '8', '9', '0'] or\
                (len(volume_str) == 2 and volume_str[-2] == '1'):
            volume_f = volume_str + ' страниц'
        elif volume_str[-1] == '1':
            volume_f = volume_str + ' страница'
        else:
            volume_f = volume_str + ' страницы'

        # Заполняем информацию об объеме в атрибутах тегов
        tag_measure = self.soup_tei.new_tag('measure')
        extent_inf.insert(0, tag_measure)

        self.soup_tei.find('measure')['unit'] = 'pages'
        self.soup_tei.find('measure')['quantity'] = volume_str

        measure_inf = self.soup_tei.find('measure')
        measure_inf.string = volume_f


    def fill_publication_date(self):
        """Заполняет дату публикации произведения"""
        publ_date = self.soup_tei.find('publicationstmt')
        publ_date1 = publ_date.find('date')
        date_1 = self.soup_html.find('meta', attrs={'name':'date'})
        publ_date1.string = date_1.get('content')
        publ_date.find('date')['when'] = date_1.get('content')


    def fill_creation_date(self):
        """Заполняет дату создания произведения"""
        date_cr = self.soup_tei.find('creation').find('date')
        abz = self._description_html.find_all('p')
        search = abz[-2].text

        date_from_to = re.findall(r'\d{4}—\d{4}', search)
        if len(date_from_to) > 0: # Если том создавался несколько лет
            date_cr.string = date_from_to[0]
            date_cr['from'] = date_from_to[0][:4]
            date_cr['to'] = date_from_to[0][-4:]
        else: # Если том создавался один год (5 и 6 тома)
            date_when = re.findall(r'\d{4}', search)[0]
            date_cr['when'] = date_when
            date_cr.string = date_when
        self._abz = abz


    def fill_edition_info(self):
        """Заполняет информацию об издании"""
        edstmt = self._abz[0].text.split('//')
        edstmt1 = edstmt[1].split('\n')[0]
        edition_stmt = self.soup_tei.find('editionstmt').find('p')
        edition_stmt.string = edstmt1
        self._edition_stmt = edition_stmt


    def fill_volume_num(self):
        """Заполняет номер тома"""
        volume = re.findall(r'Т. \d+.', self._edition_stmt.string)
        volume_n = re.findall(r'\d+', volume[0])
        bibl_sc = self.soup_tei.find('biblscope')
        bibl_sc.string = 'Том ' + volume_n[0]


    def fill_all_meta(self, transformator_name):
        """Полностью заполняет метаинформацию"""
        #Порядок выполнения функций лучше не менять
        self.fill_title()
        self.fill_description()
        self.fill_transformator_name(transformator_name)
        self.fill_size_info()
        self.fill_publication_date()
        self.fill_creation_date()
        self.fill_edition_info()
        self.fill_volume_num()