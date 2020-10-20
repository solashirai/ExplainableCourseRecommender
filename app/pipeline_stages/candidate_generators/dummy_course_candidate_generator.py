from frex import CandidateGenerator, Explanation, Candidate
from typing import Generator, Dict, Tuple
from app.models import Course, CourseCandidate, StudentPOSContext
from app.services.course import CourseQueryService


class DummyCourseCandidateGenerator(CandidateGenerator):
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
        context: StudentPOSContext
    ) -> Generator[CourseCandidate, None, None]:
        if candidates:
            yield from candidates

        # TODO: this is a dummy
        courses = self.cqs.get_all_courses()

        for course in courses:
            yield CourseCandidate(
                domain_object=course,
                context=context,
                applied_scores=[0],
                applied_explanations=[self.generator_explanation],
            )
