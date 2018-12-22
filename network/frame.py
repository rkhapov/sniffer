import os
import tools.byteprint


class Headers:
    def __init__(self, headers=None):
        self.__headers = headers or dict()

    def add(self, header, data):
        self.__headers[header] = data
        return self

    @property
    def headers(self):
        return self.__headers

    @property
    def names(self):
        return list(self.__headers)

    @property
    def values(self):
        return list(map(lambda x: self.__headers[x], list(self.__headers)))

    def __str__(self):
        return '\n'.join(map(
            lambda p: f'{p[0]}: {tools.byteprint.get_bytes_str(p[1], 30) if not isinstance(p[1], Frame) else os.linesep + str(p[1])}',
            self.__headers.items()))

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
