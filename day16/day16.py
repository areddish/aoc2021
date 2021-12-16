class Operations:
    @staticmethod
    def op_sum(packets):
        assert len(packets) >= 1
        return sum([x.eval() for x in packets])

    @staticmethod
    def op_product(packets):
        result = 1
        for p in packets:
            result *= p.eval()
        return result

    @staticmethod
    def op_min(packets):
        return min([x.eval() for x in packets])

    @staticmethod
    def op_max(packets):
        return max([x.eval() for x in packets])

    @staticmethod
    def op_greater(packets):
        assert len(packets) == 2
        if packets[0].eval() > packets[1].eval():
            return 1
        else:
            return 0

    @staticmethod
    def op_less(packets):
        assert len(packets) == 2
        if packets[0].eval() < packets[1].eval():
            return 1
        else:
            return 0

    @staticmethod
    def op_equal(packets):                
        assert len(packets) == 2
        if packets[0].eval() == packets[1].eval():
            return 1
        else:
            return 0

    @staticmethod
    def error(packets):
        raise "Unrecoverable error"

class Packet():
    def __init__(self, version, type, bits):
        self.version = version
        self.type = type
        self.bit_count = bits

    def eval(self):
        raise("Not Impl")

class LiteralPacket(Packet):
    def __init__(self, version, type, bits, literal):
        assert type == 4
        super().__init__(version, type, bits)
        self.literal = literal

    def eval(self):
        return self.literal

class OperatorPacket(Packet):
    operations = {
        0: Operations.op_sum,
        1: Operations.op_product,
        2: Operations.op_min,
        3: Operations.op_max,
        5: Operations.op_greater,
        6: Operations.op_less,
        7: Operations.op_equal,
    }

    def __init__(self, version, type, bits, sub_packets):
        super().__init__(version, type, bits)
        self.sub_packets = sub_packets

    def eval(self):
        fn = OperatorPacket.operations.get(self.type, Operations.error)
        return fn(self.sub_packets)

class PacketDecoder:
    def __init__(self,data):
        # Convert input to a stream of binary and read that as text, works as long as the input
        # doesn't become unreasonably large. If so then switch to on demand convert to binary.
        self.data = ""
        for hex_digit in list(data):
            self.data += format(int(hex_digit, 16),'04b')       
        self.read_pos = 0

    def read_bits(self, count):
        if count == 0:
            return 0

        assert self.read_pos + count < len(self.data)
        data = self.data[self.read_pos:self.read_pos+count]
        self.read_pos += count

        return data

    def read_int(self, count):
        return int(self.read_bits(count), 2)
    
    def read_literal(self, version, type_id):
        data = ""
        read = self.read_bits(5)
        bits = 5
        while read[0] == "1":
            data += read[1:]
            read = self.read_bits(5)
            bits += 5
        data += read[1:]
        
        # extra = int(self.read_bits(padding_bits), 2)
        # assert extra == 0
        return LiteralPacket(version, type_id, bits + 6, int(data, 2))

    def read_packet(self):
        version = self.read_int(3)
        type_id = self.read_int(3)

        # literal, pass the type_id in case it isn't hard coded in part 2
        if (type_id == 4): 
            return self.read_literal(version, type_id)
        
        # operator
        length_id = self.read_int(1)
        packet_bit_count = 7 # ver + type + length
        read_bits = 0
        sub_packets = []
        if length_id == 0:
            total_length = self.read_int(15)
            packet_bit_count += 15
            read_bits = 0
            while read_bits < total_length:
                packet = self.read_packet()
                sub_packets.append(packet)
                read_bits += packet.bit_count
                packet_bit_count += packet.bit_count
            assert read_bits == total_length
        else:
            assert length_id == 1
            number_of_sub_packets = self.read_int(11)
            packet_bit_count += 11
            for x in range(number_of_sub_packets):
                packet = self.read_packet()
                sub_packets.append(packet)
                packet_bit_count += packet.bit_count
        
        # FUTURE: could pass the length_id and compute bits in the packet
        return OperatorPacket(version, type_id, packet_bit_count, sub_packets)

if __name__ == "__main__":
    with open("day16.txt", "rt") as file:
        data = [x.strip() for x in file.readlines()]
        assert len(data) == 1

        decoder = PacketDecoder(data[0])
        packet = decoder.read_packet()

        def get_packet_version_sum(packet):
            version_sum = packet.version
            for sub_packet in packet.sub_packets:
                if isinstance(sub_packet, LiteralPacket):
                    version_sum += sub_packet.version
                else:
                    version_sum += get_packet_version_sum(sub_packet)
            return version_sum

        print(f"Part 1 = {get_packet_version_sum(packet)}")
        print(f"Part 2 = {packet.eval()}")
