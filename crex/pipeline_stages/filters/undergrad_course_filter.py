from frex import CandidateFilterer
from crex.models import CourseCandidate, StudentPOSContext


class UndergradCourseFilter(CandidateFilterer):
    def filter(self, *, candidate: CourseCandidate) -> bool:
        return not (
                candidate.domain_object.course_code.course_level
                and candidate.domain_object.course_code.course_level <= 6000
        )
