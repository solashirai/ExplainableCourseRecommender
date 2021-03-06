from frex.pipelines import Pipeline
from frex.pipeline_stages import CandidateRanker
from frex.models import Explanation
from escore.models import CourseCandidate
from typing import Generator
from escore.services.course import CourseQueryService
from escore.pipeline_stages import *


class RecommendCoursesForSemesterPipeline(Pipeline):
    def __init__(self, *, course_query_service: CourseQueryService):
        self.cqs = course_query_service
        Pipeline.__init__(
            self,
            stages=(
                CourseSectionsInSemesterCandidateGenerator(
                    course_query_service=self.cqs
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
