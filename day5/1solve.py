from sys import argv
from time import sleep

def get_points_between(point1, point2):
    (x1, y1) = point1
    (x2, y2) = point2

    points = []

    if x1 == x2:
        if y1 < y2:
            for i in range(y1, y2+1):
                points.append([x1, i])
        else:
            for i in range(y2, y1+1):
                points.append([x1, i])
    elif y1 == y2:
        if x1 < x2:
            for i in range(x1, x2+1):
                points.append([i, y1])
        else:
            for i in range(x2, x1+1):
                points.append([i, y1])
    
    return points


def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name>")
        exit(1)
    filename = argv[1]
    line_list = [line.strip() for line in open(filename)]

    lines = []
    for line in line_list:
        points = []
        coords = line.split(' -> ')
        for coord in coords:
            points.append(tuple([int(x) for x in coord.split(',')]))
        lines.append(points)

    map_of_vents = {}
    for line in filter(lambda coords: coords[0][0] == coords[1][0] or coords[0][1] == coords[0][1], lines):
        [point1, point2] = line
        points_between = get_points_between(point1, point2)
        for point in points_between:
            key = ",".join([str(x) for x in point])
            if key in map_of_vents.keys():
                map_of_vents[key] += 1
            else:
                map_of_vents[key] = 1

    print(len(list(filter(lambda key: map_of_vents[key] > 1, map_of_vents))))


if __name__ == "__main__":
    main()