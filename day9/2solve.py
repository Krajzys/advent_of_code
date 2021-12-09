from sys import argv
from functools import reduce

def print_map(map):
    for r in map:
            for v in r:
                print(f"{v}", end="")
            print()


def get_basin_sizes(basin_map):
    basin_sizes = {}
    for r in basin_map:
        for c in r:
            if c == 'X':
                continue
            if c in basin_sizes.keys():
                basin_sizes[c] += 1
            else:
                basin_sizes[c] = 1

    return basin_sizes


def claim_basin_within(basin_number, point, basin_map):
    r, c = point
    if r < 0 or r >= len(basin_map) or c < 0 or c >= len(basin_map[0]) or basin_map[r][c] != 0:
        return
    basin_map[r][c] = basin_number
    claim_basin_within(basin_number, (r-1, c), basin_map)
    claim_basin_within(basin_number, (r+1, c), basin_map)
    claim_basin_within(basin_number, (r, c-1), basin_map)
    claim_basin_within(basin_number, (r, c+1), basin_map)

def map_basins(low_points, basin_map):
    for r, c in low_points:
        basin_number = basin_map[r][c]
        basin_map[r][c] = 0
        claim_basin_within(basin_number, (r, c), basin_map)


def check_low_point(r, c, height_map):
    neighbors_count = 0
    low_points = 0

    if r-1 >= 0:
        if height_map[r-1][c] > height_map[r][c]:
            low_points += 1
        neighbors_count += 1
    if r+1 < len(height_map):
        if height_map[r+1][c] > height_map[r][c]:
            low_points += 1
        neighbors_count += 1
    if c-1 >= 0:
        if height_map[r][c-1] > height_map[r][c]:
            low_points += 1
        neighbors_count += 1
    if c+1 < len(height_map[0]):
        if height_map[r][c+1] > height_map[r][c]:
            low_points += 1
        neighbors_count += 1

    return neighbors_count == low_points


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

    height_map = []
    for line in line_list:
        height_map.append([int(h) for h in list(line)])

    basin_map = [r[:] for r in height_map]
    low_point_count = 1
    low_points = []
    for i, r in enumerate(height_map):
        for j, _ in enumerate(r):
            if check_low_point(i, j, height_map):
                low_points.append((i, j))
                basin_map[i][j] = low_point_count
                low_point_count += 1
            else:
                if height_map[i][j] == 9:
                    basin_map[i][j] = 'X'
                else:
                    basin_map[i][j] = 0

    map_basins(low_points, basin_map)
    basin_sizes = get_basin_sizes(basin_map)
    three_biggest_areas = sorted(basin_sizes.values())[-3:]

    print(three_biggest_areas)
    print(reduce(lambda v, acc: acc * v, three_biggest_areas, 1))


if __name__ == "__main__":
    main()