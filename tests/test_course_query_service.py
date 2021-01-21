import pytest
from escore.models import *
from escore.services.course import GraphCourseQueryService
from frex.stores import LocalGraph, RemoteGraph
from escore.utils.path import DATA_DIR
from escore.pipeline import RecommendCoursesPipeline
from rdflib import URIRef


def test_get_course_by_uri(course_qs, pl_course):
    test_course = course_qs.get_course_by_uri(
        course_uri=URIRef(
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/"
            "crs938c5b7e20ea7e1620a2dd6329e6f0af274b46c3"
        )
    )

    assert test_course == pl_course


def test_get_course_section_by_uri(course_qs, pl_course):
    cs = course_qs.get_course_section_by_uri(
        course_section_uri=URIRef(
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/"
            "schdCrsSec4594feb1968ece4682bd15fa30641a959e830a52"
        )
    )
    assert (
        cs.course == pl_course
        and cs.semester.year == 2020
        and cs.semester.term == 'FALL'
        # eventually need to be doing some testing about the schedule here too
    )


def test_get_requirement_by_uri(course_qs, csci_option_req):
    test_req = course_qs.get_requirement_by_uri(
        requirement_uri=URIRef(
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/"
            "req78e077dfe6014ee50f8fac4e06b2ae06333cc271"
        )
    )

    assert test_req == csci_option_req


def test_get_all_course_sections_by_semester(course_qs):
    all_css = course_qs.get_course_sections_by_semester(term="FALL", year=2020)

    assert len(all_css) == 2081 and all(css.semester.term == 'FALL' for css in all_css) \
           and all(css.semester.year == 2020 for css in all_css)


def test_get_student_by_uri(course_qs, owen_student):

    test_student = course_qs.get_student_by_uri(
        student_uri=URIRef(
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/usrowen"
        )
    )

    assert test_student == owen_student