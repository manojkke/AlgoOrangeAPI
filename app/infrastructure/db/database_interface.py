from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def get_data(self, table_name: str):
        pass
