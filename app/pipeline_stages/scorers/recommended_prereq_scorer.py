from frex import CandidateScorer
from typing import Tuple
from app.models import CourseCandidate, StudentPOSContext
from app.services import CourseOntologyService


class RecommendedPrereqScorer(CandidateScorer):
    def score(self, *, candidate: CourseCandidate) -> float:
        if len(candidate.domain_object.recommended_prerequisites) == 0:
            return 1
        completed_courses = {
            cc.coures for cc in candidate.context.student.study_plan.completed_courses
        }
        recommended_fulfilled = sum(
            1
            for prereq in candidate.domain_object.recommended_prerequisites
            if prereq.uri in completed_courses
        )
        return recommended_fulfilled / len(
            candidate.domain_object.recommended_prerequisites
        )
