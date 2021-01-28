import sys

"""
Fetch data from the input file
"""
input_data = []
for elephant, line in enumerate(sys.stdin):
    input_data.append([int(x) for x in line.rstrip().split()])

""" 
The elephants are represented by numbers from 1 to n.

n: number of the elephants
weights: costs of each elephant's movement
current_order: current order of the elephants
final_order: desired order of the elephants
 """
n = input_data[0][0]
weights = input_data[1]
current_order = input_data[2]
final_order = input_data[3]

"""
permutations[X] = Y,
meaning that the elephant with number X should take the place
that is currently occupied by the elephant with number Y
"""
permutations = {}
for elephant in range(n):
    permutations[final_order[elephant]] = current_order[elephant]

"""
visited: boolean that states if a vertex has been visited
For our program elephants are vertices in a graph
"""
visited = [False for _ in range(n)]
"""
Construct cycles from permutations
Start from given elephant and construct a cycle using the permutations dictionary 
e.g. e_i->e_j->e_k->e_i(seen) STOP
until an elephant that already is in a cycle is seen(has been visited)
"""
cycles = []
for elephant in range(n):
    if not visited[elephant]:
        cycle = []
        current_vertex = elephant
        while not visited[current_vertex]:
            visited[current_vertex] = True
            cycle.append(current_vertex + 1)
            current_vertex = permutations[current_vertex + 1] - 1
        cycles.append(cycle)


"""
global_min: minimum cost of movement out of all elephants
cycles_costs: array of sums of movement costs for all elephants in each cycle

structure of cycles_costs: [tuple: (sum_of_costs, min_cost), ...]
"""
global_min = sys.maxsize
cycles_costs = []

for cycle in cycles:
    cycle_cost = 0
    cycle_min = sys.maxsize
    for vertex in cycle:
        cycle_cost += weights[vertex - 1]
        cycle_min = min(cycle_min, weights[vertex - 1])

    cycles_costs.append([cycle_cost, cycle_min])
    global_min = min(global_min, cycle_min)


"""
Calculate the final result

To calculate the final result we now must transform the cycles such that each vertex in a cycle
is a self pointing vertex (meaning that every elephant from a cycle is in the correct place).
Why is that? Graph arrows from vertex to vertex represent that elephant X should replace elephant Y.
So, a self pointing vertex means that elephant X should replace elephant X - it is in the correct place.

cost[0]: sum of elephants' movement costs in a cycle
cost[1]: lowest cost of movement for some elephant from a cycle

To find the best way to re-order the elephants in a cycle we calculate the cost using following methods:
- method1
    Swap every elephant with the elephant whose cost is the lowest starting from the lowest cost elephant's predecessor.
    The lowest cost elephant moves "cycle length - 1" times.
    The rest move one time.
    
- method 2
    Swap lowest cost elephant with the global lowest cost one.
    Swap every elephant (apart from the lowest cost one from the cycle) like in method 1.
    Swap the lowest cost elephant with the global lowest one back.
    
    The global lowest cost elephant moves 
    "cycle length - 1 + 2 swaps with cycle min = cycle length + 1" times.
    The lowest cost elephant from the cycle moves exactly twice.
    The rest move one time.
    
And take the minimum value of these two.

We do not need to perform any of the operations mentioned above.
We only needed that theory to find how to sum the movement costs.

Repeat for every cycle to calculate the end result.
"""
result = 0
for cycle, cost in zip(cycles, cycles_costs):
    result += min(
        cost[0] + (len(cycle) - 2) * cost[1],  # method 1
        cost[0] + cost[1] + (len(cycle) + 1) * global_min  # method 2
    )

print(result)
