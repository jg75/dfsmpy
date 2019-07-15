from unittest.mock import create_autospec

from pytest import fixture

from dfsmpy import StateMachine


@fixture(scope="function")
def lifecycle_machine():
    def before_any(state, context, event):
        context[f"before_{event}"] = state

    def after_accepted(state, context, event):
        context[f"after_accepted"] = state

    def after_three(state, context, event):
        context[f"after_{event}"] = state

    return {
        "initialState": 1,
        "validStates": {1, 2, 3, 4},
        "acceptedStates": {3},
        "finalStates": {4},
        "alphabet": {1, 2, 3, 4},
        "lifecycles": {
            "before": [{
                "events": {1, 2, 3, 4},
                "actions": [before_any]
            }],
            "after": [{
                "events": {3},
                "actions": [after_accepted, after_three]
            }]
        }
    }


def test_lifecycles_context(lifecycle_machine):
    machine = StateMachine(lifecycle_machine)

    for event in range(2, 5):
        state = machine.state

        machine.transition(event)
        assert machine.context[f"before_{event}"] == state

        if event == 3:
            assert machine.context[f"after_accepted"] == machine.state
            assert machine.context[f"after_{event}"] == machine.state

    machine.reset()
    assert machine.context == {}


def test_lifecycles_called(lifecycle_machine):
    machine = StateMachine(lifecycle_machine)
    lifecycles = machine.blueprint["lifecycles"]

    before_any = lifecycles["before"][0]["actions"][0]
    mock_before_any = create_autospec(before_any)
    lifecycles["before"][0]["actions"][0] = mock_before_any

    after_accepted = lifecycles["after"][0]["actions"][0]
    mock_after_accepted = create_autospec(after_accepted)
    lifecycles["after"][0]["actions"][0] = mock_after_accepted

    after_three = lifecycles["after"][0]["actions"][1]
    mock_after_three = create_autospec(after_three)
    lifecycles["after"][0]["actions"][1] = mock_after_three

    for event in range(2, 5):
        machine.transition(event)

        if event == 3:
            mock_after_accepted.assert_called_once()
            mock_after_accepted.assert_called_once()

    assert mock_before_any.call_count == 3
    assert mock_after_accepted.call_count == 1
    assert mock_after_three.call_count == 1
