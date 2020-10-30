import pytest
from crex.models import *
from crex.services.course import GraphCourseQueryService
from frex.stores import LocalGraph
from crex.utils.path import DATA_DIR
from crex.pipeline import RecommendCoursesPipeline
from rdflib import URIRef


@pytest.fixture(scope="session")
def course_graph() -> LocalGraph:
    return LocalGraph(file_paths=(
        (DATA_DIR/"yacs_course_data_v1.ttl").resolve(),
        (DATA_DIR/"rpi_departments.ttl").resolve(),
        (DATA_DIR/"manualcurated_grad_requirements.ttl").resolve(),
    ))


@pytest.fixture(scope="session")
def course_qs(course_graph) -> GraphCourseQueryService:
    return GraphCourseQueryService(queryable=course_graph)


@pytest.fixture(scope="session")
def course_rec_pipe(course_qs) -> RecommendCoursesPipeline:
    return RecommendCoursesPipeline(course_query_service=course_qs)


@pytest.fixture(scope="session")
def test_pos_1():
    return PlanOfStudy(
        uri=URIRef('placeholder_pos1'),
        class_year='2022',
        planned_major=(),
        planned_degree=None,
        completed_courses=(),
        ongoing_courses=(),
        planned_courses=()
    )


@pytest.fixture(scope="session")
def test_student_1(test_pos_1):
    return Student(
        uri=URIRef('placeholder_stud1'),
        study_plan=test_pos_1,
        name='john doe',
        rin='123',
        class_year='2022',
        topics_of_interest=(),
        registered_courses=(),
        advisor=None,
    )
