"""
Test the equivalent of `feditest create-testplan`
"""

import pytest

import feditest
from feditest import test
from feditest.protocols import Node
from feditest.testplan import TestPlan, TestPlanConstellation, TestPlanSession, TestPlanTestSpec


@pytest.fixture(scope="module", autouse=True)
def init():
    """ Keep these isolated to this module """
    feditest.all_tests = {}
    feditest._registered_as_test = {}
    feditest._registered_as_test_step = {}
    feditest._loading_tests = True

    @test
    def test1(role_a: Node) -> None:
        return

    @test
    def test2(role_a: Node) -> None:
        return

    @test
    def test3(role_b: Node) -> None:
        return

    feditest._loading_tests = False
    feditest._load_tests_pass2()


@pytest.fixture
def test_specs() -> list[TestPlanTestSpec]:
    return [
        TestPlanTestSpec(name) for name in sorted(feditest.all_tests.keys()) if feditest.all_tests.get(name) is not None
    ]


@pytest.fixture
def unnamed_constellations() -> list[TestPlanConstellation]:
    return [
        TestPlanConstellation({'role_a': None, 'role_b': None}, None),
        TestPlanConstellation({'role_a': None, 'role_b': None, 'role_c': None}, None)
    ]


@pytest.fixture
def unnamed_session_templates(test_specs: list[TestPlanTestSpec]) -> list[TestPlanSession]:
    return [
        TestPlanSession(TestPlanConstellation({'role_a': None, 'role_b': None}, None), test_specs),
        TestPlanSession(TestPlanConstellation({'role_a': None, 'role_b': None, 'role_c': None}, None), test_specs),
    ]


def construct_testplan(constellations: list[TestPlanConstellation], session_templates: list[TestPlanSession], testplan_name: str) -> TestPlan:
    """
    Helper to put it together.
    """
    sessions = []
    for session_template in session_templates:
        for constellation in constellations:
            session = session_template.instantiate_with_constellation(constellation, constellation.name)
            sessions.append(session)

    test_plan = TestPlan(sessions, testplan_name)
    test_plan.simplify()

    return test_plan


def test_structure(unnamed_constellations: list[TestPlanConstellation], unnamed_session_templates: list[TestPlanSession]) -> None:
    """
    Test the structure of the TestPlan, ignore the naming.
    """
    test_plan = construct_testplan(unnamed_constellations, unnamed_session_templates, None)
    assert len(test_plan.sessions) == 4


def test_all_unnamed(unnamed_constellations: list[TestPlanConstellation], unnamed_session_templates: list[TestPlanSession]) -> None:
    """
    Only test the naming.
    """
    test_plan = construct_testplan(unnamed_constellations, unnamed_session_templates, None)
    assert test_plan.name is None
    assert str(test_plan) == "Unnamed"


def test_testplan_named(unnamed_constellations: list[TestPlanConstellation], unnamed_session_templates: list[TestPlanSession]) -> None:
    """
    Only test the naming.
    """
    TESTPLAN_NAME = 'My test plan'
    test_plan = construct_testplan(unnamed_constellations, unnamed_session_templates, TESTPLAN_NAME)
    assert test_plan.name == TESTPLAN_NAME
    assert str(test_plan) == TESTPLAN_NAME

