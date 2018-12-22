from abc import abstractmethod

from network.frame import Frame


class FrameParser:
    def __init__(self, layer):
        self.__layer = layer

    @property
    def layer(self):
        return self.__layer

    @abstractmethod
    def parse(self, data) -> Frame:
        raise NotImplementedError
