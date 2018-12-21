import argparse
import saver.pcap
from network.rawgen import RawPackageGenerator


def _parse_args():
    parser = argparse.ArgumentParser(
        description='This is simple network sniffer on python. '
                    'It may be used to capture network traffic, '
                    'display it and save into pcap format. '
                    'Please note: it is necessary to run it with superuser privileges')

    parser.add_argument('-f', '--filter', help='filter for traffic, may be tcp or udp', default='')
    parser.add_argument('-o', '--out', help='file to save traffic into pcap format')
    parser.add_argument('-i', '--interface', help='name of interface to capture traffic', default='')

    parser.add_argument('--ethernet', help='Show Ethernet headers', action='store_true')
    parser.add_argument('--ipv4', help='Show IPv4 headers', action='store_true')
    parser.add_argument('--ipv6', help='Show IPv6 headers', action='store_true')
    parser.add_argument('--tcp', help='Show TCP headers', action='store_true')
    parser.add_argument('--udp', help='Show UDP headers', action='store_true')

    return parser.parse_args()


def main():
    args = _parse_args()

    try:
        with saver.pcap.Saver('file.pcap') as s:
            gen = RawPackageGenerator()

            for _ in range(50):
                print('Caught them!')
                s.save(gen.recv_next())

    except PermissionError:
        print('Permission denied')
        print('Please, make sure you run me with superuser privileges (use sudo or su)')


if __name__ == '__main__':
    main()
