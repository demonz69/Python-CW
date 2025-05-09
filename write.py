
def inventory_add(filepath, product):
    with open(filepath, 'a') as file:
        file.write(f"{product['name']},{product['company']},{product['quantity']},{product['price']},{product['Country of origin']}\n")
    print("Inventory updated successfully!")

def write_inventory(filepath, inv):
    with open(filepath, 'w') as file:
        for product in inv:
            file.write(f"{product['name']},{product['company']},{product['quantity']},{product['price']},{product['Country of origin']}\n")


def write_invoice(file_name, header, items, total_amount, footer):
    with open(file_name, 'w') as file:
        file.write(header)
        for line in items:
            file.write(line)
        file.write("-" * 66 + "\n")
        file.write(f"{footer} Rs {total_amount:.2f}\n")

