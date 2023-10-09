from lot_sizing_policies import LotForLot, FixedOrderPeriod, FixedOrderQuantity
from material_requirements_planning import MaterialRequirementsPlanning
from product import Product
from bom_connections import BOMConnections


def main():
    """
    Creates a material requirements planning (MRP) for given products.
    """
    # scheduled receipts MUST start with 0, due to 0 index!
    A = Product(
        "A",
        initial_inventory=10,
        scheduled_receipts=[0, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        safety_stock=10,
        lead_time=1,
        lot_sizing_policy=FixedOrderPeriod(period=3),
    )
    B = Product(
        "B",
        initial_inventory=50,
        scheduled_receipts=[0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0],
        safety_stock=10,
        lead_time=1,
        lot_sizing_policy=FixedOrderQuantity(quantity=60),
    )
    X = Product(
        "X",
        initial_inventory=35,
        scheduled_receipts=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        safety_stock=10,
        lead_time=1,
        lot_sizing_policy=FixedOrderQuantity(quantity=40),
    )
    Y = Product(
        "Y",
        initial_inventory=20,
        scheduled_receipts=[0, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        safety_stock=10,
        lead_time=1,
        lot_sizing_policy=FixedOrderPeriod(period=3),
    )
    Z = Product(
        "Z",
        initial_inventory=30,
        scheduled_receipts=[0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0],
        safety_stock=10,
        lead_time=1,
        lot_sizing_policy=FixedOrderQuantity(quantity=100),
    )
    products = [A, B, X, Y, Z]

    # Specific to the above example from Global Supply Chain
    A.add_gross_requirements([11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
    B.add_gross_requirements([20 for _ in range(11)])
    matrix = [
        [0, 0, 1, 2, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    # Process the above data and run the MRP
    bom_connection = BOMConnections(products, matrix)
    mrp = MaterialRequirementsPlanning(products, bom_connection)
    mrp.run()

    # Print results
    for product in products:
        product.print_table()


if __name__ == "__main__":
    main()
