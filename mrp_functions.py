from typing import List


def netting(
    gross_requirements: List[int],
    initial_inventory: int,
    planned_receipts: List[int],
    safety_stock: int,
) -> [List[int], List[int]]:
    """Obtain net requirements update the inventory over the subperiods"""
    sub_periods = len(gross_requirements)
    inventory = []
    net_requirements = []
    net_requirements.append(0)
    inventory.append(initial_inventory)
    for i in range(1, sub_periods):
        temp = (
            inventory[i - 1]
            - gross_requirements[i]
            + planned_receipts[i]
            + net_requirements[i - 1]
        )
        inventory.append(temp)
        net_requirements.append(max(0, safety_stock - inventory[i]))

    return net_requirements, inventory


def backward_scheduling(planned_receipts: List[int], lead_time: int) -> List[int]:
    """Calculates when to start producing such that orders are ready in time"""
    planned_release = [0 for _ in range(len(planned_receipts))]
    planned_release[0] = sum(planned_receipts[0 : lead_time + 1])
    for i in range(lead_time + 1, len(planned_receipts)):
        planned_release[i - lead_time] = planned_receipts[i]
    return planned_release
