# x = [1,2,3,4,5,6]
# x = [1,1,1,1,1,1]
# print(sum(x[0:6]))

def solution(l, t):
    # Approach: have a window starting at size one and index 0,
    # if the sum of the window is less than the target the window grows
    # towards the end of list if the target is less the window shrinks
    # from the beggining of the list, O(n) time
    
    left_i = 0
    right_i = 1
    # curr_sum = l[0]
    
    
    # while right index does not go out of bounds
    while right_i <= len(l):
        
        curr_sum = sum(l[left_i:right_i])
        
        if curr_sum == t:
            return [left_i,right_i-1]
        elif curr_sum < t:
            right_i += 1
        else:
            left_i += 1
    
    
    # not found
    return [-1,-1]

assert (solution([1, 2, 3, 4], 15)) == [-1, -1]
assert (solution([4, 3, 10, 2, 8], 12)) == [2, 3]
print("All tests passed")