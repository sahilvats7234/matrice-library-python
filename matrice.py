class Matrice:


    def __init__(self, matrix):
        # Must be a non-empty list
        if not isinstance(matrix, list) or len(matrix) == 0:
            raise ValueError("Matrix must be a non-empty list of rows")

        # Every row must be a non-empty list
        for row in matrix:
            if not isinstance(row, list) or len(row) == 0:
                raise ValueError("Each row must be a non-empty list")

        cols = len(matrix[0])

        for row in matrix:
            # All rows must have the same length
            if len(row) != cols:
                raise ValueError("All rows must have the same length")
            # Only numbers are allowed
            for value in row:
                if not isinstance(value, (int, float)):
                    raise TypeError("Matrix can only contain numbers")

        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = cols

    # Display
    def display(self):
        for row in self.matrix:
            print(row)

    def __repr__(self):
        return f"Matrice({self.matrix})"
    

    def __getitem__(self, index):
        return self.matrix[index]

    # Equality
    def __eq__(self, other):
        if not isinstance(other, Matrice):
            return False
        return self.matrix == other.matrix

    # Negative
    def __neg__(self):
        return self * -1

    def is_square(self):
        return self.rows == self.cols

    # Addition
 
    def __add__(self, other):
        if not isinstance(other, Matrice):
            raise TypeError("You can only add a Matrice to a Matrice")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Addition not possible: matrices must have the same size")

        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.matrix[i][j] + other.matrix[i][j])
            result.append(row)
        return Matrice(result)


    # Subtraction
    def __sub__(self, other):
        if not isinstance(other, Matrice):
            raise TypeError("You can only subtract a Matrice from a Matrice")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Subtraction not possible: matrices must have the same size")

        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.matrix[i][j] - other.matrix[i][j])
            result.append(row)
        return Matrice(result)

    # Multiplication

    def __mul__(self, other):
        # 1) Scalar
        if isinstance(other, (int, float)):
            result = []
            for row in self.matrix:
                new_row = []
                for x in row:
                    new_row.append(x * other)
                result.append(new_row)
            return Matrice(result)

        if not isinstance(other, Matrice):
            raise TypeError("You can only multiply a Matrice by a number or a Matrice")

        # 2) Standard matrix product
        if self.cols == other.rows:
            result = []
            for i in range(self.rows):
                row = []
                for j in range(other.cols):
                    total = 0
                    for k in range(self.cols):
                        total += self.matrix[i][k] * other.matrix[k][j]
                    row.append(total)
                result.append(row)
            return Matrice(result)

        # 3) Element-wise with broadcasting (a size of 1 is stretched)
        rows_ok = self.rows == other.rows or self.rows == 1 or other.rows == 1
        cols_ok = self.cols == other.cols or self.cols == 1 or other.cols == 1
        if not (rows_ok and cols_ok):
            raise ValueError("Multiplication not possible for these sizes")

        out_rows = max(self.rows, other.rows)
        out_cols = max(self.cols, other.cols)

        result = []
        for i in range(out_rows):
            row = []
            for j in range(out_cols):
                # use index 0 when that matrix has only 1 row / 1 column
                a_i = i if self.rows > 1 else 0
                a_j = j if self.cols > 1 else 0
                b_i = i if other.rows > 1 else 0
                b_j = j if other.cols > 1 else 0
                row.append(self.matrix[a_i][a_j] * other.matrix[b_i][b_j])
            result.append(row)
        return Matrice(result)

    def __rmul__(self, scalar):
        return self * scalar

    # Division (element-wise)
 
    def __truediv__(self, other):
        # Matrice / number
        if isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = []
            for row in self.matrix:
                new_row = []
                for x in row:
                    new_row.append(x / other)
                result.append(new_row)
            return Matrice(result)

        if not isinstance(other, Matrice):
            raise TypeError("You can only divide a Matrice by a number or a Matrice")
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Division not possible: matrices must have the same size")

        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if other.matrix[i][j] == 0:
                    raise ZeroDivisionError("Division by zero not possible")
                row.append(self.matrix[i][j] / other.matrix[i][j])
            result.append(row)
        return Matrice(result)

    # Transpose

    def transpose(self):
        result = []
        for j in range(self.cols):
            row = []
            for i in range(self.rows):
                row.append(self.matrix[i][j])
            result.append(row)
        return Matrice(result)

    # Trace

    def trace(self):
        if not self.is_square():
            raise ValueError("Trace is only defined for square matrices")
        total = 0
        for i in range(self.rows):
            total += self.matrix[i][i]
        return total
    
    # Minor:
    def minor(self, i, j):
        result = []
        for r in range(self.rows):
            if r == i:
                continue
            row = []
            for c in range(self.cols):
                if c == j:
                    continue
                row.append(self.matrix[r][c])
            result.append(row)
        return Matrice(result)


    # Determinant

    def determinant(self):
        if not self.is_square():
            raise ValueError("Determinant is only defined for square matrices")

        # 1x1
        if self.rows == 1:
            return self.matrix[0][0]

        # 2x2
        if self.rows == 2:
            return (self.matrix[0][0] * self.matrix[1][1]
                    - self.matrix[0][1] * self.matrix[1][0])

        # Bigger: expand along the first row
        total = 0
        for j in range(self.cols):
            sign = 1 if j % 2 == 0 else -1
            total += sign * self.matrix[0][j] * self.minor(0, j).determinant()
        return total


    # Inverse
    def inverse(self):
        if not self.is_square():
            raise ValueError("Inverse is only defined for square matrices")

        det = self.determinant()
        if det == 0:
            raise ValueError("Matrix is singular (determinant is 0), no inverse exists")

        # 1x1 is a special case
        if self.rows == 1:
            return Matrice([[1 / self.matrix[0][0]]])

        # Cofactor matrix
        cofactors = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                sign = 1 if (i + j) % 2 == 0 else -1
                row.append(sign * self.minor(i, j).determinant())
            cofactors.append(row)

        # Adjugate = transpose of the cofactor matrix
        adjugate = Matrice(cofactors).transpose()
        return adjugate / det


    # Power: A ** n  
    def __pow__(self, n):
        if not isinstance(n, int):
            raise TypeError("Power must be an integer")
        if not self.is_square():
            raise ValueError("Power is only defined for square matrices")


        if n < 0:
            return self.inverse() ** (-n)

        result = Matrice.identity(self.rows)
        for _ in range(n):
            result = result * self
        return result

    # indentity matrix
    @staticmethod
    def identity(n):
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Size must be a positive integer")
        result = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            result.append(row)
        return Matrice(result)
    #zeroes matrix
    @staticmethod
    def zeros(rows, cols):
        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and columns must be positive")
        result = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(0)
            result.append(row)
        return Matrice(result)
    #ones martix
    @staticmethod
    def ones(rows, cols):
        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and columns must be positive")
        result = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(1)
            result.append(row)
        return Matrice(result)

