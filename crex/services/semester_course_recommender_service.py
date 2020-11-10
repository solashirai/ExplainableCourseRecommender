from crex.pipeline import RecommendCoursesForSemesterPipeline
from crex.services.course import CourseQueryService
from crex.models import Student, Semester, StudentPOSRequirementContext, CourseCandidate
from typing import List


class SemesterCourseRecommenderService:
    def __init__(self, *, course_query_service: CourseQueryService):
        self.cqs = course_query_service

    def get_recommendations_for_target_semester(
        self, *, term: str, year: int, student: Student, max_credits: int = 16
    ):

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

        candidate_courses: List[CourseCandidate] = list(rec_pipe(context=context))

        final_courses = []
        total_credits = 0
        for cand in candidate_courses:
            if total_credits + cand.domain_object.credits < max_credits:
                final_courses.append(cand)
                total_credits += cand.domain_object.credits
            else:
                break

        return tuple(final_courses)
