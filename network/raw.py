import socket

_ETH_P_ALL = 0x0003  # constant from /usr/include/linux/if_ether.h, means get all ethernet packets
_MTU = 65535


class RawFrameGenerator:
    def __init__(self, mtu=_MTU, interface=''):
        self.__mtu = mtu
        self.__conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(_ETH_P_ALL))
        if interface != '':
            self.__conn.bind((interface, 0))

    @property
    def socket(self):
        return self.__conn

    def recv_next(self):
        package, addr = self.__conn.recvfrom(self.__mtu)

        return package
