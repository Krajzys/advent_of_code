from sys import argv
from math import inf

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
        for i in range(1, 5):
            risk_map[-1].extend([[(i + int(risk) % 10) if i + int(risk) < 10 else 1 + ((i + int(risk)) % 10), inf] for risk in list(line)])
        
    orig_len = len(risk_map)
    for i in range(1, 5):
        for risks in risk_map[:orig_len]:
            risk_map.append([[(i + risk[0]) % 10 if i + risk[0] < 10 else 1 + ((i + risk[0]) % 10), inf] for risk in risks])
    risk_map[0][0][1] = 0

    risk_map_len = len(risk_map)
    visited = []
    unvisited = [(0,0)]
    
    curr_x, curr_y = 0, 0
    while ((len(risk_map)-1, len(risk_map[0])-1) not in visited) and unvisited:
        for x, y in [(-1,0), (1,0), (0,-1), (0,1)]:
            if curr_x + x >= 0 and curr_x + x < len(risk_map) and curr_y + y >= 0 and curr_y + y < len(risk_map[0]):
                if risk_map[curr_x+x][curr_y+y][0] + risk_map[curr_x][curr_y][1] < risk_map[curr_x+x][curr_y+y][1]:
                    risk_map[curr_x+x][curr_y+y][1] = risk_map[curr_x][curr_y][1] + risk_map[curr_x+x][curr_y+y][0]
                if (curr_x + x, curr_y + y) not in unvisited and (curr_x + x, curr_y + y) not in visited:
                    unvisited.append((curr_x + x, curr_y + y))
        visited.append((curr_x, curr_y))
        if unvisited:
            next = min(unvisited, key=lambda v: risk_map[v[0]][v[1]][1]+(risk_map_len-v[0] + risk_map_len-v[1]))
            unvisited.remove(next)
            curr_x, curr_y = next

    print(risk_map[len(risk_map)-1][len(risk_map[0])-1][1])


if __name__ == "__main__":
    main()