from frex import CandidateScorer
from typing import Tuple
from app.models import CourseCandidate, StudentPOSContext
from app.services.course import CourseQueryService


class TopicOfInterestScorer(CandidateScorer):
    def __init__(self, *, course_query_service: CourseQueryService, **kwargs):
        self.cqs = course_query_service
        super().__init__(**kwargs)

    def get_topic_similarity(self, *, topic_a, topic_b) -> float:
        # TODO
        return 0

    def score(self, *, candidate: CourseCandidate) -> float:
        topic_match = 0
        for c_topic in candidate.domain_object.topics:
            for i_topic in candidate.context.student.topics_of_interest:
                topic_match = max(
                    topic_match,
                    self.get_topic_similarity(topic_a=c_topic, topic_b=i_topic),
                )
        return topic_match
