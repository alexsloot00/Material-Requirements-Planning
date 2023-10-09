from bom_connections import BOMConnections
from product import Product
from typing import List


class MaterialRequirementsPlanning:
    """
    The material requirements planning algorithm
    This algorithm requires the products and connections
    between the products and implements the BOM step
    """

    def __init__(self, products: List[Product], bom_connection: BOMConnections) -> None:
        """Initialize the list of products and connections"""
        self.products = products
        self.bom_connection = bom_connection

    def run(self):
        """Performs all MRP calculations for each product."""
        product_order = self.bom_connection.get_product_order()
        # loop over products in order of which requires attention first
        for product in product_order:
            product_planned_release = product.do_iteration()
            BOM_factors = self.bom_connection.get_BOM_factors(product)
            # loop over each order to check if connected and use BOM factor
            for product_index, connected_product in enumerate(self.products):
                BOM_factor = BOM_factors[product_index]
                temp = [
                    BOM_factor * product_planned_release[i]
                    for i in range(len(product_planned_release))
                ]
                connected_product.add_gross_requirements(temp)
