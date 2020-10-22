from frex.pipelines import _Pipeline
from frex.pipeline_stages import CandidateRanker
from frex.models import Explanation
from app.models import StudentPOSContext, Student, Course
from app.services.course import CourseQueryService
from app.pipeline_stages import *


class RecommendCoursesPipeline(_Pipeline):
    def __init__(
        self,
        *,
        course_query_service: CourseQueryService
    ):
        self.cqs = course_query_service
        _Pipeline.__init__(
            self,
            candidate_generators=(
                DummyCourseCandidateGenerator(course_query_service=self.cqs),
            ),
            stages=(
                PrerequisiteUnfulfilledFilter(
                    filter_explanation=Explanation(
                        explanation_string="You have not fulfilled the required prerequisites to take this course."
                    )
                ),
                RecommendedPrereqScorer(
                    scoring_explanation=Explanation(
                        explanation_string="You have completed some of the recommended prerequisites for this course."
                    )
                ),
                TopicOfInterestScorer(
                    scoring_explanation=Explanation(
                        explanation_string="This course covers topics that you have indicated as being interested in."
                    ),
                    course_query_service=self.cqs,
                ),
                CandidateRanker(),
            ),
        )