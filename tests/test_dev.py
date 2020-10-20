from rdflib import URIRef


def test_random(dev_fixt):
    assert False


def test_dev(course_qs):
    teste = course_qs.get_course_by_uri(course_uri=URIRef('https://tw.rpi.edu/ontology-engineering/oe2020/courses/crs000384'))

    print(teste.name)
    for req in teste.required_prerequisites:
        print("-")
        print(req.uri)
        print(req.course_code)
        print(req.name)

    assert False