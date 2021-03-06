import pytest
from escore.models import *
from escore.services.course import GraphCourseQueryService
from frex.stores import LocalGraph, RemoteGraph
from escore.utils.path import DATA_DIR
from escore.pipeline import RecommendCoursesPipeline
from rdflib import URIRef, Namespace


individual_ns = Namespace(
    "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/"
)

@pytest.fixture(scope="session")
def course_graph() -> LocalGraph:
    return LocalGraph(
        file_paths=(
            (DATA_DIR / "courses.ttl").resolve(),
            (DATA_DIR / "scheduled_courses.ttl").resolve(),
            (DATA_DIR / "rpi_departments.ttl").resolve(),
            (DATA_DIR / "parsed_grad_requirements.ttl").resolve(),
            (DATA_DIR / "users.ttl").resolve(),
        )
    )


@pytest.fixture(scope="session")
def course_qs(course_graph) -> GraphCourseQueryService:
    return GraphCourseQueryService(queryable=course_graph)


@pytest.fixture(scope="session")
def course_rec_pipe(course_qs) -> RecommendCoursesPipeline:
    return RecommendCoursesPipeline(course_query_service=course_qs)


@pytest.fixture(scope="session")
def pl_course(csci_dept_code, csci_dept):
    return Course(
        uri=individual_ns['crs938c5b7e20ea7e1620a2dd6329e6f0af274b46c3'],
        course_code=CourseCode(
            uri=individual_ns['crsCodeed2eaaf90b6625c9f6a5731e3f1a933357cd88b2'],
            name="CSCI-4430",
            department_code=csci_dept_code,
            course_level=4430.0,
            cross_listed=tuple()
        ),
        name="Programming Languages",
        credits=4,
        department=csci_dept,
        description="This course is a study of the important concepts found in current programming languages. "
                    "Topics include language processing (lexical analysis, parsing, type-checking, interpretation "
                    "and compilation, run-time environment), the role of abstraction (data abstraction and control "
                    "abstraction), programming paradigms (procedural, functional, object-oriented, logic-oriented, "
                    "generic), and formal language definition.",
        special_tags=frozenset(),

        required_prerequisites=frozenset({
            individual_ns['crsd930192130a654416bffd45ce16415ee608df66d'],
            individual_ns['crs9797fa54cb6f077d0e7cf31e23bdbafbbe00e8af']
        }),
        corequisites=frozenset(),
        recommended_prerequisites=frozenset(),
        topics=frozenset({
            TopicArea(
              uri=individual_ns['topic00001'],
              name='placeholder for topic',
                sub_topic_of=frozenset(),
                discipline='placeholder discipline'
            ),
        }
        ),
        offering_terms=("FALL",),
        offering_period="ANNUAL"
    )


@pytest.fixture(scope="session")
def csci_dept_code(csci_dept):
    return DepartmentCode(
        uri=individual_ns['dptc0026'],
        name="CSCI",
        department=csci_dept
    )

@pytest.fixture(scope="session")
def csci_dept():
    return Department(
        uri=individual_ns['dpt0026'],
        name="Computer Science",
        offered_major_uris=tuple(),
        offered_degree_uris=tuple()
    )


@pytest.fixture(scope="session")
def csci_major(csci_dept):
    return Major(
        uri=individual_ns['majCSCI'],
        name="Computer Science Major",
        department=csci_dept
    )


