from Counting.GameState import GameState
from itertools import chain, combinations
import copy


# TODO: save off all calculated games of unique min_question_size
#  to reduce computation time


def allpairs(num):
    """
    Returns all distinct unordered pairs of integers from 1 to num.

    This method is primarily used for calculating the remaining pairs at
    the beginning of a game. Remaining pairs of subsequent game states are
    found as subsets from this list.

    :param num: maximum number of the set
    :return: all distinct unordered pairs from 1 to num
    """
    pairs = []
    for num1 in range(1, num):
        for num2 in range(num1 + 1, num + 1):
            pairs.append([num1, num2])
    return pairs


def powerset(iterable):
    """
    Returns as tuples the power set of iterable.

    This method has been modified to exclude the empty set and the parent set.

    powerset([1,2,3]) --> (1,) (2,) (3,) (1,2) (1,3) (2,3)

    :param iterable: the parent set to create subsets from
    :return: all subsets of iterable, as tuples
    """
    s = list(iterable)
    return (list(t) for t in
            chain.from_iterable(combinations(s, r) for r in range(1, len(s))))


def answer_zero(state: GameState, question) -> GameState:
    """
    Takes in a game state and a question set, returns the set for if the answer
    to the question is 0.

    Removes all remaining pairs which contain either 1 number from the
    question set or 2 numbers from the question set. Keeps remaining pairs that
    contain exactly 0 numbers from the question set.

    :param state: the state of the game before the question is asked
    :param question: the question set being asked about
    :return: the next state of the game if the answer to question is 0
    """
    temp_pairs = state.remaining_pairs.copy()
    saved_pairs = []
    for pair in temp_pairs:
        if not ((pair[0] in question) or (pair[1] in question)):
            saved_pairs.append(pair)
    new_questions_and_answers = []
    for pair in copy.deepcopy(state.all_question_sets_and_answers):
        temp = pair.copy()
        temp[0].append(question)
        temp[1].append(0)
        new_questions_and_answers.append(temp)
    next_state = GameState(saved_pairs,
                           questions_and_answers=new_questions_and_answers)
    return next_state


def answer_one(state: GameState, question) -> GameState:
    """
    Takes in a game state and a question set, returns the set for if the answer
    to the question is 1.

    Removes all remaining pairs which contain either no numbers from the
    question set or 2 numbers from the question set. Keeps remaining pairs that
    contain exactly 1 number from the question set.

    :param state: the state of the game before the question is asked
    :param question: the question set being asked about
    :return: the next state of the game if the answer to question is 1
    """
    temp_pairs = state.remaining_pairs.copy()
    saved_pairs = []
    for pair in temp_pairs:
        if not ((pair[0] in question) == (pair[1] in question)):
            saved_pairs.append(pair)
    new_questions_and_answers = []
    for pair in copy.deepcopy(state.all_question_sets_and_answers):
        temp = pair.copy()
        temp[0].append(question)
        temp[1].append(1)
        new_questions_and_answers.append(temp)
    next_state = GameState(saved_pairs,
                           questions_and_answers=new_questions_and_answers)
    return next_state


def answer_two(state: GameState, question) -> GameState:
    """
    Takes in a game state and a question set, returns the set for if the answer
    to the question is 2.

    Removes all remaining pairs which contain either no numbers from the
    question set or 1 number from the question set. Keeps remaining pairs that
    contain exactly 2 numbers from the question set.

    :param state: the state of the game before the question is asked
    :param question: the question set being asked about
    :return: the next state of the game if the answer to question is 2
    """
    temp_pairs = state.remaining_pairs.copy()
    saved_pairs = []
    for pair in temp_pairs:
        if (pair[0] in question) and (pair[1] in question):
            saved_pairs.append(pair)
    new_questions_and_answers = []
    for pair in copy.deepcopy(state.all_question_sets_and_answers):
        temp = pair.copy()
        temp[0].append(question)
        temp[1].append(2)
        new_questions_and_answers.append(temp)
    next_state = GameState(saved_pairs,
                           questions_and_answers=new_questions_and_answers)
    return next_state


def answer_most_pairs(state: GameState, question) -> GameState:
    """
    Takes in a game state and a question set, returns the game state which
    has the most remaining pairs.
    :param state: the state of the game before the question is asked
    :param question: the question set being asked about
    :return: the next state of the game that maximizes remaining pairs
    """
    z = answer_zero(state, question)
    o = answer_one(state, question)
    t = answer_two(state, question)
    next_state = z
    if o.remaining_pairs > next_state.remaining_pairs:
        next_state = o
    if t.remaining_pairs > next_state.remaining_pairs:
        next_state = t
    return next_state


