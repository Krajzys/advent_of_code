from sys import argv
from re import match
from math import floor, ceil

class SnailNumber:
    def __init__(self, left=0, right=0):
        self.left = left
        self.right = right

    @classmethod
    def parse(self, snail_number_str) -> object:
        snail_number_str = snail_number_str[:]
        if match(r'^\d+$', snail_number_str):
            return int(snail_number_str)
        elif match(r'^\[\d+,\d+\]$', snail_number_str):
            left, right = snail_number_str[1:-1].split(',')
            return SnailNumber(int(left), int(right))
        else:
            depth = 0
            comma_index = 0
            for i, l in enumerate(snail_number_str):
                if l == '[':
                    depth += 1
                elif l == ']':
                    depth -= 1
                elif l == ',' and depth == 1:
                    comma_index = i
            left = snail_number_str[1:comma_index]
            right = snail_number_str[comma_index+1:-1]
            return SnailNumber(SnailNumber.parse(left), SnailNumber.parse(right))

    def pair(self) -> object:
        return [self.left, self.right]

    def set(self, snail_number):
        self.left = snail_number.left
        self.right = snail_number.right

    def magnitude(self) -> int:
        mag = 0
        if type(self.left) == int:
            mag += 3*self.left
        else:
            mag += 3*self.left.magnitude()
        if type(self.right) == int:
            mag += 2*self.right
        else:
            mag += 2*self.right.magnitude()

        return mag

    def __add__(self, snail_number):
        new_snail_number = SnailNumber(self, snail_number)
        new_snail_number = new_snail_number.reduce_number()
        return new_snail_number

    def reduce_number(self):
        reduce_str = str(self)
        reduced = True

        while reduced:
            ind = 0
            depth = 0
            while ind < len(reduce_str):
                reduced = False
                if reduce_str[ind] == '[':
                    depth += 1
                elif reduce_str[ind] == ']':
                    depth -= 1
                if depth == 5:
                    reduced = True
                    ind_end_explode = reduce_str.find(']', ind) + 1
                    ind_start_explode = ind
                    to_reduce = SnailNumber.parse(reduce_str[ind_start_explode:ind_end_explode])
                    reduce_str2 = reduce_str

                    # Find first left number and increase it
                    ind -= 1
                    while ind > 0 and not match(r'^[^\d]\d+', reduce_str[ind:]):
                        ind -= 1
                    if ind != 0:
                        ind += 1
                        to_increase_end_ind = ind
                        while reduce_str[to_increase_end_ind] in '0123456789':
                            to_increase_end_ind += 1
                        reduce_str2 = reduce_str[:ind] + str(int(reduce_str[ind:to_increase_end_ind]) + to_reduce.left) + reduce_str[to_increase_end_ind:]

                    # If the string got longer move indexes
                    ind_end_explode += abs(len(reduce_str2) - len(reduce_str))
                    ind_start_explode += abs(len(reduce_str2) - len(reduce_str))

                    # Find first right number and increase it
                    ind = ind_end_explode
                    while ind < len(reduce_str2) and reduce_str2[ind] not in '0123456789':
                        ind += 1
                    if ind != len(reduce_str2):
                        to_increase_end_ind = ind
                        while reduce_str2[to_increase_end_ind] in '0123456789':
                            to_increase_end_ind += 1
                        reduce_str2 = reduce_str2[:ind] + str(int(reduce_str2[ind:to_increase_end_ind]) + to_reduce.right) + reduce_str2[to_increase_end_ind:]

                    # Replace exploded with new digit
                    reduce_str2 = reduce_str2[:ind_start_explode] + '0' + reduce_str2[ind_end_explode:]
                    reduce_str = reduce_str2[:]
                    # print(f'EXPLODE: {reduce_str} {to_reduce} i:{ind_start_explode}')
                    break
                ind += 1
                
            ind = 0
            while ind < len(reduce_str) and not reduced:
                if reduce_str[ind] in '0123456789':
                    end_ind = ind
                    while reduce_str[end_ind] in '0123456789':
                        end_ind += 1
                    number = int(reduce_str[ind:end_ind])
                    if number > 9:
                        reduced = True
                        left = int(floor(number / 2))
                        right = int(ceil(number / 2))
                        reduce_str = reduce_str[:ind] + f'[{left},{right}]' + reduce_str[end_ind:]
                        # print(f'SPLIT: {reduce_str} {number} i:{ind}')
                        break
                ind += 1

        return SnailNumber.parse(reduce_str)

    def __repr__(self):
        repr_str = "[" + str(self.left) + "," + str(self.right) + "]"
        return repr_str


def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name>")
        exit(1)
    line_list = []
    if argv[1] == '-':
        while (line := input()) != '':
            line_list.append(line)
    else:
        filename = argv[1]
        line_list = [line.strip() for line in open(filename)]

    snail_numbers = []
    for line in line_list:
        snail_numbers.append(SnailNumber.parse(line))

    res = snail_numbers[0]
    for next_number in snail_numbers[1:]:
        print('  ' + str(res))
        print('+ ' + str(next_number))
        res = res + next_number
        print('= ' + str(res))
        print()

    print(res)
    print(res.magnitude())


if __name__ == "__main__":
    main()