@pytest.fixture(scope="session")
def csci_top_level_req(csci_dept):
    return Requirement(
        uri=individual_ns['reqfd44455d4e7c62e5f83dde9ab7da8583adbfd31e'],
        fulfilled_by_requirement_uris=frozenset(),
        sub_requirement_uris=frozenset({
            individual_ns['req5f790f12a27e66b3f8c6534a79003cb5910d7fde'],
            individual_ns['req78e077dfe6014ee50f8fac4e06b2ae06333cc271'],
            individual_ns['reqa323d5f642970db3393d958ea2e8c6510032e1e2'],
            individual_ns['reqae4289fd7815ec563f927cc14309b63a797ab630'],
            individual_ns['reqbbf0c827d4009fdd91575d3974c3e9be28909b6c'],
            individual_ns['reqe29978dd3d6ce495c371fda071f87f6c36f0739f'],
        }),
        share_credits_with_requirement_uris=frozenset({
            individual_ns['req5f790f12a27e66b3f8c6534a79003cb5910d7fde'],
            individual_ns['req78e077dfe6014ee50f8fac4e06b2ae06333cc271'],
            individual_ns['reqa323d5f642970db3393d958ea2e8c6510032e1e2'],
            individual_ns['reqae4289fd7815ec563f927cc14309b63a797ab630'],
            individual_ns['reqbbf0c827d4009fdd91575d3974c3e9be28909b6c'],
            individual_ns['reqe29978dd3d6ce495c371fda071f87f6c36f0739f'],
        }),
        restriction_requirement_uris=frozenset(),
        requires_credits=128,
        course_code_restriction=CourseCodeRestriction(
            uri=individual_ns['ccr79a36c1af79f9c7271a61771aab09de994fccd4f'],
            valid_course_code_names=frozenset(),
            required_special_tag_names=frozenset(),
            valid_department_code_names=frozenset(),
        )
    )


@pytest.fixture(scope="session")
def csci_option_req():
    return Requirement(
        uri=individual_ns['req78e077dfe6014ee50f8fac4e06b2ae06333cc271'],
        requires_credits=16,
        share_credits_with_requirement_uris=frozenset({
            individual_ns['reqfd44455d4e7c62e5f83dde9ab7da8583adbfd31e'],
        }),
        sub_requirement_uris=frozenset(),
        restriction_requirement_uris=frozenset(),
        fulfilled_by_requirement_uris=frozenset(),
        course_code_restriction=CourseCodeRestriction(
            uri=individual_ns['ccr5a9b245b2af51a7b021a10d532b88f33418a97ca'],
            valid_course_code_names=frozenset(),
            required_special_tag_names=frozenset(),
            valid_department_code_names=frozenset({'CSCI'}),
            min_level=4000
        )
    )


@pytest.fixture(scope="session")
def csci_bs_deg(csci_major, csci_top_level_req):
    return Degree(
        uri=individual_ns['degBSInCSCI'],
        name='BS in Computer Science',
        major=csci_major,
        requirements=(csci_top_level_req,)
    )


