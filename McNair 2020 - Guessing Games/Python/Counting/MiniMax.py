from Counting.GameState import GameState
from Counting.Question import Question
from itertools import chain, combinations
import copy
from Counting.AllPossibilities import *


def find_max_depth_answer(pquestion: Question):
    pass


def find_min_depth_question(pstate: GameState):
    minimum_weight = min(q.weight for q in pstate.possible_questions)
    minimum_weight_question = []
    for question in pstate.possible_questions:
        if question.weight == minimum_weight:
            minimum_weight_question = question
    return minimum_weight_question



