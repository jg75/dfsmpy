# Deterministic, Finite State Machine

## Contents
* [Installation](#installation)
* [State Machine](#statemachine)
* [Usage](#usage)

---

## Installation

```
python setyp.py install
```

---

## StateMachine

### Members

* [blueprint](#blueprint)
* [state](#state)
* [context](#context)
* [accepted](#accepted)

#### blueprint

This is a propery with a getter and setter that defines the state machine.
Setting the blueprint will also reset the state machine.

```python
{
    "context": dict(),
    "alphabet": set(),
    "initialState": state,
    "validStates": set(),
    "acceptedStates": set(),
    "finalStates": set(),
    "transition": lambda context, event: state
}
```

##### Context

A dictionary, which can be used to share information between states and
updated during state transitions. Note that this is optional and won't
raise a KeyError if it's not a member of `blueprint`.

##### Alphabet

A set of events, which are used to drive state transitions.

##### Initial State

The starting state. Must be a valid state or a ValueError will be raised.

##### Valid States

A set of valid states.

##### Accepted States

A set of accepted states.

##### Final States

A set of final states, once reached, new transitions will raise `StopMachine`.

##### Transition

A function, which returns the next state. Must be a valid state or
a ValueError will be raised. This function will be called with context and
an event. The event must be a member of alphabet or a ValueError
will be raised.

#### state

The current state of the state machine.

#### context

The current context of the state machine.

#### accepted

True or False if the current state is an accepted state.

### Methods

#### reset()

Resets the state machine's state and context to their initial values defined
in the blueprint.

#### transition(event) -> blueprint.transition(context, event) -> state

Transitions the state machine to the next state by executing the transition
defined in the blueprint. The event must be a valid member of the alphabet
defined in the blueprint.

#### is_initial(state) -> True | False

#### is_valid(state) -> True | False

#### is_accepted(state) -> True | False

#### is_final(state) -> True | False

---

## Usage

Create a state machine with a blueprint and transition from the initial state
to accepted, final state `2`.

```python
from dfsmpy import StateMachine

machine = StateMachine({
    "alphabet": {1, 2},
    "initialState": 1,
    "validStates": {1, 2},
    "acceptedStates": {2},
    "finalStates": {2},
    "transition": lambda _, e: e
})

machine.transition(2)
```
