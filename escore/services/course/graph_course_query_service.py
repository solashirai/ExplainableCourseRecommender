from rdflib import URIRef, Literal
from rdflib.namespace import XSD
from escore.models import (
    Course,
    CourseSection,
    ScheduledCourseSection,
    TopicArea,
    CourseCode,
    Department,
    DepartmentCode,
    Requirement,
    CourseCodeRestriction,
    Student,
    Semester,
    PlanOfStudy,
    Degree,
    Major,
    Advisor,
)
from escore.services.course import CourseQueryService
from escore.services.graph import _GraphQueryService
from escore.utils import J2QueryStrHelper
from escore.utils.namespaces import *
from typing import Tuple
from frex.stores import LocalGraph
import math
from itertools import chain


class GraphCourseQueryService(_GraphQueryService, CourseQueryService):
    def get_course_by_uri(self, *, course_uri: URIRef) -> Course:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="course_query",
                constraints=[
                    {"var_name": "?courseUri", "var_values": [course_uri.n3()]}
                ],
            )
        )
        # self.cache_graph = self.queryable.graph
        return self._graph_get_course_by_uri(course_uri=course_uri)

    def get_all_courses(self) -> Tuple[Course, ...]:
        self.get_cache_graph(sparql=J2QueryStrHelper.j2_query(file_name="course_query"))
        # self.cache_graph = self.queryable.graph
        courses = self._graph_get_all_courses()

        return courses

    def get_courses_by_department_uri(self, *, department_uri: URIRef) -> Tuple[Course, ...]:
        pass

    def get_courses_by_topic_area(self, *, topic_area: TopicArea) -> Tuple[Course, ...]:
        pass

    def get_course_code_by_uri(self, *, course_code_uri: URIRef) -> CourseCode:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="course_code_query",
                constraints=[
                    {"var_name": "?courseCodeUri", "var_values": [course_code_uri.n3()]}
                ],
            )
        )
        # self.cache_graph = self.queryable.graph
        return self._graph_get_course_code_by_uri(course_code_uri=course_code_uri)

    def get_department_code_by_uri(
        self, *, department_code_uri: URIRef
    ) -> DepartmentCode:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="department_code_query",
                constraints=[
                    {
                        "var_name": "?departmentCodeUri",
                        "var_values": [department_code_uri.n3()],
                    }
                ],
            )
        )
        # self.cache_graph = self.queryable.graph
        return self._graph_get_department_code_by_uri(
            department_code_uri=department_code_uri
        )

    def get_department_by_uri(self, *, department_uri: URIRef) -> Department:
        # self.get_cache_graph(
        #     sparql=J2QueryStrHelper.j2_query(
        #         file_name="department_query",
        #         constraints=[
        #             {"var_name": "?departmentUri", "var_values": [department_uri.n3()]}
        #         ],
        #     )
        # )
        self.cache_graph = self.queryable.graph
        return self._graph_get_department_by_uri(department_uri=department_uri)

    def get_course_by_course_code_uri(self, *, course_code_uri: URIRef) -> Course:
        pass

    def get_course_sections_by_semester(
        self, *, term: str, year: int
    ) -> Tuple[CourseSection, ...]:

        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="course_section_by_semester_query",
                constraints=[
                    {
                        "var_name": "(?semesterYearInt ?semesterTermStr)",
                        "var_values": [
                            f'({Literal(year, datatype=XSD["integer"]).n3()} {Literal(term, datatype=XSD["string"]).n3()})'
                        ],
                    },
                ],
            )
        )
        # self.cache_graph = self.queryable.graph

        return self._graph_get_course_sections_by_semester(term=term, year=year)

    def get_course_sections_by_course_uri(
        self, *, course_uri: URIRef
    ) -> Tuple[CourseSection, ...]:
        pass

    def get_course_section_by_uri(self, *, course_section_uri: URIRef) -> CourseSection:

        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="course_section_query",
                constraints=[
                    {
                        "var_name": "?courseSectionUri",
                        "var_values": [course_section_uri.n3()],
                    },
                ],
            )
        )
        # self.cache_graph = self.queryable.graph

        return self._graph_get_course_section_by_uri(
            course_section_uri=course_section_uri
        )

    def get_scheduled_course_section_by_uri(
        self, *, scheduled_course_uri: URIRef
    ) -> ScheduledCourseSection:
        pass

    def get_scheduled_course_sections_by_instructor_uri(
        self, *, instructor_uri: URIRef
    ) -> Tuple[ScheduledCourseSection, ...]:
        pass

    def get_scheduled_course_section_by_crn(
        self, *, scheduled_course_crn: str
    ) -> ScheduledCourseSection:
        pass

    def get_all_requirements(self) -> Tuple[Requirement, ...]:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(file_name="requirement_query")
        )
        # self.cache_graph = self.queryable.graph
        requirements = self._graph_get_all_requirements()

        return requirements

    def get_all_requirements_by_degree_uri(
        self, *, degree_uri: URIRef
    ) -> Tuple[Requirement, ...]:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="requirement_for_degree_query",
                constraints=[
                    {
                        "var_name": "?degreeUri",
                        "var_values": [degree_uri.n3()],
                    }
                ],
            )
        )
        # self.cache_graph = self.queryable.graph
        requirements = self._graph_get_all_requirements()

        return requirements

    def get_requirement_by_uri(self, *, requirement_uri: URIRef) -> Requirement:
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="requirement_query",
                constraints=[
                    {
                        "var_name": "?requirementUri",
                        "var_values": [requirement_uri.n3()],
                    }
                ],
            )
        )
        # self.cache_graph = self.queryable.graph
        return self._graph_get_requirement_by_uri(requirement_uri=requirement_uri)

    def get_student_by_uri(self, *, student_uri) -> Student:
        # print(J2QueryStrHelper.j2_query(
        #         file_name="student_query",
        #         constraints=[
        #             {
        #                 "var_name": "?studentUri",
        #                 "var_values": [student_uri.n3()],
        #             }
        #         ],
        #     ))
        # return None
        self.get_cache_graph(
            sparql=J2QueryStrHelper.j2_query(
                file_name="student_query",
                constraints=[
                    {
                        "var_name": "?studentUri",
                        "var_values": [student_uri.n3()],
                    }
                ],
            )
        )

        # self.cache_graph = self.queryable.graph

        return self._graph_get_student_by_uri(student_uri=student_uri)

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
        if course_description:
            course_description = course_description.value
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
        topics = frozenset(
            self._graph_get_topic_area(topic_area_uri=ta_uri)
            for ta_uri in self.cache_graph.objects(course_uri, CRS_NS["hasTopic"])
        )
        offering_terms = tuple(
            term.value
            for term in self.cache_graph.objects(
                course_uri, CRS_NS["offerTerm"]
            )
        )
        offering_period = self.cache_graph.value(course_uri, CRS_NS["offerPeriod"])
        if offering_period:
            offering_period = offering_period.value

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
            offering_terms=offering_terms,
            offering_period=offering_period
        )

    def _graph_get_all_courses(self) -> Tuple[Course, ...]:

        courses = []
        for course_uri in self.cache_graph.subjects(RDF_NS["type"], CRS_NS["Course"]):
            courses.append(self._graph_get_course_by_uri(course_uri=course_uri))

        return tuple(courses)

    def _graph_get_courses_by_department_uri(
        self, *, department_uri: URIRef
    ) -> Tuple[Course, ...]:
        pass

    def _graph_get_courses_by_topic_area(
        self, *, topic_area: TopicArea
    ) -> Tuple[Course, ...]:
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

    def _graph_get_course_sections_by_semester(
        self, *, term: str, year: int
    ) -> Tuple[CourseSection, ...]:
        target_semester_uri = None
        for cand_uri in self.cache_graph.subjects(
            CRS_NS["hasTerm"], Literal(term, datatype=XSD.string)
        ):
            if self.cache_graph.value(cand_uri, CRS_NS["hasYear"]).value == year:
                target_semester_uri = cand_uri

        course_sections = []

        for course_section_uri in chain(
            self.cache_graph.subjects(RDF_NS["type"], CRS_NS["ScheduledCourseSection"]),
            self.cache_graph.subjects(RDF_NS["type"], CRS_NS["CourseSection"]),
        ):
            if (
                course_section_uri,
                CRS_NS["hasSemester"],
                target_semester_uri,
            ) in self.cache_graph:
                course_sections.append(
                    self._graph_get_course_section_by_uri(
                        course_section_uri=course_section_uri
                    )
                )

        return tuple(course_sections)

    def _graph_get_course_sections_by_course_uri(
        self, *, course_uri: URIRef
    ) -> Tuple[CourseSection, ...]:
        pass

    def _graph_get_course_section_by_uri(
        self, *, course_section_uri: URIRef
    ) -> CourseSection:
        course = self._graph_get_course_by_uri(
            course_uri=self.cache_graph.value(
                course_section_uri, CRS_NS["isCourseSectionOf"]
            )
        )
        semester = self._graph_get_semester_by_uri(
            semester_uri=self.cache_graph.value(
                course_section_uri, CRS_NS["hasSemester"]
            )
        )

        return CourseSection(uri=course_section_uri, course=course, semester=semester)

    def _graph_get_semester_by_uri(self, *, semester_uri: URIRef) -> Semester:
        year = self.cache_graph.value(semester_uri, CRS_NS["hasYear"]).value
        term = self.cache_graph.value(semester_uri, CRS_NS["hasTerm"]).value

        return Semester(uri=semester_uri, year=year, term=term)

    def _graph_get_scheduled_course_section_by_uri(
        self, *, scheduled_course_uri: URIRef
    ) -> ScheduledCourseSection:
        pass

    def _graph_get_scheduled_course_sections_by_instructor_uri(
        self, *, instructor_uri: URIRef
    ) -> Tuple[ScheduledCourseSection, ...]:
        pass

    def _graph_get_scheduled_course_section_by_crn(
        self, *, scheduled_course_crn: str
    ) -> ScheduledCourseSection:
        pass

    def _graph_get_all_requirements(self) -> Tuple[Requirement, ...]:
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
        if credits:
            credits = credits.value
        else:
            credits = 0

        cc_restriction = None
        cc_rest_val = self.cache_graph.value(
            requirement_uri, CRS_NS["hasCourseCodeRestriction"]
        )
        if cc_rest_val:
            cc_restriction = self._graph_get_course_code_restriction_by_uri(
                course_code_restriction_uri=self.cache_graph.value(
                    requirement_uri, CRS_NS["hasCourseCodeRestriction"]
                )
            )

        share_req_uris = frozenset(
            self.cache_graph.objects(requirement_uri, CRS_NS["canShareCreditsWith"])
        )
        sub_req_uris = frozenset(
            self.cache_graph.objects(requirement_uri, CRS_NS["hasSubRequirement"])
        )
        restrict_req_uris = frozenset(
            self.cache_graph.objects(requirement_uri, CRS_NS["hasRestriction"])
        )
        fulfill_by_req_uri = frozenset(
            self.cache_graph.objects(requirement_uri, CRS_NS["isFulfilledBy"])
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

    def _graph_get_topic_area(self, *, topic_area_uri: URIRef) -> TopicArea:
        # discipline = self.cache_graph.value(topic_area_uri, CRS_NS['belongsTo']) # TODO: currently using placeholder
        discipline = "placeholder discipline"
        name = self.cache_graph.value(topic_area_uri, RDFS_NS["label"]).value
        super_topics = frozenset(
            self._graph_get_topic_area(topic_area_uri=ta_uri)
            for ta_uri in self.cache_graph.objects(
                topic_area_uri, CRS_NS["isSubTopicOf"]
            )
        )

        return TopicArea(
            uri=topic_area_uri,
            name=name,
            sub_topic_of=super_topics,
            discipline=discipline,
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

    def _graph_get_degree_by_uri(self, *, degree_uri: URIRef) -> Degree:
        name = self.cache_graph.value(degree_uri, CRS_NS["hasName"]).value
        major = self._graph_get_major_by_uri(
            major_uri=self.cache_graph.value(degree_uri, CRS_NS["hasPlannedMajor"])
        )
        requirements = []
        for req_uri in self.cache_graph.objects(degree_uri, CRS_NS["hasRequirement"]):
            requirements.append(
                self._graph_get_requirement_by_uri(requirement_uri=req_uri)
            )

        return Degree(
            uri=degree_uri, name=name, major=major, requirements=tuple(requirements)
        )

    def _graph_get_major_by_uri(self, *, major_uri: URIRef) -> Major:
        name = self.cache_graph.value(major_uri, CRS_NS["hasName"]).value
        dept = self._graph_get_department_by_uri(
            department_uri=self.cache_graph.value(major_uri, CRS_NS["hasDepartment"])
        )

        return Major(uri=major_uri, name=name, department=dept)

    def _graph_get_plan_of_study_by_uri(
        self, *, plan_of_study_uri: URIRef
    ) -> PlanOfStudy:

        degree = self._graph_get_degree_by_uri(
            degree_uri=self.cache_graph.value(
                plan_of_study_uri, CRS_NS["hasPlannedDegree"]
            )
        )
        major = degree.major
        year = self.cache_graph.value(plan_of_study_uri, CRS_NS["hasClassYear"]).value

        completed = frozenset(
            # self._graph_get_course_section_by_uri(course_section_uri=csu)
            csu
            for csu in self.cache_graph.objects(
                plan_of_study_uri, CRS_NS["hasCompletedCourse"]
            )
        )
        ongoing = frozenset(
            # self._graph_get_course_section_by_uri(course_section_uri=csu)
            csu
            for csu in self.cache_graph.objects(
                plan_of_study_uri, CRS_NS["hasOngoingCourse"]
            )
        )
        planned = frozenset(
            # self._graph_get_course_section_by_uri(course_section_uri=csu)
            csu
            for csu in self.cache_graph.objects(
                plan_of_study_uri, CRS_NS["hasPlannedCourse"]
            )
        )

        return PlanOfStudy(
            uri=plan_of_study_uri,
            planned_major=major,
            planned_degree=degree,
            class_year=year,
            completed_courses=completed,
            ongoing_course_sections=ongoing,
            planned_courses=planned,
        )

    def _graph_get_advisor_by_uri(self, *, advisor_uri: URIRef) -> Advisor:
        name = self.cache_graph.value(advisor_uri, CRS_NS["hasName"]).value
        advisee_uris = ()  # TODO: populate advisees?

        return Advisor(uri=advisor_uri, name=name, advises_student_uris=advisee_uris)

    def _graph_get_student_by_uri(self, *, student_uri: URIRef) -> Student:

        name = self.cache_graph.value(student_uri, CRS_NS["hasName"]).value
        class_year = self.cache_graph.value(student_uri, CRS_NS["hasClassYear"]).value
        advisor = self._graph_get_advisor_by_uri(
            advisor_uri=self.cache_graph.value(student_uri, CRS_NS["hasAdvisor"])
        )
        topics = frozenset(
            self._graph_get_topic_area(topic_area_uri=tau)
            for tau in self.cache_graph.objects(student_uri, CRS_NS["hasInterest"])
        )

        study_plan = self._graph_get_plan_of_study_by_uri(
            plan_of_study_uri=self.cache_graph.value(
                student_uri, CRS_NS["hasStudyPlan"]
            )
        )

        return Student(
            uri=student_uri,
            name=name,
            class_year=class_year,
            topics_of_interest=topics,
            registered_courses=study_plan.ongoing_course_sections,
            advisor=advisor,
            study_plan=study_plan,
        )
