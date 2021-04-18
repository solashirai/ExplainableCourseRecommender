from frex import CandidateScorer
from escore.utils.path import INTEREST_TO_VEC, URI_TO_VEC
from escore.models import CourseCandidate, StudentPOSContext
from escore.services.course import CourseQueryService
from frex.utils.vector_similarity_utils import VectorSimilarityUtils
import numpy as np
import pickle


class TopicOfInterestScorer(CandidateScorer):
    def __init__(self, *, course_query_service: CourseQueryService,
                 **kwargs):
        self.cqs = course_query_service
        with open(INTEREST_TO_VEC, 'rb') as f:
            self.topic_to_vec = pickle.load(f)
        with open(URI_TO_VEC, 'rb') as f:
            self.uri_to_vec = pickle.load(f)
        self.vsu = VectorSimilarityUtils()
        super().__init__(**kwargs)

    def get_topic_similarity(self, *, interest_topic, course) -> float:

        interest_vec = self.topic_to_vec[interest_topic.name]
        course_vec = self.uri_to_vec[course.uri]

        # return self.vsu.jaccard_sim(comparison_vector=interest_vec, comparison_matrix=course_vec).tolist()[0][0]
        return self.vsu.cosine_sim(comparison_vector=interest_vec, comparison_matrix=course_vec).tolist()[0][0]

    def score(self, *, candidate: CourseCandidate) -> float:
        topic_match = 0
        for i_topic in candidate.context.student.topics_of_interest:
            topic_match = max(
                topic_match,
                self.get_topic_similarity(interest_topic=i_topic, course=candidate.domain_object),
            )
        return topic_match
