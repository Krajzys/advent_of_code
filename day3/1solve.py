from sys import argv

def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name>")
        exit(1)
    filename = argv[1]
    line_list = [line.strip() for line in open(filename)]

    count_bits = [0 for _ in range(len(line_list[0]))]
    for binary in line_list:
        for i, bit in enumerate(binary):
            if bit == "1":
                count_bits[i] += 1
            else:
                count_bits[i] -= 1

    res = 0
    for occurances in count_bits:
        if occurances >= 0:
            res |= 1
        
        res <<= 1
    res >>= 1
    res2 = res^(2**len(count_bits)-1)
    print(res * res2)

if __name__ == "__main__":
    main()