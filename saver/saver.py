from abc import abstractmethod


class Saver:
    @abstractmethod
    def save(self, package):
        raise NotImplementedError

    def save_all(self, packages):
        for p in packages:
            self.write(p)
