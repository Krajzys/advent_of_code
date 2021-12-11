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

    points = 0
    points_dict = {')': 3, ']': 57, '}': 1197, '>': 25137}
    brackets_stack = []
    brackets = {'<':'>', '(':')', '[':']', '{':'}'}
    for line in line_list:
        brackets_stack.clear()
        for char in line:
            if char in brackets.keys():
                brackets_stack.append(char)
            else:
                open_bracket = brackets_stack.pop()
                allowed_bracket = brackets[open_bracket]
                if not allowed_bracket == char:
                    points += points_dict[char]
                    break

    print(points)


if __name__ == "__main__":
    main()