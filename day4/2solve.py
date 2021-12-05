from sys import argv

def cross_number_on_boards(boards, number) -> list:
    won_boards = []
    for i, board in enumerate(boards):
        for line in board:
            if number in line:
                line[line.index(number)] = 'X'
        if check_win_on_board(board):
            won_boards.append(i)
    return won_boards

def check_win_on_board(board) -> bool:
    col_count = [0 for _ in board[0]]
    for line in board:
        if line.count('X') == 5:
            return True
        for i, number in enumerate(line):
            if number == 'X':
                col_count[i] += 1

    if 5 in col_count:
        return True

    return False


def count_points(board, last_num) -> int:
    points = 0
    for line in board:
        for number in line:
            if number != 'X':
                points += int(number)

    return points*last_num


def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <input_file>")
        exit(1)
    
    filename = argv[1]
    with open(filename, 'r') as file:
        numbers = file.readline().strip().split(',')
        file.readline()

        boards = []
        board = []
        for line in file:
            if line.strip() == '':
                boards.append(board)
                board = []
                continue
            board.append(line.split())
        boards.append(board)
        board = []

        for number in numbers:
            res = cross_number_on_boards(boards, number)

            if res != []:
                print(f"Board{'s' if len(res) > 1 else ''} {res} {'have' if len(res) > 1 else 'has'} won!")
                print(f"Last number was {number}")
                for i in res:
                    print(f"Points = {count_points(boards[i], int(number))}")
                for i, ind in enumerate(res):
                    boards.pop(ind-i)


if __name__ == '__main__':
    main()