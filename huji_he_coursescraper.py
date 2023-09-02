from collections import defaultdict
from datetime import datetime, time

from course import Course
from coursescraper import CourseScraper
from bs4 import BeautifulSoup as bs
import requests
from typing import List, Dict
from re import search

__huji_semesters_symbols = {
    'א\'': ['A'],
    'ב\'': ['B'],
    'א\' או ב\'': ['A', 'B'],
    'קורס שנתי': ['yearly']
}

def huji_semester_to_symbol(hebrew_semester: str) -> List[str]:
    """return A/B/yearly as a list, or given argument if it isn't recognize"""
    if hebrew_semester in __huji_semesters_symbols.keys():
        return __huji_semesters_symbols[hebrew_semester]
    else:
        return [hebrew_semester]

def symbol_to_huji_semester(symbol_semester_list: List[str]) -> str:
    """return hebrew semester name from A/B/yearly symbols list"""
    for key in __huji_semesters_symbols.keys():
        if sorted(__huji_semesters_symbols[key]) == \
                sorted(symbol_semester_list):
            return key
    else:
        return ','.join(symbol_semester_list)


__hebrew_weekday_symbols = {
    'א': 1,
    'ב': 2,
    'ג': 3,
    'ד': 4,
    'ה': 5,
    'ו': 6,
    'ש': 7,
    'ז': 7
}

def hebrew_weekday_symbol_to_weekday_number(symbol: str) -> int:
    """return equivalent weekday number [1-7] to hebrew symbol [א-ו,ש]
    or 0 if unrecognized"""
    if symbol in __hebrew_weekday_symbols.keys():
        return __hebrew_weekday_symbols[symbol]
    else:
        return 0

def weekday_number_to_hebrew_weekday_symbol(weekday_number: int) -> str|None:
    """return equivalent hebrew symbol [א-ו,ש] to weekday number [1-7]
        or None if unrecognized"""
    for key in __hebrew_weekday_symbols.keys():
        if __hebrew_weekday_symbols[key] == weekday_number:
            return key
    return None

