
from abc import ABC, abstractmethod

class DataframeReader(ABC):
    @abstractmethod
    def read_dataframe(self):
        ...

class CasesOutputPort(ABC):
    @abstractmethod
    def send_cases(self, cases):
        ...