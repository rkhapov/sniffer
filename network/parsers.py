import struct
from typing import Optional
from tools.byteprint import *

from network.frames import *

_IPV4_TYPE = 0x0800
_IPV6_TYPE = 0x86DD
_TCP_TYPE = 6
_UDP_TYPE = 17


class FrameParser:
    def parse(self, data) -> Optional[Frame]:
        raise NotImplementedError


class LinkFrameParser(FrameParser):
    def parse(self, data) -> Optional[LinkFrame]:
        raise NotImplementedError


class InternetFrameParser(FrameParser):
    def parse(self, data) -> Optional[InternetFrame]:
        raise NotImplementedError


class TransportFrameParser(FrameParser):
    def parse(self, data) -> Optional[TransportFrame]:
        raise NotImplementedError


class TcpFrameParser(TransportFrameParser):
    def parse(self, data) -> Optional[TcpFrame]:
        return TcpFrame(data)


class UdpFrameParser(TransportFrameParser):
    def parse(self, data) -> Optional[UdpFrame]:
        return UdpFrame(data)


class Ipv4FrameParser(InternetFrameParser):
    def __init__(self, tcp: TcpFrameParser, udp: UdpFrameParser):
        self.__tcp = tcp
        self.__udp = udp

    def parse(self, data) -> Optional[Ipv4Frame]:
        return Ipv4Frame(data, self.__tcp.parse(data))


class Ipv6FrameParser(InternetFrameParser):
    def __init__(self, tcp: TcpFrameParser, udp: UdpFrameParser):
        self.__tcp = tcp
        self.__udp = udp

    def parse(self, data) -> Optional[Ipv6Frame]:
        return Ipv6Frame(data, self.__udp.parse(data))


class EthernetFrameParser(LinkFrameParser):
    def __init__(self, ipv4: Ipv4FrameParser, ipv6: Ipv6FrameParser):
        self.__ipv4 = ipv4
        self.__ipv6 = ipv6

    def parse(self, data) -> Optional[EthernetFrame]:
        try:
            destination, source, type_, sub_frame = struct.unpack(f'! 6s 6s H {len(data) - 14}s', data)

            if type_ == _IPV4_TYPE:
                internet_frame = self.__ipv4.parse(sub_frame)
            elif type_ == _IPV6_TYPE:
                internet_frame = self.__ipv6.parse(sub_frame)
            else:
                return None

            return EthernetFrame(to_mac_address(destination),
                                 to_mac_address(source),
                                 to_hexed_int(type_, 4), sub_frame, data, internet_frame)

        except struct.error:
            return None
