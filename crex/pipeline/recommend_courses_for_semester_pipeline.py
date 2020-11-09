from frex.pipelines import _Pipeline
from frex.pipeline_stages import CandidateRanker
from frex.models import Explanation
from crex.models import CourseCandidate
from typing import Generator
from crex.services.course import CourseQueryService
from crex.pipeline_stages import *


class RecommendCoursesForSemesterPipeline(_Pipeline):
    def __init__(self, *, course_query_service: CourseQueryService):
        self.cqs = course_query_service
        _Pipeline.__init__(
            self,
            candidate_generators=(
                CourseSectionsInSemesterCandidateGenerator(
                    course_query_service=self.cqs
                ),
            ),
            stages=(
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
