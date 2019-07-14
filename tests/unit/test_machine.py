import random
from unittest.mock import create_autospec

import pytest

from dfsmpy import StateMachine, StopMachine


@pytest.fixture(scope="function")
def simple_machine():
    return {
        "alphabet": {1, 2, 3, 4},
        "initialState": 1,
        "validStates": {1, 2, 3, 4},
        "acceptedStates": {3},
        "finalStates": {4},
        "transition": lambda _, s: s
    }


def test_blueprint(simple_machine):
    machine = StateMachine(simple_machine)

    assert machine.blueprint["context"] == simple_machine.get("context", {})
    assert machine.blueprint["alphabet"] == simple_machine["alphabet"]
    assert machine.state == simple_machine["initialState"]

    for state in simple_machine["validStates"]:
        assert machine.is_valid(state)

    for state in simple_machine["acceptedStates"]:
        assert machine.is_accepted(state)

    for state in simple_machine["finalStates"]:
        assert machine.is_final(state)

    assert machine.is_initial(machine.state)
    assert not machine.is_accepted(machine.state)
    assert not machine.is_final(machine.state)
    assert not machine.accepted


def test_blueprint_invalid_initial_state(simple_machine):
    simple_machine["initialState"] = -1

    with pytest.raises(ValueError):
        StateMachine(simple_machine)


def test_transition_function(simple_machine):
    mock_transition = create_autospec(simple_machine["transition"])
    mock_transition.return_value = 1
    simple_machine["transition"] = mock_transition
    machine = StateMachine(simple_machine)

    machine.transition(1)
    mock_transition.assert_called_once_with(machine.context, 1)


def test_transition_context(simple_machine):
    def transition(context, event):
        context["value"] = event
        return event

    simple_machine["transition"] = transition
    machine = StateMachine(simple_machine)

    assert machine.context == simple_machine.get("context", {})

    machine.transition(2)

    assert machine.state == 2
    assert machine.context["value"] == 2
    assert not machine.is_initial(machine.state)
    assert not machine.is_accepted(machine.state)
    assert not machine.is_final(machine.state)
    assert not machine.accepted


def test_transition_accepted(simple_machine):
    machine = StateMachine(simple_machine)

    machine.transition(3)
    assert machine.state == 3
    assert not machine.is_initial(machine.state)
    assert machine.is_accepted(machine.state)
    assert not machine.is_final(machine.state)
    assert machine.accepted


def test_transition_final_state(simple_machine):
    machine = StateMachine(simple_machine)

    machine.transition(4)
    assert machine.state == 4
    assert not machine.is_initial(machine.state)
    assert not machine.is_accepted(machine.state)
    assert machine.is_final(machine.state)

    with pytest.raises(StopMachine):
        machine.transition(1)


def test_transition_invalid_event(simple_machine):
    machine = StateMachine(simple_machine)

    with pytest.raises(ValueError):
        machine.transition(-1)


def test_transition_invalid_state(simple_machine):
    simple_machine["transition"] = lambda *_: -1
    machine = StateMachine(simple_machine)

    with pytest.raises(ValueError):
        machine.transition(1)


def test_reset(simple_machine):
    machine = StateMachine(simple_machine)
    machine.context["value"] = "value"

    machine.transition(3)
    machine.reset()
    assert machine.is_initial(machine.state)
    assert machine.context == machine.blueprint["context"]


@pytest.fixture(scope="session")
def binary_multiples():
    """
    Return a state machine blueprint that accepts binary numbers that are
    multiples of 3.
    """
    def transition(context, event):
        """
        Trigger a transition to a new state by event and update context value.
        Shift the context value left 1 bit and add the event bit
        as the new least significant bit.
        Return the the modulus of the value by the divisor.
        """
        context["value"] = context["value"] << 1 ^ event
        return context["value"] % context["divisor"]

    return {
        "context":  {"divisor": 3, "value": 0, "results": list()},
        "alphabet": {0, 1},
        "initialState": 0,
        "validStates": {0, 1, 2},
        "acceptedStates": {0},
        "finalStates": {},
        "transition": transition
    }


def test_machine(binary_multiples):
    print(f"\n{binary_multiples}")

    for _ in range(100):
        machine = StateMachine(binary_multiples)
        result = 0

        while not machine.is_accepted(machine.state) \
                or not result \
                or result in binary_multiples["context"]["results"]:
            event = random.choice(list(machine.blueprint["alphabet"]))

            machine.transition(event)

            result = machine.context["value"]

        print(f"{machine}: {result:b} ({result})")
        assert result % machine.blueprint["context"]["divisor"] == 0
        binary_multiples["context"]["results"].append(result)
