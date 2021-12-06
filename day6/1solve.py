from sys import argv

def simulate_day(age_list, days_to_create=7, cooldown_days=2):
    new_fish = []
    for i, age in enumerate(age_list):
        if age == 0:
            new_fish.append(cooldown_days + days_to_create - 1)
        age = (age - 1) if age != 0 else days_to_create-1
        age_list[i] = age

    age_list.extend(new_fish)


def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name>")
        exit(1)
    filename = argv[1]
    line_list = [line for line in open(filename)]
    
    for line in line_list:
        ages = [int(age) for age in line.split(',')]

    for _ in range(80):
        simulate_day(ages)

    print(len(ages))


if __name__ == "__main__":
    main()