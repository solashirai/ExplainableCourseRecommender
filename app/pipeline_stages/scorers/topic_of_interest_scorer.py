from frex import CandidateScorer
from typing import Tuple
from app.models import CourseCandidate, StudentPOSContext
from app.services import CourseOntologyService


class TopicOfInterestScorer(CandidateScorer):

    def __init__(self, *, course_ontology_service: CourseOntologyService, **kwargs):
        self.cos = course_ontology_service
        super().__init__(**kwargs)

    def score(self, *, candidate: CourseCandidate) -> float:
        topic_match = 0
        for c_topic in candidate.domain_object.topics:
            for i_topic in candidate.context.student.topics_of_interest:
                topic_match = max(topic_match, self.cos.topic_similarity(topic_a=c_topic, topic_b=i_topic))
        return topic_match
