import rdflib
from rdflib.namespace import XSD
from app.utils.namespaces import CRS_NS, RDF_NS
import ast
import csv

# quick and dirty implementation to parse yacs data csv into rdf.

savename = 'yacs_course_data_v1.ttl'
files = ['spring-2020.csv', 'fall-2020.csv', 'summer-2020.csv']

data_rows = []
name_to_index = []
for file in files:
    skipfirst = True
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if not skipfirst:
                data_rows.append(row)
            else:
                if not name_to_index:
                    name_to_index = {item:row.index(item) for item in row}
                skipfirst = False

graph = rdflib.Graph()

graph.bind('crs-onto', CRS_NS)
courses_ns = rdflib.Namespace('https://tw.rpi.edu/ontology-engineering/oe2020/courses/')
graph.bind('crs-courses', courses_ns)
course_uri_dict = dict()


def new_course_uri():
    return courses_ns[f'crs{str(len(course_uri_dict)).zfill(6)}']


for row in data_rows[1:]:
    course_uri = course_uri_dict.get(row[name_to_index['short_name']], '')
    if not course_uri:
        course_uri = new_course_uri()
        course_uri_dict[row[name_to_index['short_name']]] = course_uri

    graph.add((course_uri, RDF_NS['type'], CRS_NS['Course']))
    graph.add((course_uri, CRS_NS['hasName'], rdflib.Literal(row[name_to_index['full_name']], datatype=XSD.string)))
    graph.add((course_uri, CRS_NS['hasCredits'], rdflib.Literal(row[name_to_index['course_credit_hours']], datatype=XSD.integer)))
    graph.add((course_uri, CRS_NS['hasDepartment'], rdflib.Literal(row[name_to_index['course_department']], datatype=XSD.string)))
    graph.add((course_uri, CRS_NS['hasLevel'], rdflib.Literal(row[name_to_index['course_level']], datatype=XSD.string)))
    graph.add((course_uri, CRS_NS['hasCourseCode'], rdflib.Literal(row[name_to_index['short_name']], datatype=XSD.string)))
    graph.add((course_uri, CRS_NS['hasDescription'], rdflib.Literal(row[name_to_index['description']], datatype=XSD.string)))
    graph.add((course_uri, CRS_NS['hasTopic'], rdflib.Literal('placeholder for topic', datatype=XSD.string)))

for row in data_rows[1:]:
    # TODO: prerequisite information is not correctly parsed in the current data (10/20/2020). need to
    #  apply an extra check for "and" vs "or" vs "/" (slash usually for crosslisted courses)
    course_uri = course_uri_dict[row[name_to_index['short_name']]]
    if row[name_to_index['prerequisites']]:
        for prereq in ast.literal_eval(row[name_to_index['prerequisites']]):

            prereq_uri = course_uri_dict.get(prereq, '')
            if not prereq_uri:
                prereq_uri = new_course_uri()
                course_uri_dict[prereq] = prereq_uri

            graph.add((course_uri, CRS_NS['hasRequiredPrerequisite'], prereq_uri))
    if row[name_to_index['corequisites']]:
        for coreq in ast.literal_eval(row[name_to_index['corequisites']]):

            coreq_uri = course_uri_dict.get(coreq, '')
            if not coreq_uri:
                coreq_uri = new_course_uri()
                course_uri_dict[coreq] = coreq_uri

            graph.add((course_uri, CRS_NS['hasCorequisite'], coreq_uri))
graph.serialize(savename, format='ttl')
