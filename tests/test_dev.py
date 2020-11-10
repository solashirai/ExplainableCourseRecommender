from rdflib import URIRef, Namespace
from crex.models import StudentPOSRequirementContext
from crex.services import SemesterCourseRecommenderService

individual_ns = Namespace(
    "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/"
)


def test_dev(course_qs):
    # basic placeholder test for getting course, under development
    print(len(course_qs.queryable.graph))
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


def test_dev_2(course_rec_pipe, test_pos_1, test_student_1, course_qs):
    # placeholder test for running the course recommende pipeline. under development.
    context = StudentPOSRequirementContext(
        student=test_student_1,
        plan_of_study=test_pos_1,
        requirements=frozenset(course_qs.get_all_requirements()),
    )

    # the pipeline should be doing some degere of filtering using requirements - still under development
    rec_courses = list(course_rec_pipe(context=context))

    print(len(rec_courses))
    for ff in rec_courses[:3]:
        print(ff.domain_object.course_code.name)

    assert len(rec_courses) != len(course_qs.get_all_courses()) and len(rec_courses) > 0


def test_dev_4(course_qs):
    cs = course_qs.get_course_section_by_uri(
        course_section_uri=URIRef(
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/crsSec000017"
        )
    )

    print(cs)

    assert False


def test_dev_3(course_qs):
    all_css = course_qs.get_course_sections_by_semester(term="fall", year=2020)

    print(f"len: {len(all_css)}")
    print(all_css[0])
    assert False


def test_dev_4(course_qs, test_student_1):

    scrs = SemesterCourseRecommenderService(course_query_service=course_qs)
    test_recs = scrs.get_recommendations_for_target_semester(
        student=test_student_1, year=2020, term="fall"
    )
    print(len(test_recs))
    for rec in test_recs:
        print(rec)

    assert False


def test_dev_5(course_qs):

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
