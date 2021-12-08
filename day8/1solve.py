from sys import argv

def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name>")
        exit(1)
    filename = argv[1]
    line_list = [line for line in open(filename)]

    count = 0
    for line in line_list:
        _, display = line.split(" | ")
        for digit in display.split():
            if len(digit) in [2,3,4,7]:
                count += 1

    print(count)

if __name__ == "__main__":
    main()