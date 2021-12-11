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

    scores = []
    points_dict = {')': 1, ']': 2, '}': 3, '>': 4}
    brackets_stack = []
    brackets = {'<':'>', '(':')', '[':']', '{':'}'}
    for j, line in enumerate(line_list):
        brackets_stack.clear()
        for i, char in enumerate(line):
            if char in brackets.keys():
                brackets_stack.append(char)
            else:
                open_bracket = brackets_stack.pop()
                allowed_bracket = brackets[open_bracket]
                if not allowed_bracket == char:
                    break
        else:
            if brackets_stack != []:
                score = 0
                for bracket in reversed(brackets_stack):
                    score *= 5
                    score += points_dict[brackets[bracket]]
                scores.append(score)

    print(sorted(scores)[int(len(scores)/2)])


if __name__ == "__main__":
    main()