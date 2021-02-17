import re
from bs4 import BeautifulSoup
from src.existence_seter import ExistenceSeter

class TextSetter():
    """Класс с методами для заполнения текста произведения"""

    def __init__(self, soup_html, soup_tei, soup_notes_html):
        self.soup_html = soup_html
        self.soup_tei = soup_tei
        self.soup_notes_html = soup_notes_html

    def _help_get_id(self):
        """Получает id нашего текста"""
        self._text_id = self.soup_html.find_all('a')[1].get('href').split('#')[1]

    def _help_find_text_tags(self):
        """Создает переменные-теги, отвечающие за произведение"""
        self._pars = self.soup_html.find_all(['p', 'span', 'img'])
        self._body = self.soup_tei.select('text body')[0]
        first_page = self.soup_html.find('span', class_='page').get('id')[2:]
        self._pb_tag = self.soup_tei.new_tag('pb', attrs={'n': first_page})

    def process_page(self, cur_tag):
        """Обрабатывает абзац-страницу"""
        cur_page = cur_tag.get('id')[2:]
        self._pb_tag = self.soup_tei.new_tag('pb', attrs={'n': cur_page})
        self._pb_tag.string = cur_tag.get('id')[2:]
        self._body.append(self._pb_tag)

    def move_text_with_notes(self, tag_to, tag_from):
        """Переносит содержиомое тега с сохранением сносок"""

        def help_recursive(tag_from):
            if isinstance(tag_from, str):
                return tag_from
            res = ''
            note_format = '<note xml:id={0}>{1}</note>'
            for tag_part in tag_from.contents:
                if isinstance(tag_part, str):
                    res += tag_part
                elif tag_part.name == 'a':
                    if tag_part.has_attr('class') and tag_part['class'][0] == 'footnote':
                        res += note_format.format(tag_part['href'][1:], tag_part.text)
                    elif tag_part.has_attr('href') and re.match(r'#$\S*', tag_part['href'][0]) is None:
                        res += note_format.format('external_link', tag_part.text)
                elif tag_part.name not in ['p', 'div']:
                    res += help_recursive(tag_part)
            return res

        tag_to.string = help_recursive(tag_from)

    def process_image(self, cur_tag):
        """Обрабатывает абзац-изображение"""
        fig_tag = self.soup_tei.new_tag('figure')
        self._pb_tag.append(fig_tag)
        graph_tag = self.soup_tei.new_tag('graphic')
        fig_tag.append(graph_tag)
        get_href = cur_tag.get('src').split('/')
        fig_tag.find('graphic')['url'] = f'http://feb-web.ru/feb/chekhov/{get_href[-2]}/{get_href[-1]}'
        desc_tag = self.soup_tei.new_tag('figDesc')
        fig_tag.append(desc_tag)
        # desc_tag.string = cur_tag.get('alt')
        self.move_text_with_notes(desc_tag, cur_tag.get('alt'))
        ExistenceSeter.process_all_existences(desc_tag, 'figure')

    def process_subheading(self, cur_tag):
        """Обрабатывает абзац-подзаголовок"""
        new_p = self.soup_tei.new_tag('p')
        self._pb_tag.append(new_p)
        tag_headline = self.soup_tei.new_tag('head')
        new_p.append(tag_headline)
        self._body.find('head')['rend'] = 'center'
        self._body.find('head')['type'] = 'subtitle'
        # tag_headline.string = cur_tag.text.split('\n')[0]
        self.move_text_with_notes(tag_headline, cur_tag)
        ExistenceSeter.process_all_existences(tag_headline, 'subtitle')

    def process_heading(self, cur_tag):
        """Обрабатывает абзац-заголовок"""
        new_p = self.soup_tei.new_tag('p')
        self._pb_tag.append(new_p)
        tag_headline = self.soup_tei.new_tag('head')
        new_p.append(tag_headline)
        self._body.find('head')['rend'] = 'center'
        tag_hi = self.soup_tei.new_tag('hi')
        tag_headline.append(tag_hi)
        self._body.find('hi')['rend'] = 'strong'
        # tag_hi.string = cur_tag.text.split('\n')[0]
        self.move_text_with_notes(tag_hi, cur_tag)
        ExistenceSeter.process_all_existences(tag_hi, 'title')

    def process_epigraph(self, cur_tag):
        """Обрабатывает абзац-эпиграф"""
        new_p = self.soup_tei.new_tag('p')
        self._pb_tag.append(new_p)
        tag_epigraph = self.soup_tei.new_tag('epigraph')
        new_p.append(tag_epigraph)
        self._body.find('epigraph')['rend'] = 'right'
        # tag_epigraph.string = cur_tag.text
        self.move_text_with_notes(tag_epigraph, cur_tag)
        ExistenceSeter.process_all_existences(tag_epigraph, 'epigraph')

    def process_greeting(self, cur_tag):
        """Обрабатывает абзац-приветствие/обращение"""
        new_p = self.soup_tei.new_tag('p')
        self._pb_tag.append(new_p)
        tag_salute = self.soup_tei.new_tag('salute')
        new_p.append(tag_salute)
        # tag_salute.string = cur_tag.text.split('\n')[0]
        self.move_text_with_notes(tag_salute, cur_tag)
        ExistenceSeter.process_all_existences(tag_salute, 'salute')

    def process_signature(self, cur_tag):
        """Обрабатывает абзац-подпись"""
        new_p = self.soup_tei.new_tag('p')
        self._pb_tag.append(new_p)
        tag_podp = self.soup_tei.new_tag('signed')
        new_p.append(tag_podp)
        # tag_podp.string = cur_tag.text.split('\n')[0]
        self.move_text_with_notes(tag_podp, cur_tag)
        ExistenceSeter.process_all_existences(tag_podp, 'signed')

    def process_text(self, cur_tag):
        """Обрабатывает абзац-текст"""
        new_p = self.soup_tei.new_tag('p')
        self._pb_tag.append(new_p)
        # new_p.string = cur_tag.text.split('\n')[0]
        self.move_text_with_notes(new_p, cur_tag)
        ExistenceSeter.process_all_existences(new_p, 'text')

    def process_notes(self):
        """Обработка примечаний"""
        self._link_tag = self.soup_tei.new_tag('linkGrp')
        self._body.append(self._link_tag)
        self._link_tag.string = 'Примечания'
        try:
            first_tag = self.soup_notes_html.find('h4', attrs={'id': self._text_id})
            next_tag = first_tag.find_next('h4')

            note_tag = self.soup_tei.new_tag('link')
            note_tag['target'] = 'external_snos'
            self._link_tag.append(note_tag)
        except:
            return
        all_tags = first_tag.find_all_next()
        for cur_tag in all_tags:
            if cur_tag == next_tag:
                break
            if cur_tag.has_attr('class') and re.match(r'small\S*|prim\S*|text\S*|txt\S*|mtext\S*',
                                                      cur_tag['class'][0]) is not None:
                if cur_tag.text[:4].lstrip() == 'Стр.' or cur_tag.text[:3].lstrip() == '...':
                    note_tag1 = self.soup_tei.new_tag('link')
                    note_tag1['target'] = 'external_snos'
                    self._link_tag.append(note_tag1)
                    new_p = self.soup_tei.new_tag('p')
                    note_tag1.append(new_p)
                    new_p.string = cur_tag.text.split('\n')[0]
                    ExistenceSeter.process_all_existences(new_p, 'note')
                else:
                    new_p = self.soup_tei.new_tag('p')
                    note_tag.append(new_p)
                    new_p.string = cur_tag.text.split('\n')[0]
                    ExistenceSeter.process_all_existences(new_p, 'note')

    def process_snos(self):
        """Получает примечания внутри произведения из раздела сноски"""
        text = self.soup_html.find_all('p', class_=['snos', 'snoska'])
        for a in text:
            note_tag = self.soup_tei.new_tag('link')
            note_tag['target'] = a['id']
            self._link_tag.append(note_tag)
            note_tag.string = re.sub('^\d+ ', '', a.text)
            ExistenceSeter.process_all_existences(note_tag, 'note')

    def link_notes_in_text(self):
        """Присваиваем примечаниям id"""
        notes = self.soup_tei.find('body').find_all('note')
        linkgrp = self.soup_tei.find('linkgrp')
        links_snos = linkgrp.find_all('link', target=lambda x: x != 'external_snos')
        links_external = linkgrp.find_all('link', target='external_snos')
        for note in notes:
            if note['xml:id'] == 'external_link':
                for i_link in range(len(links_external) - 1, -1, -1):
                    if links_external[i_link].text.find(note.text.strip()) != -1:
                        note['xml:id'] = f'note{i_link + 1}'
                        break
                    note['xml:id'] = 'note1'
            else:
                for i_link in range(len(links_snos)):
                    if note['xml:id'] == links_snos[i_link]['target']:
                        note['xml:id'] = 'note' + str(i_link + 1 + len(links_external))
                        break

        for i_link in range(len(links_external)):
            links_external[i_link]['target'] = f'#note{i_link + 1}'

        for i_link in range(len(links_snos)):
            links_snos[i_link]['target'] = f'#note{i_link + 1 + len(links_external)}'

    def fill_all_text(self):
        """Полная обработка текста"""
        self._help_get_id()
        self._help_find_text_tags()

        for cur_tag in self._pars[1:]:
            if cur_tag.has_attr('class') and cur_tag['class'][0] == 'page':  # Если это страница
                self.process_page(cur_tag)
            elif cur_tag.has_attr('alt'):  # Если это изображение
                self.process_image(cur_tag)
            elif cur_tag.has_attr('class') and re.match(r'zg\S*',
                                                        cur_tag['class'][0]) is not None:  # Если это подзаголовок
                self.process_subheading(cur_tag)
            elif cur_tag.has_attr('class') and re.match(r'tit\S*|zag\S*',
                                                        cur_tag['class'][0]) is not None:  # Если это заголовок
                self.process_heading(cur_tag)
            elif cur_tag.has_attr('class') and re.match(r'epig\S*',
                                                        cur_tag['class'][0]) is not None:  # Если это эпиграф
                self.process_epigraph(cur_tag)
            elif cur_tag.has_attr('class') and re.match(r'obraw\S*', cur_tag['class'][
                0]) is not None:  # Если это приветствие/обращение (в письме)
                self.process_greeting(cur_tag)
            elif cur_tag.has_attr('class') and re.match(r'podp\S*',
                                                        cur_tag['class'][0]) is not None:  # Если это подпись (в письме)
                self.process_signature(cur_tag)
            elif cur_tag.has_attr('class') and re.match(r'text\S*|curs\S*|small\S*|vis\S*|center\S*',
                                                        cur_tag['class'][0]) is not None:  # Если это текст
                self.process_text(cur_tag)

        # Переносим сноски
        self.process_notes()

        # Получаем примечания внутри произведения из раздела сноски
        self.process_snos()

        # исправляем возможные ошибки
        tei_doc = str(self.soup_tei.prettify()[2:])
        tei_doc = tei_doc.replace('&lt;', r'<')
        tei_doc = tei_doc.replace('&gt;', r'>')
        self.soup_tei = BeautifulSoup(tei_doc, 'html.parser')

        # Присваиваем примечаниям id
        self.link_notes_in_text()