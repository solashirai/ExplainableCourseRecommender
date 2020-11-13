import pytest
from rdflib import URIRef, Namespace
from crex.models import StudentPOSRequirementContext, Course
from crex.services import SemesterCourseRecommenderService

individual_ns = Namespace(
    "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/"
)


def test_get_course_by_uri(course_qs):
    # basic placeholder test for getting course, under development
    test_course = course_qs.get_course_by_uri(
        course_uri=URIRef(
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/crs006142"
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
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/crsSec006080"
        )
    )
    assert (
        cs.course == course_qs.get_course_by_uri(course_uri=URIRef('https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/crs001728'))
        and cs.semester.year == 2020 and cs.semester.term == 'fall'
    )


def test_get_all_course_sections_by_semester(course_qs):
    all_css = course_qs.get_course_sections_by_semester(term="fall", year=2020)

    assert len(all_css) == 2833 and all(css.semester.term == 'fall' for css in all_css) and all(css.semester.year == 2020 for css in all_css)


def test_generate_semester_course_recommendations(course_qs, test_student_1):

    scrs = SemesterCourseRecommenderService(course_query_service=course_qs)
    semester_rec_soln = scrs.get_recommendations_for_target_semester(
        student=test_student_1, year=2020, term="fall"
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
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/usr009034"
        )
    )

    assert (
        student.name == "owen"
        and student.class_year == 2021
        and set(cs.uri for cs in student.study_plan.completed_course_sections)
        == {
            individual_ns["crsSec001796"],
            individual_ns["crsSec001826"],
            individual_ns["crsSec001842"],
            individual_ns["crsSec003626"],
            individual_ns["crsSec004683"],
        }
    )
