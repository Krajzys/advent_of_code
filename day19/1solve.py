from sys import argv

def parse_input(line_list) -> list:
    scanners = []
    scanner = []
    for line in line_list:
        if line != '':
            if line.startswith('---'):
                if scanner:
                    scanners.append(scanner)
                scanner = []
            else:
                scanner.append([int(x) for x in line.split(',')])
    if scanner:
        scanners.append(scanner)

    return scanners


def get_b2b_dist(from_beacon, to_beacon):
    return (to_beacon[0] - from_beacon[0], to_beacon[1] - from_beacon[1], to_beacon[2] - from_beacon[2])


def is_same_b2b_dist(dis1, dis2):
    dis1 = dis1[:]
    dis2 = list(dis2[:])
    for i in dis1:
        if abs(i) in dis2:
            dis2.remove(abs(i))
            continue
        elif i in dis2:
            dis2.remove(i)
            continue
        break
    else:
        return True
    return False


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

    scanners = parse_input(line_list)
    in_scanner_distances = {}
    for i, b in enumerate(scanners):
        scanner_distances = {}
        for i2, b2 in enumerate(b):
            b2b_distances = {}
            for j2, c2 in enumerate(b):
                if i2 == j2:
                    continue
                b2b_distances[j2] = get_b2b_dist(b2, c2)
            scanner_distances[i2] = b2b_distances
        in_scanner_distances[i] = scanner_distances


if __name__ == "__main__":
    main()
