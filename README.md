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
* [initial](#initial)
* [accepted](#accepted)
* [final](#final)

#### blueprint

This is a propery with a getter and setter that defines the state machine.
Setting the blueprint will also reset the state machine.

```python
{
    "initialState": state,
    "initialContext": dict(),
    "alphabet": set(),
    "validStates": set(),
    "acceptedStates": set(),
    "finalStates": set(),
    "transition": lambda context, event: state
}
```

##### Initial Context

An optional dictionary, which can be used to share information between states and
updated during state transitions.

##### Alphabet

A set of events, which are used to drive state transitions.

##### Initial State

The starting state. Must be a valid state.

##### Valid States

A set of valid states.

##### Accepted States

A set of accepted states.

##### Final States

A set of final states, once reached, new transitions will raise `StopMachine`.

##### Transition

A function, which takes context and event as parameters and returns the next state.
The event must be a member of the alphabet and the state must be a valid state.

#### state

The current state of the state machine.

#### context

The current context of the state machine.

#### initial

True or False if the current state is the initial state.

#### accepted

True or False if the current state is an accepted state.

#### final

True or False if the current state is a final state.

### Methods

#### reset()

Resets the state machine's state and context to their initial values defined
in the blueprint. The initial state must be a valid state.

* `ValueError` - Invalid initial state

#### set_state(state, context)

Set the state machine's state and context. The state must be a valid state.

* `ValueError` - Invalid state

#### transition(event)

Transitions the state machine to the next state by executing the transition
defined in the blueprint. The event must be a valid member of the alphabet
defined in the blueprint. The state must be a valid state.

* `StopMachine` - Current state is final
* `ValueError` - Invalid event

#### is_initial(state) -> True | False

#### is_valid(state) -> True | False

#### is_accepted(state) -> True | False

#### is_final(state) -> True | False

#### is_event(event) -> True | False

---

## Usage

Create a state machine with a blueprint and transition
from the initial state `1` to accepted, final state `2`.

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
