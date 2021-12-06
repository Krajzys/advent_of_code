from sys import argv

def print_sorted_dict(dict):
    print("{", end="")
    for k in sorted(dict.keys()):
        print(f"{k}: {dict[k]}, ", end="")
    bs = '\b\b'
    print(f"{bs if len(dict.keys()) > 0 else ''}}}")


def simulate_day(age_dict, days_to_create=7, cooldown_days=2):
    sorted_ages = sorted(age_dict.keys())
    new_age_dict = {}
    for age in sorted_ages:
        new_age_dict.update({age-1: age_dict[age]})
    
    if -1 in new_age_dict.keys():
        to_create = new_age_dict.pop(-1)
        new_age_dict[cooldown_days + days_to_create - 1] = to_create
        if days_to_create - 1 in new_age_dict.keys():
            new_age_dict[days_to_create - 1] += to_create
        else:
            new_age_dict[days_to_create - 1] = to_create

    return new_age_dict


def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name> <iter_days=256>")
        exit(1)

    filename = argv[1]
    iter_days = 256

    if len(argv) == 3:
        iter_days = int(argv[2])

    line_list = [line for line in open(filename)]
    
    for line in line_list:
        ages = [int(age) for age in line.split(',')]

    age_dict = {}
    for age in ages:
        if age in age_dict.keys():
            age_dict[age] += 1
        else:
            age_dict[age] = 1

    res_age_dict = age_dict
    for _ in range(iter_days):
        res_age_dict = simulate_day(res_age_dict)

    print(sum(res_age_dict.values()))


if __name__ == "__main__":
    main()