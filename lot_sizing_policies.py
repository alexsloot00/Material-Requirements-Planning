from typing import List, Protocol


class LotSizingPolicy(Protocol):
    """Base class for the lot sizing policies"""


class LotForLot(LotSizingPolicy):
    def __init__(self) -> None:
        super().__init__()
        pass

    def lot_sizing(self, net_requirements: List[int]) -> List[int]:
        """Lot for lot only copies the net requirements to the planned release."""
        planned_release = net_requirements
        return planned_release


class FixedOrderPeriod(LotSizingPolicy):
    def __init__(self, period) -> None:
        super().__init__()
        self.period = period

    def lot_sizing(self, net_requirements: List[int]) -> List[int]:
        """FOP can only order on a fixed period basis"""
        planned_release = [0 for _ in range(len(net_requirements))]
        for i in range(len(net_requirements)):
            if i % self.period == 1:
                planned_release[i] = sum(net_requirements[i : (i + self.period)])
        return planned_release


class FixedOrderQuantity(LotSizingPolicy):
    def __init__(self, quantity: int) -> None:
        super().__init__()
        self.quantity = quantity

    def lot_sizing(self, net_requirements: List[int]) -> List[int]:
        """FOQ can only order a specific quantity each time"""
        planned_release = [0 for _ in range(len(net_requirements))]
        j = 0
        for i in range(len(net_requirements)):
            if net_requirements[i] != 0 and i >= j and i < len(net_requirements) - 1:
                for j in range(i, len(net_requirements)):
                    if planned_release[i] + net_requirements[j] <= self.quantity:
                        planned_release[i] += net_requirements[j]
                    else:
                        break

        return planned_release
