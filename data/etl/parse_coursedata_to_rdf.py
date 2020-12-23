import rdflib
from rdflib.namespace import XSD, OWL, RDFS
from crex.utils.namespaces import CRS_NS, RDF_NS, LCC_LR_NS, DATE_NS
from crex.utils.path import DATA_DIR, PROJECT_ROOT
import ast
from unidecode import unidecode
import csv
import hashlib
import yaml


# quick and dirty implementation to parse yacs data csv into rdf.

course_save_file = 'courses.ttl'
course_save_file = str((DATA_DIR / course_save_file).resolve())

offerings_save_file = 'scheduled_courses.ttl'
offerings_save_file = str((DATA_DIR / offerings_save_file).resolve())

user_save_file = 'users.ttl'
user_save_file = str((DATA_DIR / user_save_file).resolve())

graduation_req_save_file = 'parsed_grad_requirements.ttl'
graduation_req_save_file = str((DATA_DIR / graduation_req_save_file).resolve())

RAW_DIR = (PROJECT_ROOT / "data/raw").resolve()
# savename = 'yacs_course_data_v1.ttl'
# combine_save_name = 'course-recommender-individuals.rdf'
# combine_save_name = 'course-recommender-individuals.rdf'
core_course_info = ['catalog.csv']
core_course_info = [(RAW_DIR / file).resolve() for file in core_course_info]
course_offerings = ['spring-2020.csv', 'fall-2020.csv', 'summer-2020.csv']
course_offerings = [(RAW_DIR / file).resolve() for file in course_offerings]
transcript_files = {
    'owen': (RAW_DIR / 'ox_transcript.csv').resolve(),
    'jacob': (RAW_DIR / 'js_transcript.csv').resolve(),
    'kelly': (RAW_DIR / 'kf_transcript.csv').resolve()
}

graduation_req_file = 'graduation_requirements.yaml'
graduation_req_file = str((RAW_DIR / graduation_req_file).resolve())



LIMIT_COURSE_DEPT = False
COURSE_DEPT_CHOICES = ['CSCI', 'COGS']
SKIP_NONEXISTING_PREREQ = False
save_combined = False#True

department_data = (DATA_DIR / 'rpi_departments.ttl').resolve()
q = rdflib.Graph()
q.parse(str(department_data), format='ttl')

code_to_uri = dict()
code_to_dept_uri = dict()
for s, p, o in q.triples((None, RDF_NS['type'], CRS_NS['DepartmentCode'])):
    code_to_uri[q.value(s, rdflib.URIRef('https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/hasTag')).value] = s
    code_to_dept_uri[q.value(s, rdflib.URIRef('https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/hasTag')).value] = q.value(s, CRS_NS['hasDepartment'])

entity_ns = rdflib.Namespace('https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/')


