import math
import matplotlib.pyplot as plt
from genetic import genetic_algorithm

H = 0.4


def read_problem_file(f_name):
    """
    Reads an instance of the problem from the given file.
    file is expected to be in the format:

    number of problems (k)
    for each problem in turn:
       number of jobs (n)
       for each job i (i=1,...,n) in turn:
          p(i), a(i), b(i)

    :param f_name: file name to read problem instance from
    :return: problems: a dictionary mapping the current k to its n, processing times, and penalties
             k: number of problems contained in the file
    """
    file = open(f_name, 'r')
    lines = file.readlines()
    file.close()

    k = int(lines[0])
    problems = {}
    index = 1
    current_k = 1
    while index < len(lines):
        n = int(lines[index])  # Getting n from file
        problem = [n]
        index += 1

        processing = []
        earliness = []
        tardiness = []

        for _ in range(n):
            p, a, b = map(int, lines[index].split())
            index += 1

            processing.append(p)
            earliness.append(a)
            tardiness.append(b)

        problem.append(processing)
        problem.append(earliness)
        problem.append(tardiness)

        problems[current_k] = problem
        current_k += 1

    return problems, k


def solve_most_possible(p, a, b):
    jobs = []
    for i in range(len(p)):
        jobs.append((p[i], a[i], b[i]))

    jobs.sort()
    return jobs


def solve_late_first(p, a, b):
    """"
    Attempt to avoid largest late penalties
    """
    jobs = []
    for i in range(len(p)):
        jobs.append((b[i], p[i], a[i], i))

    # Get highest late penalty at start
    jobs.sort()
    jobs.reverse()

    final_order = []
    for job in jobs:
        index = job[3]
        final_order.append((p[index], a[index], b[index]))

    return final_order


def solve_early_first(p, a, b):
    """
    Goal is to avoid large early penalties
    """
    jobs = []
    for i in range(len(p)):
        jobs.append((a[i], p[i], b[i], i))

    jobs.sort()
    final_order = []
    for job in jobs:
        index = job[3]
        final_order.append((p[index], a[index], b[index]))

    return final_order


def get_penalty(jobs, due_date):
    total_penalty = 0
    date = 0
    for job in jobs:
        date += job[0]
        if date < due_date:
            total_penalty += job[1]  # Early penalty
        elif date > due_date:
            total_penalty += job[2]  # Late Penalty
    return total_penalty


def plot_results(times, names, problem_number):
    num_lines = len(times)

    for index in range(num_lines):
        plt.plot(problem_number, times[index], label=names[index], marker='o')

    plt.xlabel('Problem Number')
    plt.ylabel('Penalty')
    plt.title('Method Comparison for Single Machine Job Scheduling')
    plt.legend()

    plt.show()
    return


def main():
    f_name = 'sch100.txt'
    process_method = []
    lateness_method = []
    early_method = []
    genetic_method = []
    problem_number = []

    problems, k = read_problem_file(f_name)
    for index in range(1, k + 1):
        print(f'Problem {index}')
        problem_number.append(index)
        problem = problems[index]

        due_date = math.floor(sum(problem[1]) * H)

        p = problem[1]
        a = problem[2]
        b = problem[3]

        print('Process Method')
        order = solve_most_possible(p, a, b)
        penalty = get_penalty(order, due_date)
        process_method.append(penalty)

        print('Lateness Method')
        order = solve_late_first(p, a, b)
        penalty = get_penalty(order, due_date)
        lateness_method.append(penalty)

        print('Early Method')
        order = solve_early_first(p, a, b)
        penalty = get_penalty(order, due_date)
        early_method.append(penalty)

        print('Genetic Method')
        penalty = genetic_algorithm(p, a, b)
        genetic_method.append(penalty)

    plot_results([process_method, lateness_method, early_method, genetic_method], ['Process Method', 'Lateness Method', 'Early Method', 'Genetic Method'], problem_number)
    return


if __name__ == "__main__":
    main()
