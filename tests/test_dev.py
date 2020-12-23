import pytest
from typing import FrozenSet, Tuple
from rdflib import URIRef, Namespace
from crex.models import StudentPOSRequirementContext, Course, Semester
from crex.services import SemesterCourseRecommenderService
from frex.utils import ConstraintSolver
from frex.utils.constraints import ConstraintType, SectionSetConstraint,SectionConstraintHierarchy

@pytest.mark.skip()
def test_generate_semester_course_recommendations(course_qs, test_student_1):

    scrs = SemesterCourseRecommenderService(course_query_service=course_qs)
    semester_rec_soln = scrs.get_recommendations_for_target_semester(
        student=test_student_1, year=2020, term="FALL"
    )

    # TODO: later on this should actually check that 'good' courses are getting recommended based on some scores...
    assert (
        len(semester_rec_soln.sections[0].section_candidates) == 4
        and 12 <= semester_rec_soln.sections[0].section_attribute_values['credits'] <= 16
        and 12 <= semester_rec_soln.overall_attribute_values['credits'] <= 16
        and len(set(cc.domain_object.course_code for cc in semester_rec_soln.sections[0].section_candidates)) == 4
    )

@pytest.mark.skip()
def test_run_pipeline(course_rec_pipe, test_pos_1, test_student_1, course_qs):
    # placeholder test for running the course recommende pipeline. under development.
    context = StudentPOSRequirementContext(
        student=test_student_1,
        plan_of_study=test_pos_1,
        requirements=frozenset(course_qs.get_all_requirements()),
    )

    # the pipeline should be doing some degee of filtering using requirements - still under development
    rec_courses = list(course_rec_pipe(context=context))

    assert len(rec_courses) != len(course_qs.get_all_courses()) and len(rec_courses) > 0

