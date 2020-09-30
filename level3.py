def permutations(curr_height, remaining, memory):

    if (curr_height, remaining) in memory:
        return memory[curr_height, remaining]

    # staircase complete
    if remaining == 0:
        return 1

    # infeasible staircase
    if remaining < curr_height:
        return 0

    # add to current step and create new step, save to memory
    memory[curr_height, remaining] =  permutations(curr_height + 1, remaining - curr_height, memory) + permutations(curr_height + 1, remaining, memory)
    return memory[curr_height, remaining]

def solution(n):
    memory = {}
    return permutations(1,n, memory) -1

assert (solution(200)) == 487067745
assert (solution(3)) == 1
assert (solution(4)) == 1
assert (solution(5)) == 2
print("All tests passed")