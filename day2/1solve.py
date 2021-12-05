from sys import argv

def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name>")
        exit(1)
    filename = argv[1]
    line_list = [line for line in open(filename)]

    distance = 0
    depth = 0
    for line in line_list:
        command, value = line.split(' ')
        if command == 'forward':
            distance += int(value)
        elif command == 'down':
            depth += int(value)
        elif command == 'up':
            depth -= int(value)

    print(f"distance: {distance}, depth: {depth}, result: {distance*depth}")


if __name__ == "__main__":
    main()