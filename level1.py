def solution(data, n): 
    # for time complexity let N be the length of data
    
    if len(data) == 0:
        return []
        
    # O(N), count task occurrence
    counts = {}
    for task in data:
        if task in counts:
            counts[task] += 1
        else:
            counts[task] = 1
    
    # O(N), find tasks that occure more than n times
    to_del = [task for task in counts.keys() if counts[task] > n]
    for task in to_del: del counts[task]
    
    # O(N), remove tasks that occure more than n times
    result = [task for task in data if task in counts]
    
    return result

assert (solution([1,2,2,3,4,5,6], 1)) == [1, 3, 4, 5, 6]
assert (solution([1,2,2,3,4,5,6], 3)) == [1, 2, 2, 3, 4, 5, 6]
assert (solution([2,2,2,2,2,1], 5)) == [2, 2, 2, 2, 2, 1]
print("All tests passed")