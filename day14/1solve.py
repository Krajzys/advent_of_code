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

    polymer_template = ''
    rules = {}
    for line in line_list:
        if polymer_template == '':
            polymer_template = line
        elif line != '':
            key, res = line.split(' -> ')
            rules[key] = res

    for _ in range(10):
        new_polymer = polymer_template[0]
        for i in range(len(polymer_template)-1):
            insertion = ''
            pair = polymer_template[i:i+2]
            if pair in rules.keys():
                insertion = rules[pair]
            new_polymer += insertion + pair[1]
        polymer_template = new_polymer

    polymer_template_list = list(polymer_template)
    element_occurances = list(sorted([(el, polymer_template_list.count(el)) for el in set(polymer_template_list)], key=lambda x: x[1]))
    print(element_occurances)
    print(element_occurances[-1][1]-element_occurances[0][1])


if __name__ == "__main__":
    main()