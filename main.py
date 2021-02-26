import sys
import copy

def read_matrix(index):
    options = [" first", " second", ""]
    matrix = []
    while True:
        inp = input("Enter size of{} matrix: > ".format(options[index])).split()
        if not validate_size(inp):
            continue
        break
    n = int(inp[0])
    m = int(inp[1])
    print("Enter{} matrix:".format(options[index]))
    for i in range(int(n)):
        line = convert_line(input("> "))
        if len(line) != m:
            print("Wrong columns amount")
            sys.exit()
        matrix.append(line)

    return matrix


# converts str line into list of int/float values and returns it
def convert_line(s):
    s = s.split()
    for i in range(len(s)):
        s[i] = get_number(s[i])
        if s[i] is None:
            print("Matrix values must be integers or floats")
            sys.exit()
    return s


def sum_matrices(a, b):
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        return None
    for i in range(len(a)):
        for j in range(len(a[0])):
            a[i][j] += b[i][j]
    return a


def print_matrix(matrix):
    print("The result is:")
    for i in matrix:
        for j in i:
            print(round(j, 2), end=" ")
        print()


def multiply_matrix(m, k=None):
    # scalar multiplication
    if k is None:
        while True:
            k = input("Enter constant: > ")
            k = get_number(k)
            if k is None:
                print("Value must be integer or float")
                continue
            break

    for i in range(len(m)):
        for j in range(len(m[0])):
            m[i][j] *= k

    return m


# converts string into int or float
def get_number(s):
    if s.isdigit() or (s[0] == '-' and s[1:].isdigit()):
        s = int(s)
    else:
        try:
            s = float(s)
        except ValueError:
            return None
    return s


def multiply_matrices(m1, m2):
    if len(m1[0]) != len(m2):
        return None
    row = []
    m = []
    element = 0
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for n in range(len(m1[0])):
                element += m1[i][n]*m2[n][j]
            row.append(element)
            element = 0
        m.append(row)
        row = []
    return m


def transpose_matrix(m, t):
    transposed_m = []
    row = []
    if t == "1":
        for i in range(len(m[0])):
            for j in range(len(m)):
                row.append(m[j][i])
            transposed_m.append(row)
            row = []
    elif t == "2":
        for i in reversed(range(len(m[0]))):
            for j in reversed(range(len(m))):
                row.append(m[j][i])
            transposed_m.append(row)
            row = []
    elif t == "3":
        for i in range(len(m)):
            for j in range(len(m[0]) // 2):
                m[i][j], m[i][len(m[0]) - j - 1] = m[i][len(m[0]) - j - 1], m[i][j]
        transposed_m = m
    elif t == "4":
        for i in range(len(m) // 2):
            m[i], m[len(m) - i - 1] = m[len(m) - i - 1], m[i]
        transposed_m = m
    return transposed_m


def calculate_minor(m, i, j):
    new_matr = copy.deepcopy(m)
    del new_matr[i]
    for row in new_matr:
        del row[j]
    return calculate_determinant(new_matr)


def calculate_determinant(m):
    if len(m) == 1:
        return m[0][0]
    elif len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    else:
        determinant = 0
        sign = 1
        for i in range(len(m[0])):
            # forming a new matrix without raw and column
            new_m = []
            for row in range(1, len(m)):
                new_r = copy.deepcopy(m[row])
                del new_r[i]
                new_m.append(new_r)

            determinant += m[0][i] * sign * calculate_determinant(new_m)
            sign *= -1

    return determinant


def inverse_matrix(m):
    m_cpy = copy.deepcopy(m)
    for i in range(len(m)):
        for j in range(len(m[0])):
            m_cpy[i][j] = calculate_minor(m, i, j) * pow(-1, i + j + 2)
    m_cpy = transpose_matrix(m_cpy, "1")
    det = calculate_determinant(m)
    if det == 0:
        return None
    return multiply_matrix(m_cpy, 1/det)


def call_interface():
    options = ["1. Add matrices", "2. Multiply matrix by a constant", "3. Multiply matrices",
               "4. Transpose matrix", "5. Calculate a determinant", "6. Inverse matrix", "0. Exit"]
    transposition_options = ["1. Main diagonal", "2. Side diagonal", "3. Vertical line", "4. Horizontal line"]

    while True:
        for option in options:
            print(option)
        choice = input("Your choice: > ")
        if choice not in list("0123456"):
            print("Wrong input")
            continue

        if choice == "1":
            matrix_1 = read_matrix(0)
            matrix_2 = read_matrix(1)
            s = sum_matrices(matrix_1, matrix_2)
            if not s:
                print("The operation cannot be performed.")
                continue
            print_matrix(s)
        elif choice == "2":
            matrix = read_matrix(2)
            matrix = multiply_matrix(matrix)
            print_matrix(matrix)
        elif choice == "3":
            matrix_1 = read_matrix(0)
            matrix_2 = read_matrix(1)
            m = multiply_matrices(matrix_1, matrix_2)
            if not m:
                print("The operation cannot be performed.")
                continue
            print_matrix(m)
        elif choice == "4":
            print()
            for option in transposition_options:
                print(option)
            tr_choice = input("Your choice: > ")
            if tr_choice not in list("1234"):
                print("Wrong input")
                continue
            matrix = read_matrix(2)
            matrix = transpose_matrix(matrix, tr_choice)
            print_matrix(matrix)
        elif choice == "5":
            matrix = read_matrix(2)
            d = calculate_determinant(matrix)
            print("The result is:")
            print(d)
            print()
        elif choice == "6":
            matrix = read_matrix(2)
            inversed = inverse_matrix(matrix)
            if inversed is None:
                print("This matrix doesn't have an inverse.\n")
                continue
            print_matrix(inversed)
        else:
            sys.exit()


# validates input size of matrix
# gets array, checks if there are 2 digits
def validate_size(inp):
    if len(inp) != 2 or not inp[0].isdigit() or not inp[0].isdigit():
        print("Wrong matrix size")
        return 0
    return 1


if __name__ == "__main__":
    call_interface()


