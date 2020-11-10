from frex import CandidateGenerator, Explanation, Candidate
from typing import Generator, Dict, Tuple
from crex.models import Course, CourseCandidate, StudentPOSRequirementContext
from crex.services.course import CourseQueryService


class CourseSectionsInSemesterCandidateGenerator(CandidateGenerator):
    def __init__(self, *, course_query_service: CourseQueryService, **kwargs):
        self.cqs = course_query_service
        generator_explanation = Explanation(
            explanation_string="This is a dummy explanation, generate all courses."
        )
        CandidateGenerator.__init__(
            self, generator_explanation=generator_explanation, **kwargs
        )

    def __call__(
        self,
        *,
        candidates: Generator[Candidate, None, None] = None,
        context: StudentPOSRequirementContext
    ) -> Generator[CourseCandidate, None, None]:
        if candidates:
            yield from candidates

        course_sections = self.cqs.get_course_sections_by_semester(
            year=context.target_year, term=context.target_term
        )

        for course_section in course_sections:
            yield CourseCandidate(
                domain_object=course_section.course,
                context=context,
                applied_scores=[0],
                applied_explanations=[self.generator_explanation],
            )
