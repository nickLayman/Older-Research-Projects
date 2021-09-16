import math

"""
This script finds the number of questions it takes to reach
a single remaining pair if the devils heuristic is used and
questions of 1/3 are used
"""


def ask_answer_largest(pairs, question):
    # favors an answer of 1 if sizes are equal
    largest_set = ask_answer_zero(pairs, question)
    largest_answer = 0
    if len(ask_answer_one(pairs, question)) >= len(largest_set):
        largest_set = ask_answer_one(pairs, question)
        largest_answer = 1
    if len(ask_answer_two(pairs, question)) > len(largest_set):
        largest_set = ask_answer_two(pairs, question)
        largest_answer = 2
    return largest_set, largest_answer


def ask_answer_zero(ppairs, pquestion):
    return_pairs = []
    for pair in ppairs:
        if pair[0] not in pquestion and pair[1] not in pquestion:
            return_pairs.append(pair)
    return return_pairs


def ask_answer_one(ppairs, pquestion):
    return_pairs = []
    for pair in ppairs:
        if pair[0] in pquestion and pair[1] not in pquestion:
            return_pairs.append(pair)
        if pair[0] not in pquestion and pair[1] in pquestion:
            return_pairs.append(pair)
    return return_pairs


def ask_answer_two(ppairs, pquestion):
    return_pairs = []
    for pair in ppairs:
        if pair[0] in pquestion and pair[1] in pquestion:
            return_pairs.append(pair)
    return return_pairs


def find_disjoint_components(ppairs):
    unknown_pairs = ppairs.copy()
    components = []
    while unknown_pairs:
        new_component = [unknown_pairs[0]]
        unchecked_pairs = [unknown_pairs[0]]
        while unchecked_pairs:
            remove_pairs = []
            for pair in unchecked_pairs:
                remove_pairs.append(pair)
                curr_pair = [pair[0] + 1, pair[1]]
                if curr_pair in ppairs and curr_pair not in new_component:
                    new_component.append(curr_pair)
                    unchecked_pairs.append(curr_pair)
                curr_pair = [pair[0], pair[1] + 1]
                if curr_pair in ppairs and curr_pair not in new_component:
                    new_component.append(curr_pair)
                    unchecked_pairs.append(curr_pair)
                curr_pair = [pair[0] - 1, pair[1]]
                if curr_pair in ppairs and curr_pair not in new_component:
                    new_component.append(curr_pair)
                    unchecked_pairs.append(curr_pair)
                curr_pair = [pair[0], pair[1] - 1]
                if curr_pair in ppairs and curr_pair not in new_component:
                    new_component.append(curr_pair)
                    unchecked_pairs.append(curr_pair)
            for pair in remove_pairs:
                unchecked_pairs.remove(pair)
                unknown_pairs.remove(pair)
        components.append(new_component)
    return components


def find_horizontal_range(pcomponent):
    # assumes a single connected component
    hrange = []
    for num in range(min(pair[0] for pair in pcomponent),
                     max(pair[0] for pair in pcomponent) + 1):
        hrange.append(num)
    return hrange


def find_vertical_range(pcomponent):
    # assumes a single connected component
    vrange = []
    for num in range(min(pair[1] for pair in pcomponent),
                     max(pair[1] for pair in pcomponent) + 1):
        vrange.append(num)
    return vrange


def find_first_best_question(component):
    # assumes a single connected component
    # "best" -> minimizes maximum area region
    # finds the first question which produces the smallest largest region
    # if a subsequent question produces the same size smallest largest region,
    # and the subsequent one produces it with an answer of 1 while the previous
    # one produces it with an answer of 0 or 2, this method prioritizes
    # the one with an answer of 1
    best_question = []
    smallest_largest_region, max_answer = ask_answer_largest(component,
                                                             best_question)
    hrange = find_horizontal_range(component)
    vrange = find_vertical_range(component)
    for hval in range(len(hrange)):
        for vval in range(len(vrange)):
            current_question = hrange[:hval] + vrange[:vval]
            current_largest_region, current_max_answer = ask_answer_largest(
                component, current_question)
            if len(current_largest_region) == len(smallest_largest_region):
                if current_max_answer == 1 and max_answer != 1:
                    best_question = current_question
                    smallest_largest_region, max_answer = current_largest_region, current_max_answer
            elif len(current_largest_region) < len(smallest_largest_region):
                best_question = current_question
                smallest_largest_region, max_answer = current_largest_region, current_max_answer
    return best_question


