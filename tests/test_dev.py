from rdflib import URIRef
from app.models import StudentPOSContext


def test_dev(course_qs):
    teste = course_qs.get_course_by_uri(course_uri=URIRef('https://tw.rpi.edu/ontology-engineering/oe2020/entity/crs000796'))

    print(teste.name)
    for req in teste.required_prerequisites:
        print("-")
        print(req.uri)
        print(req.course_code)
        print(req.name)

    assert False


def test_dev_2(course_rec_pipe, test_pos_1, test_student_1):

    context = StudentPOSContext(student=test_student_1, plan_of_study=test_pos_1)

    asdf = list(course_rec_pipe(context=context))
    print(len(asdf))
    for ff in asdf[:3]:
        print(ff)

    assert False
