from frex import CandidateFilterer
from escore.models import CourseCandidate, StudentPOSContext


class CanFulfillPOSRequirementFilter(CandidateFilterer):
    def filter(self, *, candidate: CourseCandidate) -> bool:
        if not candidate.domain_object.course_code.course_level:
            print(candidate.domain_object.uri)
        return not any(
            req.course_code_restriction(course=candidate.domain_object)
            for req in candidate.context.requirements
        )
