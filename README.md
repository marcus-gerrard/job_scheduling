# Job Scheduling
This problem was originally found on OR-Library linked here: https://people.brunel.ac.uk/~mastjjb/jeb/orlib/schinfo.html

## Problem Description
Each given problem starts with a number of jobs to be completed, in any order on a single machine, that are all to be completed by a common due date d. Each job comes with a processing time(p), an early penalty(a) incurred if the job is completed before the common due date, and a late penalty(b) incurred if the job is completed after the due date.

## Naive Heuristics
There are three very naive heurstics that are graphed with each result.
  1. Process Method: Simply sorting all jobs by their processing times and taking them in order, akin to attempting to complete as many jobs as possible before the common deadline.
  2. Lateness Method: Simply sorting all jobs by their lateness penalty, and completing the highest lateness penalties first, akin to avoiding large late penalties.
  3. Early Method: Simply sorting all jobs by their early penalty, and completing the lowest early penalties first, akin to avoiding large early penalties.

None of these naive heuristics acheive overly impressive results, most likely because all of them have very obvious counterpoints.  For example, by processing as many jobs as possible, you are avoiding paying the maximum number of late penalties, but you would also be incurring the maximum number of early penalties.

## More Advanced Approach
As a slightly more involved approach I chose to use a genetic algorithm.  The basic approach is to start with a random initial population of individuals, each of which is a candidate solution to the problem.  Then using a fitness function that evaluates the total early penalty and total late penalty each candidate incurs, rank all members in the population by their early penalty and late penalty respectively.  Using the top K members in each category, lowest K early penalties and lowest K late penalties, you can merge these two parents into child individual, and doing so with all top K candidates creates a new generation of individuals.  Repeating this process over a set number of generations yields a final solution generation, of which the best overall penalty can be found and returned as the solution.  
There are two different merging strategies implemented.
  1. One point merge with random conflict resolution: Simply taking a random crossover point, and splicing up to that point in the early ranking parent, and from the crossover point onwards in the late ranking parent.  To resolve conflicting numbers(times in which a job appears in both the early part of the early parent and late part of the late parent) a number not already present in the child sequence is substituted at random into that positon in the child, producing one total child.  This merging method is labelled in the graphs as Random Crossover.
  2. PMX Merging: Partially mapped crossover, which takes a random segment of the first parent, and copies that to one child, and taking that same random start and end point to copy the middle segment from the second parent to a second child.  Then to fill in the left and right ends of the children, you can take the left and right ends that were not included in the middle segments, and give them to the other child, resolving conflicts through a mapping established in the middle.  For example, parent 1 contributes a middle section to child 1, and it's left and right endpoints to child 2 and vice versa for parent 2.

PMX merging achieved significantly better results, most likely due to it better preserving order within the children, as random merging usually failed to preserve the order of the second parent.

## Exact Solution
Coming Soon

## Charts

### PMX Merging with 300 Generations
![Chart1](Graphed%20Results/PMX%20Crossover%20with%20300%20Generations.png)

### PMX Merging with 1000 Generations
![Chart2](Graphed%20Results/PMX%20Crossover%20with%201000%20Generations.png)

### Random Crossover with 100 Generations
![Chart3](Graphed%20Results/Random%20Crossover%20with%20100%20Generations.png)

### Random Crossover with 7000 Generations
![Chart4](Graphed%20Results/Random%20Crossover%20with%207000%20Generations.png)