@pytest.fixture(scope="session")
def owen_pos(csci_major, csci_bs_deg):
    return PlanOfStudy(
        uri=individual_ns['pos9a8e6844c6ecbac12f9f92da68ac51c5bd67704f'],
        class_year=2021,
        planned_major=csci_major,
        planned_degree=csci_bs_deg,
        completed_course_sections=frozenset({
            individual_ns["crsSec0838fe4beedeff7709d32d16ca67c9aa2373dba7"],
            individual_ns["crsSec0cf0d1a768ef7b1d580ac0aaf258257b8c766ecb"],
            individual_ns["crsSec0d060d8550b4d97fa0aa0188e75a213e37114cb5"],
            individual_ns["crsSec1d571602ec11f8e32dcde3b985cb277b68b7abb5"],
            individual_ns["crsSec40567fef852031bad43995aa8cab7c4877bc0a02"],
            individual_ns["crsSec4d3630ed52401a5362753db61595b8e1aec66bd8"],
            individual_ns["crsSec5241e24de4b9d40df379b7916e4698ac81354f6f"],
            individual_ns["crsSec5fd627bdf533aefd6f25ebb995fccc08e57f8dc2"],
            individual_ns["crsSec615e6c5aee4bbf92e6e193f86346602825bba571"],
            individual_ns["crsSec663dda052cc6e9647d255c294c71409b1883963f"],
            individual_ns["crsSec6a1c91448f2bdb49b519784e470a68c37318b45c"],
            individual_ns["crsSec79431f36805f7d501cc79356e3f69b26340e1d98"],
            individual_ns["crsSec8102566ff399c31b30351decb38ba3893db8e2f5"],
            individual_ns["crsSec8281ac09fc60458b13bdfef54b75f0b8e771837e"],
            individual_ns["crsSec8bb40720e14ff5d40a16d71efbfab65bbcd742eb"],
            individual_ns["crsSec99b5492130e02e1dcb08692178a020c1c2444195"],
            individual_ns["crsSecbc29e94fcaa333888baa92efb31dad194e1718b6"],
            individual_ns["crsSecc4b387e96f764565a80950390b36235fc00eabf1"],
            individual_ns["crsSeccb117aa26ddc5cf711c70466adcc656492e8a464"],
            individual_ns["crsSecce866dba24b0cdf1e707f40e0ee7fbb8de068406"],
            individual_ns["crsSecd5c95ece2b749c2e0beb1d2bfde0e23e5ad45d93"],
            individual_ns["crsSece04b10767b92aa4d53eb5a5b044ef13673b49448"],
            individual_ns["crsSece405364a6acf6b819c02915a204114f26ff8551f"],
            individual_ns["crsSecf5a9dafe85e39b30bdbd45b3371eeefd7520569d"],
            individual_ns["crsSecf603c709ea539acc6b9bb842d574c3d9eb7c17fa"],
            individual_ns["crsSecf7b40623128f286084d451d67cc7fb4b60b11c94"],
            individual_ns["crsSecf8b3e82fd2f512b3db0727642c6a1b7153581d47"],
            individual_ns["crsSecfb9210e5ca6bd4844b7bf9bdf1cb1c5956f81d08"],
        }),
        completed_courses=frozenset({
            individual_ns["crsafed9cb99a22f3c1c24a461212de74c061147fdc"],
            individual_ns["crsd13b01ead0fba8b4aa112ce4a06999a774cf7b2d"],
            individual_ns["crs16512f1cf1a0772c4b025c3d6ec1edcd0d8fe1fb"],
            individual_ns["crsfb2686b704f12418fbb57e79c573d4bb0fd2f418"],
            individual_ns["crsbb2f79ec60f43618cd25567f87e71171d29aee83"],
            individual_ns["crs3040f719acb6d5f911e4a1e0efdae1aab16e71d5"],
            individual_ns["crs76deeb1ecf1123e7b7b6918afd3e7e9c65a5bbdc"],
            individual_ns["crsa9004db87efa99687062b8819ace3f59d4e235cd"],
            individual_ns["crs8e3b954b259c3b7c341a8839f81fb05deeff68ea"],
            individual_ns["crs938c5b7e20ea7e1620a2dd6329e6f0af274b46c3"],
            individual_ns["crs667378d70c52e4a84617225e20e380eb49540f42"],
            individual_ns["crsd930192130a654416bffd45ce16415ee608df66d"],
            individual_ns["crs11d22a217c292f1bd278d88b96fa770c9a6fa207"],
            individual_ns["crs66ece4f97b7ad555666d9477af785bcaa7a40e8a"],
            individual_ns["crs547b5ccb36b817d3e2df2a96a09aa18f678bc4e0"],
            individual_ns["crs4b79ba1b9717a21b3aff7a7d656a471eea21448a"],
            individual_ns["crs0f4511984f6fb0682b0185c2dc94b50dbc4efd2a"],
            individual_ns["crs70c201e1b37def5c83e4458b044028e8a44f91c7"],
            individual_ns["crs9797fa54cb6f077d0e7cf31e23bdbafbbe00e8af"],
            individual_ns["crs1f544a878959fae04cb9d08b258e527007df5491"],
            individual_ns["crs61c14eb096ee7002039fb8baee948b4495f08440"],
            individual_ns["crsb195823511b1f4a6f4b656734aab626993defec6"],
            individual_ns["crs8aabf92b49dce005f10db4d14605ad4d5eb920d7"],
            individual_ns["crs2a22ca2e61da1be778732a493f944011f5b30519"],
            individual_ns["crs72de52b44f46d5b08b2917495701f202699880ca"],
            individual_ns["crsc746a794a800d873f1e5deff86c0c58e25f94848"],
            individual_ns["crs622f7a32272ea2f04599f688790c2571325b949a"],
            individual_ns["crs7c03aa6fefaf99476e8158ef5943f5ee91ee6146"],
        }),
        ongoing_course_sections=frozenset(),
        planned_courses=frozenset(),
    )


