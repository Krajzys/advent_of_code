import functools
from sys import argv
from statistics import median
from functools import reduce

def main():
    debug = False
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name>")
        exit(1)
    if '-d' in argv:
        debug = True
    filename = argv[1]
    line_list = [line for line in open(filename)]

    fuel_list = []
    for line in line_list:
        fuel_list.extend([int (x) for x in line.split(',')])

    fuel_list = sorted(fuel_list)
    optimal = fuel_list[len(fuel_list)//2]

    acc = 0
    for i in fuel_list:
        acc += abs(optimal-i)
        if debug:
            print(f'opt:{optimal} val:{i} diff: {abs(optimal-i)} acc:{acc}')

    print(acc)


if __name__ == "__main__":
    main()