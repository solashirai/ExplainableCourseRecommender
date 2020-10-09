from frex.pipelines import _Pipeline
from frex.pipeline_stages import CandidateRanker
from frex.models import Explanation
from app.models import StudentPOSContext, Student, Course
from app.services.course import CourseQueryService
from app.services import CourseOntologyService
from app.pipeline_stages import *


class RecommendCoursesPipeline(_Pipeline):

    def __init__(
        self,
        *,
        target_student: Student,
        course_query_service: CourseQueryService,
        course_ontology_service: CourseOntologyService
    ):
        self.cqs = course_query_service
        self.cos = course_ontology_service
        context = StudentPOSContext(student=target_student,
                                    plan_of_study=target_student.study_plan)
        _Pipeline.__init__(
            self,
            context=context,
            candidate_generators=(
                DummyCourseCandidateGenerator(
                    course_query_service=self.cqs
                ),
            ),
            stages=(
                PrerequisiteUnfulfilledFilter(
                    filter_explanation=Explanation(
                        explanation_string='You have not fulfilled the required prerequisites to take this course.'
                    )
                ),
                RecommendedPrereqScorer(
                    scoring_explanation=Explanation(
                        explanation_string='You have completed some of the recommended prerequisites for this course.'
                    )
                ),
                TopicOfInterestScorer(
                    scoring_explanation=Explanation(
                        explanation_string='This course covers topics that you have indicated as being interested in.'
                    ),
                    course_ontology_service=self.cos
                ),
                CandidateRanker(),
            ),
        )
