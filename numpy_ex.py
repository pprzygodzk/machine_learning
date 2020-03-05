import numpy as np

X = np.random.randn(4, 2)
print("original matrix:")
print(X, "\n")


def minValueIndex(A):
    indexes = []
    for i in range(len(A[0])):
        index = A[:, i].argmin()
        indexes.append((i, index))
    return(indexes)
    
print(minValueIndex(X), "\n")

def standarize(A):
    for i in range(len(A[0])):
        m = A[:, i].mean()
        s = A[:, i].std()
        for j in range(len(A)):
            A[j][i] = (A[j][i]-m)/s
    return A

print(standarize(X), "\n")