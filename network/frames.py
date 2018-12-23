from tools.byteprint import *
from abc import abstractmethod, ABC


class Frame:
    def __init__(self, layer, protocol, raw):
        self.__layer = layer
        self.__protocol = protocol
        self.__raw = raw

    @abstractmethod
    def get_description(self, tab):
        raise NotImplementedError

    @property
    def layer(self):
        return self.__layer

    @property
    def protocol(self):
        return self.__protocol

    @property
    def raw(self):
        return self.__raw


class TransportFrame(Frame, ABC):
    def __init__(self, protocol, raw):
        super().__init__('transport', protocol, raw)


class InternetFrame(Frame, ABC):
    def __init__(self, protocol, raw, transport_frame: TransportFrame):
        super().__init__('internet', protocol, raw)
        self.__transport_frame = transport_frame

    @property
    def transport_frame(self):
        return self.__transport_frame


class LinkFrame(Frame, ABC):
    def __init__(self, protocol, raw, internet_frame: InternetFrame):
        super().__init__('link', protocol, raw)
        self.__internet_frame = internet_frame

    @property
    def internet_frame(self):
        return self.__internet_frame


class TcpFrame(TransportFrame):
    def __init__(self, raw):
        super().__init__('tcp', raw)

    def get_description(self, tab):
        return tab + 'i am tcp frame'


class UdpFrame(TransportFrame):
    def __init__(self, src_port, dst_port, length, data, raw):
        super().__init__('udp', raw)
        self.__src_port = src_port
        self.__dst_port = dst_port
        self.__length = length
        self.__data = data

    @property
    def source_port(self):
        return self.__src_port

    @property
    def destination_port(self):
        return self.__dst_port

    @property
    def length(self):
        return self.__length

    @property
    def data(self):
        return self.__data

    def get_description(self, tab):
        return \
            f'{tab}User Datagram Protocol\n'\
            f'{tab}Source Port: {self.__src_port}\n'\
            f'{tab}Destination Port: {self.__dst_port}\n'\
            f'{tab}Length: {self.__length}\n'\
            f'{to_hex_dump(self.data, tab=tab)}'


class Ipv4Frame(InternetFrame):
    def __init__(self, src, dst, identifier, flags, ttl, size, raw, transport_frame: TransportFrame):
        super().__init__('ipv4', raw, transport_frame)
        self.__src = src
        self.__dst = dst
        self.__ttl = ttl
        self.__flags = flags
        self.__size = size
        self.__identifier = identifier

    @property
    def identifier(self):
        return self.__identifier

    @property
    def src(self):
        return self.__src

    @property
    def dst(self):
        return self.__dst

    @property
    def flags(self):
        return self.__flags

    @property
    def ttl(self):
        return self.__ttl

    @property
    def size(self):
        return self.__size

    def get_description(self, tab):
        return \
            f'{tab}Internet IPv4 Frame\n' \
            f'{tab}Source: {self.src}\n' \
            f'{tab}Destination: {self.dst}\n' \
            f'{tab}Identifier: {self.identifier}\n' \
            f'{tab}Flags: {self.flags}\n' \
            f'{tab}TTL: {self.ttl}\n' \
            f'{tab}Size: {self.size}\n' \
            f'{self.transport_frame.get_description(tab + " ")}'


class Ipv6Frame(InternetFrame):
    def __init__(self, raw, transport_frame: TransportFrame):
        super().__init__('ipv6', raw, transport_frame)

    def get_description(self, tab):
        return tab + 'i am ipv6 frame:\n' + self.transport_frame.get_description(tab + ' ')


class EthernetFrame(LinkFrame):
    def __init__(self, destination, source, type_, data, raw, internet_frame: InternetFrame):
        super().__init__('ethernet', raw, internet_frame)
        self.__destination = destination
        self.__source = source
        self.__type = type_
        self.__data = data

    @property
    def destination(self):
        return self.__destination

    @property
    def source(self):
        return self.__source

    @property
    def type(self):
        return self.__type

    @property
    def data(self):
        return self.__data

    def get_description(self, tab=''):
        return tab + 'Ethernet frame:\n' \
            f'{tab}Destination: {self.destination}\n' \
            f'{tab}Source: {self.source}\n' \
            f'{tab}Type: {self.type}\n' \
            f'{self.internet_frame.get_description(tab + " ")}'


link_frame_classes = LinkFrame.__subclasses__()
internet_frame_classes = InternetFrame.__subclasses__()
transport_frame_classes = TransportFrame.__subclasses__()
