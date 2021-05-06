#Program for gaussian elimination
import numpy as np
import sys

n = int(input('Enter n for an nxn matrix'))

#makes array nx(n+1) of zeros
augmented = np.zeros((n,(n+1)))
#makes array to store solution vector
solution = np.zeros(n)

print('Please enter your coefficients for the augmented matrix:')
for i in range(n):
    for j in range(n+1):
        augmented[i][j] = float(input('A['+str(i)+']['+ str(j)+']='))

for i in range(n):
    if augmented[i][i] == 0.0:
        sys.exit('Pivot=0 Error')

    for j in range(i + 1, n):
        factor = augmented[j][i] / augmented[i][i]

    for k in range(n + 1):
        augmented[j][k] = augmented[j][k] - factor * augmented[i][k]

solution[n - 1] = augmented[n - 1][n] / augmented[n - 1][n - 1]

for i in range(n - 2, -1, -1):
    solution[i] = augmented[i][n]

    for j in range(i + 1, n):
        solution[i] = solution[i] - augmented[i][j] * solution[j]

    solution[i] = solution[i] / augmented[i][i]

print('\nSolution: ')
for i in range(n):
    print('X%d = %0.2f' % (i, solution[i]), end='\t')








