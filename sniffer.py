import argparse
import errno
import saver.pcap
from network.gen import FrameGenerator
from network.parsers import EthernetFrameParser, Ipv6FrameParser, Ipv4FrameParser, TcpFrameParser, UdpFrameParser
from network.raw import RawFrameGenerator


def _parse_args():
    parser = argparse.ArgumentParser(
        description='This is simple network sniffer on python. '
                    'It may be used to capture network traffic, '
                    'display it and save into pcap format. '
                    'Please note: it is necessary to run it with superuser privileges. '
                    'To stop sniffer use keyboard interruption (Ctrl+C)')

    parser.add_argument('-f', '--filter', help='filter for traffic, may be tcp or udp', default='')
    parser.add_argument('-o', '--out', help='file to save traffic in pcap format')
    parser.add_argument('-i', '--interface', help='name of interface to capture traffic', default='')

    return parser.parse_args()


def main():
    args = _parse_args()

    try:
        with saver.pcap.PcapSaver('file.pcap') as s:
            tcp = TcpFrameParser()
            udp = UdpFrameParser()
            ipv4 = Ipv4FrameParser(tcp, udp)
            ipv6 = Ipv6FrameParser(tcp, udp)
            ethernet = EthernetFrameParser(ipv4, ipv6)

            gen = FrameGenerator(RawFrameGenerator(interface=args.interface), ethernet)

            while True:
                frame = gen.get_next()
                if frame.internet_frame.transport_frame.protocol == 'udp':
                    s.save(frame.raw)
                    print(frame.get_description())
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    except PermissionError:
        print('Permission denied')
        print('Please, make sure you run me with superuser privileges (use sudo or su)')
    except KeyboardInterrupt:
        print('\nStopped')
    except OSError as e:
        if e.errno == errno.ENODEV:
            print('No such interface')
        else:
            raise


if __name__ == '__main__':
    main()
