from frex import CandidateScorer
from typing import Tuple
from crex.models import CourseCandidate, StudentPOSContext


class RecommendedPrereqScorer(CandidateScorer):
    def score(self, *, candidate: CourseCandidate) -> float:
        if len(candidate.domain_object.recommended_prerequisites) == 0:
            return 1
        completed_courses = {
            cc.coures for cc in candidate.context.plan_of_study.completed_courses
        }
        recommended_fulfilled = sum(
            1
            for prereq in candidate.domain_object.recommended_prerequisites
            if prereq in completed_courses
        )
        return recommended_fulfilled / len(
            candidate.domain_object.recommended_prerequisites
        )
