"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor

codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """

    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score
    """
    items = [hand.count(item) * item for item in hand]
    return max(items)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    # generating all sequences
    sequences = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)

    # alla scores
    total_scores = 0.0
    for seq in sequences:
        new_seq = seq + held_dice
        total_scores += score(new_seq)

        # expected value
    exp_value = total_scores / len(sequences)
    return exp_value


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    ans = []
    temp_ans1 = []
    temp_ans1.append(tuple())

    for dice in hand:
        temp_ans2 = list(temp_ans1)
        for seq in temp_ans1:
            temp_seq = list(seq)
            temp_seq.append(dice)
            temp_ans2.append(tuple(temp_seq))
        temp_ans1 = temp_ans2
        ans.extend(tuple(sorted(temp_ans2)))

    return set(sorted(ans))


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    ans = 0
    ans_hand = tuple()
    all_holds = gen_all_holds(hand)
    for hold in all_holds:
        free_dice = len(hand) - len(hold)
        exp_val = expected_value(hold, num_die_sides, free_dice)
        if (exp_val > ans):
            ans = exp_val
            ans_hand = hold
    return (ans, ans_hand)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print
    "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


run_example()

