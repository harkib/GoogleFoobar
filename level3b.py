from fractions import Fraction, gcd
import functools 

# Given numpy is not a standard library to invert a matrix the following functions 
# are taken from link; transposeMatrix, getMatrixMinor, getMatrixDeternminant, getMatrixInverse
# https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy
def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = list(transposeMatrix(cofactors))
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

def subtractMatrix(A,B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def multiplyMatrix(A,B):
    n = len(A)
    m = len(B[0])
    return [[sum([A[Arow][i] * B[i][Bcol] for i in range(n)]) for Bcol in range(m)] for Arow in range(n)]


def LCM(fractions):
    
    # LCM of 2 numbers
    def LCM_(a,b):
        return a*b // gcd(a,b)

    # Get denominators
    dems = []
    for frac in fractions: dems.append(frac.denominator)

    # Get lcm of all denominators
    lcm = functools.reduce(LCM_,dems)

    return int(lcm)


def formatOutput(probs):
    output = []
    fractions = []

    # Convert to fractions
    for prob in probs: fractions.append(Fraction.from_float(prob).limit_denominator())
    
    # Find LCM
    lcm = LCM(fractions)
    
    # Create output
    for frac in fractions: output.append(int(frac.numerator * lcm/frac.denominator))
    output.append(lcm)

    return output


def relocateState(m, i0, iNew):
    assert iNew < i0 #only for moving state up and shifting down

    # shift rows
    temp = m[i0]
    for  i in range(i0,iNew,-1): m[i] = m[i-1]
    m[iNew] = temp

    # shift cols
    for row in m:
        temp = row[i0]
        for  i in range(i0,iNew,-1): row[i] = row[i-1]
        row[iNew] = temp
    
    return m


def formatMarkovMatrix(m):

    # Check if termination states are above transition states
    trans_states = []
    trem_states = []
    for i,row in enumerate(m): trem_states.append(i) if (sum(row) == 0) else trans_states.append(i)
    
    # Move all trans states above trem states, perserving trem state order
    while max(trans_states) > min(trem_states):
        j = min(trem_states)
        i = max(trans_states)
        m = relocateState(m,i,j)

        # revaluate matrix
        trans_states = []
        trem_states = []
        for i,row in enumerate(m): trem_states.append(i) if (sum(row) == 0) else trans_states.append(i)

    return m

def solution(m):
    # https://brilliant.org/wiki/absorbing-markov-chains/
    
    # Count state types and normalize rows
    n_trans = 0
    n_trem = 0
    for i,row in enumerate(m):
        if sum(row) == 0:
            n_trem += 1
        else:
            n_trans += 1
            m[i] = [float(elem)/sum(row) for elem in row]

    # If s0 is a termination state
    if sum(m[0]) == 0:
        P0 = [0]*n_trem
        P0[0] = 1
        P0.append(1)
        return P0

    # Ensure proper matrix form, termination states are at bottom
    m = formatMarkovMatrix(m)

    # Get Q matrix
    Q = m[:n_trans]
    for i in range(n_trans): Q[i] = Q[i][:n_trans]

    # Get R matrix 
    R = m[:n_trans]
    for i in range(n_trans): R[i] = R[i][n_trans:]

    # Get I matrix
    I = [[1 if i == j else 0 for j in range(n_trans)] for i in range(n_trans)]

    # Get N matrix
    N = getMatrixInverse(subtractMatrix(I,Q))

    # Get M matrix 
    M = multiplyMatrix(N,R)

    # Get probabilities assuming starting at s0
    I0 = [0]*n_trem
    I0[0] = 1
    P = multiplyMatrix([I0],M)

    # Format and return probabilities
    return formatOutput(P[0])









m0 = [
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]

m1 = [
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

m2 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

assert (solution(m0)) == [0, 3, 2, 9, 14]
assert (solution(m1)) == [2, 1, 1, 1, 1, 6]
assert (solution(m2)) == [1, 1, 1, 1, 1, 5]
assert (solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])) == [7, 6, 8, 21]
assert (solution([[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])) == [1, 0, 0, 0, 1]
print("All tests passed")