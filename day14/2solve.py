from sys import argv

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

    occur_dict = {}
    el_dict = {}
    rules = {}
    for line in line_list:
        if occur_dict == {}:
            for i in range(len(line)-1):
                bigram = line[i:i+2]
                el_dict[line[i]] = el_dict.setdefault(line[i], 0) + 1
                occur_dict[bigram] = occur_dict.setdefault(bigram, 0) + 1

            el_dict[line[-1]] = el_dict.setdefault(line[-1], 0) + 1
        elif line != '':
            key, res = line.split(' -> ')
            rules[key] = res

    for _ in range(40):
        occur_dict2 = dict(occur_dict.items())
        for k, v in occur_dict.items():
            new = str(rules[k])
            pair1, pair2 = str(k[0])+new, new+str(k[1])
            el_dict[new] = el_dict.setdefault(new, 0) + v

            occur_dict2[k] -= v
            occur_dict2[pair1] = occur_dict2.setdefault(pair1, 0) + v
            occur_dict2[pair2] = occur_dict2.setdefault(pair2, 0) + v

        occur_dict = dict(occur_dict2.items())

    print(el_dict)
    el_count = sorted([(k, v) for k, v in el_dict.items()], key=lambda x: x[1])
    print(f"{el_count[-1][1]} - {el_count[0][1]} = {el_count[-1][1] - el_count[0][1]}")


if __name__ == "__main__":
    main()