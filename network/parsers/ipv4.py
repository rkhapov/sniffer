from network.frame import Ipv4Frame, Headers
from network.parsers.parser import FrameParser


class Ipv4FrameParser(FrameParser):
    def __init__(self):
        super().__init__('internet')

    def parse(self, data) -> Ipv4Frame:
        return Ipv4Frame(Headers({'data': data}), data)
