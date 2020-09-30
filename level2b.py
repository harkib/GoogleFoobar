def solution(x, y):
    # Brute force, traverse in diagonal fasion until x,y is reached. O(n) n= num prisinors
    count = 1
    
    h = 1
    w = 1
    level = 1
    
    while (h != y) or (w != x):
        count += 1
        
        if h == 1:
            level += 1
            h = level 
            w = 1
        else:
            h -= 1
            w += 1
    
    return count


def solution2(x, y):

    diagonal_level = x + y -2 
    count = (diagonal_level*(diagonal_level+1)/2) + x
    return count


# check brute force 
assert solution(5,10) == 96
assert solution(3,3) == 13

# check final solution
assert solution2(5,10) == 96
assert solution2(3,3) == 13
assert solution(5,5) == solution2(5,5)
assert solution(2,7) == solution2(2,7)
assert solution(8,7) == solution2(8,7)
assert solution(8,12) == solution2(8,12)
print("All tests passed")