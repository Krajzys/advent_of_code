from sys import argv

def print_board_from_dots(dots):
    board = []
    for dot in dots:
        while dot[1] >= len(board):
            board.append([])
        while dot[0] >= len(board[dot[1]]):
            board[dot[1]].append(' ')
        board[dot[1]][dot[0]] = 'X'
    
    for line in board:
        for val in line:
            print(val, end="")
        print()


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

    new_dots = []
    for fold in folds:
        axis, coord = fold
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
        dots = new_dots[:]

    print_board_from_dots(new_dots)


if __name__ == "__main__":
    main()