from abc import abstractmethod


class Saver:
    @abstractmethod
    def save(self, package):
        raise NotImplementedError
