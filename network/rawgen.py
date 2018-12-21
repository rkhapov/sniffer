import socket

_ETH_P_ALL = 0x0003  # constant from /usr/include/linux/if_ether.h, means get all ethernet packets
_MTU = 65535


class RawPackageGenerator:
    def __init__(self, mtu=_MTU, interface=''):
        self.__mtu = mtu
        self.__conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(_ETH_P_ALL))
        self.__interface = interface

    @property
    def socket(self):
        return self.__conn

    def recv_next(self):
        while True:
            package, addr = self.__conn.recvfrom(self.__mtu)

            # if captured package from needed interface
            if self.__interface.lower() == addr[0].lower() or self.__interface == '':
                break

        return package

    def recv_all(self):
        while True:
            yield self.recv_next()
