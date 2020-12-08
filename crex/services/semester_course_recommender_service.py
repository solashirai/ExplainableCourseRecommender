from crex.pipeline import RecommendCoursesForSemesterPipeline
from crex.services.course import CourseQueryService
from crex.models import Student, Semester, StudentPOSRequirementContext, CourseCandidate
from typing import List
from frex.utils import ConstraintSolver, ConstraintType
from frex.models import ConstraintSolution


class SemesterCourseRecommenderService:
    def __init__(self, *, course_query_service: CourseQueryService):
        self.cqs = course_query_service

    def get_recommendations_for_target_semester(
        self, *, term: str, year: int, student: Student, max_credits: int = 16, min_credits: int = 12
    ) -> ConstraintSolution:

        rec_pipe = RecommendCoursesForSemesterPipeline(course_query_service=self.cqs)
        requirements = (
            self.cqs.get_all_requirements()
        )  # TODO: requirements should be specific to students / major

        context = StudentPOSRequirementContext(
            student=student,
            plan_of_study=student.study_plan,
            requirements=frozenset(requirements),
            target_term=term,
            target_year=year,
        )

        candidate_courses = list(rec_pipe(context=context))
        candidate_courses = [crs for crs in candidate_courses if crs.domain_object.credits]

        print("cand len: ", len(candidate_courses))

        soln = ConstraintSolver().set_sections(sections=1)\
            .set_candidates(candidates=candidate_courses)\
            .set_items_per_section(count=4)\
            .add_section_constraint(attribute_name='credits',
                                    constraint_type=ConstraintType.LEQ,
                                    constraint_value=max_credits)\
            .add_section_constraint(attribute_name='credits',
                                    constraint_type=ConstraintType.GEQ,
                                    constraint_value=min_credits)\
            .solve()

        return soln
