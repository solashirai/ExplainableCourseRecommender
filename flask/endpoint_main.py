from flask import Flask, request, abort
import rdflib
from app.pipeline import RecommendCoursesPipeline
from app.services.course import GraphCourseQueryService
from app.utils.path import DATA_DIR
from app.models import StudentPOSRequirementContext, CourseCandidate
from typing import Tuple
from frex.stores import LocalGraph


def create_app(*, TESTING=True):

    app = Flask(__name__)

    if TESTING:
        # for testing locally
        kg_files = tuple((DATA_DIR / file).resolve() for file in [
            "yacs_course_data_v1.ttl",
            "rpi_departments.ttl",
            "manualcurated_grad_requirements.ttl",
        ])

        COURSEKG_GRAPH = LocalGraph(file_paths=kg_files)
    # else:
    #     COURSEKG_GRAPH = RemoteGraph(
    #         sparql_endpoint="?"
    #     )

    COURSE_QS = GraphCourseQueryService(queryable=COURSEKG_GRAPH)
    PLACEHOLDER_PIPE = RecommendCoursesPipeline(course_query_service=COURSE_QS)

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    @app.route("/get_recommended_courses_for_student", methods=["GET"])
    def get_subs_for_recipe():
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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True, port=80)
