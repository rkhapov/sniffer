from network.frame import Ipv6Frame, Headers
from network.parsers.parser import FrameParser


class Ipv6FrameParser(FrameParser):
    def __init__(self):
        super().__init__('internet')

    def parse(self, data) -> Ipv6Frame:
        return Ipv6Frame(Headers({'data': data}), data)
