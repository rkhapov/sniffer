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
    def get_description(self, tab):
        return tab + 'i am udp frame'

    def __init__(self, raw):
        super().__init__('udp', raw)


class Ipv4Frame(InternetFrame):
    def __init__(self, raw, transport_frame: TransportFrame):
        super().__init__('ipv4', raw, transport_frame)

    def get_description(self, tab):
        return tab + 'i am ipv4 frame:\n' + self.transport_frame.get_description(tab + ' ')


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
