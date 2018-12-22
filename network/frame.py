from typing import Union

import tools.byteprint


class Header:
    def __init__(self, name: str, value: Union[int, bytes], str_repr: str = None):
        self.__name = name
        self.__value = value
        self.__str_repr = str_repr or tools.byteprint.get_bytes_str(value, 25)

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def str_repr(self):
        return self.__str_repr

    def __str__(self):
        return 'Header {}: {}'.format(self.name, self.str_repr)

    def __repr__(self):
        return self.__str__()


class Headers:
    def __init__(self, headers=None):
        self.__headers = headers or dict()

    def add(self, header: Header):
        self.__headers[header.name] = header

        return self

    @property
    def names(self):
        return list(self.__headers)

    @property
    def headers(self):
        return list(map(lambda x: self.__headers[x], list(self.__headers)))

    def __getitem__(self, name):
        try:
            return self.__headers[name]
        except KeyError:
            raise KeyError(f'No header with name {name}')

    def __setitem__(self, name, bytes_):
        self.__headers[name] = bytes_


class Frame:
    def __init__(self, layer, headers: Headers, protocol, raw):
        self.__layer = layer
        self.__headers = headers
        self.__protocol = protocol
        self.__raw = raw

    @property
    def protocol(self):
        return self.__protocol

    @property
    def layer(self):
        return self.__layer

    @property
    def headers(self):
        return self.__headers

    @property
    def raw(self):
        return self.__raw

    def __str__(self):
        return 'Frame {}\nHeaders:\n{}'.format(self.__protocol, str(self.__headers))


class LinkFrame(Frame):
    def __init__(self, headers: Headers, raw):
        super().__init__(layer, headers, protocol, raw)


class EthernetFrame(Frame):
    def __init__(self, headers, raw):
        super().__init__('link', headers, 'ethernet', raw)


class Ipv4Frame(Frame):
    def __init__(self, headers, raw):
        super().__init__('internet', headers, 'ipv4', raw)


class Ipv6Frame(Frame):
    def __init__(self, headers, raw):
        super().__init__('internet', headers, 'ipv6', raw)


class UdpFrame(Frame):
    def __init__(self, headers, raw):
        super().__init__('transport', headers, 'udp', raw)


class TcpFrame(Frame):
    def __init__(self, headers, raw):
        super().__init__('transport', headers, 'tcp', raw)