@pytest.fixture(scope="session")
def placeholder_advisor():
    return Advisor(
        uri=individual_ns['PLACEHOLDER-ADVISOR-URI'],
        name="Placeholder advisor name",
        advises_student_uris=tuple()
    )


@pytest.fixture(scope="session")
def owen_student(owen_pos, placeholder_advisor):
    return Student(
        uri=individual_ns['usrowen'],
        study_plan=owen_pos,
        name="owen",
        class_year=2021,
        topics_of_interest=frozenset({TopicArea(
            uri=individual_ns['hardcodedUserInterest'],
            name='semantic web',
            sub_topic_of=frozenset(),
            discipline="placeholder discipline",
        )}),
        registered_courses=frozenset(),
        advisor=placeholder_advisor,
    )


@pytest.fixture(scope="session")
def blank_student(placeholder_advisor, csci_major, csci_bs_deg):
    return Student(
        uri=individual_ns['blank_user'],
        study_plan=PlanOfStudy(
            uri=individual_ns['blank_user_pos'],
            class_year=2023,
            planned_major=csci_major,
            planned_degree=csci_bs_deg,
            completed_courses=frozenset({}),
            completed_course_sections=frozenset({}),
            ongoing_course_sections=frozenset(),
            planned_courses=frozenset(),
        ),
        name="blank",
        class_year=2023,
        topics_of_interest=frozenset({TopicArea(
            uri=individual_ns['hardcodedUserInterest'],
            name='ontology engineering',
            sub_topic_of=frozenset(),
            discipline="placeholder discipline",
        )}),
        registered_courses=frozenset(),
        advisor=placeholder_advisor,
    )


@pytest.fixture(scope="session")
def bs2(placeholder_advisor, csci_major, csci_bs_deg):
    return Student(
        uri=individual_ns['blank_user'],
        study_plan=PlanOfStudy(
            uri=individual_ns['blank_user_pos'],
            class_year=2023,
            planned_major=csci_major,
            planned_degree=csci_bs_deg,
            completed_courses=frozenset({}),
            completed_course_sections=frozenset({}),
            ongoing_course_sections=frozenset(),
            planned_courses=frozenset(),
        ),
        name="blank",
        class_year=2023,
        topics_of_interest=frozenset({TopicArea(
            uri=individual_ns['hardcodedUserInterest'],
            name='artificial intelligence',
            sub_topic_of=frozenset(),
            discipline="placeholder discipline",
        )}),
        registered_courses=frozenset(),
        advisor=placeholder_advisor,
    )


@pytest.fixture(scope="session")
def bs1(placeholder_advisor, csci_major, csci_bs_deg):
    return Student(
        uri=individual_ns['blank_user'],
        study_plan=PlanOfStudy(
            uri=individual_ns['blank_user_pos'],
            class_year=2023,
            planned_major=csci_major,
            planned_degree=csci_bs_deg,
            completed_courses=frozenset({}),
            completed_course_sections=frozenset({}),
            ongoing_course_sections=frozenset(),
            planned_courses=frozenset(),
        ),
        name="blank",
        class_year=2023,
        topics_of_interest=frozenset({TopicArea(
            uri=individual_ns['hardcodedUserInterest'],
            name='machine learning',
            sub_topic_of=frozenset(),
            discipline="placeholder discipline",
        )}),
        registered_courses=frozenset(),
        advisor=placeholder_advisor,
    )