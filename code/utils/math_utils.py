def solve_sle(A):
    """Solves a system of linear equations using the Gaussian elimination method.
    The system should be specified as an augmented matrix
    
    [
      [a_1_1, a_1_2, ..., b_1],
      [a_2_1, a_2_2, ..., b_2],
      ...
      [a_n_1, a_n_2, ..., b_n]
    ],

    which corresponds to a system of equations
    
    {
      a_1_1*x_1 + a_1_2*x_2 + ... = b_1
      a_2_1*x_1 + a_2_2*x_2 + ... = b_2
      ...
      a_n_1*x_1 + a_n_2*x_2 + ... = b_n
    }
    
    Based on: https://martin-thoma.com/solving-linear-equations-with-gaussian-elimination/
    """
    n = len(A)

    # Make A an upper triangular matrix
    for i in range(0, n):
        # Search for maximum in this column
        maxEl = abs(A[i][i])
        maxRow = i
        for k in range(i+1, n):
            if abs(A[k][i]) > maxEl:
                maxEl = abs(A[k][i])
                maxRow = k

        # Swap maximum row with current row (column by column)
        for k in range(i, n+1):
            tmp = A[maxRow][k]
            A[maxRow][k] = A[i][k]
            A[i][k] = tmp

        # Make all rows below this one 0 in current column
        for k in range(i+1, n):
            c = -A[k][i]/A[i][i]
            for j in range(i, n+1):
                if i == j:
                    A[k][j] = 0
                else:
                    A[k][j] += c * A[i][j]

    # Solve the equation Ax = b for an upper triangular matrix A
    x = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = A[i][n]/A[i][i]
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return x
