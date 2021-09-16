from Counting.Question import Question


class GameState:
    remaining_pairs = []
    numbers_used = []
    next_states = []
    previous_states = []
    possible_questions = []
    all_question_sets_and_answers = []
    weight = None

    def __init__(self, premaining_pairs,
                 questions_and_answers=None):
        self.numbers_used = []
        self.previous_states = []
        self.remaining_pairs = premaining_pairs

        if questions_and_answers is None:
            self.all_question_sets_and_answers = [[[], []]]
        else:
            self.all_question_sets_and_answers = questions_and_answers

        for pair in self.remaining_pairs:
            for num in pair:
                if num not in self.numbers_used:
                    self.numbers_used.append(num)


    def __eq__(self, other: 'GameState'):
        for pair in self.remaining_pairs:
            if pair not in other.remaining_pairs:
                return False
        for pair in other.remaining_pairs:
            if pair not in self.remaining_pairs:
                return False
        return True

    def __str__(self):
        return str(self.remaining_pairs)

    def get_used_questions(self):
        used_questions = []
        for pair in self.all_question_sets_and_answers:
            for question in pair[0]:
                if question not in used_questions:
                    used_questions.append(question)
        return used_questions
