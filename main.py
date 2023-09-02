from typing import List, Dict

import huji_he_coursescraper
from course import Course
from huji_he_coursescraper import HujiHebrewCourseScraper
import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    courses_dict_list: List[Dict] = []
    
    courses_id_list = [
        67579, 67865, 67894, 67311, 67313, 67601, 67646, 67689, 67733, 67734,
        67819, 67836, 67838, 67841, 67843, 67844, 67845, 67848, 67860, 67874,
        67879, 67882, 67887, 67888, 67890, 67896, 67979, 67980, 67996, 76551,
        67660, 67834, 67846, 67897, 67898, 67903, 67977, 67512, 67568, 67581,
        67618, 67619, 67709, 67817, 67817, 67839, 67850, 67861, 67866, 67870,
        67881, 67895, 67927, 67297, 67470, 67598, 67695, 67702, 67717, 67811,
        67840, 67885, 67508, 67509, 67548, 67561, 67564, 67596, 67677, 67720,
        67731, 67648, 67663, 67691, 67781, 67790, 67824, 67883, 67892, 67513,
        67515, 67519, 67607, 67613, 67466, 67534, 67612, 67681, 67883, 67886,
        67455, 67508, 67548, 67561, 67564, 67658, 67664, 67705, 67731, 67800,
        67818, 67822, 67912, 67978, 76558, 76562, 67103, 67296, 67609, 67680,
        67682, 67735, 76906, 51601, 52311, 55923, 67392, 67398, 67455, 67506,
        67508, 67509, 67513, 67515, 67518, 67519, 67531, 67542, 67548, 67561,
        67564, 67577, 67579, 67581, 67594, 67596, 67604, 67607, 67613, 67658,
        67664, 67668, 67677, 67678, 67678, 67688, 67692, 67705, 67720, 67731,
        67734, 67800, 67817, 67829, 67842, 67850, 67850, 67859, 67912, 67913,
        67916, 67978, 72920, 76553, 76562, 76908, 76909, 76915, 76921, 80972,
        6111, 67103, 67381, 67466, 67470, 67501, 67534, 67612, 67624, 67648,
        67663, 67680, 67681, 67682, 67691, 67706, 67735, 67790, 67840, 67871,
        67883, 67886, 67892, 76906, 77812
    ]
    
    for i in range(len(courses_id_list)):
        course_id = courses_id_list[i]
        print("[{}/{} | {:3.2f}%]".format(i, len(courses_id_list),
                                     i/len(courses_id_list)*100),
              course_id, end=' >> ')
        _course = Course()
        huji_course_scraper = HujiHebrewCourseScraper(course_id, 2024)
        huji_course_scraper.update_course(_course)
        course_dict = _course.to_dict()

        # semester: from list to string
        semester = course_dict.pop('Semester [A, B, yearly or other]', None)
        if semester is not None:
            semester_str = \
                huji_he_coursescraper.symbol_to_huji_semester(semester)
            course_dict.update({'Semester': semester_str})

        # periods to strings
        periods_list = course_dict.pop('Course Lectures & Exercises Periods', None)
        if periods_list is not None:
            periods_str = ''

            for period in periods_list:
                periods_str += period['type']
                weekday = period['weekday']
                if weekday != 0:
                    start, end = period['start_time'], period['end_time']
                    periods_str += ': יום ' + huji_he_coursescraper \
                        .weekday_number_to_hebrew_weekday_symbol(weekday) \
                        + '\' ' + start.strftime('%H:%M') + '-' \
                        + end.strftime('%H:%M')
                periods_str += '\n'
            course_dict.update({
                'Course Lectures & Exercises Periods':
                    periods_str[0:-1] # without the last newline
            })

        # exams due dates to strings
        due_dates_list = course_dict.pop('Final Exam Due Date', None)
        if due_dates_list is not None:
            due_dates_str = ''
            for (date, metadata) in due_dates_list:
                due_dates_str += 'סמסטר ' \
                        + huji_he_coursescraper \
                            .symbol_to_huji_semester(metadata['semester']) \
                        + ' מועד ' + metadata['MOED'] + ': ' \
                        + date.strftime('%d/%m/%y') + '\r\n'
            course_dict.update({'Final Exam Due Date': due_dates_str})

        # other_data: insert normally to dict
        course_dict.update(course_dict.pop('other_data'))

        # append to list
        courses_dict_list.append(course_dict)
        print('Success')

    courses_df = pd.DataFrame.from_dict(courses_dict_list)
    courses_df.to_excel('output.xlsx')
