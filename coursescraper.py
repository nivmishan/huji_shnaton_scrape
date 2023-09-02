from abc import ABC, abstractmethod
from typing import List, Dict
from course import Course

class CourseScraper(ABC):
    @abstractmethod
    def __init__(self, *args):
        pass

    @abstractmethod
    def scrape(self, *args) -> None:
        pass

    def update_course(self, course: Course) -> None:
        course.set_course_name(self.get_name())
        course.set_id(self.get_course_id())
        course.set_department(self.get_department())
        course.set_credits(self.get_credits())
        course.set_semesters(self.get_semesters())
        course.set_teaching_languages(self.get_teaching_languages())
        course.set_staff(self.get_staff())
        course.set_description(self.get_description())
        course.set_attendance_requirements(self.get_attendance_requirements())
        course.set_periods(self.get_periods())
        course.set_exam_type(self.get_exam_type())
        course.set_exam_dates(self.get_exam_dates())
        course.set_institute(self.get_institute())

    def get_course_id(self) -> str|None:
        """scrape course id"""
        return None

    def get_institute(self) -> str|None:
        """scrape course institute"""

    def get_name(self) -> str | None:
        """scrape course name"""
        return None

    def get_department(self) -> str|None:
        """scrape course department"""
        return None

    def get_credits(self) -> int|None:
        """scrape course credits"""
        return None

    def get_semesters(self) -> List[str]|None:
        """scrape semester"""
        return None

    def get_periods(self) -> List[Dict]|None:
        """scrape lectures & exercises periods"""
        return None

    def get_teaching_languages(self):
        """scrape teaching languages"""
        return None

    def get_staff(self):
        """scrape course staff"""
        return None

    def get_description(self):
        """scrape course description"""
        return None

    def get_attendance_requirements(self):
        """scrape attendance requirements"""
        return None

    def get_exam_type(self):
        """scrape exam type"""
        return None

    def get_exam_dates(self):
        """scrape exam due date"""
        return None