# Function to read inventory from a file
import datetime

def inventory_read(filepath):
    """
    Reads inventory from a file and returns a list of products.
    
    Args:
    - filepath (str): Path to the inventory file.
    
    Returns:
    - list: A list of product dictionaries.
    """
    inv = []
    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 5:
                        try:
                            inv.append({
                                'name': parts[0],
                                'company': parts[1],
                                'quantity': int(parts[2]),
                                'price': float(parts[3]),
                                'Country of origin': parts[4]
                            })
                        except ValueError:
                            print(f"Skipping line no. {line} due to incorrect value error.")
                    else:
                        print(f"Skipping line no.{line} due to incorrect format.")
    except FileNotFoundError:
        print(f"File {filepath} not found. Please enter correct file path.")
    return inv

def inventory_display(filepath):
    """
    Displays the inventory from the given file.
    
    Args:
    - filepath (str): Path to the inventory file.
    
    Returns:
    - None: Displays inventory to the console.
    """
    inv = inventory_read(filepath)
    if not inv:
        print("No products in inventory.")
        return
    
    print("\n"+"-" * 34 + "Current Inventory" + "-" * 34 +"\n")
    print(f"{'Name':20} {'Company':20} {'Quantity':10} {'Price (Rs)':12} {'Country of Origin':20}")
    print("-" * 85)
    for product in inv:
        print(f"{product['name']:20} {product['company']:20} "
              f"{str(product['quantity']):10} {str(format(product['price'], '.2f')):12} "
              f"{product['Country of origin']:20}")


def check_product(inv, product_name):
    """
    Checks if a product exists in the inventory by name.
    
    Args:
    - inv (list): The inventory list.
    - product_name (str): The product name to search for.
    
    Returns:
    - dict or None: The product if found, else None.
    """
    product_check = product_name.replace(" ","").lower()
    for product in inv:
        if product['name'].replace(" ","").lower() == product_check:
            return product
    return None
