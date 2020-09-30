import itertools
import collections
import math
import fractions

# generates all possible cycle partions with n elements in set
def generate_cycle_partitions(n):
    cp = []
    for l in range(1,n+1):
        nums = range(1,n-l+2)
        cp.extend([list(p) for p in itertools.combinations_with_replacement(nums, r=l) if sum(p) == n])

    return cp

# considering swapping 0 to n rows/cols, count the number of actions that could 
# produce the given cycle partition.
def count_actions(cycle_partition):
    n = sum(cycle_partition)
    NA_actions = 1 # actions that cannot produce this cycle partition
    for length, count in collections.Counter(cycle_partition).items():
        NA_actions *= (length**count)*math.factorial(count)

    return math.factorial(n)/NA_actions # all actions/not possible actions


# Polya enumeration theorem: Lecture 16.12
# https://www.youtube.com/playlist?list=PLl-gb0E4MII1_QX6h6TzMW3rF_7Taapyd
# we use seperate action groups for rows and cols as we can combine the 
# sub solutions to get the final solution 
# https://www.sciencedirect.com/science/article/pii/0012365X9390015L
def solution(w, h, s):
    
    # total actions
    len_G = math.factorial(w) * math.factorial(h)

    # all possible cycle partions
    row_cycle_partitions = generate_cycle_partitions(h)
    col_cycle_partitions = generate_cycle_partitions(w)

    # for all combinations of row and col cycle permutations get number of actions 
    # and \sum{for g in G} \product{k = 1 to n} s^cycle_k(g) which becomes
    # \sum{for g in G} s^( \sum{k = 1 to n } cycle_k(g))   
    weighted_exp = 0
    for rcp in row_cycle_partitions:
        for ccp in col_cycle_partitions:

            # compute number of actions that produce given cycle partion
            actions = count_actions(rcp)*count_actions(ccp)

            # compute sum of patition cycles for cols and rows
            # take gcd of cycle indices: https://www.sciencedirect.com/science/article/pii/0012365X9390015L
            index_sum = sum([sum([fractions.gcd(r,c) for r in rcp]) for c in ccp])
            
            weighted_exp += actions*(s**index_sum)

    # Z = (1/len(G))*(\sum{for g in G} \product{k = 1 to n} s^cycle_k(g))
    return str(weighted_exp/len_G)

assert solution(2, 3, 4) == "430"
assert solution(2, 2, 2) == "7"
assert solution(3, 3, 2) == "36"
assert solution(5, 2, 3) == "678"
print("All tests passed")