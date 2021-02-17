import re
from src.ner_tools import extract_names, extract_dates

class ExistenceSeter():
    """Класс с методами для разметки сущностей"""

    @staticmethod
    def set_people(par_tag, location_text):
        """Расставляет теги имен"""

        def pattern_repl_name_fio(name_part, name_info_fio, name_format):
            """Готовит шаблоны для замены"""
            if name_part in name_info_fio:
                pattern_start = name_info_fio[name_part]
                pattern_end = r'.'
                repl_end = r'.'
                if len(name_info_fio[name_part]) != 1:
                    try:
                        pattern_start = name_info_fio[name_part][:-2]
                    except:
                        pattern_start = name_info_fio[name_part][:-1]
                    pattern_end = r'(\w*)'
                    repl_end = r'\g<1>'
                return pattern_start + pattern_end, name_format.format(name_info_fio[name_part],
                                                                       pattern_start + repl_end)
            return None

        names = extract_names(str(par_tag.string))
        person_format = '<PersName type="{0}">{1}</PersName>'
        name_format = '<forename xml:id="{0}">{1}</forename>'
        surname_format = '<surname xml:id="{0}">{1}</surname>'
        middlename_format = '<forename type="patronym" xml:id="{0}">{1}</forename>'
        for name_info in names[::-1]:
            person_part = par_tag.string[name_info['start']:name_info['end']]
            patterns_repls = []
            pattern_repl = pattern_repl_name_fio('first', name_info['fio'], name_format)
            if pattern_repl is not None:
                patterns_repls.append((*pattern_repl, False))

            pattern_repl = pattern_repl_name_fio('last', name_info['fio'], surname_format)
            if pattern_repl is not None:
                patterns_repls.append((*pattern_repl, False))

            pattern_repl = pattern_repl_name_fio('middle', name_info['fio'], middlename_format)
            if pattern_repl is not None:
                patterns_repls.append((*pattern_repl, False))

            name_parts = re.split('\s+', person_part)
            for i in range(len(name_parts)):
                for j in range(len(patterns_repls)):
                    pattern, repl, used = patterns_repls[j]
                    if used:
                        continue
                    if re.search(pattern, name_parts[i]):
                        name_parts[i] = re.sub(pattern, repl, name_parts[i])
                        patterns_repls[j] = (pattern, repl, True)
                        break

            new_person_part = person_format.format(location_text, ' '.join(name_parts))

            par_tag.string = par_tag.string[:name_info['start']] + \
                             new_person_part + \
                             par_tag.string[name_info['end']:]

    @staticmethod
    def set_dates(par_tag):
        """Расставляет теги дат"""

        def set_date_part(res_lst, date_part_type):
            if date_part_type:
                res_lst.append(str(date_part_type))
            else:
                res_lst.append('')

        dates = extract_dates(str(par_tag.string))
        date_format = '<date when="{0}">{1}</date>'
        for date_info in dates[::-1]:
            date_part = par_tag.string[date_info.start:date_info.stop]
            res_lst = []
            set_date_part(res_lst, date_info.fact.year)
            set_date_part(res_lst, date_info.fact.month)
            set_date_part(res_lst, date_info.fact.day)
            new_date_part = date_format.format('-'.join(res_lst), date_part)
            par_tag.string = par_tag.string[:date_info.start] + \
                             new_date_part + \
                             par_tag.string[date_info.stop:]

    @staticmethod
    def process_all_existences(par_tag, location_text):
        """Полная обработка сущностей"""
        ExistenceSeter.set_people(par_tag, location_text)
        ExistenceSeter.set_dates(par_tag)