from sys import argv

def bfs_kindof(graph, start_node, path):
    lower_occurs = [path.count(lower_nodes) for lower_nodes in filter(lambda n: n == n.lower(), path)]
    new_rule = False
    if lower_occurs != []:
        new_rule = (max(lower_occurs) > 1)
    if start_node == 'end' or ((start_node == start_node.lower()) and (start_node in path) and (new_rule)) or (start_node == 'start' and start_node in path):
        if start_node == 'end':
            path.append('end')
            return 1
        return 0
    path.append(start_node)
    successors = graph[start_node]
    result = 0
    for s in successors:
        path2 = path[:]
        result += bfs_kindof(graph, s, path2)
    return result


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

    graph = {}
    for line in line_list:
        ln, rn = line.split('-')
        if ln in graph.keys():
            if rn not in graph[ln]:
                graph[ln].append(rn)
        else:
            graph[ln] = [rn]
        if rn in graph.keys():
            if ln not in graph[rn]:
                graph[rn].append(ln)
        else:
            graph[rn] = [ln]

    path = []
    paths_count = bfs_kindof(graph, 'start', path)
    print(paths_count)


if __name__ == "__main__":
    main()
