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
    def __init__(self, src, dst, sequence_number, ack_number, data_offset, urg, ack, psh, rst, syn, fin, window_size, urgent_pointer, data, raw):
        super().__init__('tcp', raw)
        self.__src = src
        self.__dst = dst
        self.__sequence_number = sequence_number
        self.__ack_number = ack_number
        self.__data_offset = data_offset
        self.__window_size = window_size
        self.__data = data
        self.__urgent_pointer = urgent_pointer
        self.__urg = urg
        self.__ack = ack
        self.__psh = psh
        self.__rst = rst
        self.__syn = syn
        self.__fin = fin

    @property
    def urg(self):
        return self.__urg

    @property
    def ack(self):
        return self.__ack

    @property
    def psh(self):
        return self.__psh

    @property
    def rst(self):
        return self.__rst

    @property
    def syn(self):
        return self.__syn

    @property
    def fin(self):
        return self.__fin

    @property
    def src(self):
        return self.__src

    @property
    def dst(self):
        return self.__dst

    @property
    def sequence_number(self):
        return self.__sequence_number

    @property
    def ack_number(self):
        return self.__ack_number

    @property
    def data_offset(self):
        return self.__data_offset

    @property
    def window_size(self):
        return self.__window_size

    @property
    def urgent_pointer(self):
        return self.__urgent_pointer

    @property
    def data(self):
        return self.__data

    def get_description(self, tab):
        return \
            f'{tab}Transmission Control Protocol (TCP)\n' \
            f'{tab}Source Port: {self.src}\n' \
            f'{tab}Destination Port: {self.dst}\n' \
            f'{tab}Sequence number: {self.sequence_number}\n' \
            f'{tab}Acknowledgment number: {self.ack_number}\n' \
            f'{tab}Data offset: {self.data_offset}\n' \
            f'{tab}Flags: URG={self.urg} ACK={self.ack} PSH={self.psh} RST={self.rst} SYN={self.syn} FIN={self.fin}\n' \
            f'{tab}Window size: {self.window_size}\n' \
            f'{tab}Urgent pointer: {self.urgent_pointer}\n' \
            f'{to_hex_dump(self.data, tab=tab)}'


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
            f'{tab}User Datagram Protocol (UDP)\n'\
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
            f'{"" if self.transport_frame is None else self.transport_frame.get_description(tab + " ")}'


class Ipv6Frame(InternetFrame):
    def __init__(self, traffic_class, flow_label, payload_length,
                 next_header, hop_limit, src, dst, raw, transport_frame: TransportFrame):
        super().__init__('ipv6', raw, transport_frame)
        self.__traffic_class = traffic_class
        self.__flow_label = flow_label
        self.__payload_length = payload_length
        self.__next_header = next_header
        self.__hop_limit = hop_limit
        self.__src = src
        self.__dst = dst

    @property
    def traffic_class(self):
        return self.__traffic_class

    @property
    def flow_label(self):
        return self.__flow_label

    @property
    def payload_length(self):
        return self.__payload_length

    @property
    def next_header(self):
        return self.__next_header

    @property
    def hop_limit(self):
        return self.__hop_limit

    @property
    def source(self):
        return self.__src

    @property
    def destination(self):
        return self.__dst

    def get_description(self, tab):
        return \
            f'{tab}Internet IPv6 Frame\n' \
            f'{tab}Traffic class: {self.traffic_class}\n' \
            f'{tab}Flow label: {self.flow_label}\n' \
            f'{tab}Payload length: {self.payload_length}\n' \
            f'{tab}Next header: {self.next_header}\n' \
            f'{tab}Hop limit: {self.hop_limit}\n' \
            f'{tab}Source: {self.source}\n' \
            f'{tab}Destination: {self.destination}\n' \
            f'{self.transport_frame.get_description(tab + " ")}'


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
