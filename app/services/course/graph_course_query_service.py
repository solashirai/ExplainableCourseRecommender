from rdflib import URIRef
from app.models import Course, CourseSection, ScheduledCourseSection, Topic
from app.services.course import CourseQueryService
from app.services.graph import _GraphQueryService
from typing import Tuple


class GraphCourseQueryService(_GraphQueryService, CourseQueryService):
    def get_course_by_uri(self, *, course_uri: URIRef) -> Course:
        pass

    def get_courses_by_department_uri(self, *, department_uri: URIRef) -> Tuple[Course]:
        pass

    def get_courses_by_topic(self, *, topic: Topic) -> Tuple[Course]:
        pass

    def get_course_by_course_code_uri(self, *, course_code_uri: URIRef) -> Course:
        pass

    def get_course_sections_by_course_uri(
        self, *, course_uri: URIRef
    ) -> Tuple[CourseSection]:
        pass

    def get_course_section_by_uri(self, *, course_section_uri: URIRef) -> CourseSection:
        pass

    def get_scheduled_course_section_by_uri(
        self, *, scheduled_course_uri: URIRef
    ) -> ScheduledCourseSection:
        pass

    def get_scheduled_course_sections_by_instructor_uri(
        self, *, instructor_uri: URIRef
    ) -> Tuple[ScheduledCourseSection]:
        pass

    def get_scheduled_course_section_by_crn(
        self, *, scheduled_course_crn: str
    ) -> ScheduledCourseSection:
        pass

    ###

    def graph_get_course_by_uri(self, *, course_uri: URIRef) -> Course:
        pass

    def graph_get_courses_by_department_uri(
        self, *, department_uri: URIRef
    ) -> Tuple[Course]:
        pass

    def graph_get_courses_by_topic(self, *, topic: Topic) -> Tuple[Course]:
        pass

    def graph_get_course_by_course_code_uri(self, *, course_code_uri: URIRef) -> Course:
        pass

    def graph_get_course_sections_by_course_uri(
        self, *, course_uri: URIRef
    ) -> Tuple[CourseSection]:
        pass

    def graph_get_course_section_by_uri(
        self, *, course_section_uri: URIRef
    ) -> CourseSection:
        pass

    def graph_get_scheduled_course_section_by_uri(
        self, *, scheduled_course_uri: URIRef
    ) -> ScheduledCourseSection:
        pass

    def graph_get_scheduled_course_sections_by_instructor_uri(
        self, *, instructor_uri: URIRef
    ) -> Tuple[ScheduledCourseSection]:
        pass

    def graph_get_scheduled_course_section_by_crn(
        self, *, scheduled_course_crn: str
    ) -> ScheduledCourseSection:
        pass
