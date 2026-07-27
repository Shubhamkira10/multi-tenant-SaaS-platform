from __future__ import annotations

from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine


class BaseConnector(ABC):
    """Base database connector."""

    @abstractmethod
    def create_engine(self) -> Engine:
        raise NotImplementedError