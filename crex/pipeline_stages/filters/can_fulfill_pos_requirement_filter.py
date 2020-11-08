from frex import CandidateFilterer
from crex.models import CourseCandidate, StudentPOSContext


class CanFulfillPOSRequirementFilter(CandidateFilterer):
    def filter(self, *, candidate: CourseCandidate) -> bool:
        return not any(
            req.course_code_restriction(course=candidate.domain_object)
            for req in candidate.context.requirements
        )
