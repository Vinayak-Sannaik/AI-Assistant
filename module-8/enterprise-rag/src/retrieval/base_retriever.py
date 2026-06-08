from abc import ABC, abstractmethod
from src.configg.settings import TOP_K_RERANK

class BaseRetriever(ABC):

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = TOP_K_RERANK,
    ):
        pass