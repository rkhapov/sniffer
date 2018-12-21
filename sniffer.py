import socket
import struct
import constants


def main():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(constants.ETH_P_ALL))

    while True:
        raw_data, addr = conn.recvfrom(constants.ETH_MTU)
        dest_mac, src_mac, proto, data = ethernet_frame(raw_data)

        print(f'Frame {len(raw_data)}: {dest_mac} {src_mac} {hex(proto)}')


def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[14:]


def get_mac_addr(bytes_addr):
    bytes_addr = map('{:02x}'.format, bytes_addr)
    return ':'.join(bytes_addr).upper()


if __name__ == '__main__':
    main()
