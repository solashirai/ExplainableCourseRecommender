import pytest
from app.models import *
from app.services.course import GraphCourseQueryService
from frex.stores import LocalGraph
from app.utils.path import DATA_DIR


@pytest.fixture(scope="session")
def course_graph() -> LocalGraph:
    return LocalGraph(file_paths=((DATA_DIR/"yacs_course_data_v1.ttl").resolve(), ))


@pytest.fixture(scope="session")
def course_qs(course_graph) -> GraphCourseQueryService:
    return GraphCourseQueryService(queryable=course_graph)


@pytest.fixture(scope="session")
def dev_fixt():
    student = Student(
        uri=None,
        study_plan=None,
        name=None,
        rin=None,
        class_year=None,
        topics_of_interest=None,
        registered_courses=None,
        advisor=None,
    )
    f = Degree(
        uri=None,
        major=3,
        department=None,
        name="",
        description="",
        requirements=(None,),
    )
    return student
