from itertools import permutations

# assumes graph is the problem provided dense graph as matrix, 
# does not detect negative cycles
def bellmanFord(start_node, graph):

    # intialize
    vertices = range(len(graph))
    distances = [float('inf')]*len(vertices)
    distances[start_node] = 0

    # relax each edge V-1 times 
    for _ in range(len(vertices)-1):
        for V_from in vertices:
            if distances[V_from] != float('inf'):    
                for V_to in vertices: 
                     if distances[V_from] + graph[V_from][V_to] < distances[V_to]:
                         distances[V_to] = distances[V_from] + graph[V_from][V_to] 

    return distances


# since the graph is dense, do one more bellmanFord itteration to find a negative cycle
def hasNegativeCycle(bellmanFordResult, graph):
    
    vertices = range(len(graph))
    distances = bellmanFordResult

    # one itteration, if shorter path is found we have a negative cycle
    for V_from in vertices:
            if distances[V_from] != float('inf'):    
                for V_to in vertices: 
                     if distances[V_from] + graph[V_from][V_to] < distances[V_to]:
                         return True

    return False

def checkPath(path, distanceMap, times_limit):

    cost = 0
    for i in range(len(path)-1): cost += distanceMap[path[i]][path[i+1]]
    return cost <= times_limit

def solution(times, times_limit):
    
    n_nodes = len(times)
    nodes = range(n_nodes)

    #  build distance matrix, min distance between all nodes
    distanceMap = [] # distanceMap[from][to]
    for node in nodes: 
        bellmanFordResult = bellmanFord(node, times)

        # all bunnies saved if there is a negative cycle 
        if hasNegativeCycle(bellmanFordResult, times): return range(n_nodes-2)
        distanceMap.append(bellmanFordResult)


    # check all permutations until first possible path, 
    # starting with most bunnies with tiebreaker winners comming first 
    bunnies = range(1,n_nodes-1)
    for n_saved in range(n_nodes-1, 0,-1):
        for bunniesSaved in permutations(bunnies,n_saved):

            path = [0]
            path.extend(bunniesSaved)
            path.append(n_nodes-1)
            

            if checkPath(path, distanceMap, times_limit):

                # zero index bunnies  
                bunniesSaved_ids = []
                for bunny in bunniesSaved: bunniesSaved_ids.append(bunny - 1)
                bunniesSaved_ids.sort()
                return bunniesSaved_ids
    
    # no bunnies could be saved
    return []


assert (solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1))  == [1,2]
assert (solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)) == [0, 1]
assert (solution([[0, 1], [1, 0]], 3)) == []
assert (solution([[0,1, -2], [1,1, 0], [1,1, 0]], 3))  == [0]
print("All tests passed")