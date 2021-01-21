from escore.models import StudentPOSRequirementContext
from escore.services import PlanOfStudyRecommenderService
from escore.pipeline import RecommendCoursesForPOSPipeline
import pytest


def test_generate_pos_for_blank_student(course_qs, blank_student):

    posrs = PlanOfStudyRecommenderService(course_query_service=course_qs)
    solution = posrs.get_pos_recommendation_for_target_student(student=blank_student,
                                                               min_credits_per_semester=12,
                                                               max_credits_per_semester=16)

    assert (
            solution.items is not None
            and all(
        12 <= sem.section_attribute_values['credits'] <= 16
        for sem in solution.solution_section_sets[1].sections
    )
    )


def test_generate_pos_for_progressed_student(course_qs, owen_student):

    posrs = PlanOfStudyRecommenderService(course_query_service=course_qs)
    solution = posrs.get_pos_recommendation_for_target_student(student=owen_student,
                                                               min_credits_per_semester=12,
                                                               max_credits_per_semester=16)

    candidate_courses = tuple(RecommendCoursesForPOSPipeline(course_query_service=course_qs)(
        context=StudentPOSRequirementContext(
            student=owen_student,
            plan_of_study=owen_student.study_plan,
            requirements=frozenset(owen_student.study_plan.planned_degree.requirements)
        )))
    candidate_course_uris = set(cc.domain_object.uri for cc in candidate_courses)
    completed_valid_uris = candidate_course_uris.intersection(owen_student.study_plan.completed_courses)

    assert (
            solution.items is not None
            and all(c in {item.domain_object.uri for item in solution.items}
                    for c in completed_valid_uris)
            and all(
                12 <= sem.section_attribute_values['credits'] <= 20
                for sem in solution.solution_section_sets[1].sections
            )
    )


'''
0
time to get courses and reqs:  1.773897409439087
setup time:  23.674071073532104
time to solution:  47.0415244102478
PASSED [ 21%]1
time to get courses and reqs:  0.724149227142334
setup time:  22.516698122024536
time to solution:  47.705142974853516
PASSED [ 28%]2
time to get courses and reqs:  0.7019932270050049
setup time:  22.516957759857178
time to solution:  73.32651495933533
PASSED [ 35%]3
time to get courses and reqs:  0.7085459232330322
setup time:  22.94572424888611
time to solution:  159.60301995277405
PASSED [ 42%]4
time to get courses and reqs:  0.6653313636779785
setup time:  21.93260622024536
time to solution:  1214.9857609272003
PASSED [ 50%]5
time to get courses and reqs:  0.6863586902618408
setup time:  22.49541687965393
time to solution:  539.8135826587677

0
time to get courses and reqs:  1.905360460281372
setup time:  23.783711910247803
time to solution:  274.21828031539917
PASSED [ 21%]1
time to get courses and reqs:  0.7019977569580078
setup time:  22.595621347427368
time to solution:  202.8629183769226
PASSED [ 28%]2
time to get courses and reqs:  0.6863563060760498
setup time:  22.548495054244995
time to solution:  78.08073854446411
PASSED [ 35%]3
time to get courses and reqs:  0.7020442485809326
setup time:  22.887386083602905
time to solution:  128.26283597946167
PASSED [ 42%]4
time to get courses and reqs:  0.6955044269561768
setup time:  22.526991605758667
time to solution:  459.1165759563446
PASSED [ 50%]5
time to get courses and reqs:  0.68634033203125
setup time:  22.24803352355957
time to solution:  64.87369084358215

0
time to get courses and reqs:  1.9055495262145996
setup time:  23.6525137424469
time to solution:  76.43988418579102
PASSED [ 21%]1
time to get courses and reqs:  0.7020235061645508
setup time:  22.49564814567566
time to solution:  193.29008173942566
PASSED [ 28%]2
time to get courses and reqs:  0.7020025253295898
setup time:  22.526930332183838
time to solution:  81.802898645401
PASSED [ 35%]3
time to get courses and reqs:  0.7019915580749512
setup time:  22.542011499404907
time to solution:  73.37696647644043
PASSED [ 42%]4
time to get courses and reqs:  0.7020103931427002
setup time:  22.395220041275024
time to solution:  637.0260272026062
PASSED [ 50%]5
time to get courses and reqs:  0.6684253215789795
setup time:  22.018203496932983
time to solution:  644.475301027298
'''