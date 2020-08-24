""" A colony of super-intelligent alien bio-engineers has landed on Earth and
    has created new species of farm animals. The aliens are performing their
    experiments on Earth and plan on transporting the mutant animals back to
    their home planet.
    In this problem set, you will implement algorithms to figure out how the aliens
    should shuttle their experimental animals back across space."""

from collections import OrderedDict
import time


def partitions(set_):  # partition function to help for solving problem
    if not set_:
        yield []
        return
    for i in range(2 ** len(set_) // 2):
        parts = [set(), set()]
        for item in set_:
            parts[i & 1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]] + b


def get_partitions(set_):  # get_partitions function to help for solving problem
    for partition in partitions(set_):
        yield [list(elt) for elt in partition]


""" PART A: Transporting cows across space """
""" Problem 1: Loading cow data
    File source: ps1_cow_data
    Parameters: file name (the name of the data file) as a string
    Returns: a dictionary of cow name (string), weight (int) pairs"""


def load_cows(filename):
    cows_dict = {}
    fin = open(filename, mode='r')
    for line in fin:
        cow_details = line.split(',')
        cows_dict[cow_details[0]] = int(cow_details[1].rstrip())
    fin.close()
    return cows_dict


# print('Problem 1: Loading cow data\n',
#       load_cows("ps1_cow_data.txt")) # to run function and print the return items
""" Problem 2: Greedy cow transport
    One way of transporting cows is to always pick the heaviest cow that will fit
    onto the spaceship first. This is an example of a Greedy algorithm.
    So, if there is only 2 tons of free space on your spaceship, with one cow
    that is 3 tons and another that is 1 ton, the 1 ton cow will still get put
    onto the spaceship.
    In this problem, uses a Greedy heuristic algorithm to determine an allocation of
    cows that attempts to minimize the number of spaceship trips needed to transport
    all the cows. The returned allocation of cows may or may not be optimal.
    The Greedy heuristic should follow the following method:
    1. As long as the current trip can fit another cow, add the largerst cow that
       will fit on the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows
    Does not mutate (modify) the given data of cows
    Parameter: cows -a dictionary of name (string), weight (int) pairs
               limit -weight limit of the spaceship (an int)
    Returns: a list of lists, with each inner list containing the names of cows that
             transported on a particular trip and the overall list containing all the trips"""


def greedy_cow_transport(cows, limit):
    trips = []
    cows_copy = cows.copy()  # create copy of dictionary
    cows_sorted = OrderedDict(sorted(cows_copy.items(), reverse=True,
                                     key=lambda x: x[1]))  # sort dictionary by each cows weight, descending
    list_index = 0
    while len(cows_sorted) > 0:  # keep iterating until all cows to a trip
        total_weight = 0
        trips.append([])
        for (cow, weight) in cows_sorted.copy().items():
            """ for each cow, check if its weight plus the current total weight
                is less than the limit, then add to a trip"""
            if total_weight + weight <= limit:
                trips[list_index].append(cow)
                total_weight += weight
                """ remove the cow from the sorted list to prevent re-carrying
                    in the next trips"""
                del cows_sorted[cow]
        list_index += 1
    print('The number of trips using Greedy algorithm:', list_index, 'trips')
    return trips


# list_of_cows01 = load_cows("ps1_cow_data.txt")
# greedy_cow_transport(list_of_cows01, 10)  # to run function
""" Problem 3: Brute-Force cow transport
    Another way to transport the cows is to look at every possible combination of
    trips and pick the best one. This is an example of a Brute-Force algorithm
    In this problem, finds the allocation of cows that minimize the number of spaceship
    trips via Brute-Force. The Brute-Force algorithm should follow the following method:
    1. Enumerate all possible ways that the cows can be divided into separate trips,
       use the given get_partitions function to help you
    2. Select the allocation that minimizes the number of trips without making any trip
       that does obey the weight limitation
    Does not mutate (modify) the given dictionary of cows.
    Parameter: cows -a dictionary of name (string), weight (int) pairs
               limit -weight limit of the spaceship (an int)
    Returns: a list of list, with each inner list containing the names of cows transported
             on a particular trip and the overall list containing all the trips"""


def brute_force_cow_transport(cows, limit):
    trips = []
    cows_copy = cows.copy()
    cows_sorted = OrderedDict(sorted(cows_copy.items(), reverse=True,
                                     key=lambda x: x[1]))
    cows_partitions = get_partitions(cows_sorted)
    for trip_combo in cows_partitions:
        allowable_trip = 0
        found_cows = []
        for item in trip_combo:
            trip_weight = 0
            successful_score = 0
            for cow in item:
                if trip_weight + cows_sorted[cow] <= limit and cow not in found_cows:
                    trip_weight = trip_weight + cows_sorted[cow]
                    successful_score += 1
                    found_cows.append(cow)
                else:
                    break
            if successful_score == len(item):
                allowable_trip += 1
        if allowable_trip == len(trip_combo):
            if item not in trips:
                trips.append(trip_combo)
    minLength = len(trips[0])
    minTrip = trips[0]
    for trip in trips:
        if len(trip) < minLength:
            minLength = len(trip)
            minTrip = trip
    print('The number of trips using Brute-Force algorithm:', len(minTrip), 'trips')
    return list(minTrip)


# list_of_the_cows02 = load_cows("ps1_cow_data.txt")
# brute_force_cow_transport(list_of_the_cows02, 10)
""" Problem 4: Comparing the cow transport algorithm
    Use the default weight limits of 10 both for Greedy algorithm and Brute-Force algorithm,
    print out the number of trips returned by each method and how long each method takes to
    run in seconds.
    Returns: does not return anything"""


def compare_cow_transport_algorithm():
    list_of_cows = load_cows('ps1_cow_data.txt')
    limit_of_trips = 10
    print('===Greedy algorithm===')
    start = time.time()
    greedy_cow_transport(list_of_cows, limit_of_trips)
    end = time.time()
    print(end-start, 'seconds\n')
    print('===Brute-Force algorithm===')
    start = time.time()
    brute_force_cow_transport(list_of_cows, limit_of_trips)
    end = time.time()
    print(end-start, 'seconds\n')


compare_cow_transport_algorithm()
""" Write-up
    From the program we know that the Greedy algorithm runs faster than
    Brute-Force algorithm. Greedy algorithm only need almost 0.0 seconds to runs,
    then Brute-Force algorithm need more than 2 seconds to runs.
    Yet, Brute-Force algorithm give more optimal solution than Greedy algorithm, which
    Greedy algorithm need 6 trips, and Brute-Force algorithm only need 5 trips."""
