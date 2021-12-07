import functools
from sys import argv
from statistics import mean
from functools import reduce
from math import cos, floor, ceil

def get_fuel_cost(dist):
    cost = 0
    for i in range(0,dist+1):
        cost += i

    return cost


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

    optimal = floor(mean(fuel_list))

    acc = 0
    for i in fuel_list:
        acc += get_fuel_cost(abs(optimal-i))
        if debug:
            print(f'opt:{optimal} val:{i} diff: {abs(optimal-i)} cost: {get_fuel_cost(abs(optimal-i))} acc:{acc}')

    print(optimal, acc)


if __name__ == "__main__":
    main()