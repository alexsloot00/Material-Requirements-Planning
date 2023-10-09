from lot_sizing_policies import LotSizingPolicy
from mrp_functions import (
    netting,
    backward_scheduling,
)
from typing import List
import pandas as pd


class Product:
    """
    Represents a product type
    Each product requires a full run of the MRP, i.e.
    netting -> lot sizing -> backward scheduling -> bill of materials
    """

    def __init__(
        self,
        name: str,
        initial_inventory: int,
        scheduled_receipts: List[int],
        safety_stock: int,
        lead_time: int,
        lot_sizing_policy: LotSizingPolicy,
    ) -> None:
        self.name = name
        self.initial_inventory = initial_inventory
        self.scheduled_receipts = scheduled_receipts
        self.safety_stock = safety_stock
        self.lead_time = lead_time
        self.lot_sizing_policy = lot_sizing_policy
        self.gross_requirements = [0 for _ in range(len(self.scheduled_receipts))]

    def add_gross_requirements(self, gross_requirements: List[int]) -> None:
        """Add gross requirements to this product over subperiods"""
        for i in range(len(gross_requirements)):
            self.gross_requirements[i] += gross_requirements[i]

    def do_iteration(self) -> List[int]:
        """Performs one iteration of netting -> lot sizing -> backward scheduling (no BOM)"""
        [self.net_requirements, self.inventory] = netting(
            self.gross_requirements,
            self.initial_inventory,
            self.scheduled_receipts,
            self.safety_stock,
        )
        self.planned_receipts = self.lot_sizing_policy.lot_sizing(self.net_requirements)
        self.planned_release = backward_scheduling(
            self.planned_receipts, self.lead_time
        )
        self.update_table()
        return self.planned_release

    def update_table(self) -> None:
        """Updates the MRP table for printing or accessing data"""
        temp = [x for x in range(len(self.gross_requirements))]
        data_frames = {
            "subperiods": pd.DataFrame(temp),
            "gross_requirements": pd.DataFrame(self.gross_requirements),
            "scheduled_receipts": pd.DataFrame(self.scheduled_receipts),
            "inventory": pd.DataFrame(self.inventory),
            "net_requirements": pd.DataFrame(self.net_requirements),
            "planned_receipts": pd.DataFrame(self.planned_receipts),
            "planned_release": pd.DataFrame(self.planned_release),
        }

        table = pd.concat(data_frames, axis=1)
        table.columns = data_frames.keys()
        table.reset_index(drop=True, inplace=True)
        self.table = table

    def print_table(self) -> None:
        """Prints the table to the command window"""
        print(f"Table for product {self.name}")
        print(self.table.T)
