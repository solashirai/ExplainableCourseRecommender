from frex import CandidateFilterer
from app.models import CourseCandidate, StudentPOSContext


class PrerequisiteUnfulfilledFilter(CandidateFilterer):
    def filter(self, *, candidate: CourseCandidate) -> bool:
        completed_courses = {
            cc.coures for cc in candidate.context.plan_of_study.completed_courses
        }
        return not all(
            prereq in completed_courses
            for prereq in candidate.domain_object.required_prerequisites
        )
