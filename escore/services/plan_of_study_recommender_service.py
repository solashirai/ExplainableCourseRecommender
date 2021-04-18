from escore.pipeline import RecommendCoursesForPOSPipeline
from escore.services.course import CourseQueryService
from escore.models import Student, Semester, StudentPOSRequirementContext, CourseCandidate, Course
from typing import List, Tuple
from frex.utils import ConstraintSolver
from frex.models.constraints import SectionSetConstraint, ConstraintType, SectionConstraintHierarchy
from frex.models import ConstraintSolution, ConstraintSolutionSection
from rdflib import URIRef


class PlanOfStudyRecommenderService:
    def __init__(self, *, course_query_service: CourseQueryService):
        self.cqs = course_query_service

    def add_req_to_dict(self, *, req_uri, req_dict,
                        parent_uris, all_requirements, all_restriction_uris) -> SectionConstraintHierarchy:
        if req_uri in req_dict:
            return None
        req = self.cqs.get_requirement_by_uri(requirement_uri=req_uri)
        all_requirements.append(req)

        for parent_uri in parent_uris:
            req_dict[parent_uri]['allow'].add(req_uri)

        relationship_dict = {'require': set(), 'allow': set()}
        req_dict[req_uri] = relationship_dict

        extended_parents = [req_uri]
        extended_parents.extend(parent_uris)

        # go through the other requirements and add them to the dict
        for nreq_uri in req.restriction_requirement_uris:
            relationship_dict['require'].add(nreq_uri)
            nested_sch = self.add_req_to_dict(
                req_uri=nreq_uri, req_dict=req_dict, parent_uris=extended_parents,
                all_requirements=all_requirements, all_restriction_uris=all_restriction_uris)
            all_restriction_uris.add(nreq_uri)

        sch_and_list = []
        for nreq_uri in req.sub_requirement_uris:
            relationship_dict['allow'].add(nreq_uri)
            nested_sch = self.add_req_to_dict(
                req_uri=nreq_uri, req_dict=req_dict, parent_uris=extended_parents,
                all_requirements=all_requirements, all_restriction_uris=all_restriction_uris)
            sch_and_list.append(nested_sch)

        sch_or_list = []
        for nreq_uri in req.fulfilled_by_requirement_uris:
            relationship_dict['allow'].add(nreq_uri)
            nested_sch = self.add_req_to_dict(
                req_uri=nreq_uri, req_dict=req_dict, parent_uris=extended_parents,
                all_requirements=all_requirements, all_restriction_uris=all_restriction_uris)
            sch_or_list.append(nested_sch)

        for nreq_uri in req.share_credits_with_requirement_uris:
            relationship_dict['allow'].add(nreq_uri)

            # TODO some subtleties with sharing and parents needs to be addressed.
            # for parent_uri in parent_uris:
            #     req_dict[parent_uri]['allow'].add(nreq_uri)

        return SectionConstraintHierarchy(
            root_uri=req.uri,
            dependency_and=tuple(sch_and_list),
            dependency_or=tuple(sch_or_list)
        )

    def get_pos_recommendation_for_target_student(
        self,
        *,
        student: Student,
        max_credits_per_semester: int = 16,
        min_credits_per_semester: int = 12
    ) -> ConstraintSolution:
        # import time
        # starttime = time.time()

        rec_pipe = RecommendCoursesForPOSPipeline(course_query_service=self.cqs)

        # build up a list of requirements, based on the requirements found int he student's plan of study
        all_requirements = []
        all_restriction_uris = set()
        req_sharing_relationships = dict()
        req_hierarchies = []
        for req in student.study_plan.planned_degree.requirements:
            req_hierarchy = self.add_req_to_dict(
                req_uri=req.uri, req_dict=req_sharing_relationships, parent_uris=[],
                all_requirements=all_requirements, all_restriction_uris=all_restriction_uris)
            req_hierarchies.append(req_hierarchy)
        # print('time to get courses and reqs: ', time.time()-starttime)

        context = StudentPOSRequirementContext(
            student=student,
            plan_of_study=student.study_plan,
            requirements=frozenset(all_requirements)
        )

        candidate_courses: Tuple[CourseCandidate] = tuple(rec_pipe(context=context))

        grad_requirements_section_set = (
            SectionSetConstraint()
                .set_sections(
                sections=tuple(all_requirements)
            )
        )

        for rh in req_hierarchies:
            grad_requirements_section_set.add_hierarchical_section_constraint(hierarchy=rh)

        for ind, req in enumerate(all_requirements):

            if req.uri in all_restriction_uris:
                # restrictions must have <= the 'required' credits
                grad_requirements_section_set.add_section_constraint(
                    target_uri=req.uri,
                    constraint_type=ConstraintType.LEQ,
                    attribute_name='credits',
                    constraint_value=req.requires_credits
                )
                # because of how restrictions are modeled/implemented, we want to allow 'invalid' item assignments
                grad_requirements_section_set.allow_invalid_assignment_to_section(target_uri=req.uri)
            else:
                grad_requirements_section_set.add_section_constraint(
                    target_uri=req.uri,
                    constraint_type=ConstraintType.GEQ,
                    attribute_name='credits',
                    constraint_value=req.requires_credits
                )
            grad_requirements_section_set.set_section_assignment_filter(
                target_uri=req.uri,
                filter_function=req.course_code_restriction
            )

            req_share_rel = req_sharing_relationships[req.uri]
            for other_req in all_requirements[ind + 1:]:
                if other_req == req:
                    continue
                other_req_share_rel = req_sharing_relationships[other_req.uri]
                if other_req.uri in req.restriction_requirement_uris or req.uri in other_req.restriction_requirement_uris:
                    # sharing credits is required, as per how constraints are modeled in this system.
                    grad_requirements_section_set.add_section_assignment_constraint(
                        section_a_uri=req.uri,
                        section_b_uri=other_req.uri,
                        constraint_type=ConstraintType.EQ
                    )
                elif other_req.uri not in req_share_rel['allow'] and req.uri not in other_req_share_rel['allow']:
                    # print('cant share: ', req.uri, '-', other_req.uri)
                    # sharing credits not allowed, ensure an item is only assigned to one of these requirements
                    grad_requirements_section_set.add_section_assignment_constraint(
                        section_a_uri=req.uri,
                        section_b_uri=other_req.uri,
                        constraint_type=ConstraintType.AM1
                    )

        # set up for fake 'semester' objects, to demonstrate assigning recommended courses to semesters
        end_year = student.class_year
        fake_semesters = []
        for yr in range(end_year-4, end_year):
            fake_semesters.append(Semester(uri=URIRef(f'fakeuri.com/semester/fall{yr}'), term='FALL', year=yr))
            fake_semesters.append(Semester(uri=URIRef(f'fakeuri.com/semester/spring{yr+1}'), term='SPRING', year=yr+1))
        fake_semesters = tuple(fake_semesters)
        semester_section_set = (
            SectionSetConstraint()
                .set_sections(
                sections=tuple(fake_semesters)
            )
        )

        def course_offered_during_semester(*, semester: Semester):
            def course_valid_for_sem(course: Course):
                if semester.term in course.offering_terms:
                    if course.offering_period == "ANNUAL":
                        return True
                    elif course.offering_period == "EVEN":
                        return semester.year % 2 == 0
                    elif course.offering_period == "ODD":
                        return semester.year % 2 == 1
                return False

            return course_valid_for_sem

        for ind, sem in enumerate(fake_semesters):
            semester_section_set.set_section_assignment_filter(
                target_uri=sem.uri,
                filter_function=course_offered_during_semester(semester=sem))
            # full time students take between 12-15 credits
            semester_section_set.add_section_constraint(
                target_uri=sem.uri,
                constraint_type=ConstraintType.GEQ,
                attribute_name='credits',
                constraint_value=min_credits_per_semester
            )
            semester_section_set.add_section_constraint(
                target_uri=sem.uri,
                constraint_type=ConstraintType.LEQ,
                attribute_name='credits',
                constraint_value=max_credits_per_semester
            )
            # a course can only be assigned to 1 term
            for sem_2 in fake_semesters[ind + 1:]:
                semester_section_set.add_section_assignment_constraint(
                    section_a_uri=sem.uri,
                    section_b_uri=sem_2.uri,
                    constraint_type=ConstraintType.AM1
                )


        # set up courses the student has already taken
        for cc_uri in student.study_plan.completed_course_sections:
            course_sec = self.cqs.get_course_section_by_uri(course_section_uri=cc_uri)
            semester_section_set.add_required_item_assignment(section_uri=course_sec.semester.uri,
                                                              item_uri=course_sec.course.uri)

        solver_sections = (
            grad_requirements_section_set,
            semester_section_set,
        )

        solver = (
            ConstraintSolver(scaling=1000)
                .set_candidates(candidates=candidate_courses)
                .set_section_set_constraints(section_sets=solver_sections)
                .add_overall_count_constraint(max_count=100)  # maybe this one should be removed?
                .add_overall_item_constraint(
                attribute_name="credits",
                constraint_type=ConstraintType.EQ,
                constraint_value=128,
            )
        )

        # set up courses the student has already taken
        for cc_uri in student.study_plan.completed_courses:
            solver.add_required_item_selection(target_uri=cc_uri)

        # apply additional constraints on course prerequisites
        candidate_course_uris = frozenset({cc.domain_object.uri for cc in candidate_courses})
        for cc in candidate_courses:
            if cc.domain_object.required_prerequisites:
                for prereq_uri in cc.domain_object.required_prerequisites:
                    # TODO: currently ignoring prereqs that do not occur in the candidate courses. this could very
                    #  easily lead to incorrect results, since it is assuming that all relevant courses are present
                    #  in the candidate set.
                    if prereq_uri not in candidate_course_uris:
                        continue
                    # the prereq's ordering must be <= the candidate course's ordering
                    semester_section_set.add_item_ordering_dependence_constraint(
                        independent_uri=prereq_uri,
                        dependent_uri=cc.domain_object.uri,
                        constraint_type=ConstraintType.LESS
                    )
                    # if the candidate course is selected, the prereq must be selected.
                    solver.add_item_selection_constraint(
                        item_a_uri=prereq_uri,
                        item_b_uri=cc.domain_object.uri,
                        constraint_type=ConstraintType.GEQ
                    )

        # print('setup time: ', time.time()-starttime)
        solution = solver.solve(output_uri=URIRef("placeholder.com/output_studyplan"))
        # print('time to solution: ', time.time()-starttime)
        return solution

    def get_semester_recommendations_for_student(
        self,
        *,
        term: str,
        year: int,
        student: Student,
        max_credits_per_semester: int = 16,
        min_credits_per_semester: int = 12
    ) -> ConstraintSolutionSection:

        pos_soln = self.get_pos_recommendation_for_target_student(student=student,
                                                                  max_credits_per_semester=max_credits_per_semester,
                                                                  min_credits_per_semester=min_credits_per_semester)

        target_semester = Semester(uri=URIRef(f'fakeuri.com/semester/{term.lower()}{year}'), term=term, year=year)
        solution_section = None
        for section in pos_soln.solution_section_sets[1].sections:
            if section.section_object.uri == target_semester.uri:
                solution_section = section
                break

        return solution_section