def find_first_thirds_question(psize):
    question = []
    for num in range(math.ceil(psize / 3)):
        question.append(num)
    return question


def find_thirds_question(component):
    hrange = find_horizontal_range(component)
    vrange = find_vertical_range(component)
    return hrange[:math.ceil(len(hrange) / 3)] + vrange[
                                                 :math.ceil(len(vrange) / 3)]


def find_first_halves_question(psize):
    question = []
    for num in range(math.ceil(psize / 2)):
        question.append(num)
    return question


def find_halves_question(component):
    hrange = find_horizontal_range(component)
    vrange = find_vertical_range(component)
    return hrange[:math.ceil(len(hrange) / 2)] + vrange[
                                                 :math.ceil(len(vrange) / 2)]


def are_all_singletons(pairs):
    for component in find_disjoint_components(pairs):
        if len(find_horizontal_range(component)) > 1:
            return False
        if len(find_vertical_range(component)) > 1:
            return False
    return True


def questions_until_singletons(ppairs):
    pairs = ppairs
    num_questions = 0
    questions = []
    while not are_all_singletons(pairs):
        new_pairs = []
        for component in find_disjoint_components(pairs):
            best_question = find_first_best_question(component)
            questions.append(best_question)
            new_pairs += ask_answer_largest(component, best_question)[0]
        num_questions += 1
        pairs = new_pairs
    return num_questions, pairs, questions


def thirds_until_singletons(ppairs):
    pairs = ppairs
    num_questions = 0
    questions = []
    new_pairs = []
    third_question = find_first_thirds_question(
        len(find_horizontal_range(pairs)) + 1)
    new_pairs += ask_answer_one(pairs, third_question)
    pairs = new_pairs
    num_questions += 1
    questions.append(third_question)
    while not are_all_singletons(pairs):
        new_pairs = []
        question = []
        for component in find_disjoint_components(pairs):
            thirds_question = find_thirds_question(component)
            question += thirds_question
            new_pairs += ask_answer_largest(component, thirds_question)[0]
        questions.append(question)
        num_questions += 1
        pairs = new_pairs
    return num_questions, pairs, questions


def halves_until_singletons(ppairs):
    pairs = ppairs
    num_questions = 0
    questions = []
    new_pairs = []
    half_question = find_first_halves_question(len(find_horizontal_range(pairs)) + 1)
    new_pairs += ask_answer_one(pairs, half_question)
    pairs = new_pairs
    num_questions += 1
    questions.append(half_question)
    while not are_all_singletons(pairs):
        new_pairs = []
        question = []
        for component in find_disjoint_components(pairs):
            halves_question = find_halves_question(component)
            question += halves_question
            new_pairs += ask_answer_largest(component, halves_question)[0]
        questions.append(question)
        num_questions += 1
        pairs = new_pairs
    return num_questions, pairs, questions


def make_starting_space(psize):
    pairs = []
    for smaller in range(psize - 1):
        for larger in range(smaller + 1, psize):
            pairs.append([larger, smaller])
    return pairs


for n in range(3, 50):
    # print(find_thirds_question(make_starting_space(n)))
    num_questions, singletons, questions = halves_until_singletons(
        make_starting_space(n))
    total_num_questions = num_questions + math.ceil(
        math.log(len(singletons), 3))
    print(f"{n}: {total_num_questions} from {len(singletons)} singletons")
#
# for n in range(3, 21):
#     num_questions, singletons, questions = halves_until_singletons(
#         make_starting_space(n))
#     total_num_questions = num_questions + math.ceil(
#         math.log(len(singletons), 3))
#     print(f"{n}: {total_num_questions}")

