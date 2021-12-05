from sys import argv
from functools import reduce

def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name>")
        exit(1)
    filename = argv[1]
    num_list = [int(line) for line in open(filename)]
    sum_num_list = [sum(num_list[i:i+3]) for i in range(len(num_list)-2)]
    
    res_dict = reduce(lambda acc, v: {"count": acc["count"]+1, "val": v} if v > acc["val"] else {"count": acc["count"], "val": v}, sum_num_list, {"count": 0, "val": sum_num_list[0]})
    print(res_dict["count"])


if __name__ == "__main__":
    main()