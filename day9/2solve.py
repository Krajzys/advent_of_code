from sys import argv

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
    for i, r in enumerate(height_map):
        for j, _ in enumerate(r):
            if check_low_point(i, j, height_map):
                basin_map[i][j] = low_point_count
                low_point_count += 1
            else:
                if height_map[i][j] == 9:
                    basin_map[i][j] = 9
                else:
                    basin_map[i][j] = 0

    for r in basin_map:
        for v in r:
            print(f"{v}", end="")
        print()


if __name__ == "__main__":
    main()