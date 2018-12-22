from typing import Iterable

from network.frames import EthernetFrame
from network.parsers import EthernetFrameParser
from network.raw import RawFrameGenerator


class FrameGenerator:
    def __init__(self, raw: RawFrameGenerator, ethernet_parser: EthernetFrameParser):
        self.__raw = raw
        self.__ethernet = ethernet_parser

    def get_next(self) -> EthernetFrame:
        while True:
            frame = self.__ethernet.parse(self.__raw.recv_next())

            if frame is not None:
                return frame

    def get_all(self) -> Iterable[EthernetFrame]:
        while True:
            yield self.get_next()
