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

    ranges = []
    for line in line_list:
        _, coords = line.split(': ')
        x, y = coords.split(', ')
        x_range = range(int(x[2:].split('..')[0]), int(x[2:].split('..')[1])+1)
        y_range = range(int(y[2:].split('..')[0]), int(y[2:].split('..')[1])+1)
        ranges.append({"x": x_range, "y": y_range})

    for target in ranges:

        # Find every inital x that at some point lands in the zone at least once
        possible_x_speeds = []
        x_init_speed = 1
        while x_init_speed < target["x"].stop:
            x_pos = 0
            x_speed = x_init_speed
            prev_x_speed = -1
            while x_speed != prev_x_speed and x_pos < target["x"].stop:
                if x_pos in target["x"]:
                    possible_x_speeds.append(x_init_speed)
                    break
                x_pos += x_speed
                prev_x_speed = x_speed
                x_speed -= (1 if x_speed != 0 else 0)
            x_init_speed += 1

        results = []
        for x_init_speed in possible_x_speeds:
            y_init_speed = target["y"].start
            while y_init_speed+1 <= abs(target["y"].start):
                x_speed = x_init_speed
                y_speed = y_init_speed
                x_pos = 0
                y_pos = 0
                max_pos = 0
                while (y_pos >= target["y"].start) and (x_pos < target["x"].stop):
                    if y_pos > max_pos:
                        max_pos = y_pos
                    if (y_pos in target["y"]) and (x_pos in target["x"]):
                        results.append({"x_init": x_init_speed, "y_init": y_init_speed, "max_pos": max_pos})
                        break
                    y_pos += y_speed
                    x_pos += x_speed
                    y_speed -= 1
                    x_speed -= (1 if x_speed > 0 else 0)

                y_init_speed += 1

        print(len(results))


if __name__ == "__main__":
    main()