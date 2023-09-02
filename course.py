import os
from typing import List, Callable, Dict, Tuple
from datetime import date

class Course:

    def __init__(self):
        self.__id: str|None = None                  # uniq course id
        self.__name: str|None = None                # course name
        self.__department: str|None = None          # course department
        self.__credits: int|None = None             # credits amount
        self.__semesters: List[str]|None = None     # semesters [A,B,yearly]
        self.__teaching_languages: List[str]|None = None
                                                    # course teaching language
        self.__staff: List[str]|None = None         # list of staff names
        self.__description: str|None = None         # course description
        self.__attendance_requirements: float|None = None
                                                    # float between 0 and 1
        self.__periods: List[Dict]|None = None      # classes time periods
        self.__exam_type: str|None = None           # final exam/assigment type
        self.__exam_dates: List[Tuple[date, Dict]]|None = None
                                                    # final exam/assigment time
        self.__institute: str|None = None           # the course's institute
        self.other_data: Dict = {}

    def get_id(self) -> str:
        """return Course id"""
        return self.__id

    def get_course_name(self) -> str:
        """return Course name"""
        return self.__name

    def get_department(self) -> str:
        """return Course Department"""
        return self.__department

    def get_credits(self) -> int:
        """return Course Credits Amount"""
        return self.__credits

    def get_semesters(self) -> List[str]:
        """return Semester [A, B, yearly or other]"""
        return self.__semesters

    def get_teaching_languages(self) -> List[str]:
        """return Course Teaching Language"""
        return self.__teaching_languages

    def get_staff(self) -> List[str]:
        """return Course Staff Members"""
        return self.__staff

    def get_description(self) -> str:
        """return The Course Description"""
        return self.__description

    def get_attendance_requirements(self) -> float:
        """return Attendance Requirements"""
        return self.__attendance_requirements

    def get_periods(self) -> List[Dict]:
        """return Course Lectures & Exercises Periods"""
        return self.__periods

    def get_exam_type(self) -> str:
        """return Final Exam Type"""
        return self.__exam_type

    def get_exam_dates(self) -> List[Tuple[date, Dict]]:
        """return Final Exam Due Date"""
        return self.__exam_dates

    def get_institute(self) -> str:
        """return Course Parent Institute"""
        return self.__institute

    def set_id(self, course_id: str|None) -> None:
        """Set Course id"""
        self.__id = course_id

    def set_course_name(self, course_name: str|None) -> None:
        """Set Course name"""
        self.__name = course_name

    def set_department(self, department: str|None) -> None:
        """Set Course Department"""
        self.__department = department

    def set_credits(self, _credits: int|None) -> None:
        """Set Course Credits Amount"""
        self.__credits = _credits

    def set_semesters(self, semesters: List[str]|None) -> None:
        """Set Semester [A, B, yearly or other]"""
        self.__semesters = semesters

    def set_teaching_languages(self,
                               teaching_languages: List[str]|None) -> None:
        """Set Course Teaching Language"""
        self.__teaching_languages = teaching_languages

    def set_staff(self, staff: List[str]|None) -> None:
        """Set Course Staff Members"""
        self.__staff = staff

    def set_description(self, description: str|None) -> None:
        """Set The Course Description"""
        self.__description = description

    def set_attendance_requirements(self,
                                    attendance_requirements: float|None) -> None:
        """Set Attendance Requirements"""
        self.__attendance_requirements = attendance_requirements

    def set_periods(self, periods: List[Dict]|None) -> None:
        """Set Course Lectures & Exercises Periods"""
        self.__periods = periods

    def set_exam_type(self, exam_type: str|None) -> None:
        """Set Final Exam Type"""
        self.__exam_type = exam_type

    def set_exam_dates(self, exam_dates: List[Tuple[date, Dict]]|None) -> None:
        """Set Final Exam Due Date"""
        self.__exam_dates = exam_dates

    def set_institute(self, institute: str|None) -> None:
        """Set Course Parent Institute"""
        self.__institute = institute


    def to_dict(self) -> Dict:
        return_dict: Dict = {}

        course_information_functions: List[Callable] = [
            self.get_id,
            self.get_course_name,
            self.get_institute,
            self.get_department,
            self.get_credits,
            self.get_semesters,
            self.get_teaching_languages,
            self.get_staff,
            self.get_description,
            self.get_attendance_requirements,
            self.get_periods,
            self.get_exam_type,
            self.get_exam_dates
        ]

        for func in course_information_functions:
            info = func()
            if info is not None:
                return_dict.update({
                    func.__doc__[len('return '):]: func()
                })

        if self.other_data is not None:
            return_dict.update({'other_data': self.other_data})

        return return_dict

    def to_str(self) -> str:
        return_str: str = ""
        course_as_dict = self.to_dict()
        for key in course_as_dict:
            return_str += key + ': ' + str(course_as_dict[key]) + '\n'
        return return_str

