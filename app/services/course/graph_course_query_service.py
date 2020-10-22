from rdflib import URIRef
from app.models import Course, CourseSection, ScheduledCourseSection, Topic, CourseCode, Department, DepartmentCode
from app.services.course import CourseQueryService
from app.services.graph import _GraphQueryService
from app.utils import J2QueryStrHelper
from app.utils.namespaces import *
from typing import Tuple


class GraphCourseQueryService(_GraphQueryService, CourseQueryService):
    def get_course_by_uri(self, *, course_uri: URIRef) -> Course:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="construct_course_query",
                constraints=[
                    {"var_name": "?courseUri", "var_values": [course_uri.n3()]}
                ],
            )
        )
        return self._graph_get_course_by_uri(course_uri=course_uri)

    def get_all_courses(self) -> Tuple[Course]:
        # self.get_cache_graph(
        #     sparql=J2QueryStrHelper.j2_query(file_name="construct_course_query")
        # )
        self.cache_graph = self.queryable.graph
        courses = self._graph_get_all_courses()

        return courses

    def get_courses_by_department_uri(self, *, department_uri: URIRef) -> Tuple[Course]:
        pass

    def get_courses_by_topic(self, *, topic: Topic) -> Tuple[Course]:
        pass

    def get_course_code_by_uri(
        self, *, course_code_uri: URIRef
    ) -> CourseCode:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="construct_course_code_query",
                constraints=[
                    {"var_name": "?courseCodeUri", "var_values": [course_code_uri.n3()]}
                ],
            )
        )
        return self._graph_get_course_code_by_uri(course_code_uri=course_code_uri)

    def get_department_code_by_uri(
        self, *, department_code_uri: URIRef
    ) -> DepartmentCode:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="construct_department_code_query",
                constraints=[
                    {"var_name": "?departmentCodeUri", "var_values": [department_code_uri.n3()]}
                ],
            )
        )
        return self._graph_get_department_code_by_uri(department_code_uri=department_code_uri)

    def get_department_by_uri(
        self, *, department_uri: URIRef
    ) -> Department:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="construct_department_query",
                constraints=[
                    {"var_name": "?departmentUri", "var_values": [department_uri.n3()]}
                ],
            )
        )
        return self._graph_get_department_by_uri(department_uri=department_uri)

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

    def _graph_get_course_by_uri(self, *, course_uri: URIRef) -> Course:
        if (course_uri, None, None) not in self.cache_graph:
            # TODO: exceptions like raise RecipeNotFoundException(recipe_uri=recipe_uri)
            pass

        # TODO: revised implementation based on ontology updates
        course_name = self.cache_graph.value(course_uri, CRS_NS["hasName"])
        course_description = self.cache_graph.value(
            course_uri, CRS_NS["hasDescription"]
        )
        course_code = self._graph_get_course_code_by_uri(course_code_uri=self.cache_graph.value(course_uri, CRS_NS["hasCourseCode"]))
        department = self._graph_get_department_by_uri(department_uri=self.cache_graph.value(course_uri, CRS_NS["hasDepartment"]))
        course_credits = self.cache_graph.value(course_uri, CRS_NS["hasCredits"])
        special_tags = frozenset(
            st.value
            for st in self.cache_graph.objects(course_uri, CRS_NS["hasSpecialTag"])
        )
        required_prerequisites = frozenset(
            self.cache_graph.objects(
                course_uri, CRS_NS["hasRequiredPrerequisite"]
            )
        )
        recommended_prerequisites = frozenset(
            self.cache_graph.objects(
                course_uri, CRS_NS["hasRecommendedPrerequisite"]
            )
        )
        corequisites = frozenset(
            self.cache_graph.objects(
                course_uri, CRS_NS["hasCorequisite"]
            )
        )
        topics = tuple(
            tp.value for tp in self.cache_graph.objects(course_uri, CRS_NS["hasTopic"])
        )
        offered_semesters = tuple(
            sem.value
            for sem in self.cache_graph.objects(
                course_uri, CRS_NS["hasOfferedSemesters"]
            )
        )

        return Course(
            uri=course_uri,
            name=course_name,
            description=course_description,
            course_code=course_code,
            special_tags=special_tags,
            required_prerequisites=required_prerequisites,
            corequisites=corequisites,
            recommended_prerequisites=recommended_prerequisites,
            department=department,
            credits=course_credits,
            topics=topics,
            offered_semesters=offered_semesters,
        )

    def _graph_get_all_courses(self) -> Tuple[Course]:

        courses = []
        for course_uri in self.cache_graph.subjects(RDF_NS["type"], CRS_NS["Course"]):
            courses.append(self._graph_get_course_by_uri(course_uri=course_uri))

        return tuple(courses)

    def _graph_get_courses_by_department_uri(
        self, *, department_uri: URIRef
    ) -> Tuple[Course]:
        pass

    def _graph_get_courses_by_topic(self, *, topic: Topic) -> Tuple[Course]:
        pass

    def _graph_get_course_by_course_code_uri(
        self, *, course_code_uri: URIRef
    ) -> Course:
        pass

    def _graph_get_course_code_by_uri(
        self, *, course_code_uri: URIRef
    ) -> CourseCode:
        name = self.cache_graph.value(course_code_uri, LCC_LR_NS['hasTag']).value
        level = self.cache_graph.value(course_code_uri, CRS_NS['hasLevel']).value
        department_code = self._graph_get_department_code_by_uri(department_code_uri=self.cache_graph.value(course_code_uri, CRS_NS['hasDepartmentCode']))
        cross_listed = tuple(self.cache_graph.objects(course_code_uri, CRS_NS['hasCrossListing']))
        return CourseCode(
            uri=course_code_uri,
            name=name,
            cross_listed=cross_listed,
            course_level=level,
            department_code=department_code
        )

    def _graph_get_department_code_by_uri(
        self, *, department_code_uri: URIRef
    ) -> DepartmentCode:
        name = self.cache_graph.value(department_code_uri, LCC_LR_NS['hasTag']).value
        dept = self._graph_get_department_by_uri(department_uri=self.cache_graph.value(department_code_uri, CRS_NS['hasDepartment']))
        return DepartmentCode(
            uri=department_code_uri,
            name=name,
            department=dept
        )

    def _graph_get_department_by_uri(
            self, *, department_uri: URIRef
    ) -> Department:
        name = self.cache_graph.value(department_uri, CRS_NS['hasName']).value
        return Department(
            uri=department_uri,
            name=name,
            offered_major_uris=(),  # TODO
            offered_degree_uris=()  # TODO
        )

    def _graph_get_course_sections_by_course_uri(
        self, *, course_uri: URIRef
    ) -> Tuple[CourseSection]:
        pass

    def _graph_get_course_section_by_uri(
        self, *, course_section_uri: URIRef
    ) -> CourseSection:
        pass

    def _graph_get_scheduled_course_section_by_uri(
        self, *, scheduled_course_uri: URIRef
    ) -> ScheduledCourseSection:
        pass

    def _graph_get_scheduled_course_sections_by_instructor_uri(
        self, *, instructor_uri: URIRef
    ) -> Tuple[ScheduledCourseSection]:
        pass

    def _graph_get_scheduled_course_section_by_crn(
        self, *, scheduled_course_crn: str
    ) -> ScheduledCourseSection:
        pass
