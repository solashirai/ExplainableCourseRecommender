from flask import Flask, request, abort
import rdflib
from escore.pipeline import RecommendCoursesPipeline
from escore.services.course import GraphCourseQueryService
from escore.services import PlanOfStudyRecommenderService
from escore.utils.path import DATA_DIR
from escore.models import StudentPOSRequirementContext, CourseCandidate, Student, PlanOfStudy
from typing import Tuple
from frex.stores import LocalGraph


app = Flask(__name__)

# for testing locally
kg_files = tuple((DATA_DIR / file).resolve() for file in [
    "courses.ttl",
    "scheduled_courses.ttl",
    "rpi_departments.ttl",
    "parsed_grad_requirements.ttl",
    "users.ttl",
])

COURSEKG_GRAPH = LocalGraph(file_paths=kg_files)

# COURSEKG_GRAPH = RemoteGraph(
#     sparql_endpoint="?"
# )

COURSE_QS = GraphCourseQueryService(queryable=COURSEKG_GRAPH)
PLACEHOLDER_PIPE = RecommendCoursesPipeline(course_query_service=COURSE_QS)

PR_SERVICE = PlanOfStudyRecommenderService(
    course_query_service=COURSE_QS
)

@app.route("/crex_api/")
def hello_world():
    return "Hello, Worrld!"

@app.route("/crex_api/dummy_get_rec", methods=["GET"])
def dummy_recommend_courses():
    args = request.args

    # dummy plan of study and student to test
    pos = PlanOfStudy(
        uri=rdflib.URIRef('placeholder_pos1'),
        class_year=2022,
        planned_major=None,
        planned_degree=None,
        completed_courses=frozenset(),
        ongoing_course_sections=frozenset(),
        planned_courses=frozenset()
    )
    student = Student(
        uri=rdflib.URIRef('placeholder_stud1'),
        study_plan=pos,
        name='john doe',
        class_year=2022,
        topics_of_interest=frozenset(),
        registered_courses=frozenset(),
        advisor=None,
    )

    context = StudentPOSRequirementContext(student=student, plan_of_study=pos,
                                           requirements=frozenset(COURSE_QS.get_all_requirements()))

    rec_courses: Tuple[CourseCandidate, ...] = PLACEHOLDER_PIPE(context=context)
    app.logger.info(f'retrieved recommended courses.')

    rec_course_codes = [rc.domain_object.course_code.name for rc in rec_courses]
    return {'recommend_course_codes': rec_course_codes}

@app.route("/crex_api/get_recommended_courses_for_student", methods=["GET"])
def get_course_recommendation_for_student():
    args = request.args

    #https%3A%2F%2Ftw.rpi.edu%2Fontology-engineering%2Foe2020%2Fcourse-recommender-individuals%2Fusrowen

    student_uri = rdflib.URIRef(args["student_uri"])
    student = COURSE_QS.get_student_by_uri(student_uri=student_uri)
    print(f'got student {student.name}')

    # will plan of study be saved somehow...? or have person input and pass it via this method...?
    # assuming POS will have some structure... ignoring for now since it's not properly used anyways
    pos = args.get('plan_of_study', None)
    if pos is None:
        pos = student.study_plan
    print(f'got student plan of study')

    context = StudentPOSRequirementContext(student=student, plan_of_study=pos,
                                           requirements=frozenset(COURSE_QS.get_all_requirements()))

    rec_courses: Tuple[CourseCandidate, ...] = PLACEHOLDER_PIPE(context=context)
    app.logger.info(f'retrieved recommended courses.')

    rec_course_codes = [rc.domain_object.course_code.name for rc in rec_courses]
    return {'recommend_course_codes': rec_course_codes}
    #
    # except NotFoundException as e:
    #     abort(404, description=e)
    # except MalformedContentException as e:
    #     abort(500, description=e)

@app.route("/crex_api/get_pos_rec_for_student", methods=["GET"])
def get_pos_recommendation_for_student():
    args = request.args

    # ?student_uri=https%3A%2F%2Ftw.rpi.edu%2Fontology-engineering%2Foe2020%2Fcourse-recommender-individuals%2Fusrowen

    student_uri = rdflib.URIRef(args["student_uri"])
    student = COURSE_QS.get_student_by_uri(student_uri=student_uri)
    print(f'got student {student.name}')

    pos_rec = PR_SERVICE.get_pos_recommendation_for_target_student(student=student)

    rec_sem_courses = {f'{sec.section_object.term} {sec.section_object.year} semester': [cand.domain_object.name
                                              for cand in sec.section_candidates]
                       for sec in pos_rec.solution_section_sets[1].sections}
    return {'recommend_course_per_semester': rec_sem_courses}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
