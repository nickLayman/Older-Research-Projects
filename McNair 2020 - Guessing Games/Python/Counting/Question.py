class Question:
    question = []
    weight = 0
    previous_state = None
    possible_states = []

    def __init__(self, pquestion, pweight=0, pprevious_state=None,
                 ppossible_states=None):
        self.question = pquestion
        self.weight = pweight

        if ppossible_states is None:
            self.possible_states = []
        else:
            self.possible_states = ppossible_states

    def __eq__(self, other: 'Question'):
        return self.question == other.question

    def __str__(self):
        return str(self.question)