# Material-Requirements-Planning
The material requirements planning runs for an arbitrary number of products. The products can be connected, requiring a previous product for the production of the next one.
This Python repository calculates the inventory and when each product should start to produce using several lot sizing policies. 
Each product has an associated table consisting of the subperiods, gross requirements, scheduled receipts, inventory, net requirements, planned receipts and planned release. 
The planned release is multiplied with the bill-of-materials (BOM) factor to the next products to obtain the gross requirements for this next product. 

## To execute
Running _main.py_ will execute the MRP algorithm and print the resulting tables for each product. An example of connected products is already stated in the _main.py_ file.
In this example, products **A** and **B** are end products. **A** consists of products 1 **X** and 2 **Y**. B consists of 1 **Y** and 1 **Z**. Product **X** requires 1 **Z**.
