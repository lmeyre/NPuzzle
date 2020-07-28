import sys

def translate_position(self, number, size):
    x = number / size
    y = number % size
    return x, y

def collect_numbers(array):
    numbers = []
    exception = False
    for i in range(0, len(array)):
        for j in range(0, len(array)):
            try:
                int(array[i][j])
                numbers.append(int(array[i][j]))
            except ValueError:
                    if (array[i][j] == '_' and exception == False):
                        exception = True
                    else:
                        print("One of the cells isnt a number")
                        sys.exit()
    return numbers

def verify_numbers_link(numbers, size):
    a = 1
    total = size * size - 1
    while (a <= total):
        for i in numbers:
            print(i)
            if i == a:
                a += 1;
                break
        print("problem numbers dont link")
        sys.exit()



