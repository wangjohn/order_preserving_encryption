# Test code to check that if you have a sequence of n random numbers [0,1], then
# the n+1st number you draw has equal likelihood of being any rank.

import random
import matplotlib.pyplot as plt

def generate_sequence(n):
    sequence = []
    for i in xrange(n):
        sequence.append(random.random())
    return sequence

def find_rank(x, sequence):
    rank = 0
    for i in sequence:
        if i < x:
            rank += 1
    return rank

def test_rank_of_last(n):
    sequence = generate_sequence(n)
    x = random.random()

    return find_rank(x, sequence)

def test_distribution(num_trials, sequence_length):
    rank_dist = {}
    for i in xrange(num_trials):
        rank = test_rank_of_last(sequence_length)
        frequency = rank_dist.get(rank, 0)
        rank_dist[rank] = frequency + 1

    # flatten the dictionary
    expected_value = (num_trials * 1.0 / sequence_length)
    ranks = [rank_dist.get(i, 0) for i in xrange(sequence_length)]
    difference_from_expected = [abs(rank_dist.get(i, 0) - expected_value) / expected_value for i in xrange(sequence_length)]

    return sum(difference_from_expected) / len(difference_from_expected)

if __name__ == '__main__':
    test_trials = [5000000] #, 5000, 10000, 50000, 100000, 200000, 500000]
    sequence_lengths = [10, 20, 50, 100, 200, 500]
    for trials in test_trials:
        row = [trials]
        for length in sequence_lengths:
            row.append(test_distribution(trials, length))

        print ' & '.join([str(i) for i in row])
