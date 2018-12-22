import struct
from typing import Iterable, Optional

from network.frame import Frame, EthernetFrame
from network.parsers.ethernet import EthernetFrameParser
from network.parsers.ipv4 import Ipv4FrameParser
from network.parsers.ipv6 import Ipv6FrameParser
from network.raw import RawFrameGenerator

_IPV4_TYPE = 0x0800
_IPV6_TYPE = 0x86DD

ethernet_parser = EthernetFrameParser()
ipv4_parser = Ipv4FrameParser()
ipv6_parser = Ipv6FrameParser()


def _parse_internet(ethernet_frame: EthernetFrame):
    data_ = ethernet_frame.headers['data']
    type_ = struct.unpack('!H', ethernet_frame.headers['protocol'])[0]

    if type_ == _IPV4_TYPE:
        ip_parser = ipv4_parser
    elif type_ == _IPV6_TYPE:
        ip_parser = ipv6_parser
    else:
        return None

    ip_frame = ip_parser.parse(data_)

    if ip_frame is None:
        return None

    ethernet_frame.headers['data'] = ip_frame

    return ethernet_frame


def _parse_link(data_) -> Optional[Frame]:
    ethernet = ethernet_parser.parse(data_)

    if ethernet is None:
        return None

    return _parse_internet(ethernet)


class FrameGenerator:
    def __init__(self, raw: RawFrameGenerator):
        self.__raw = raw

    def get_next(self) -> Frame:
        while True:
            frame = _parse_link(self.__raw.recv_next())

            if frame is not None:
                return frame

    def get_all(self) -> Iterable[Frame]:
        while True:
            yield self.get_next()
