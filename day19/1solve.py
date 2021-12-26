from sys import argv
from progress import Progress
import data


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
    dis2 = list(abs(x) for x in dis2[:])
    for i in dis1:
        if abs(i) in dis2:
            dis2.remove(abs(i))
            continue
        break
    else:
        return True
    return False


def get_intersect_len(list1, list2):
    intersect = 0
    for v in list1:
        for v2 in list2:
            if is_same_b2b_dist(v, v2):
                intersect += 1
    return intersect


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

    export_data = False
    if '-e' in argv:
        export_data = True

    import_data = False
    if '-i' in argv:
        import_data = True

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

    overlaps = dict()
    if not import_data:
        count = 1
        progress = Progress(0, len(in_scanner_distances) **
                            2 - len(in_scanner_distances))
        print('Determining overlapping scanners...')
        for scanner_no, poss_dist in in_scanner_distances.items():
            for scanner_no_2, poss_dist2 in in_scanner_distances.items():
                progress.print()
                if scanner_no == scanner_no_2:
                    continue
                for from_no, dist in poss_dist.items():
                    for from_no2, dist2 in poss_dist2.items():
                        intersect_len = get_intersect_len(
                            dist.values(), dist2.values())
                        if intersect_len >= 11:
                            if (scanner_no, scanner_no_2) not in overlaps and (scanner_no_2, scanner_no) not in overlaps:
                                overlaps[(scanner_no, scanner_no_2)] = (
                                    from_no, from_no2)
                progress.update(count)
                count += 1

    if export_data:
        with open('data.py', 'w') as file:
            file.write('overlaps = ' + str(overlaps))

    if import_data:
        overlaps = data.overlaps

    uniq_beacons = []
    for si, s in enumerate(scanners):
        for bi, b in enumerate(s):
            uniq_beacons.append((si, bi))

    print(len(uniq_beacons))

    same_beacons = {}
    for (s1, s2), (f1, f2) in overlaps.items():
        beacons = in_scanner_distances[s1][f1]
        beacons2 = in_scanner_distances[s2][f2]
        same_beacons[(s1, f1)] = set()
        same_beacons[(s1, f1)].add((s2, f2))

        for k, v in beacons.items():
            for k2, v2 in beacons2.items():
                if is_same_b2b_dist(v, v2):
                    if (s1, k) not in same_beacons:
                        same_beacons[(s1, k)] = set()
                    same_beacons[(s1, k)].add((s2, k2))

    print(f"Same beacons ({len(same_beacons)}):")
    for k, v in same_beacons.items():
        print(k, v)

    merged = {}
    for k, v in same_beacons.items():
        merged[k] = v.copy()

    # Phase 1 - Reduce keys that are also in values
    # for every key and values:
    #   for every value in values:
    #     if value in all_keys:
    #       values = values.union(whole.pop(value))
    # dict{(1,2): {(2,3)},
    #      (1,3): {(2,3)},
    #      (3,4): {(1,2),(1,3)}
    # }
    # dict{(1,3): {(2,3)},
    #      (3,4): {(1,2),(1,3),(2,3)}
    # }
    # dict{(3,4): {(1,2),(1,3),(2,3),(1,3)}}

    popped = set()
    for k, vals in merged.items():
        new_vals = vals.copy()
        for v in vals:
            if v in merged and v not in popped:
                new_vals = new_vals.union(merged[v])
                popped.add(v)
        merged[k] = new_vals

    for i in popped:
        merged.pop(i)

    print(f"Popped: {popped}")
    print(f"Merged P1 ({len(merged)}):")
    for k, v in merged.items():
        print(k, v)

    # Phase 2 - Match beacons if the overlapping beacon only appears in values
    # For every key and values:
    #   For every value in values:
    #     For every key2 and values2:
    #       If value in values2:
    #         values.add(key2)
    #         values = values.union(whole.pop(key2))
    #         break
    # dict{(1,2): {(2,3)},
    #      (1,3): {(2,3),(3,4),(4,5)}}
    # dict{(1,2): {(2,3),(1,3),(2,3),(3,4),(4,5)}}

    popped.clear()
    checked = set()
    for k, vals in merged.items():
        new_vals = vals.copy()
        for v in vals:
            for k2, vals2 in merged.items():
                if k == k2:
                    continue
                if v in vals2 and k2 not in popped:
                    if k2 not in checked:
                        popped.add(k2)
                    new_vals = new_vals.union(merged[k2])
                    new_vals.add(k2)
        checked.add(k)
        merged[k] = new_vals

    print("Popping:")
    for i in popped:
        print(i, merged[i])
        merged.pop(i)

    all_vals = set()
    for k, v in merged.items():
        all_vals = all_vals.union(v)

    print(f"Popped: {popped}")
    print(f"Merged P2 ({len(merged)}):")
    for k, v in merged.items():
        print(k, v)

    print(len(uniq_beacons))

    # Remove overlapping beacons (leaves only the beacon that is the key in the dictionary)
    for (s, b), non_uniques in merged.items():
        for n in non_uniques:
            if (s, b) == n:
                continue
            uniq_beacons.remove(n)

    print(len(uniq_beacons), len(all_vals))


if __name__ == "__main__":
    main()
