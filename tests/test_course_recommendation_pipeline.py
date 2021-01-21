import pytest
from typing import FrozenSet, Tuple
from rdflib import URIRef, Namespace
from escore.models import StudentPOSRequirementContext, Course, Semester
from escore.models import StudentPOSRequirementContext
from escore.services import PlanOfStudyRecommenderService
from escore.pipeline import RecommendCoursesForPOSPipeline


def test_generate_semester_course_recommendations(course_qs, owen_student):

    posrs = PlanOfStudyRecommenderService(course_query_service=course_qs)
    sem_solution = posrs.get_semester_recommendations_for_student(
        student=owen_student,
        min_credits_per_semester=12,
        max_credits_per_semester=16,
        term="FALL",
        year=2021
    )

    # TODO: more checks that the contents are any good...
    assert (
        12 <= sem_solution.section_attribute_values['credits'] <= 16
    )


def test_run_pipeline(course_rec_pipe, owen_pos, owen_student, course_qs):
    # placeholder test for running the course recommende pipeline. under development.
    context = StudentPOSRequirementContext(
        student=owen_student,
        plan_of_study=owen_pos,
        requirements=owen_pos.planned_degree.requirements,
    )

    # the pipeline should be doing some degee of filtering using requirements - still under development
    rec_courses = list(course_rec_pipe(context=context))

    assert len(rec_courses) != len(course_qs.get_all_courses()) and len(rec_courses) > 0
