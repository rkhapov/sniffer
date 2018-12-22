import struct
from typing import Optional

from network.frame import EthernetFrame, Headers
from network.parsers.parser import FrameParser

_FRAME_FORMAT = '! 6s 6s 2s'


class EthernetFrameParser(FrameParser):
    def __init__(self):
        super().__init__('link')

    def parse(self, data) -> Optional[EthernetFrame]:
        try:
            destination, source, protocol, proto_data = struct.unpack(_FRAME_FORMAT + f'{len(data) - 14}s', data)
            headers = Headers()\
                .add('destination', destination)\
                .add('source', source)\
                .add('protocol', protocol)\
                .add('data', proto_data)

            return EthernetFrame(headers, data)
        except struct.error:
            return None
