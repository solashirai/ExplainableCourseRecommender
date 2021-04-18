from frex.pipelines import Pipeline
from frex.pipeline_stages import CandidateRanker
from frex.models import Explanation
from escore.models import CourseCandidate
from typing import Tuple
from escore.services.course import CourseQueryService
from escore.pipeline_stages import *


class RecommendCoursesPipeline(Pipeline):
    def __init__(self, *, course_query_service: CourseQueryService):
        self.cqs = course_query_service
        Pipeline.__init__(
            self,
            stages=(
                DummyCourseCandidateGenerator(course_query_service=self.cqs),
                CompletedCourseFilter(
                    filter_explanation=Explanation(
                        explanation_string="This course hasn't been completed by the student yet."
                    )
                ),
                UndergradCourseFilter(
                    filter_explanation=Explanation(
                        explanation_string="This is an undergraduate-level course."
                    )
                ),
                PrerequisiteUnfulfilledFilter(
                    filter_explanation=Explanation(
                        explanation_string="You have fulfilled the required prerequisites to take this course."
                    )
                ),
                CanFulfillPOSRequirementFilter(
                    filter_explanation=Explanation(
                        explanation_string="This course can fulfill some requirement towards your degree."
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
