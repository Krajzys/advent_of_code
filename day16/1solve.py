from os import read
from sys import argv, version

class Packet:
    def __init__(self):
        self.type = ''
        self.version = ''
        self.len_type = ''
        self.packets = []
        self.value = ''

    def sum_version(self):
        res = self.get_version()
        for p in self.packets:
            res += p.sum_version()
        return res

    def get_value(self, in_binary=False):
        return self.value if in_binary else int(self.value, 2)

    def get_version(self, in_binary=False):
        return self.version if in_binary else int(self.version, 2)

    def __repr__(self):
        if self.type == '100':
            return f"{self.version} {self.type} {self.value} ({self.get_value()})"
        else:
            repr_str = f"{self.version} {self.type} {self.len_type} ({len(self.packets)=})"
            for subpacket in self.packets:
                repr_str += "\n  " + str(subpacket)
            return repr_str


def read_bits(bits, count, offset):
    bit_str = ''
    for i in range(offset, offset + count):
        bit_str += bits[i]
    return bit_str


def parse_packet(packet, offset=0):
    bin_packet = hex_2_bin(packet)
    bits_read = offset
    # print(f"{bin_packet=}, {packet=}, {offset=}")
    parsed_packet = Packet()

    parsed_packet.version = read_bits(bin_packet, 3, bits_read)
    bits_read += 3

    parsed_packet.type = read_bits(bin_packet, 3, bits_read)
    bits_read += 3
    print(f"{parsed_packet.version=}, {parsed_packet.type=}")

    value_str = ''
    if parsed_packet.type == '100': # Literal value
        segment = read_bits(bin_packet, 5, bits_read)
        bits_read += 5

        value_str += segment[1:]
        while segment[0] == '1':
            segment = read_bits(bin_packet, 5, bits_read)
            bits_read += 5

            value_str += segment[1:]
        parsed_packet.value = value_str
        # print(f"{value_str=} {int(value_str,2)=}")
        return parsed_packet, bits_read
    else: # Operation
        parsed_packet.len_type = read_bits(bin_packet, 1, bits_read)
        bits_read += 1
        print(f"{parsed_packet.len_type=}")

        if parsed_packet.len_type == '0': # Bit count
            bit_count = read_bits(bin_packet, 15, bits_read)
            bits_read += 15
            start_bits_read = bits_read
            print(f"{bits_read=}, {start_bits_read=}, {bit_count=}")
            while bits_read < start_bits_read + int(bit_count, 2):
                subpacket, bits_read = parse_packet(packet, bits_read)
                parsed_packet.packets.append(subpacket)

                print(parsed_packet)
        elif parsed_packet.len_type == '1': # Sub-packet count
            packet_count = read_bits(bin_packet, 11, bits_read)
            bits_read += 11
            print(f"{packet_count=}")

            for _ in range(int(packet_count, 2)):
                subpacket, bits_read = parse_packet(packet, bits_read)
                parsed_packet.packets.append(subpacket)

        return parsed_packet, bits_read


def hex_2_bin(hex):
    hex_int = int(hex, 16)
    bin_str = ''
    for _ in hex:
        for _ in range(4):
            bin_str = str(hex_int & 1) + bin_str
            hex_int >>= 1
    # print(f"{hex=}: {bin_str=}")
    return bin_str


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

    for line in line_list:
        packet, bits_read = parse_packet(line)
        
        print(packet)
        print(packet.sum_version())

if __name__ == "__main__":
    main()