class HujiHebrewCourseScraper(CourseScraper):

    def __init__(self, course_id: str, year: int):
        self.__catalog_url = f"https://catalog.huji.ac.il/pages/wfrCourse.aspx?" \
                             "year={year}&faculty=12&courseId={course_id}" \
            .format(year=year, course_id=course_id)
        self.__syllabus_url = f"https://shnaton.huji.ac.il/index.php/NewSyl/" \
                              "{course_id}/1/{year}/" \
            .format(year=year, course_id=course_id)

        self.__syllabus_page = None
        self.__catalog_page = None
        self.scrape(course_id, year)

        self.__id = course_id
        self.__institute = 'האוניברסיטה העברית בירושלים'

    def update_course(self, course: Course) -> None:
        super().update_course(course)

        course.other_data.update({
            'catalog_url': self.__catalog_url,
            'syllabus_url': self.__syllabus_url,
            'coordinator': self.get_coordinator(),
            'coordinator mail': self.get_coordinator_mail()
        })


    def scrape(self, course_id: str, year: int):
        self.__syllabus_page = \
            self._get_huji_he_course_syllabus_page(course_id, year)
        self.__catalog_page = \
            self._get_huji_he_course_catalog_page(course_id, year)

    def _get_huji_he_course_catalog_page(self, course_id: str, year: int):
        catalog_data = requests.get(self.__catalog_url)
        catalog_soup = bs(catalog_data.content.decode('utf-8'), 'html5lib')
        return catalog_soup

    def _get_huji_he_course_syllabus_page(self, course_id: str, year: int) -> bs:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        syllabus_data = requests.get(self.__syllabus_url, headers=headers)
        syllabus_soup = bs(syllabus_data.content.decode('windows-1255'), 'html5lib')
        return syllabus_soup

    def _find_in_text_syllabus_by_header(self, header: str):
        for tag in self.__syllabus_page.find_all('div'):
            for b_tag in tag.find_all('b'):
                if header in b_tag.text:
                    # remove header & newlines
                    ret_value = tag.text[len(b_tag.text)+1:]
                    ret_value = ret_value.replace('\n', '')
                    return ret_value
        return None

    def get_course_id(self) -> str|None:
        """return given course id"""
        return self.__id

    def get_institute(self) -> str|None:
        """return given course institute"""
        return self.__institute

    def get_name(self) -> str|None:
        """scrape course name"""
        name_tag = self.__catalog_page.find(name='span',
                            attrs={'id': 'lblCourseName'})
        return name_tag.text if name_tag is not None else None

    def get_department(self) -> str|None:
        """scrape course department"""
        department_tag = self.__catalog_page.find(name='span',
                            attrs={'class': 'toarTitle'})
        return department_tag.text if department_tag is not None else None

    def get_credits(self) -> int|None:
        """scrape course credits"""
        credits_tag = self.__catalog_page.find(name='span',
                            attrs={'id': 'lblPoints'})
        return int(credits_tag.text) if credits_tag is not None else None

    def get_semesters(self) -> List[str]|None:
        """scrape semester"""
        semester_tag = self.__catalog_page.find(name='span',
                            attrs={'id': 'lblSemester'})
        if semester_tag is not None:
            semester_text = semester_tag.text
            return huji_semester_to_symbol(semester_text)
        else:
            return None

    def get_periods(self) -> List[Dict]|None:
        """scrape lectures & exercises periods"""
        periods = []
        periods_table = self.__catalog_page.find(name='table',
                            attrs={'id': 'grdMoadim'})
        if periods_table is None: return None

        periods_tag_list = periods_table.find_all(name='tr',
                            class_=lambda x: x != 'courseTabHeader')
        if periods_tag_list is None: return None

        for period_tag in periods_tag_list:
            class_type_tag = \
                period_tag.find(name='span', id=lambda x: 'lblGroupType' in x)
            class_start_time_tag = \
                period_tag.find(name='span', id=lambda x: 'lblFrom' in x)
            class_end_time_tag = \
                period_tag.find(name='span', id=lambda x: 'lblTo' in x)
            class_day_tag = \
                period_tag.find(name='span', id=lambda x: 'lblDay' in x)

            period_dict = {
                'type': class_type_tag.text,
                'weekday': hebrew_weekday_symbol_to_weekday_number(
                               class_day_tag.text)
            }

            # period stat time
            try:
                period_dict['start_time'] = datetime.strptime(
                    class_start_time_tag.text, "%H:%M").time()
            except ValueError:
                period_dict['start_time'] = time()

            # period end time
            try:
                period_dict['end_time'] = datetime.strptime(
                    class_end_time_tag.text, "%H:%M").time()
            except ValueError:
                period_dict['end_time'] = time()

            # add to periods list
            if period_dict not in periods:
                periods.append(period_dict)

        return periods

    def get_teaching_languages(self):
        """scrape teaching languages"""
        teaching_languages = self._find_in_text_syllabus_by_header('שפת ההוראה')
        return teaching_languages

    def get_staff(self):
        """scrape course staff"""
        staff = self._find_in_text_syllabus_by_header('מורי הקורס')
        return staff

    def get_description(self):
        """scrape course description"""
        description = self._find_in_text_syllabus_by_header('תאור כללי של הקורס')
        return description

    def get_attendance_requirements(self):
        """scrape attendance requirements"""
        requirements_text = self._find_in_text_syllabus_by_header('דרישות נוכחות')
        if requirements_text is None:
            return None
        if 'אין' in requirements_text:
            return 0
        elif requirements_text.isnumeric():
            return int(requirements_text)/100
        else:
            return None

    def get_exam_type(self):
        """scrape exam type"""
        teaching_languages_tag = self.__catalog_page.find(name='span',
                                                          id='lblExamType')
        return teaching_languages_tag.text if teaching_languages_tag \
                                              is not None else None

    def get_exam_dates(self):
        """scrape exam dates"""
        dates = []
        exam_dates_table = self.__catalog_page.find(name='table',
                                                    id='grdBhinot')
        if exam_dates_table is None:
            return None
        exam_dates_line_list = exam_dates_table.find_all(name='tr',
                                                attrs={'class': 'conditions'})
        for exam_dates_line in exam_dates_line_list:

            date_tag = exam_dates_line.find(name='span',
                                            id=lambda x: 'lblBhinotDate' in x)
            match = search('\d{2}/\d{2}/\d{4}', date_tag.text)
            if match.group(0) is None:
                return None
            date = datetime.strptime(match.group(0), '%d/%m/%Y').date()
            # get metadata
            semester_tag = exam_dates_line.find(name='span',
                                        id=lambda x: 'lblBhinotSemeste' in x)
            MOED_tag = exam_dates_line.find(name='span',
                                        id=lambda x: 'lblBhinotMoed' in x)

            metadata = {
                'semester': huji_semester_to_symbol(semester_tag.text),
                'MOED': MOED_tag.text
            }
            # push to array
            dates.append((date, metadata))

        return dates


    def get_coordinator(self):
        """scrape course coordinator"""
        coordinator = self \
            ._find_in_text_syllabus_by_header('מורה אחראי על הקורס')
        return coordinator
    
    
    def get_coordinator_mail(self):
        """scrape course coordinator mail"""
        coordinator_mail = self \
            ._find_in_text_syllabus_by_header('דוא"ל של המורה האחראי על הקורס')
        return coordinator_mail