import datetime

def inventory_add(filepath, product):
    """
    Adds a new product to the inventory file.
    
    Args:
    - filepath (str): Path to the inventory file.
    - product (dict): Product details to add.
    
    Returns:
    - None: Updates the inventory file.
    """
    with open(filepath, 'a') as file:
        file.write(f"{product['name']},{product['company']},{product['quantity']},{product['price']},{product['Country of origin']}\n")
    print("Inventory updated successfully!")


def write_inventory(filepath, inv):
    """
    Writes the entire inventory list to the file, overwriting the existing file.
    
    Args:
    - filepath (str): Path to the inventory file.
    - inv (list): List of product dictionaries to write.
    
    Returns:
    - None: Updates the inventory file.
    """
    with open(filepath, 'w') as file:
        for product in inv:
            file.write(f"{product['name']},{product['company']},{product['quantity']},{product['price']},{product['Country of origin']}\n")


def write_invoice(file_name, date_sell, header, items,footer):
    """
    Generates an invoice file with the provided details.
    
    Args:
    - file_name (str): Name of the invoice file.
    - date_sell (str): Date of the sale.
    - header (str): Header of the invoice.
    - items (list): List of items to be included in the invoice.
    - footer (str): Footer of the invoice.
    
    Returns:
    - None: Creates an invoice file with the details.
    """
    with open(file_name, 'w') as file:
        file.write(date_sell)
        file.write(header)
        file.write("-" * 85 + "\n")
        for line in items:
            file.write(line)
        file.write("-" * 85 + "\n")
        file.write(f"{footer}\n")

def display_invoice(invoice_file):
    """
    Displays the content of an invoice file on the console.
    
    Args:
    - invoice_file (str): Path to the invoice file to display.
    
    Returns:
    - None: Prints the invoice content to the console.
    """
    with open(invoice_file, 'r') as file:
            print(file.read())

