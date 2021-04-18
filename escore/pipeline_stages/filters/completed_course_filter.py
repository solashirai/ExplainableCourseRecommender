from frex import CandidateFilterer
from escore.models import CourseCandidate, StudentPOSContext


class CompletedCourseFilter(CandidateFilterer):
    def filter(self, *, candidate: CourseCandidate) -> bool:
        return not (
                candidate.domain_object.uri not in candidate.context.plan_of_study.completed_courses
        )
