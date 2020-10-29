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
    Student
)
from app.services.course import CourseQueryService
from app.services.graph import _GraphQueryService
from app.utils import J2QueryStrHelper
from app.utils.namespaces import *
from typing import Tuple
import math


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
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(file_name="construct_course_query")
        )
        # self.cache_graph = self.queryable.graph
        courses = self._graph_get_all_courses()

        return courses

    def get_courses_by_department_uri(self, *, department_uri: URIRef) -> Tuple[Course]:
        pass

    def get_courses_by_topic(self, *, topic: Topic) -> Tuple[Course]:
        pass

    def get_course_code_by_uri(self, *, course_code_uri: URIRef) -> CourseCode:
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
                    {
                        "var_name": "?departmentCodeUri",
                        "var_values": [department_code_uri.n3()],
                    }
                ],
            )
        )
        return self._graph_get_department_code_by_uri(
            department_code_uri=department_code_uri
        )

    def get_department_by_uri(self, *, department_uri: URIRef) -> Department:
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

    def get_all_requirements(self) -> Tuple[Requirement]:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(file_name="construct_requirement_query")
        )
        # self.cache_graph = self.queryable.graph
        courses = self._graph_get_all_requirements()

        return courses

    def get_requirement_by_uri(self, *, requirement_uri: URIRef) -> Requirement:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="construct_requirement_query",
                constraints=[
                    {
                        "var_name": "?requirementUri",
                        "var_values": [requirement_uri.n3()],
                    }
                ],
            )
        )
        return self._graph_get_requirement_by_uri(requirement_uri=requirement_uri)

    def get_student_by_uri(self, *, student_uri) -> Student:
        pass

    ###

    def _graph_get_course_by_uri(self, *, course_uri: URIRef) -> Course:
        if (course_uri, None, None) not in self.cache_graph:
            # TODO: exceptions like raise RecipeNotFoundException(recipe_uri=recipe_uri)
            pass

        # TODO: revised implementation based on ontology updates
        course_name = self.cache_graph.value(course_uri, CRS_NS["hasName"]).value
        course_description = self.cache_graph.value(
            course_uri, CRS_NS["hasDescription"]
        )
        course_code = self._graph_get_course_code_by_uri(
            course_code_uri=self.cache_graph.value(course_uri, CRS_NS["hasCourseCode"])
        )
        department = self._graph_get_department_by_uri(
            department_uri=self.cache_graph.value(course_uri, CRS_NS["hasDepartment"])
        )
        course_credits = self.cache_graph.value(course_uri, CRS_NS["hasCredits"]).value
        special_tags = frozenset(
            st.value
            for st in self.cache_graph.objects(course_uri, CRS_NS["hasSpecialTag"])
        )
        required_prerequisites = frozenset(
            self.cache_graph.objects(course_uri, CRS_NS["hasRequiredPrerequisite"])
        )
        recommended_prerequisites = frozenset(
            self.cache_graph.objects(course_uri, CRS_NS["hasRecommendedPrerequisite"])
        )
        corequisites = frozenset(
            self.cache_graph.objects(course_uri, CRS_NS["hasCorequisite"])
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

    def _graph_get_course_code_by_uri(self, *, course_code_uri: URIRef) -> CourseCode:
        name = self.cache_graph.value(course_code_uri, LCC_LR_NS["hasTag"]).value
        level = self.cache_graph.value(course_code_uri, CRS_NS["hasLevel"]).value
        department_code = self._graph_get_department_code_by_uri(
            department_code_uri=self.cache_graph.value(
                course_code_uri, CRS_NS["hasDepartmentCode"]
            )
        )
        cross_listed = tuple(
            self.cache_graph.objects(course_code_uri, CRS_NS["hasCrossListing"])
        )
        return CourseCode(
            uri=course_code_uri,
            name=name,
            cross_listed=cross_listed,
            course_level=level,
            department_code=department_code,
        )

    def _graph_get_department_code_by_uri(
        self, *, department_code_uri: URIRef
    ) -> DepartmentCode:
        name = self.cache_graph.value(department_code_uri, LCC_LR_NS["hasTag"]).value
        dept = self._graph_get_department_by_uri(
            department_uri=self.cache_graph.value(
                department_code_uri, CRS_NS["hasDepartment"]
            )
        )
        return DepartmentCode(uri=department_code_uri, name=name, department=dept)

    def _graph_get_department_by_uri(self, *, department_uri: URIRef) -> Department:
        name = self.cache_graph.value(department_uri, CRS_NS["hasName"]).value
        return Department(
            uri=department_uri,
            name=name,
            offered_major_uris=(),  # TODO
            offered_degree_uris=(),  # TODO
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

    def _graph_get_all_requirements(self) -> Tuple[Requirement]:
        requirements = []
        for requirement_uri in self.cache_graph.subjects(
            RDF_NS["type"], CRS_NS["Requirement"]
        ):
            requirements.append(
                self._graph_get_requirement_by_uri(requirement_uri=requirement_uri)
            )

        return tuple(requirements)

    def _graph_get_requirement_by_uri(self, *, requirement_uri: URIRef) -> Requirement:

        credits = self.cache_graph.value(requirement_uri, CRS_NS["requiresCredits"])
        cc_restriction = self._graph_get_course_code_restriction_by_uri(
            course_code_restriction_uri=self.cache_graph.value(
                requirement_uri, CRS_NS["hasCourseCodeRestriction"]
            )
        )
        share_req_uris = self.cache_graph.objects(
            requirement_uri, CRS_NS["canShareCreditsWith"]
        )
        sub_req_uris = self.cache_graph.objects(
            requirement_uri, CRS_NS["hasSubRequirement"]
        )
        restrict_req_uris = self.cache_graph.objects(
            requirement_uri, CRS_NS["hasRestriction"]
        )
        fulfill_by_req_uri = self.cache_graph.objects(
            requirement_uri, CRS_NS["isFulfilledBy"]
        )

        return Requirement(
            uri=requirement_uri,
            requires_credits=credits,
            share_credits_with_requirement_uris=share_req_uris,
            restriction_requirement_uris=restrict_req_uris,
            sub_requirement_uris=sub_req_uris,
            fulfilled_by_requirement_uris=fulfill_by_req_uri,
            course_code_restriction=cc_restriction,
        )

    def _graph_get_course_code_restriction_by_uri(
        self, *, course_code_restriction_uri: URIRef
    ) -> CourseCodeRestriction:

        cc_uri = course_code_restriction_uri
        valid_cc_names = frozenset(
            vcct.value
            for vcct in self.cache_graph.objects(
                cc_uri, CRS_NS["hasValidCourseCodeTag"]
            )
        )
        valid_dc_names = frozenset(
            vcct.value
            for vcct in self.cache_graph.objects(
                cc_uri, CRS_NS["hasValidDepartmentCodeTag"]
            )
        )
        rstag_names = frozenset(
            vcct.value
            for vcct in self.cache_graph.objects(cc_uri, CRS_NS["hasSpecialTag"])
        )
        min_lvl = self.cache_graph.value(cc_uri, CRS_NS["hasValidLevelMin"])
        if min_lvl:
            min_lvl = min_lvl.value
        else:
            min_lvl = 0

        max_lvl = self.cache_graph.value(cc_uri, CRS_NS["hasValidLevelMax"])
        if max_lvl:
            max_lvl = max_lvl.value
        else:
            max_lvl = math.inf

        return CourseCodeRestriction(
            uri=course_code_restriction_uri,
            required_special_tag_names=rstag_names,
            valid_course_code_names=valid_cc_names,
            valid_department_code_names=valid_dc_names,
            min_level=min_lvl,
            max_level=max_lvl,
        )
