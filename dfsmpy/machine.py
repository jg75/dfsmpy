"""State machine."""
import copy


class StopMachine(Exception):
    """StopMachine is raised when the state machine is in a final state."""
    pass


class StateMachine:
    """
    StateMachine:
    A deterministic, finite state machine.

    Blueprint:
    {
        "context": {dict},
        "alphabet": {set},
        "initialState": state,
        "validStates": {set},
        "acceptedStates": {set},
        "finalStates": {set},
        "transition": function(context, event) -> state
    }

    Context:
    A dictionary, which can be modified during state transition.

    Alphabet:
    A set of events, which are used to drive state transitions.

    Initial State:
    The starting state.

    Valid States:
    A set of valid states.

    Accepted States:
    A set of accepted states.

    Final States:
    A set of final states, which raise StopMachine if a transition made from.

    Transition:
    A function, which returns the next state.
    """

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
        if blueprint["initialState"] not in blueprint["validStates"]:
            raise ValueError("Invalid state")

        if not blueprint.get("context"):
            blueprint["context"] = dict()

        self.__blueprint = blueprint

        self.reset()

    def reset(self):
        """Set the state machine to its initial state and context."""
        self.state = self.blueprint["initialState"]
        self.context = self.blueprint["context"]
        self.accepted = self.is_accepted(self.state)

    def is_valid(self, state):
        """Return True if state is a valid state."""
        return state in self.blueprint["validStates"]

    def is_initial(self, state):
        """Return True if state is the initial state."""
        return state == self.blueprint["initialState"]

    def is_final(self, state):
        """Return True if state is the final state."""
        return state in self.blueprint["finalStates"]

    def is_accepted(self, state):
        """Return True if state is an accepted state."""
        return state in self.blueprint["acceptedStates"]

    def transition(self, event):
        """
        Transition to the next state by executing the transition function.

        Raise StopMachine if the current state is final or
        ValueError if event is not in alphabet or state is invalid.
        """
        if self.is_final(self.state):
            raise StopMachine()

        if event not in self.blueprint["alphabet"]:
            raise ValueError("Invalid event")

        function = self.blueprint["transition"]
        context = copy.deepcopy(self.context)
        state = function(context, event)

        if not self.is_valid(state):
            raise ValueError("Invalid state")

        self.state = state
        self.context = context
        self.accepted = self.is_accepted(self.state)


if __name__ == "__main__":
    machine = StateMachine({
        "alphabet": {1, 2},
        "initialState": 1,
        "validStates": {1, 2},
        "acceptedStates": {2},
        "finalStates": {2},
        "transition": lambda _, e: e
    })
