from sys import argv

def get_most_common_bits(list_of_binary):
    count_bits = [0 for _ in range(len(list_of_binary[0]))]
    for binary in list_of_binary:
        for i, bit in enumerate(binary):
            if bit == "1":
                count_bits[i] += 1
            else:
                count_bits[i] -= 1
    return "".join(["1" if i >= 0 else "0" for i in count_bits])

def bit_xor(binary):
    return "".join(["1" if i == "0" else "0" for i in binary])

def find_oxygen_rating(list_of_binary, position=0):
    if len(list_of_binary) == 1:
        return list_of_binary[0]
    else:
        common_bits = get_most_common_bits(list_of_binary)
        return find_oxygen_rating(list(filter(lambda x: x[position] == common_bits[position], list_of_binary)), position+1)

def find_co2_rating(list_of_binary, position=0):
    if len(list_of_binary) == 1:
        return list_of_binary[0]
    else:
        uncommon_bits = bit_xor(get_most_common_bits(list_of_binary))
        return find_co2_rating(list(filter(lambda x: x[position] == uncommon_bits[position], list_of_binary)), position+1)

def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name>")
        exit(1)
    filename = argv[1]
    line_list = [line.strip() for line in open(filename)]

    oxygen_rating = find_oxygen_rating(line_list)
    co2_rating = find_co2_rating(line_list)

    print(int(oxygen_rating, 2)*int(co2_rating, 2))


if __name__ == "__main__":
    main()