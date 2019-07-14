from random import choice
from unittest.mock import create_autospec

from pytest import fixture, raises

from dfsmpy import StateMachine, StopMachine


@fixture(scope="function")
def simple_machine():
    return {
        "initialState": 1,
        "validStates": {1, 2, 3, 4},
        "acceptedStates": {3},
        "finalStates": {4},
        "alphabet": {1, 2, 3, 4},
        "transition": lambda _, s: s
    }


def test_blueprint(simple_machine):
    machine = StateMachine(simple_machine)

    assert machine.blueprint["initialState"] == simple_machine.get("initialState")
    assert machine.blueprint["initialContext"] == simple_machine.get("initialContext", {})
    assert machine.blueprint["alphabet"] == simple_machine["alphabet"]

    for state in simple_machine["validStates"]:
        assert machine.is_valid(state)

    for state in simple_machine["acceptedStates"]:
        assert machine.is_accepted(state)

    for state in simple_machine["finalStates"]:
        assert machine.is_final(state)

    assert machine.is_initial(machine.state)
    assert not machine.is_accepted(machine.state)
    assert not machine.is_final(machine.state)
    assert machine.context == machine.blueprint["initialContext"]
    assert not machine.accepted


def test_blueprint_invalid_initial_state(simple_machine):
    simple_machine["initialState"] = -1

    with raises(ValueError):
        StateMachine(simple_machine)


def test_transition_function(simple_machine, event=1):
    mock_transition = create_autospec(simple_machine["transition"])
    mock_transition.return_value = event
    simple_machine["transition"] = mock_transition
    machine = StateMachine(simple_machine)

    machine.transition(event)
    mock_transition.assert_called_once_with(machine.context, event)


def test_transition_context(simple_machine, event=2):
    def transition(context, event):
        context["value"] = event
        return event

    simple_machine["transition"] = transition
    machine = StateMachine(simple_machine)

    assert machine.context == simple_machine.get("context", {})

    machine.transition(event)

    assert machine.state == event
    assert not machine.accepted
    assert machine.context["value"] == event


def test_transition_accepted(simple_machine, event=3):
    machine = StateMachine(simple_machine)

    machine.transition(event)
    assert machine.state == event
    assert machine.accepted


def test_transition_final_state(simple_machine, event=4):
    machine = StateMachine(simple_machine)

    machine.transition(event)
    assert machine.state == event
    assert not machine.accepted

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
    def transition(context, event):
        context["value"] = event
        return event

    simple_machine["transition"] = transition
    machine = StateMachine(simple_machine)

    machine.transition(event)
    assert machine.context == {"value": event}

    machine.reset()
    assert machine.is_initial(machine.state)
    assert machine.context == machine.blueprint["initialContext"]


@fixture(scope="session")
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
        "initialContext":  {"divisor": 3, "value": 0, "results": list()},
        "initialState": 0,
        "validStates": {0, 1, 2},
        "acceptedStates": {0},
        "finalStates": {},
        "alphabet": {0, 1},
        "transition": transition
    }


def test_machine(binary_multiples):
    print(f"\n{binary_multiples}")

    for _ in range(100):
        machine = StateMachine(binary_multiples)
        result = 0

        while not machine.is_accepted(machine.state) \
                or not result \
                or result in machine.context["results"]:
            event = choice(list(machine.blueprint["alphabet"]))

            machine.transition(event)

            result = machine.context["value"]

        print(f"{machine}: {result:b} ({result})")
        assert result % machine.context["divisor"] == 0
        machine.context["results"].append(result)
