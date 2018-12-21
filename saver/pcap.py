import time
import struct

GLOBAL_HEADER_FMT = '@ I H H i I I I '
LOCAL_HEADER_FMT = '@ I I I I'

MAGICAL_NUMBER = 2712847316
MJ_VERN_NUMBER = 2
MI_VERN_NUMBER = 4
LOCAL_CORECTIN = 0
ACCUR_TIMSTAMP = 0
MAX_LENGTH_CAP = 65535
DATA_LINK_TYPE = 1


class Saver:
    def __init__(self, filename):
        if filename == '' or filename is None:
            self.__file = None
        else:
            self.__file = open(filename, 'wb')
            self.__file.write(
                struct.pack(GLOBAL_HEADER_FMT, MAGICAL_NUMBER, MJ_VERN_NUMBER, MI_VERN_NUMBER,
                            LOCAL_CORECTIN, ACCUR_TIMSTAMP, MAX_LENGTH_CAP, DATA_LINK_TYPE))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def fileobj(self):
        return self.__file

    def close(self):
        if self.__file is not None:
            self.__file.close()

    def save(self, package):
        ts_sec, ts_usec = map(int, str(time.time()).split('.'))
        size = len(package)

        self.__file.write(struct.pack(LOCAL_HEADER_FMT, ts_sec, ts_usec, size, size))
        self.__file.write(package)

    def save_all(self, packages):
        for p in packages:
            self.save(p)
