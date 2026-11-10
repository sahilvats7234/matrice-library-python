
class Matrice:

    # Constructor
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])

    # Display matrix
    def display(self):
        for row in self.matrix:
            print(row)
    def __repr__(self):
        return f"Matrice({self.matrix})"
    

    # Addition
    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            print("Addition not possible")
            return 
        result = []

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.matrix[i][j] + other.matrix[i][j])
            result.append(row)
        result = Matrice(result)
        return result

    # Subtraction
    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            print("Subtraction not possible")
            return

        result = []

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.matrix[i][j] - other.matrix[i][j])
            result.append(row)
        result = Matrice(result)
        return result

    # Multiplication
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Matrice([[x * other for x in row] for row in self.matrix])
    
        if self.cols != other.rows:
            print("Multiplication not possible")
            return

        result = []

        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                total = 0
                for k in range(self.cols):
                    total += self.matrix[i][k] * other.matrix[k][j]
                row.append(total)
            result.append(row)
        result = Matrice(result)
        return result
    # scalar
    def __rmul__(self, scalar):
        return self * scalar 


    # Division (element-wise)
    def __truediv__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            print("Division not possible")
            return

        result = []

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if other.matrix[i][j] == 0:
                    print("Division by zero not possible")
                    return
                row.append(self.matrix[i][j] / other.matrix[i][j])
            result.append(row)
        result = Matrice(result)
        return result
    def transpose(self):
        return Matrice([
            [self.matrix[i][j] for i in range(self.rows)]
            for j in range(self.cols)
        ])


    # Identity Matrix
    @staticmethod
    def identity(n):
        result = []

        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)

            result.append(row)
        result = Matrice(result)
        return result


add1 = Matrice([[1,2],[3,4]])
add2 = Matrice([[5,6],[7,8]])

