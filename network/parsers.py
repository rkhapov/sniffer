import struct
from typing import Optional

import tools.byteprint
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
        try:
            version_header_length, frame_size, identifier, flags_offset, ttl, sub_proto, src, dst = \
                struct.unpack('! B 1x H H H B B 2x 4s 4s', data[:20])
            version = version_header_length >> 4

            if version != 4:
                return None

            header_length = (version_header_length & 0xF) * 4
            flags = to_hexed_int(flags_offset, 4)
            src = tools.byteprint.to_ipv4_address(src)
            dst = tools.byteprint.to_ipv4_address(dst)
            data_ = data[header_length:]

            if sub_proto == _TCP_TYPE:
                transport_frame = self.__tcp.parse(data_)
            elif sub_proto == _UDP_TYPE:
                transport_frame = self.__udp.parse(data_)
            else:
                return None

            return Ipv4Frame(src, dst, identifier, flags, ttl, frame_size, data, transport_frame)
        except struct.error:
            return None


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

            if internet_frame is None:
                return None

            return EthernetFrame(to_mac_address(destination),
                                 to_mac_address(source),
                                 to_hexed_int(type_, 4), sub_frame, data, internet_frame)

        except struct.error:
            return None
