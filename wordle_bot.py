from collections import defaultdict
from util import arg_timer, timer
import random

with open("answers.txt", "r") as f:
    answers = f.read().split()
with open("vocabulary.txt", "r") as f:
    vocabulary = f.read().split()

def hash(guess, target):
    """Tri-bit encoding: green = 0, yellow = 1, grey = 2"""
    hash = 0
    for c1, c2 in zip(guess, target):
        hash *= 3
        if c1 == c2:
            hash += 0
        elif c1 in target:
            hash += 1
        else:
            hash += 2
    return hash

def outcome_sets(guess, vocab):
    res = defaultdict(set)
    for target in vocab:
        res[hash(guess, target)].add(target)
    return res

def outcome_sizes(guess, vocab):
    res = [0] * 243
    for target in vocab:
        res[hash(guess, target)] += 1
    return res


def score(guess, vocab):
    sets = outcome_sizes(guess, vocab)
    return sum(sz for sz in sets) / sum(1 for sz in sets if sz != 0)

def verbose_solve(target):
    print("Playing wordle", target)

    remaining_answers = answers
    attempts = 0
    while True:
        attempts += 1
        if attempts == 1:
            guess = "salet"
        elif len(remaining_answers) == 1:
            guess = remaining_answers.pop()
        else:
            guess = min(vocabulary, key=lambda gss: score(gss, remaining_answers))
        print(" - Guessing:", guess)
        if guess == target:
            print("Correct in", attempts)
            break
        sets = outcome_sets(guess, remaining_answers)
        remaining_answers = sets[hash(guess, target)]

@arg_timer
def solve(target):
    remaining_answers = answers
    attempts = 0
    while True:
        attempts += 1
        if attempts == 1:
            guess = "salet"
        elif len(remaining_answers) == 1:
            guess = remaining_answers.pop()
        else:
            guess = min(vocabulary, key=lambda gss: score(gss, remaining_answers))
        if guess == target:
            return attempts
        sets = outcome_sets(guess, remaining_answers)
        remaining_answers = sets[hash(guess, target)]

@timer
def solve_all():
    attempts = {}
    for ans in random.sample(answers, 10):
        attempts[ans] = solve(ans)
    return attempts

attempts = solve_all()

print()
print("Average attempts:", sum(attempts.values()) / len(attempts))
mn = min(attempts, key=lambda x: attempts[x])
print("Min attempts:", mn, attempts[mn])
mx = max(attempts, key=lambda x: attempts[x])
print("Max attempts:", mx, attempts[mx])