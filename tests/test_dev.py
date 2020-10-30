from rdflib import URIRef
from crex.models import StudentPOSRequirementContext


def test_dev(course_qs):
    # basic placeholder test for getting course, under development
    test_course = course_qs.get_course_by_uri(course_uri=URIRef('https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/crs002440'))

    assert test_course.name == 'Programming Languages' and test_course.credits == 4 and test_course.course_code.name == 'CSCI-4430'


def test_dev_2(course_rec_pipe, test_pos_1, test_student_1, course_qs):
    # placeholder test for running the course recommende pipeline. under development.
    context = StudentPOSRequirementContext(student=test_student_1, plan_of_study=test_pos_1,
                                           requirements=frozenset(course_qs.get_all_requirements()))

    # the pipeline should be doing some degere of filtering using requirements - still under development
    rec_courses = list(course_rec_pipe(context=context))

    print(len(rec_courses))
    for ff in rec_courses[:3]:
        print(ff.domain_object.course_code.name)

    assert len(rec_courses) != len(course_qs.get_all_courses()) and len(rec_courses) > 0
