from abc import ABC, abstractmethod

class TodoRepository(ABC):

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def create(self, todo: dict) -> dict:
        pass

    @abstractmethod
    def get_by_id(self, todo_id: int) -> dict | None:
        pass

    @abstractmethod
    def update(self, todo: dict) -> dict:
        pass

    @abstractmethod
    def delete(self, todo_id: int) -> None:
        pass