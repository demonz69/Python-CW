import datetime

def inventory_add(filepath, product):
    with open(filepath, 'a') as file:
        file.write(f"{product['name']},{product['company']},{product['quantity']},{product['price']},{product['Country of origin']}\n")
    print("Inventory updated successfully!")

def write_inventory(filepath, inv):
    with open(filepath, 'w') as file:
        for product in inv:
            file.write(f"{product['name']},{product['company']},{product['quantity']},{product['price']},{product['Country of origin']}\n")


def write_invoice(file_name,invoice_number, items,footer):
    with open(file_name, 'w') as file:
        file.write(invoice_number)
        file.write(f"{'Name':15} {'Company':15} {'Quantity purched':10} {'Free items':10}{'Price (Rs)':12} {'Country of Origin':15} \n")
        file.write("-" * 85 + "\n")
        for line in items:
            file.write(line)
        file.write("-" * 85 + "\n")
        file.write(f"{footer}\n")

def display_invoice(invoice_file):
    with open(invoice_file, 'r') as file:
            print(file.read())

