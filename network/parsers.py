import struct
from typing import Optional

import tools.byteprint
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
    def parse(self, raw) -> Optional[TcpFrame]:
        try:
            src, dst, seq_num, ack_num, do_flags, window_size, urgent_pointer = \
                struct.unpack('! H H 4s 4s H H 2x H', raw[:20])

            data_offset = (do_flags >> 12) * 4

            flags = do_flags & 0x1FF
            urg = (flags & 32) >> 5
            ack = (flags & 16) >> 4
            psh = (flags & 8) >> 3
            rst = (flags & 4) >> 2
            syn = (flags & 2) >> 1
            fin = (flags & 1) >> 0

            data = raw[data_offset:]

            return TcpFrame(src, dst, get_bytes_str(seq_num), get_bytes_str(ack_num), data_offset,
                            urg, ack, psh, rst, syn, fin,
                            window_size, urgent_pointer, data, raw)
        except struct.error:
            return None


class UdpFrameParser(TransportFrameParser):
    def parse(self, raw) -> Optional[UdpFrame]:
        try:
            src_port, dst_port, length, data = struct.unpack(f'! H H H 2x {len(raw) - 8}s', raw)

            return UdpFrame(src_port, dst_port, length, data, raw)
        except struct.error:
            return None


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

    def parse(self, raw) -> Optional[Ipv6Frame]:
        try:
            ver_tc_fw, payload_length, next_header, hop_limit, src, dst = struct.unpack(f'! I H B B 16s 16s', raw[:40])

            version = ver_tc_fw >> 28

            if version != 6:
                return None

            traffic_class = to_hexed_int((ver_tc_fw >> 20) & 0xFF, 1)
            flow_label = to_hexed_int(ver_tc_fw & 0xFFFFF, 3)

            if next_header == _TCP_TYPE:
                transport_frame = self.__tcp.parse(raw[payload_length:])
            elif next_header == _UDP_TYPE:
                transport_frame = self.__udp.parse(raw[payload_length:])
            else:
                return None

            if transport_frame is None:
                return None

            return Ipv6Frame(traffic_class, flow_label, payload_length, to_hexed_int(next_header, 1), hop_limit,
                             to_ipv6_address(src), to_ipv6_address(dst), raw, transport_frame)
        except struct.error:
            return None


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
