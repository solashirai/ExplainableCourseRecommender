from crex.models import StudentPOSRequirementContext
from crex.services import PlanOfStudyRecommenderService
from crex.pipeline import RecommendCoursesForPOSPipeline
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
