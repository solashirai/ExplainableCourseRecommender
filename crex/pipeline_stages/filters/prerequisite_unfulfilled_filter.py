from frex import CandidateFilterer
from crex.models import CourseCandidate, StudentPOSContext


class PrerequisiteUnfulfilledFilter(CandidateFilterer):
    def filter(self, *, candidate: CourseCandidate) -> bool:
        return not all(
            prereq in candidate.context.completed_courses
            for prereq in candidate.domain_object.required_prerequisites
        )