@pytest.mark.skip("skipping constraint solving")
def test_solve_for_requirements(course_qs):

    print("starting timer for setup time...")
    import time
    start = time.time()

    student = course_qs.get_student_by_uri(
        student_uri=URIRef(
            "https://tw.rpi.edu/ontology-engineering/oe2020/course-recommender-individuals/usrowen"
        )
    )

    from crex.models import CourseCandidate
    import random

    all_courses = course_qs.get_all_courses()

    placeholder_course_candidates = tuple(
        CourseCandidate(
            domain_object=c,
            context=None,
            applied_scores=[c.credits+c.credits*min((c.credits//3), 1)],#random.random()+2**c.credits],
            applied_explanations=[],
        )
        for c in all_courses
        # extra filtering, which should be unnecessary if proper querying is done.
        if c.credits and c.credits > 0 and c.course_code.course_level < 6000
    )

    all_requirements = []
    all_restriction_uris = set()
    req_sharing_relationships = dict()
    def add_req_to_dict(*, req_uri, req_dict, parent_uris) -> SectionConstraintHierarchy:
        if req_uri in req_dict:
            return None
        req = course_qs.get_requirement_by_uri(requirement_uri=req_uri)
        all_requirements.append(req)

        for parent_uri in parent_uris:
            req_dict[parent_uri]['allow'].add(req_uri)

        relationship_dict = {'require':set(), 'allow':set()}
        req_dict[req_uri] = relationship_dict

        extended_parents = [req_uri]
        extended_parents.extend(parent_uris)

        # go through the other requirements and add them to the dict
        for nreq_uri in req.restriction_requirement_uris:
            relationship_dict['require'].add(nreq_uri)
            nested_sch = add_req_to_dict(req_uri=nreq_uri, req_dict=req_dict, parent_uris=extended_parents)
            all_restriction_uris.add(nreq_uri)

        sch_and_list = []
        for nreq_uri in req.sub_requirement_uris:
            relationship_dict['allow'].add(nreq_uri)
            nested_sch = add_req_to_dict(req_uri=nreq_uri, req_dict=req_dict, parent_uris=extended_parents)
            sch_and_list.append(nested_sch)

        sch_or_list = []
        for nreq_uri in req.fulfilled_by_requirement_uris:
            relationship_dict['allow'].add(nreq_uri)
            nested_sch = add_req_to_dict(req_uri=nreq_uri, req_dict=req_dict, parent_uris=extended_parents)
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

    req_hierarchies = []
    for req in student.study_plan.planned_degree.requirements:
        req_hierarchy = add_req_to_dict(req_uri=req.uri, req_dict=req_sharing_relationships, parent_uris=[])
        req_hierarchies.append(req_hierarchy)
    print("_-------ordering-----_")
    from rdflib.namespace import RDFS
    for req in all_requirements:
        print(course_qs.queryable.graph.value(req.uri, RDFS['label']))
    print('done with ordering')
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
        for other_req in all_requirements[ind+1:]:
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
    fake_semesters = [
        Semester(uri=URIRef('fakeuri.com/semester/f2020'), term='FALL', year=2020),
        Semester(uri=URIRef('fakeuri.com/semester/s2021'), term='SPRING', year=2021),
        Semester(uri=URIRef('fakeuri.com/semester/f2021'), term='FALL', year=2021),
        Semester(uri=URIRef('fakeuri.com/semester/s2022'), term='SPRING', year=2022),
        Semester(uri=URIRef('fakeuri.com/semester/f2022'), term='FALL', year=2022),
        Semester(uri=URIRef('fakeuri.com/semester/s2023'), term='SPRING', year=2023),
        Semester(uri=URIRef('fakeuri.com/semester/f2023'), term='FALL', year=2023),
        Semester(uri=URIRef('fakeuri.com/semester/s2024'), term='SPRING', year=2024),
    ]
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
                constraint_value=12
        )
        semester_section_set.add_section_constraint(
                target_uri=sem.uri,
                constraint_type=ConstraintType.LEQ,
                attribute_name='credits',
                constraint_value=16
        )
        # a course can only be assigned to 1 term
        for sem_2 in fake_semesters[ind+1:]:
            semester_section_set.add_section_assignment_constraint(
                section_a_uri=sem.uri,
                section_b_uri=sem_2.uri,
                constraint_type=ConstraintType.AM1
            )

    solver_sections = (
        grad_requirements_section_set,
        semester_section_set,
    )

    solver = (
        ConstraintSolver()
        .set_candidates(candidates=placeholder_course_candidates)
        .set_section_set_constraints(section_sets=solver_sections)
        .add_overall_count_constraint(max_count=100) # maybe this one should be removed?
        .add_overall_item_constraint(
            attribute_name="credits",
            constraint_type=ConstraintType.EQ,
            constraint_value=128,
        )
    )
    print('setup time: ', start-time.time())

    print('solving...')
    solution = solver.solve()

    print('num candidates: ', len(placeholder_course_candidates))
    print('item count: ', len(solution.items))
    print('solution credits: ', solution.overall_attribute_values['credits'])
    print('chosen items: ')
    for item in solution.items:
        print(item.domain_object.course_code.name, item.domain_object.credits)

    from rdflib.namespace import RDFS
    print('grad requirement assignments:')
    for req_sec in solution.solution_section_sets[0].sections:
        print(course_qs.queryable.graph.value(req_sec.section_object.uri, RDFS['label']), req_sec.section_object.requires_credits)
        print([c.domain_object.course_code.name for c in req_sec.section_candidates])
    print("--")

    print('semester assignments:')
    for sem in solution.solution_section_sets[1].sections:
        print(sem.section_object.uri, ':', sem.section_attribute_values['credits'], ':',
              [(c.domain_object.course_code.name, c.domain_object.credits, c.domain_object.offering_terms, c.domain_object.offering_period) for c in sem.section_candidates])
    # # experimental setup for constraint solving
    #
    # req_uri_to_req = dict()
    # req_uri_to_index = dict()
    #
    # index_to_req = dict()
    # def add_req_to_dict(req_uri):
    #     if req_uri in req_uri_to_req:
    #         return
    #     req = course_qs.get_requirement_by_uri(requirement_uri=req_uri)
    #     req_uri_to_index[req_uri] = len(req_uri_to_index)
    #     index_to_req[len(index_to_req)] = req
    #     req_uri_to_req[req_uri] = req
    #
    #     # go through the other requirements and add them to the dict
    #     for nreq_uri in req.restriction_requirement_uris:
    #         add_req_to_dict(nreq_uri)
    #     for nreq_uri in req.fulfilled_by_requirement_uris:
    #         add_req_to_dict(nreq_uri)
    #     for nreq_uri in req.sub_requirement_uris:
    #         add_req_to_dict(nreq_uri)
    #
    # for req in student.study_plan.planned_degree.requirements:
    #     add_req_to_dict(req.uri)
    #
    # model = cp_model.CpModel()
    assert False

"""
    import rdflib
    # row is course, col is requirement
    course_applicable_matrix = {}
    for i in range(len(all_courses)):
        for j in range(len(index_to_req)):
            course_applicable_matrix[i, j] = 1 if index_to_req[j].course_code_restriction(all_courses[i]) else 0
    # whether or not to take a course, ignoring how its applied to requirements
    course_choices = {}
    # course credit values
    course_credits = {}
    # how courses are assigned to restrictions
    course_assignments = {}
    for i in range(len(all_courses)):
        course_choices[i] = model.NewIntVar(0, 1, "")
        course_credits[i] = all_courses[i].credits
        for j in range(len(index_to_req)):
            course_assignments[i, j] = model.NewIntVar(0, 1, "")
            if course_applicable_matrix[i, j] == 1:
                model.Add(course_assignments[i, j] <= course_choices[i])

###

    import numpy as np

    req_relations = np.zeros(shape=(len(index_to_req), len(index_to_req)))

    def add_req_constraints(*, req, parent_req_indices, boolvar=None):
        j = req_uri_to_index[req.uri]
        for k in parent_req_indices:
            req_relations[j, k] = 1
            req_relations[k, j] = 1
        new_indices = [j]
        new_indices.extend(parent_req_indices)

        if boolvar:
            model.Add(
                sum([course_credits[i]*course_applicable_matrix[i, j]*course_assignments[i, j]#*course_choices[i]#
                     for i in range(len(all_courses))])
                >= req.requires_credits
            ).OnlyEnforceIf(boolvar)
        else:
            model.Add(
                sum([course_credits[i]*course_applicable_matrix[i, j]*course_assignments[i, j]#*course_choices[i]#
                     for i in range(len(all_courses))])
                >= req.requires_credits
            ).OnlyEnforceIf([])

        for nreq_uri in req.share_credits_with_requirement_uris:
            # saftey measure to be sure we're only dealing with requirements for this degree
            share_j = req_uri_to_index.get(nreq_uri, -1)
            if share_j > -1:
                req_relations[share_j, j] = 1
                req_relations[j, share_j] = 1
                for k in parent_req_indices:
                    req_relations[share_j, k] = 1
                    req_relations[k, share_j] = 1

        for nreq_uri in req.restriction_requirement_uris:
            # TODO restrictions don't have any deeper level for now
            restrict_j = req_uri_to_index[nreq_uri]
            restrict_req = req_uri_to_req[nreq_uri]
            model.Add(
                sum([course_credits[i]*course_applicable_matrix[i, restrict_j]*course_assignments[i, restrict_j]#*course_choices[i]#
                     for i in range(len(all_courses))])
                <= restrict_req.requires_credits
            )

            req_relations[j, restrict_j] = 2
            req_relations[restrict_j, j] = 2
            for k in parent_req_indices:
                req_relations[restrict_j, k] = 1
                req_relations[k, restrict_j] = 1

        collect_or_bools = []
        for nreq_uri in req.fulfilled_by_requirement_uris:
            new_or_bool = model.NewBoolVar("")
            collect_or_bools.append(new_or_bool)
            nreq_bool = [new_or_bool]
            nreq_bool.extend(boolvar)

            add_req_constraints(req=req_uri_to_req[nreq_uri], parent_req_indices=new_indices, boolvar=nreq_bool)
        if collect_or_bools:
            model.Add(sum(collect_or_bools) >= 1).OnlyEnforceIf(boolvar)

        collect_and_bools = []
        for nreq_uri in req.sub_requirement_uris:
            new_and_bool = model.NewBoolVar("")
            collect_and_bools.append(new_and_bool)
            nreq_bool = [new_and_bool]
            nreq_bool.extend(boolvar)

            add_req_constraints(req=req_uri_to_req[nreq_uri], parent_req_indices=new_indices, boolvar=nreq_bool)
        if collect_and_bools:
            model.Add(sum(collect_and_bools) >= len(req.sub_requirement_uris)).OnlyEnforceIf(boolvar)



    for req in student.study_plan.planned_degree.requirements:
        req_bool = model.NewBoolVar("")
        model.Add(req_bool == 1)
        add_req_constraints(req=req, parent_req_indices=[], boolvar=[req_bool])

        # to make results come out faster - top level requirement should be using all applicable choices
        for i in range(len(all_courses)):
            model.Add(course_assignments[i, req_uri_to_index[req.uri]] == course_choices[i])

    # # set up credit sharing between reqs
    for j in range(len(index_to_req)):
        for k in range(j+1, len(index_to_req)):
            if req_relations[j, k] == 2:
                for i in range(len(all_courses)):
                    model.Add(course_assignments[i, j] == course_assignments[i, k])
            elif req_relations[j, k] == 0:
                for i in range(len(all_courses)):
                    model.Add(course_assignments[i, j] + course_assignments[i, k] <= 1)


    # minimize credits - for next implementation, maximize score
    mini_objective_terms = []
    for i in range(len(all_courses)):
        mini_objective_terms.append(course_credits[i]*course_choices[i])
    model.Minimize(sum(mini_objective_terms))

    maxi_objective_terms = []
    fake_scores = []
    for i in range(len(all_courses)):
        # TODO placeholder 'score'
        fake_score = int(round(np.random.random()*10))
        fake_scores.append(fake_score)
        maxi_objective_terms.append(course_choices[i]*fake_score)
    # model.Maximize(sum(maxi_objective_terms))

    from rdflib.namespace import RDFS
    print('setup complete: ', time.time()-starttime)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status != cp_model.OPTIMAL and status != cp_model.FEASIBLE:
        # possibly to revisit, if in the future it makes more sense to raise an exception than return None
        print('not optimal and not feasible. :(', status)
    else:
        if status == cp_model.OPTIMAL:
            print('optimal soln')
        print('chosen courses: ')
        credit_sum = 0
        for i in range(len(all_courses)):
            if solver.Value(course_choices[i]):
                credit_sum += all_courses[i].credits
                print(all_courses[i].course_code.name, ':', all_courses[i].name, ':', all_courses[i].credits, ': fake score -', fake_scores[i])
                print('assigned to: ', [
        course_qs.queryable.graph.value(k, RDFS['label']).value for k in req_uri_to_index.keys() if solver.Value(course_assignments[i, req_uri_to_index[k]])])
    print('credits: ', credit_sum)
    print('objective value: ', solver.ObjectiveValue())
    print('nested reqs ~', len(req_uri_to_req.keys()))


    assert False
    """