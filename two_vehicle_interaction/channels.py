from fib_heaps import FibHeap
from dataclasses import dataclass

@dataclass(order=False,eq=False)
class ChannelData:
    priority: int
    dat: bytes
    def __eq__(self, __o) -> bool:
        return self.priority==__o.priority
    def __ne__(self, __o) -> bool:
        return self.priority!=__o.priority
    def __lt__(self, __o) -> bool:
        return self.priority<__o.priority
    def __gt__(self, __o) -> bool:
        return self.priority>__o.priority
    def __le__(self, __o) -> bool:
        return self.priority<=__o.priority
    def __ge__(self, __o) -> bool:
        return self.priority>=__o.priority

class Channel(FibHeap):
    pass

__all__ = ["ChannelData", "Channel"]