def find_next_states(state: GameState, min_question_size):
    """
    Takes in a game state and a minimum question size and makes a list
    of all possible next game states where the question to arrive there
    involved at least minimum_question_size numbers.

    This function uses powerset to find all possible questions, asks the ones
    that are at least minimum_question_size large, and only keeps the next
    states that reduce the number of possibilities. This ensures that the same
    questions are not asked in an infinite loop. The next states are added
    directly to state.next_states and not returned.

    :param state: the state of the game for which we want all next states
    :param min_question_size: the questions asked will involve at least this
    many numbers
    :return: none, just changes state.next_states
    """
    state.next_states = []

    # asks every possible question of a certain size
    for question in powerset(state.numbers_used):
        # only adds states coming from unique questions
        if question not in state.get_used_questions():
            if len(question) >= min_question_size:
                # finds all next states by answering 0, 1, and 2
                # next state if answer to question is 0
                z = answer_zero(state, question)  # z -> zero
                # only adds unique next states
                if z not in state.next_states:
                    # only adds states that reduce the number of pairs
                    # increasing is impossible, this prevents an infinite loop
                    # of having itself as a next state
                    if len(z.remaining_pairs) < len(state.remaining_pairs):
                        state.next_states.append(z)

                # next state if answer to question is 1
                o = answer_one(state, question)  # o -> one
                if o not in state.next_states:
                    if len(o.remaining_pairs) < len(state.remaining_pairs):
                        state.next_states.append(o)

                # next state if answer to question is 2
                t = answer_two(state, question)  # t -> two
                if t not in state.next_states:
                    if len(t.remaining_pairs) < len(state.remaining_pairs):
                        state.next_states.append(t)

    # additional check to ensure state.next_states does not contain state
    if state in state.next_states:
        state.next_states.remove(state)


def first_state(starting_size) -> GameState:
    """
    Creates the starting state of a game of size starting_size

    :param starting_size: size of original game set
    :return: the starting GameState with all pairs possible
    """
    return GameState(allpairs(starting_size))


def is_leaf(state: GameState) -> bool:
    """
    Takes in a game state and returns whether that state is a leaf of the tree.

    :param state: the GameState being checked for its leafiness
    :return: whether state is a leaf (has exactly 1 possible pair)
    """
    return len(state.remaining_pairs) == 1


def find_all_previous_states(ptree):
    """
    Takes a tree of GameStates and for each node, i, finds each node, j, where
    i is a next_state of j and adds j to previous_states of i

    :param ptree: the tree whose nodes are being updated
    :return: none, directly updates the GameState instance variables
    """
    for top in ptree:
        for bottom in top.next_states:
            if top not in bottom.previous_states:
                bottom.previous_states.append(top)


def make_full_tree(size, min_question_size, condensed=True):
    """
    Creates a tree structure which contains all possible games that could be
    played.

    Begins with the first state of a given size, asks all possible questions
    of at least minimum size, and does not create duplicate states. If a state
    is repeated, the question sets are combined.

    :param size: starting size of the game
    :param min_question_size: all questions must be at least this large
    :param condensed: whether the tree should save on memory by combining
    equivalent states to one object
    :return: the starting game state and the entire tree (list)
    """
    start = first_state(size)
    tree = [start]
    # loops until all games have reached a leaf or empty set
    while True:
        done = True
        for state in tree:
            # if the next states have not been calculated yet
            # and state is not a leaf or an empty set
            if len(state.next_states) == 0 and len(state.remaining_pairs) > 1:
                # if reached, new states will be calculated which should be
                # checked, so loop again
                done = False
                find_next_states(state, min_question_size)
                for s in state.next_states:
                    if condensed:
                        for t in tree:
                            if s == t:
                                # if state's next state is already in the tree,
                                # add the questions that it took to reach s
                                # to t's questions but dont add s
                                for pair in s.all_question_sets_and_answers:
                                    t.all_question_sets_and_answers.append(pair)
                                s = t
                        # if the next state is brand new, add it and check it in
                        # the next loop
                        if s not in tree:
                            tree.append(s)
                    else:
                        tree.append(s)
        if done:
            # if no new states were added or calculated in this loop,
            # exit the loop
            break
    find_all_previous_states(tree)
    return start, tree


def find_all_leaves(size, min_question_size, condensed=True):
    """
    Takes in a game starting size and minimum question size, returns all
    leaf GameStates from those games with questions to reach them calculated.

    :param size: game starting size
    :param min_question_size: minimum question size for every question
    :param condensed: whether the tree saved on memory by combining
    equivalent states to one object
    :return: a list containing all leaf GameStates from every possible game.
    These leaves contain the questions asked to reach them
    """
    start, tree = make_full_tree(size, min_question_size, condensed)
    leaves = []
    # checks every state in the tree for its leafiness
    for candidate in tree:
        if is_leaf(candidate):
            leaves.append(candidate)
    return leaves


if __name__ == '__main__':
    start_size = 3
    minimum_question_size = 1
    condense = True
    start, tree = make_full_tree(start_size, minimum_question_size, condense)
