from random import choice
from unittest.mock import MagicMock

from pytest import fixture, raises

from dfsmpy import StateMachine, StopMachine


def test_invalid_machine():
    with raises(ValueError):
        StateMachine(dict())


@fixture(scope="function")
def default_machine():
    return {
        "initialState": 0,
        "validStates": {0}
    }


def test_default_machine(default_machine):
    machine = StateMachine(default_machine)

    assert machine.context == dict()
    assert not machine.is_accepted(machine.state)
    assert not machine.is_final(machine.state)


@fixture(scope="function")
def simple_machine():
    return {
        "initialState": 1,
        "validStates": {1, 2, 3, 4},
        "acceptedStates": {3},
        "finalStates": {4},
        "alphabet": {1, 2, 3, 4}
    }


def test_blueprint(simple_machine):
    machine = StateMachine(simple_machine)

    for state in simple_machine["validStates"]:
        assert machine.is_valid(state)

    for state in simple_machine["acceptedStates"]:
        assert machine.is_accepted(state)

    for state in simple_machine["finalStates"]:
        assert machine.is_final(state)

    assert machine.initial
    assert not machine.accepted
    assert not machine.final


def test_blueprint_invalid_initial_state(simple_machine):
    simple_machine["initialState"] = -1

    with raises(ValueError):
        StateMachine(simple_machine)


def test_transition_function(simple_machine, event=1):
    mock_transition = MagicMock(return_value=event)
    simple_machine["transition"] = mock_transition
    machine = StateMachine(simple_machine)

    machine.transition(event)
    mock_transition.assert_called_once_with(
        machine.state, machine.context, event
    )


def test_transition_context(simple_machine, event=2):
    def transition(state, context, event):
        context["value"] = event
        return event

    simple_machine["transition"] = transition
    machine = StateMachine(simple_machine)

    assert machine.context == simple_machine.get("context", dict())

    machine.transition(event)

    assert machine.state == event
    assert machine.context["value"] == event
    assert not machine.initial
    assert not machine.accepted
    assert not machine.final


def test_transition_accepted(simple_machine, event=3):
    machine = StateMachine(simple_machine)

    machine.transition(event)
    assert machine.state == event
    assert not machine.initial
    assert machine.accepted
    assert not machine.final


def test_transition_final_state(simple_machine, event=4):
    machine = StateMachine(simple_machine)

    machine.transition(event)
    assert machine.state == event
    assert not machine.initial
    assert not machine.accepted

    assert machine.final
    assert machine.is_final(machine.state)

    with raises(StopMachine):
        machine.transition(event)


def test_transition_invalid_event(simple_machine):
    machine = StateMachine(simple_machine)

    with raises(ValueError):
        machine.transition(-1)


def test_transition_invalid_state(simple_machine, event=1):
    simple_machine["transition"] = lambda *_: -1
    machine = StateMachine(simple_machine)

    with raises(ValueError):
        machine.transition(event)


def test_reset(simple_machine, event=3):
    def transition(state, context, event):
        context["value"] = event
        return event

    simple_machine["transition"] = transition
    machine = StateMachine(simple_machine)

    machine.transition(event)
    assert machine.context == {"value": event}

    machine.reset()
    assert machine.initial
    assert machine.context == simple_machine.get("context", dict())


@fixture(scope="session")
def binary_multiples():
    """
    Return a state machine blueprint that accepts binary numbers that are
    multiples of 3.
    """
    def transition(state, context, event):
        """
        Trigger a transition to a new state by event and update context value.
        Shift the context value left 1 bit and add the event bit
        as the new least significant bit.
        Return the the modulus of the value by the divisor.
        """
        context["value"] = context["value"] << 1 ^ event
        return context["value"] % context["divisor"]

    return {
        "initialContext":  {"divisor": 3, "value": 0},
        "initialState": 0,
        "validStates": {0, 1, 2},
        "acceptedStates": {0},
        "finalStates": {},
        "alphabet": {0, 1},
        "transition": transition
    }


def test_machine(binary_multiples):
    results = list()

    for _ in range(100):
        machine = StateMachine(binary_multiples)
        result = 0

        while not machine.is_accepted(machine.state) \
                or not result or result in results:
            event = choice(list(machine.blueprint["alphabet"]))

            machine.transition(event)

            result = machine.context["value"]

        print(f"{machine}: {result:b} ({result})")
        assert result % machine.context["divisor"] == 0
        results.append(result)
