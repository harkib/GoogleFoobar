def solution(x, y):
    # work bottom up, compute steps to go from goal to intail state (1,1)
    m = int(x)
    f = int(y)
    steps = 0

    # Keep steping while not at intial state
    while(m != 1 or f != 1):

        # impossible state
        if (m < 1 or f < 1):
            return 'impossible'
        
        # all steps from this point upward must have been all m-> f or f -> m
        if m == 1 or f == 1:
            steps += max(m,f) - 1
            m , f = 1, 1

        # steps must have been from the smaller to larger type for 
        # as many steps as it requires the relative size to flip
        elif m < f:
            steps += f/m
            f = f % m
        else:
            steps += m/f
            m = m % f

    return str(steps)



assert (solution('2','1')) == '1'
assert (solution('4','7')) == '4'
assert (solution('2','4')) == "impossible"
assert (solution('1','950')) == '949'
assert (solution('950','1')) == '949'
print("All tests passed")