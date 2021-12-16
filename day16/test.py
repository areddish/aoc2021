from day16 import LiteralPacket, PacketDecoder
from day16 import OperatorPacket

print ("D2FE28", end="")
packet = PacketDecoder("D2FE28").read_packet()
assert packet.version == 6
assert packet.type == 4
assert isinstance(packet, LiteralPacket)
assert packet.literal == 2021
print ("... Pass")

print ("38006F45291200", end="")
packet = PacketDecoder("38006F45291200").read_packet()
assert packet.version == 1
assert packet.type == 6
assert isinstance(packet, OperatorPacket)
assert len(packet.sub_packets) == 2
assert isinstance(packet.sub_packets[0], LiteralPacket)
assert packet.sub_packets[0].literal == 10
assert isinstance(packet.sub_packets[1], LiteralPacket)
assert packet.sub_packets[1].literal == 20
assert packet.eval() == 1
print ("... Pass")

print ("EE00D40C823060", end="")
packet = PacketDecoder("EE00D40C823060").read_packet()
assert packet.version == 7
assert packet.type == 3
assert isinstance(packet, OperatorPacket)
assert len(packet.sub_packets) == 3
assert isinstance(packet.sub_packets[0], LiteralPacket)
assert packet.sub_packets[0].literal == 1
assert isinstance(packet.sub_packets[1], LiteralPacket)
assert packet.sub_packets[1].literal == 2
assert isinstance(packet.sub_packets[2], LiteralPacket)
assert packet.sub_packets[2].literal == 3
assert packet.eval() == 3
print ("... Pass")