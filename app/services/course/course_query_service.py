from abc import ABC, abstractmethod
from rdflib import URIRef
from app.models import (
    Course,
    CourseSection,
    ScheduledCourseSection,
    Topic,
    CourseCode,
    Department,
    DepartmentCode,
    Requirement,
    CourseCodeRestriction,
)
from typing import Tuple


class CourseQueryService(ABC):
    @abstractmethod
    def get_course_by_uri(self, *, course_uri: URIRef) -> Course:
        pass

    @abstractmethod
    def get_all_courses(self) -> Tuple[Course]:
        pass

    @abstractmethod
    def get_courses_by_department_uri(self, *, department_uri: URIRef) -> Tuple[Course]:
        pass

    @abstractmethod
    def get_courses_by_topic(self, *, topic: Topic) -> Tuple[Course]:
        pass

    @abstractmethod
    def get_course_by_course_code_uri(self, *, course_code_uri: URIRef) -> Course:
        pass

    @abstractmethod
    def get_course_code_by_uri(self, *, course_code_uri: URIRef) -> CourseCode:
        pass

    @abstractmethod
    def get_department_code_by_uri(
        self, *, department_code_uri: URIRef
    ) -> DepartmentCode:
        pass

    @abstractmethod
    def get_department_by_uri(self, *, department_uri: URIRef) -> Department:
        pass

    @abstractmethod
    def get_course_sections_by_course_uri(
        self, *, course_uri: URIRef
    ) -> Tuple[CourseSection]:
        pass

    @abstractmethod
    def get_course_section_by_uri(self, *, course_section_uri: URIRef) -> CourseSection:
        pass

    @abstractmethod
    def get_scheduled_course_section_by_uri(
        self, *, scheduled_course_uri: URIRef
    ) -> ScheduledCourseSection:
        pass

    @abstractmethod
    def get_scheduled_course_sections_by_instructor_uri(
        self, *, instructor_uri: URIRef
    ) -> Tuple[ScheduledCourseSection]:
        pass

    @abstractmethod
    def get_scheduled_course_section_by_crn(
        self, *, scheduled_course_crn: str
    ) -> ScheduledCourseSection:
        pass

    @abstractmethod
    def get_requirement_by_uri(self, *, requirement_uri: URIRef) -> Requirement:
        pass

    @abstractmethod
    def get_all_requirements(self) -> Tuple[Requirement]:
        pass
