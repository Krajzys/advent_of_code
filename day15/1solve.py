from sys import argv
from math import inf
from time import sleep

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

    risk_map = []
    for line in line_list:
        risk_map.append([[int(risk), inf] for risk in list(line)])
    risk_map[0][0][1] = 0

    visited = []
    unvisited = []
    for x in range(len(risk_map)):
        for y in range(len(risk_map)):
            unvisited.append((x, y))
    curr_x, curr_y = 0, 0
    while ((len(risk_map)-1, len(risk_map[0])-1) not in visited) and unvisited:
        for x, y in [(-1,0), (1,0), (0,-1), (0,1)]:
            if curr_x + x >= 0 and curr_x + x < len(risk_map) and curr_y + y >= 0 and curr_y + y < len(risk_map[0]):
                if risk_map[curr_x+x][curr_y+y][0] + risk_map[curr_x][curr_y][1] < risk_map[curr_x+x][curr_y+y][1]:
                    risk_map[curr_x+x][curr_y+y][1] = risk_map[curr_x][curr_y][1] + risk_map[curr_x+x][curr_y+y][0]
        visited.append(unvisited.pop(0))
        if unvisited:
            unvisited.sort(key=lambda v: risk_map[v[0]][v[1]][1])
            curr_x, curr_y = unvisited[0]

    print(risk_map[len(risk_map)-1][len(risk_map[0])-1][1])


if __name__ == "__main__":
    main()