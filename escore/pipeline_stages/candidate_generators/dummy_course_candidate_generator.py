from frex import CandidateGenerator, Explanation, Candidate
from typing import Generator, Dict, Tuple
from escore.models import Course, CourseCandidate, StudentPOSRequirementContext
from escore.services.course import CourseQueryService


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
        context: StudentPOSRequirementContext
    ) -> Generator[CourseCandidate, None, None]:
        if candidates:
            yield from candidates

        # TODO: this is a dummy
        courses = self.cqs.get_all_courses()

        # filter out coursese without credits for now - TODO maybe revisit later
        courses = tuple(c for c in courses if c.credits and c.credits > 0)

        for course in courses:
            yield CourseCandidate(
                domain_object=course,
                context=context,
                applied_scores=[0],
                applied_explanations=[self.generator_explanation],
            )
