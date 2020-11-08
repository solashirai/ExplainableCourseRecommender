from flask import Flask, request, abort
import rdflib
from crex.pipeline import RecommendCoursesPipeline
from crex.services.course import GraphCourseQueryService
from crex.utils.path import DATA_DIR
from crex.models import StudentPOSRequirementContext, CourseCandidate, Student, PlanOfStudy
from typing import Tuple
from frex.stores import LocalGraph


app = Flask(__name__)

# for testing locally
kg_files = tuple((DATA_DIR / file).resolve() for file in [
    "yacs_course_data_v1.ttl",
    "rpi_departments.ttl",
    "manualcurated_grad_requirements.ttl",
])

COURSEKG_GRAPH = LocalGraph(file_paths=kg_files)

# COURSEKG_GRAPH = RemoteGraph(
#     sparql_endpoint="?"
# )

COURSE_QS = GraphCourseQueryService(queryable=COURSEKG_GRAPH)
PLACEHOLDER_PIPE = RecommendCoursesPipeline(course_query_service=COURSE_QS)

@app.route("/crex_api/")
def hello_world():
    return "Hello, Worrld!"

@app.route("/crex_api/dummy_get_rec", methods=["GET"])
def dummy_recommend_courses():
    args = request.args

    # dummy plan of study and student to test
    pos = PlanOfStudy(
        uri=rdflib.URIRef('placeholder_pos1'),
        class_year='2022',
        planned_major=(),
        planned_degree=None,
        completed_courses=(),
        ongoing_courses=(),
        planned_courses=()
    )
    student = Student(
        uri=rdflib.URIRef('placeholder_stud1'),
        study_plan=pos,
        name='john doe',
        rin='123',
        class_year='2022',
        topics_of_interest=(),
        registered_courses=(),
        advisor=None,
    )

    context = StudentPOSRequirementContext(student=student, plan_of_study=pos,
                                           requirements=frozenset(COURSE_QS.get_all_requirements()))

    rec_courses: Tuple[CourseCandidate] = PLACEHOLDER_PIPE(context=context)
    app.logger.info(f'retrieved recommended courses.')

    rec_course_codes = [rc.domain_object.course_code.name for rc in rec_courses]
    return {'recommend_course_codes': rec_course_codes}

@app.route("/crex_api/get_recommended_courses_for_student", methods=["GET"])
def get_course_recommendation_for_student():
    args = request.args

    student_uri = rdflib.URIRef(args["student_uri"])
    student = COURSE_QS.get_student_by_uri(student_uri=student_uri)

    # will plan of study be saved somehow...? or have person input and pass it via this method...?
    # assuming POS will have some structure... ignoring for now since it's not properly used anyways
    pos = args['plan_of_study']

    context = StudentPOSRequirementContext(student=student, plan_of_study=pos,
                                           requirements=frozenset(COURSE_QS.get_all_requirements()))

    rec_courses: Tuple[CourseCandidate] = PLACEHOLDER_PIPE(context=context)
    app.logger.info(f'retrieved recommended courses.')

    rec_course_codes = [rc.domain_object.course_code.name for rc in rec_courses]
    return {'recommend_course_codes': rec_course_codes}
    #
    # except NotFoundException as e:
    #     abort(404, description=e)
    # except MalformedContentException as e:
    #     abort(500, description=e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
