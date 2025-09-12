# from abc import ABC, abstractmethod
# from typing import Iterable, Mapping, Optional

# class NewsClient(ABC):
#     @abstractmethod
#     async def latest(self, )

from typing import AsyncIterator, Mapping, Optional

class NewsClient:
    async def latest(self, since_iso: Optional[str] = None) -> AsyncIterator[Mapping]:
        raise NotImplementedError