def setup_graph_and_data(load_files):
    graph = rdflib.Graph()

    graph.bind('crs-rec', CRS_NS)
    graph.bind('owl', OWL)
    graph.bind('crs-rec-ind', entity_ns)
    graph.bind('lcc-lr', rdflib.URIRef('https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/'))
    entity_uri_dict = dict()

    data_rows = []
    name_to_index = []
    for file in load_files:
        skipfirst = True
        with open(file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                if not skipfirst:
                    data_rows.append([unidecode(item.replace("’", "'")) for item in row])
                else:
                    if not name_to_index:
                        name_to_index = {item: row.index(item) for item in row}
                    skipfirst = False

    return graph, data_rows, name_to_index


def semester_to_uri(term, year):
    hasher = hashlib.sha1()
    hasher.update(term.encode('utf-8'))
    hasher.update(str(year).encode('utf-8'))
    return entity_ns[f'sem{hasher.hexdigest()}']

def course_code_to_uri(course_code):
    hasher = hashlib.sha1()
    hasher.update(course_code.encode('utf-8'))
    return entity_ns[f'crsCode{hasher.hexdigest()}']

def course_to_uri(course_code):
    hasher = hashlib.sha1()
    hasher.update("COURSE".encode('utf-8'))
    hasher.update(course_code.encode('utf-8'))
    return entity_ns[f'crs{hasher.hexdigest()}']

def course_section_to_uri(*, course_code, semester):
    hasher = hashlib.sha1()
    hasher.update(course_code.encode('utf-8'))
    hasher.update(semester.encode('utf-8'))
    return entity_ns[f'crsSec{hasher.hexdigest()}']

def scheduled_course_section_to_uri(*, course_code, section, semester):
    hasher = hashlib.sha1()
    hasher.update(course_code.encode('utf-8'))
    hasher.update(section.encode('utf-8'))
    hasher.update(semester.encode('utf-8'))
    return entity_ns[f'schdCrsSec{hasher.hexdigest()}']

def scheduled_course_sec_schedule_uri(*, course_code, section, semester):
    hasher = hashlib.sha1()
    hasher.update(course_code.encode('utf-8'))
    hasher.update(section.encode('utf-8'))
    hasher.update(semester.encode('utf-8'))
    hasher.update("SCHEDULE".encode('utf-8'))
    return entity_ns[f'sched{hasher.hexdigest()}']

def grad_req_id_to_uri(req_id):
    hasher = hashlib.sha1()
    hasher.update(str(req_id).encode('utf-8'))
    return entity_ns[f'req{hasher.hexdigest()}']

def course_restriction_to_uri(req_id):
    hasher = hashlib.sha1()
    hasher.update(str(req_id).encode('utf-8'))
    hasher.update('course_code_restriction'.encode('utf-8'))
    return entity_ns[f'ccr{hasher.hexdigest()}']


def get_time_int(time_str):
    time_str = time_str.replace(":", "")

    int_time = int(time_str[:-2])
    if time_str[-2:].lower() == 'am':
        return int_time
    elif time_str[-2:].lower() == 'pm':
        # use military time to get rid of AM/PM
        return int_time + 1200
    else:
        # if for some reason AM/PM is missing, assume anything before 750 is pm, 800 and after is am
        if int_time < 800:
            return int_time+1200
        else:
            return int_time

# load core course info data

graph, data_rows, name_to_index = setup_graph_and_data(load_files=core_course_info)

placeholder_topic_uri = entity_ns['topic00001']
graph.add((placeholder_topic_uri, RDF_NS['type'], CRS_NS['TopicArea']))
graph.add((placeholder_topic_uri, RDF_NS['type'], OWL['NamedIndividual']))
graph.add((placeholder_topic_uri, rdflib.namespace.RDFS['label'],
           rdflib.Literal('placeholder for topic', datatype=XSD.string)))

for row in data_rows[1:]:
    dept = row[name_to_index['department']]
    level = row[name_to_index['level']]
    course_code = row[name_to_index['short_name']].strip().replace(" ", "-")
    if not course_code:
        course_code = f'{dept}-{level}'
    name = row[name_to_index['full_name']]
    description = row[name_to_index['description']].strip()
    #raw_precoreqs, offer_frequency, cross_listed, short_name, prerequisites, corequisites
    credit_hours = row[name_to_index['credit_hours']]

    course_uri = course_to_uri(course_code=course_code)
    course_code_uri = course_code_to_uri(course_code=course_code)

    dept_code_uri = code_to_uri[dept]
    department_uri = code_to_dept_uri[dept]

    graph.add((course_uri, RDF_NS['type'], CRS_NS['Course']))
    graph.add((course_uri, RDF_NS['type'], OWL['NamedIndividual']))
    graph.add((course_uri, CRS_NS['hasName'], rdflib.Literal(name, datatype=XSD.string)))
    graph.add((course_uri, RDFS['label'], rdflib.Literal(name, datatype=XSD.string)))

    # TODO: not sure how to handle credit hours with ranges (e.g. "1-9" or "1 to 4") so just set to 1 for now
    if "-" in credit_hours or "to" in credit_hours:
        graph.add((course_uri, CRS_NS['hasCredits'],
                   rdflib.Literal(1, datatype=XSD.integer)))
    else:
        graph.add((course_uri, CRS_NS['hasCredits'], rdflib.Literal(credit_hours, datatype=XSD.integer)))

    graph.add((course_uri, CRS_NS['hasDepartment'], department_uri))
    graph.add((course_uri, CRS_NS['hasCourseCode'], course_code_uri))
    graph.add((course_uri, CRS_NS['hasDescription'], rdflib.Literal(description, datatype=XSD.string)))
    graph.add((course_uri, CRS_NS['hasTopic'], placeholder_topic_uri))

    # offerings, need to enhance later such as checking crosslistings or checking real offerings
    raw_offer_freq = row[name_to_index['offer_frequency']].lower()
    if 'fall' in raw_offer_freq:
        graph.add((course_uri, CRS_NS['offerTerm'], rdflib.Literal("FALL", datatype=XSD.string)))
    if 'spring' in raw_offer_freq:
        graph.add((course_uri, CRS_NS['offerTerm'], rdflib.Literal("SPRING", datatype=XSD.string)))
    if 'annual' in raw_offer_freq:
        graph.add((course_uri, CRS_NS['offerPeriod'], rdflib.Literal("ANNUAL", datatype=XSD.string)))
    elif 'even-num' in raw_offer_freq:
        graph.add((course_uri, CRS_NS['offerPeriod'], rdflib.Literal("EVEN", datatype=XSD.string)))
    elif 'odd-num' in raw_offer_freq:
        graph.add((course_uri, CRS_NS['offerPeriod'], rdflib.Literal("ODD", datatype=XSD.string)))

    graph.add((course_code_uri, RDF_NS['type'], CRS_NS['CourseCode']))
    graph.add((course_code_uri, RDF_NS['type'], OWL['NamedIndividual']))
    graph.add((course_code_uri, CRS_NS['hasLevel'], rdflib.Literal(level, datatype=XSD.float)))
    graph.add((course_code_uri, CRS_NS['hasDepartmentCode'], dept_code_uri))
    graph.add((course_code_uri, LCC_LR_NS['hasTag'], rdflib.Literal(course_code, datatype=XSD.string)))

# TODO: WIP
# for row in data_rows[1:]:
#     # TODO: prerequisite information is not correctly parsed in the current data (10/20/2020). need to
#     #  apply an extra check for "and" vs "or" vs "/" (slash usually for crosslisted courses)
#     if LIMIT_COURSE_DEPT and not row[name_to_index['course_department']] in COURSE_DEPT_CHOICES:
#         continue
#     course_uri = entity_uri_dict[f"course-{row[name_to_index['short_name']]}"]
#     if row[name_to_index['prerequisites']]:
#         for prereq in ast.literal_eval(row[name_to_index['prerequisites']]):
#
#             prereq_uri = entity_uri_dict.get(f"course-{prereq}", '')
#             if not prereq_uri:
#                 if SKIP_NONEXISTING_PREREQ:
#                     continue
#                 prereq_uri = new_course_uri()
#                 entity_uri_dict[prereq] = prereq_uri
#
#             graph.add((course_uri, CRS_NS['hasRequiredPrerequisite'], prereq_uri))
#     if row[name_to_index['corequisites']]:
#         for coreq in ast.literal_eval(row[name_to_index['corequisites']]):
#
#             coreq_uri = entity_uri_dict.get(f"course-{coreq}", '')
#             if not coreq_uri:
#                 if SKIP_NONEXISTING_PREREQ:
#                     continue
#                 coreq_uri = new_course_uri()
#                 entity_uri_dict[coreq] = coreq_uri
#
#             graph.add((course_uri, CRS_NS['hasCorequisite'], coreq_uri))

# save
graph.serialize(course_save_file, format='ttl')


graph, data_rows, name_to_index = setup_graph_and_data(load_files=course_offerings)

# manually add a few schedules
semesters = ['SPRING', 'SUMMER', 'FALL']
years = [2017, 2018, 2019, 2020, 2021]
for year in years:
    for sem in semesters:
        sem_yr = sem+" "+str(year)
        schedule_uri = semester_to_uri(sem, year)
        graph.add((schedule_uri, RDF_NS['type'], CRS_NS['SemesterSchedule']))
        graph.add((schedule_uri, RDF_NS['type'], OWL['NamedIndividual']))
        graph.add((schedule_uri, CRS_NS['hasTerm'], rdflib.Literal(sem, datatype=XSD.string)))
        graph.add((schedule_uri, CRS_NS['hasYear'], rdflib.Literal(year, datatype=XSD.integer)))

for row in data_rows[1:]:
    section = row[name_to_index['course_section']]
    course_code = row[name_to_index['short_name']]
    name = row[name_to_index['full_name']]
    semester = row[name_to_index['semester']].upper()

    course_sec_uri = scheduled_course_section_to_uri(course_code=course_code, section=section, semester=semester)
    if (course_sec_uri, None, None) not in graph:
        term = semester.split(" ")[0]
        year = int(semester.split(" ")[1])
        sem_sched_uri = semester_to_uri(term=term, year=year)

        graph.add((course_sec_uri, RDF_NS['type'], CRS_NS['ScheduledCourseSection']))
        graph.add((course_sec_uri, RDF_NS['type'], OWL['NamedIndividual']))
        graph.add((course_sec_uri, CRS_NS['hasSemester'], sem_sched_uri))

        course_uri = course_to_uri(course_code=course_code)
        graph.add((course_sec_uri, CRS_NS['isCourseSectionOf'], course_uri))

        course_sec_label = name + " " + semester + " Section " + section
        graph.add((course_sec_uri, RDFS['label'], rdflib.Literal(course_sec_label, datatype=XSD.string)))

    course_sched_uri = scheduled_course_sec_schedule_uri(course_code=course_code, section=section, semester=semester)
    graph.add((course_sec_uri, CRS_NS['hasSchedule'], course_sched_uri))

    graph.add((course_sched_uri, RDF_NS['type'], CRS_NS['CourseSchedule']))
    start_time = row[name_to_index['course_start_time']]
    if start_time:
        time_int = get_time_int(start_time)
        graph.add((course_sched_uri, CRS_NS['hasStartTime'], rdflib.Literal(time_int, datatype=XSD.integer)))
    end_time = row[name_to_index['course_end_time']]
    if end_time:
        time_int = get_time_int(end_time)
        graph.add((course_sched_uri, CRS_NS['hasEndTime'], rdflib.Literal(time_int, datatype=XSD.integer)))
    dates = row[name_to_index['course_days_of_the_week']]
    if dates:
        if "M" in dates:
            graph.add((course_sched_uri, CRS_NS['hasDayOfWeek'], DATE_NS['Monday']))
        if "T" in dates:
            graph.add((course_sched_uri, CRS_NS['hasDayOfWeek'], DATE_NS['Tuesday']))
        if "W" in dates:
            graph.add((course_sched_uri, CRS_NS['hasDayOfWeek'], DATE_NS['Wednesday']))
        if "R" in dates:
            graph.add((course_sched_uri, CRS_NS['hasDayOfWeek'], DATE_NS['Thursday']))
        if "F" in dates:
            graph.add((course_sched_uri, CRS_NS['hasDayOfWeek'], DATE_NS['Friday']))

graph.serialize(offerings_save_file, format='ttl')

graph, _, _ = setup_graph_and_data([])
course_graph = rdflib.Graph()
course_graph.parse(course_save_file, format='ttl')

# user stuff

def new_pos_uri(user_uri):
    hasher = hashlib.sha1()
    hasher.update(user_uri.encode('utf-8'))
    return entity_ns[f'pos{hasher.hexdigest()}']

def new_usr_uri(rin):
    # assume we actually have rin.
    return entity_ns[f'usr{rin}']

# PLACEHOLDER STUFF
graph.add((entity_ns['majCSCI'], RDF_NS['type'], CRS_NS['Major']))
graph.add((entity_ns['majCSCI'], RDF_NS['type'], OWL['NamedIndividual']))
graph.add((entity_ns['majCSCI'], CRS_NS['hasName'], rdflib.Literal('placeholder computer science major', datatype=XSD.string)))
graph.add((entity_ns['majCSCI'], CRS_NS['hasDepartment'], entity_ns['dpt0026']))

graph.add((entity_ns['degBSInCSCI'], RDF_NS['type'], CRS_NS['Degree']))
graph.add((entity_ns['degBSInCSCI'], RDF_NS['type'], OWL['NamedIndividual']))
graph.add((entity_ns['degBSInCSCI'], CRS_NS['hasName'], rdflib.Literal('BS in Computer Science', datatype=XSD.string)))
graph.add((entity_ns['degBSInCSCI'], CRS_NS['hasPlannedMajor'], entity_ns['majCSCI']))

graph.add((entity_ns['PLACEHOLDER-ADVISOR-URI'], RDF_NS['type'], CRS_NS['Advisor']))
graph.add((entity_ns['PLACEHOLDER-ADVISOR-URI'], RDF_NS['type'], OWL['NamedIndividual']))
graph.add((entity_ns['PLACEHOLDER-ADVISOR-URI'], CRS_NS['hasName'], rdflib.Literal('Placeholder advisor name', datatype=XSD.string)))
# END OF SUPER PLACEHOLDER STUFF

for user, file in transcript_files.items():
    print(user, file)
    user_uri = new_usr_uri(user)
    graph.add((user_uri, CRS_NS['hasName'], rdflib.Literal(user, datatype=XSD.string)))
    graph.add((user_uri, CRS_NS['hasClassYear'], rdflib.Literal(2021, datatype=XSD.integer))) # placeholder class yr
    graph.add((user_uri, CRS_NS['hasAdvisor'], entity_ns['PLACEHOLDER-ADVISOR-URI'])) # placeholder advisor
    graph.add((user_uri, RDF_NS['type'], CRS_NS['Student']))
    graph.add((user_uri, RDF_NS['type'], OWL['NamedIndividual']))

    pos_uri = new_pos_uri(user_uri)
    graph.add((pos_uri, RDF_NS['type'], CRS_NS['PlanOfStudy']))
    graph.add((pos_uri, RDF_NS['type'], OWL['NamedIndividual']))
    graph.add((pos_uri, CRS_NS['hasClassYear'],
               rdflib.Literal(2021, datatype=XSD.integer)))  # placeholder class yr
    graph.add((pos_uri, CRS_NS['hasPlannedMajor'], entity_ns['majCSCI']))
    graph.add((pos_uri, CRS_NS['hasPlannedDegree'], entity_ns['degBSInCSCI']))
    graph.add((user_uri, CRS_NS['hasStudyPlan'], pos_uri))


    with open(file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:

            course_code = row[0].replace(" ", "-")
            course_uri = course_to_uri(course_code=course_code)

            if (course_uri, None, None) not in course_graph:
                print(f"{course_code} not found.")
                continue

            term = row[1].upper()
            year = int(row[2])
            semschedule_uri = semester_to_uri(term=term, year=year)

            course_sec_uri = course_section_to_uri(course_code=course_code, semester=f'{term}-{year}')
            graph.add((course_sec_uri, RDF_NS['type'], CRS_NS['CourseSection']))
            graph.add((course_sec_uri, RDF_NS['type'], OWL['NamedIndividual']))
            graph.add((course_sec_uri, CRS_NS['isCourseSectionOf'], course_uri))
            graph.add((course_sec_uri, CRS_NS['hasSemester'], semschedule_uri))

            graph.add((pos_uri, CRS_NS['hasCompletedCourse'], course_sec_uri))

graph.serialize(user_save_file, format='ttl')

print("----------------------")
print("----------------------")
print("----------------------")
print("----------------------")
print("----------------------")
print("----------------------")

with open(graduation_req_file, 'r') as f:
    grad_data_dict = yaml.load(f)
grg = rdflib.Graph()

grg.bind('crs-rec', CRS_NS)
grg.bind('owl', OWL)
grg.bind('crs-rec-ind', entity_ns)

print(grad_data_dict)
for deg_id in grad_data_dict['degree_IDs']:
    deg_uri = entity_ns[deg_id]
    for req in grad_data_dict['degree_IDs'][deg_id]['has_req']:
        grg.add((deg_uri, CRS_NS['hasRequirement'], grad_req_id_to_uri(req)))

for spec_tag in grad_data_dict['special_tags']:
    for course_tag in grad_data_dict['special_tags'][spec_tag]['courses']:
        course_tag_uri = course_graph.value(predicate=rdflib.URIRef('https://www.omg.org/spec/LCC/Languages/LanguageRepresentation/hasTag'),
                                            object=rdflib.Literal(course_tag, datatype=XSD.string))
        course_uri = course_graph.value(predicate=CRS_NS['hasCourseCode'], object=course_tag_uri)
        if course_uri:
            grg.add((course_uri, CRS_NS['hasSpecialTag'], rdflib.Literal(spec_tag, datatype=XSD.string)))

for req_id in grad_data_dict['req_IDs']:
    req_uri = grad_req_id_to_uri(req_id)

    this_req = grad_data_dict['req_IDs'][req_id]
    grg.add((req_uri, RDF_NS['type'], CRS_NS['Requirement']))
    grg.add((req_uri, RDF_NS['type'], OWL['NamedIndividual']))
    grg.add((req_uri, rdflib.namespace.RDFS['label'], rdflib.Literal(req_id, datatype=XSD.string)))
    mc = this_req.get('req_credits', None)

    if mc is not None:
        grg.add((req_uri, CRS_NS['requiresCredits'], rdflib.Literal(mc, datatype=XSD.integer)))
    for subr in this_req.get('sub_req_IDs', []):
        grg.add((req_uri, CRS_NS['hasSubRequirement'], grad_req_id_to_uri(subr)))
        grg.add((req_uri, CRS_NS['canShareCreditsWith'], grad_req_id_to_uri(subr)))
        grg.add((grad_req_id_to_uri(subr), CRS_NS['canShareCreditsWith'], req_uri))
    for subr in this_req.get('share_credit_IDs', []):
        grg.add((req_uri, CRS_NS['canShareCreditsWith'], grad_req_id_to_uri(subr)))
        grg.add((grad_req_id_to_uri(subr), CRS_NS['canShareCreditsWith'], req_uri))
    for subr in this_req.get('restriction_IDs', []):
        grg.add((req_uri, CRS_NS['hasRestriction'], grad_req_id_to_uri(subr)))
        grg.add((req_uri, CRS_NS['canShareCreditsWith'], grad_req_id_to_uri(subr)))
        grg.add((grad_req_id_to_uri(subr), CRS_NS['canShareCreditsWith'], req_uri))
    for subr in this_req.get('fulfillable_by_IDs', []):
        grg.add((req_uri, CRS_NS['isFulfilledBy'], grad_req_id_to_uri(subr)))
        grg.add((req_uri, CRS_NS['canShareCreditsWith'], grad_req_id_to_uri(subr)))
        grg.add((grad_req_id_to_uri(subr), CRS_NS['canShareCreditsWith'], req_uri))

    vc = this_req.get('valid_courses', None)
    if vc:
        ccr_uri = course_restriction_to_uri(req_id)

        grg.add((ccr_uri, RDF_NS['type'], CRS_NS['CourseCodeRestriction']))
        grg.add((ccr_uri, RDF_NS['type'], OWL['NamedIndividual']))
        grg.add((req_uri, CRS_NS['hasCourseCodeRestriction'], ccr_uri))

        for valid_code in vc.get('valid_codes', []):
            grg.add((ccr_uri, CRS_NS['hasValidCourseCodeTag'], rdflib.Literal(valid_code, datatype=XSD.string)))

        for dept_code in vc.get('valid_dept_codes', []):
            grg.add((ccr_uri, CRS_NS['hasValidDepartmentCodeTag'], rdflib.Literal(dept_code, datatype=XSD.string)))

        for spec_tag in vc.get('special_tags', []):
            grg.add((ccr_uri, CRS_NS['hasSpecialTag'], rdflib.Literal(spec_tag, datatype=XSD.string)))

        maxlevel = vc.get('max_level', None)
        if maxlevel is not None:
            grg.add((ccr_uri, CRS_NS['hasValidLevelMax'], rdflib.Literal(maxlevel, datatype=XSD.integer)))

        minlevel = vc.get('min_level', None)
        if minlevel is not None:
            grg.add((ccr_uri, CRS_NS['hasValidLevelMin'], rdflib.Literal(minlevel, datatype=XSD.integer)))

        # print(vc)
    # print(req_id)

grg.serialize(graduation_req_save_file, format='ttl')