from sys import argv

def decode_display(display, codes_to_digits):
    res = ""
    for code in display:
        res += str(codes_to_digits[code])

    return int(res)


def inferr_digits(scrambled_digits):
    digits = {}
    for code in scrambled_digits:
        if len(code) == 2:
            digits[1] = code
        elif len(code) == 3:
            digits[7] = code
        elif len(code) == 4:
            digits[4] = code
        elif len(code) == 7:
            digits[8] = code

    set_1 = set(digits[1])
    set_4 = set(digits[4])
    for code in scrambled_digits:
        set_code = set(code)
        if len(code) == 6:
            if len(set_code.difference(set_1)) == 5:
                digits[6] = code
            elif len(set_code.difference(set_1)) == 4:
                if len(set_code.difference(set_4)) == 2:
                    digits[9] = code
                elif len(set_code.difference(set_4)) == 3:
                    digits[0] = code
        elif len(code) == 5:
            if len(set_code.difference(set_4)) == 3:
                digits[2] = code
            elif len(set_code.difference(set_4)) == 2:
                if len(set_code.difference(set_1)) == 3:
                    digits[3] = code
                elif len(set_code.difference(set_1)) == 4:
                    digits[5] = code

    code_to_digit = {}
    for k, v in digits.items():
        code_to_digit[v] = k

    return code_to_digit


def main():
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <file_name>")
        exit(1)
    filename = argv[1]
    line_list = [line for line in open(filename)]

    res = 0
    for line in line_list:
        unique_values, display = line.split(" | ")
        unique_values = unique_values.split()
        unique_values = ["".join(sorted(list(val))) for val in unique_values]
            
        display = display.split()
        display = ["".join(sorted(list(val))) for val in display]
        
        codes_to_digits = inferr_digits(unique_values)
        res += decode_display(display, codes_to_digits) 

    print(res)

if __name__ == "__main__":
    main()