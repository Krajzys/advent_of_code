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

    dots = []
    folds = []
    for line in line_list:
        if line != '' and not line.startswith('fold'):
            dots.append(tuple([int(val) for val in line.split(',')]))
        elif line.startswith('fold'):
            axis, value = line.split(' ')[2].split('=')
            folds.append((axis, int(value)))

    axis, coord = folds[0]
    new_dots = []
    if axis == 'x':
        for dot in dots:
            if dot[0] > coord and dot not in new_dots:
                new_dots.append((coord - (dot[0] - coord), dot[1]))
        new_dots.extend(filter(lambda x: (x[0] < coord) and (x not in new_dots), dots))
    elif axis == 'y':
        for dot in dots:
            if dot[1] > coord and dot not in new_dots:
                new_dots.append((dot[0], coord - (dot[1] - coord)))
        new_dots.extend(filter(lambda x: (x[1] < coord) and (x not in new_dots), dots))
    else:
        print('Unknown axis!')
        exit(1)

    print(len(new_dots))


if __name__ == "__main__":
    main()