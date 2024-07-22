import math
import random
import time
import cProfile
import heapq

H = 0.4


def random_initial_population(n, population_size):
    """
    Returns a randomly initialized population of a given size,
    which are just random permutations of the first given sequence of n numbers.
    :param n: number of jobs
    :param population_size: size of the random population to initialize
    :return: list of random permutation of jobs
    """
    starter_sequence = []
    for i in range(1, n + 1):
        starter_sequence.append(i)

    perms = []
    for _ in range(population_size):
        perm = starter_sequence[:]
        random.shuffle(perm)
        perms.append(perm)

    return perms


def fitness(p, a, b, sequence, due_date):
    """
    Evaluates a job sequence based on the tardiness and earliness penalties it would incur
    :param p: processing times of all jobs
    :param a: earliness penalties of all jobs
    :param b: tardiness penalties of all jobs
    :param sequence: sequence to be evaluated, string of numbers
    :return total_tardy: total tardiness penalty incurred
            total_early: total earliness penalty incurred
    """
    total_tardy = 0
    total_early = 0

    current_date = 0
    for job in sequence:
        current_date += p[job - 1]
        if current_date < due_date:
            total_early += a[job - 1]
        elif current_date > due_date:
            total_tardy += b[job - 1]

    return total_early, total_tardy


def one_point_merge(seq1, seq2):
    crossover_point = random.randint(0, len(seq1) - 1)

    all_jobs = set([i for i in range(1, len(seq1) + 1)])
    start_half = seq1[:crossover_point]
    back_half = seq2[crossover_point:]

    # Deal with incorrect sequences that overlap numbers
    shared_nums = set(start_half).intersection(set(back_half))
    back_doesnt_contain = all_jobs.difference(set(back_half))
    available = list(back_doesnt_contain.difference(set(start_half)))

    # Fix incorrect sequences through random replacement(mutation)
    for overlapped_num in shared_nums:
        index = back_half.index(overlapped_num)
        replacement = random.choice(available)
        back_half[index] = replacement
        available.remove(replacement)

    return start_half + back_half


def PMX(parent1, parent2):
    crossover_points = random.sample(range(len(parent1)), 2)
    crossover_points.sort()

    c1 = [0 for i in range(len(parent1))]
    c2 = [0 for i in range(len(parent1))]

    # Copy middle section to both children
    p1_middle = parent1[crossover_points[0]:crossover_points[1]]
    p2_middle = parent2[crossover_points[0]:crossover_points[1]]

    c1[crossover_points[0]:crossover_points[1]] = p1_middle
    c2[crossover_points[0]:crossover_points[1]] = p2_middle

    # Copy Left and Right section of p2 to c1, and resolve conflicts
    for chromosome_index in range(crossover_points[0]):
        replacement = parent2[chromosome_index]
        if replacement in p1_middle:
            index = p1_middle.index(replacement)
            replacement = p2_middle[index]
        c1[chromosome_index] = replacement

    for chromosome_index in range(crossover_points[1], len(parent2)):
        replacement = parent2[chromosome_index]
        if replacement in p1_middle:
            index = p1_middle.index(replacement)
            replacement = p2_middle[index]

        c1[chromosome_index] = replacement

    # Copy Left and Right section of p1 to c2, and resolve conflicts
    for chromosome_index in range(crossover_points[0]):
        replacement = parent1[chromosome_index]
        if replacement in p2_middle:
            index = p2_middle.index(replacement)
            replacement = p1_middle[index]
        c2[chromosome_index] = replacement

    for chromosome_index in range(crossover_points[1], len(parent1)):
        replacement = parent1[chromosome_index]
        if replacement in p2_middle:
            index = p2_middle.index(replacement)
            replacement = p1_middle[index]

        c2[chromosome_index] = replacement
    return [c1, c2]


def genetic_algorithm(p, a, b, due_date):
    # Hyperparameters
    # starting_size = int(math.factorial(len(p)) * 0.02)
    starting_size = 50000
    # top_k = int(starting_size * 0.25)
    top_k = 50
    number_of_generations = 500

    # Testing Parameters
    best_ranking = []

    # Create a random starter population
    population = random_initial_population(len(p), starting_size)
    print(f'Starting Population Size: {len(population)}')

    for _ in range(number_of_generations):

        if _ % 100 == 0:
            print(f'Generation {_}')

        early_rankings = []
        tardy_rankings = []
        test_rank = []

        for index in range(len(population)):
            individual = population[index]
            early_penalty, tardy_penalty = fitness(p, a, b, individual, due_date)

            # test_rank.append((early_penalty + tardy_penalty, individual))
            # early_rankings.append((early_penalty, index))
            # tardy_rankings.append((tardy_penalty, index))

            heapq.heappush(test_rank, ((early_penalty + tardy_penalty) * -1, individual))
            heapq.heappush(early_rankings, (early_penalty * -1, individual))
            heapq.heappush(tardy_rankings, (tardy_penalty * -1, individual))

        # early_rankings.sort()
        # tardy_rankings.sort()
        # test_rank.sort()

        best = heapq.heappop(test_rank)
        best_ranking.append((best[0] * -1, best[1]))

        # top_early = early_rankings[:top_k]
        # top_tardy = tardy_rankings[:top_k]

        top_early = heapq.nsmallest(top_k, early_rankings)
        top_tardy = heapq.nsmallest(top_k, tardy_rankings)

        next_gen = []
        for pair1 in top_early:
            # first_parent_seq = population[pair1[1]]
            for pair2 in top_tardy:
                # second_parent_seq = population[pair2[1]]
                # child = one_point_merge(first_parent_seq, second_parent_seq)
                # next_gen.append(child)
                children = PMX(pair1[1], pair2[1])
                next_gen += children

        population = next_gen

    lowest_penalty = 100000
    for item in best_ranking:
        if item[0] < lowest_penalty:
            lowest_penalty = item[0]

    return lowest_penalty


def test():
    p = [20, 6, 13, 13, 12, 12, 12, 3, 12, 13]
    a = [4, 1, 5, 2, 7, 9, 5, 6, 6, 10]
    b = [5, 15, 13, 13, 6, 8, 15, 1, 8, 1]

    due_date = math.floor(sum(p) * H)

    genetic_algorithm(p, a, b, due_date)
    return

def main():
    start = time.time()
    cProfile.run('test()')
    end = time.time()

    print(f'Time Elapsed: {end - start}')
    return


if __name__ == "__main__":
    main()
    # test()