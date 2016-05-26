import heapq as hq
from collections import defaultdict as dd


def describe_list(input_, input_length):
    """
        Print out list statistics.
    """

    assert input_length

    # getting max value using heap
    input_inverted = [-1*i for i in input_]

    hq.heapify(input_inverted)

    max_ = -1*input_inverted[0]

    del input_inverted

    # getting min value, same heap approach
    hq.heapify(input_)

    min_ = input_[0]

    print('Range is %s to %s' % (min_, max_))

    # print out missing numbers and counting duplicates
    previous = None
    duplicates = dd(lambda: 1)

    print('Missing Numbers:')

    while len(input_):
        current = hq.heappop(input_)

        # formally here is a nested loop,
        # but the complexity will still be O(length of the range of the input)
        if previous and current > previous + 1:
            for missing in range(previous+1, current):
                print("\t%s" % missing)

        # counting duplicates
        if current == previous:
            duplicates[current] += 1

        previous = current

    print('Duplicate Numbers:')

    for key, value in duplicates.items():
        print("\t%s appears %s times" % (key, value))

test = [3, 1, -5, 3, 3, -5, 0, 10, 1, 1]

describe_list(test, len(test))