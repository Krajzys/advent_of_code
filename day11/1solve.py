from sys import argv
from time import sleep
from termcolor import colored

def print_octopus_grid(octopus_grid):
    for r in octopus_grid:
        for c in r:
            if c > 9:
                print(colored('X', 'red'), end="")
            else:
                print(c, end="")
        print()

def increase_surrounding_energy(octopus_grid, r, c, flashed=[]):
    if ((r, c) in flashed) or (octopus_grid[r][c] <= 9):
        return

    flashed.append((r, c))
    for rd in [-1, 0, 1]:
        for cd in [-1, 0, 1]:
            if rd == 0 and cd == 0:
                continue
            if r+rd >= 0 and r+rd < len(octopus_grid) and c+cd >= 0 and c + cd < len(octopus_grid[r]):
                octopus_grid[r+rd][c+cd] += 1
                if octopus_grid[r+rd][c+cd] > 9:
                    increase_surrounding_energy(octopus_grid, r+rd, c+cd, flashed)

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

    octopus_grid = []
    for line in line_list:
        octopus_grid.append([int(energy) for energy in list(line)])

    total_flashes = 0
    for i in range(100):
        for r, row in enumerate(octopus_grid):
            for c, _ in enumerate(row):
                octopus_grid[r][c] += 1

        flashed = []
        for r, row in enumerate(octopus_grid):
            for c, octopus_energy in enumerate(row):
                increase_surrounding_energy(octopus_grid, r, c, flashed)

        flashes = 0
        for r, row in enumerate(octopus_grid):
            for c, octopus_energy in enumerate(row):
                if octopus_energy > 9:
                    octopus_grid[r][c] = 0
                    flashes += 1

        total_flashes += flashes

    print(total_flashes)


if __name__ == "__main__":
    main()