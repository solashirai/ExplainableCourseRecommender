import pytest
from rdflib import URIRef, Namespace
from crex.models import StudentPOSRequirementContext, Course
from crex.services import SemesterCourseRecommenderService
from frex.stores import RemoteGraph

individual_ns = Namespace(
    "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/"
)


def test_get_course_by_uri(course_qs):
    # ree = RemoteGraph(endpoint="http://192.168.1.170:9999/blazegraph/sparql")
    # asdf = ree.query(sparql="SELECT * WHERE {?s ?p ?o} LIMIT 10")
    # print(asdf)
    # basic placeholder test for getting course, under development
    test_course = course_qs.get_course_by_uri(
        course_uri=URIRef(
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/crs938c5b7e20ea7e1620a2dd6329e6f0af274b46c3"
        )
    )

    assert (
        test_course.name == "Programming Languages"
        and test_course.credits == 4
        and test_course.course_code.name == "CSCI-4430"
    )


def test_run_pipeline(course_rec_pipe, test_pos_1, test_student_1, course_qs):
    # placeholder test for running the course recommende pipeline. under development.
    context = StudentPOSRequirementContext(
        student=test_student_1,
        plan_of_study=test_pos_1,
        requirements=frozenset(course_qs.get_all_requirements()),
    )

    # the pipeline should be doing some degee of filtering using requirements - still under development
    rec_courses = list(course_rec_pipe(context=context))

    assert len(rec_courses) != len(course_qs.get_all_courses()) and len(rec_courses) > 0


def test_get_course_section_by_uri(course_qs):
    cs = course_qs.get_course_section_by_uri(
        course_section_uri=URIRef(
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/schdCrsSec769736c732063d1555a5d8a1d1ec2eb63062f663"
        )
    )
    assert (
        cs.course == course_qs.get_course_by_uri(course_uri=URIRef('https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/crsc746a794a800d873f1e5deff86c0c58e25f94848'))
        and cs.semester.year == 2020 and cs.semester.term == 'FALL'
    )


def test_get_all_course_sections_by_semester(course_qs):
    all_css = course_qs.get_course_sections_by_semester(term="FALL", year=2020)

    assert len(all_css) == 2081 and all(css.semester.term == 'FALL' for css in all_css) and all(css.semester.year == 2020 for css in all_css)


def test_generate_semester_course_recommendations(course_qs, test_student_1):

    scrs = SemesterCourseRecommenderService(course_query_service=course_qs)
    semester_rec_soln = scrs.get_recommendations_for_target_semester(
        student=test_student_1, year=2020, term="FALL"
    )

    # TODO: later on this should actually check that 'good' courses are getting recommended based on some scores...
    assert (
        len(semester_rec_soln.sections[0].section_candidates) == 4
        and 12 <= semester_rec_soln.sections[0].section_attribute_values['credits'] <= 16
        and 12 <= semester_rec_soln.overall_attribute_values['credits'] <= 16
        and len(set(cc.domain_object.course_code for cc in semester_rec_soln.sections[0].section_candidates)) == 4
    )


def test_get_student_by_uri(course_qs):

    student = course_qs.get_student_by_uri(
        student_uri=URIRef(
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/usrowen"
        )
    )

    assert (
        student.name == "owen"
        and student.class_year == 2021
        and set(cs.uri for cs in student.study_plan.completed_course_sections)
        == {
            individual_ns["crsSec0838fe4beedeff7709d32d16ca67c9aa2373dba7"],
            individual_ns["crsSec0cf0d1a768ef7b1d580ac0aaf258257b8c766ecb"],
            individual_ns["crsSec0d060d8550b4d97fa0aa0188e75a213e37114cb5"],
            individual_ns["crsSec1d571602ec11f8e32dcde3b985cb277b68b7abb5"],
            individual_ns["crsSec40567fef852031bad43995aa8cab7c4877bc0a02"],
            individual_ns["crsSec4d3630ed52401a5362753db61595b8e1aec66bd8"],
            individual_ns["crsSec5241e24de4b9d40df379b7916e4698ac81354f6f"],
            individual_ns["crsSec5fd627bdf533aefd6f25ebb995fccc08e57f8dc2"],
            individual_ns["crsSec615e6c5aee4bbf92e6e193f86346602825bba571"],
            individual_ns["crsSec663dda052cc6e9647d255c294c71409b1883963f"],
            individual_ns["crsSec6a1c91448f2bdb49b519784e470a68c37318b45c"],
            individual_ns["crsSec79431f36805f7d501cc79356e3f69b26340e1d98"],
            individual_ns["crsSec8102566ff399c31b30351decb38ba3893db8e2f5"],
            individual_ns["crsSec8281ac09fc60458b13bdfef54b75f0b8e771837e"],
            individual_ns["crsSec8bb40720e14ff5d40a16d71efbfab65bbcd742eb"],
            individual_ns["crsSec99b5492130e02e1dcb08692178a020c1c2444195"],
            individual_ns["crsSecbc29e94fcaa333888baa92efb31dad194e1718b6"],
            individual_ns["crsSecc4b387e96f764565a80950390b36235fc00eabf1"],
            individual_ns["crsSeccb117aa26ddc5cf711c70466adcc656492e8a464"],
            individual_ns["crsSecce866dba24b0cdf1e707f40e0ee7fbb8de068406"],
            individual_ns["crsSecd5c95ece2b749c2e0beb1d2bfde0e23e5ad45d93"],
            individual_ns["crsSece04b10767b92aa4d53eb5a5b044ef13673b49448"],
            individual_ns["crsSece405364a6acf6b819c02915a204114f26ff8551f"],
            individual_ns["crsSecf5a9dafe85e39b30bdbd45b3371eeefd7520569d"],
            individual_ns["crsSecf603c709ea539acc6b9bb842d574c3d9eb7c17fa"],
            individual_ns["crsSecf7b40623128f286084d451d67cc7fb4b60b11c94"],
            individual_ns["crsSecf8b3e82fd2f512b3db0727642c6a1b7153581d47"],
            individual_ns["crsSecfb9210e5ca6bd4844b7bf9bdf1cb1c5956f81d08"],
        }
    )
