from abc import abstractmethod


class Saver:
    @abstractmethod
    def write(self, package):
        raise NotImplementedError

    def write_all(self, packages):
        for p in packages:
            self.write(p)
