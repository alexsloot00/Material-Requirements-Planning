from typing import List, Tuple
from collections import defaultdict, deque

from product import Product


class BOMConnections:
    """
    Contains all connections between products and
    specific BOM relations. This class also checks
    if cycles exist within the given product connections.
    """

    def __init__(self, products: List[Product], matrix: List[List[int]]) -> None:
        """Initialize the matrix containing product relations and product arrays"""
        self.matrix = matrix
        self.products = products
        self.product_names = [product.name for product in self.products]
        self.process_matrix()

    def process_matrix(self):
        """Finds the order of products to compute the MRP later"""
        # Initialize dictionaries to store in-degrees and dependencies
        in_degree = defaultdict(int)
        dependencies = defaultdict(list)

        # Calculate in-degrees and dependencies
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    in_degree[j] += 1
                    dependencies[i].append(j)

        # Perform topological sort
        result = []
        queue = deque()

        # Initialize the queue with nodes having in-degree of 0
        for node in range(len(self.matrix)):
            if in_degree[node] == 0:
                queue.append(node)

        while queue:
            node = queue.popleft()
            result.append(node)

            # Update in-degrees and add to queue
            for neighbor in dependencies[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Check for cycles (if not all nodes were included)
        if len(result) != len(self.matrix):
            return None  # Graph has a cycle

        # Map product order to product names
        self.product_order = [self.products[i] for i in result]
        self.product_order_names = [self.product_names[i] for i in result]
        print("Product order:", " -> ".join(self.product_order_names))

    def get_product_order(self) -> List[Product]:
        return self.product_order

    def get_BOM_factors(self, product: Product) -> Tuple[Product, List[int]]:
        """Returns the row of BOM factors from the matrix for a particular product"""
        for count, name in enumerate(self.product_names):
            if name == product.name:
                break
        return self.matrix[count]
