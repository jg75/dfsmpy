"""Deterministic, Finite State machine."""
import copy


class StopMachine(Exception):
    """StopMachine is raised when the state machine is in a final state."""
    pass


class StateMachine:
    """Deterministic, Finite State machine."""
    def __init__(self, blueprint):
        """Override."""
        self.blueprint = blueprint

    def __str__(self):
        """Override."""
        accepted = "OK" if self.accepted else "NO"

        return f"{self.state} ({accepted})"

    @property
    def blueprint(self):
        """Get the blueprint for the state machine."""
        return self.__blueprint

    @blueprint.setter
    def blueprint(self, blueprint):
        """
        Set the blueprint for the state machine and initial state.

        Raise ValueError if the initial state is invalid.
        """
        self.__blueprint = blueprint

        self.reset()

    def is_initial(self, state):
        """Return True if state is the initial state."""
        try:
            return state == self.blueprint["initialState"]
        except KeyError:
            return False

    def is_valid(self, state):
        """Return True if state is a valid state."""
        try:
            return state in self.blueprint["validStates"]
        except KeyError:
            return False

    def is_accepted(self, state):
        """Return True if state is an accepted state."""
        try:
            return state in self.blueprint["acceptedStates"]
        except KeyError:
            return False

    def is_final(self, state):
        """Return True if state is the final state."""
        try:
            return state in self.blueprint["finalStates"]
        except KeyError:
            return False

    def is_event(self, event):
        """Return True if the event is a valid event."""
        try:
            return event in self.blueprint["alphabet"]
        except KeyError:
            return False

    def reset(self):
        """
        Set the state machine to its initial state and context.

        Raise ValueError if the state is invalid.
        """
        state = self.blueprint.get("initialState")
        context = self.blueprint.get("initialContext", dict())

        if not self.is_initial(state):
            raise ValueError("Invalid state")

        self.set_state(state, context)

    def set_state(self, state, context):
        """
        set the state machine to a new state and context.

        Raise ValueError if the state is invalid.
        """
        if not self.is_valid(state):
            raise ValueError("Invalid state")

        self.state = state
        self.context = context
        self.initial = self.is_initial(self.state)
        self.accepted = self.is_accepted(self.state)
        self.final = self.is_final(self.state)

    def transition(self, event):
        """
        Transition to the next state by executing the transition function.

        Raise StopMachine if the current state is final or
        ValueError if event is not in alphabet or state is invalid.
        """
        if self.is_final(self.state):
            raise StopMachine()

        if not self.is_event(event):
            raise ValueError("Invalid event")

        function = self.blueprint.get("transition", lambda _, e: e)
        context = copy.deepcopy(self.context)
        state = function(context, event)

        self.set_state(state, context)
