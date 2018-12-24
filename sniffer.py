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

    parser.add_argument('-f', '--filter', help='filter for traffic', type=str,
                        choices=['tcp', 'udp', 'ipv4', 'ipv6'], default='')
    parser.add_argument('-o', '--out', help='file to save traffic in pcap format')
    parser.add_argument('-i', '--interface', help='name of interface to capture traffic', default='')
    parser.add_argument('-n', '--number', help='maximum number of caught frames', default=-1, type=int)

    return parser.parse_args()


class Sniffer:
    def __init__(self, interface='', filter_='', out='', max_frames=-1):
        self.__interface = interface
        self.__filter = filter_
        self.__out = out
        self.__max_frames = max_frames

    def run(self):
        try:
            with saver.pcap.PcapSaver(self.__out) as s:
                tcp = TcpFrameParser()
                udp = UdpFrameParser()
                ipv4 = Ipv4FrameParser(tcp, udp)
                ipv6 = Ipv6FrameParser(tcp, udp)
                ethernet = EthernetFrameParser(ipv4, ipv6)

                gen = FrameGenerator(RawFrameGenerator(interface=self.__interface), ethernet)

                count = 0

                while self.__max_frames == -1 or count < self.__max_frames:
                    frame = gen.get_next()

                    if not self._frame_completes_to_filter(frame):
                        continue

                    s.save(frame.raw)
                    print(f'Frame #{count}:')
                    print(frame.get_description())
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

                    count += 1

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

    def _frame_completes_to_filter(self, frame):
        if self.__filter == '':
            return True

        return frame.internet_frame.protocol == self.__filter or \
            frame.internet_frame.transport_frame.protocol == self.__filter


def main():
    args = _parse_args()
    sniffer = Sniffer(interface=args.interface, filter_=args.filter, out=args.out, max_frames=args.number)

    sniffer.run()


if __name__ == '__main__':
    main()
