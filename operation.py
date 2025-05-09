from read import inventory_read, inventory_display, check_product
from write import inventory_add, write_inventory, write_invoice
import datetime


def get_from_user():
    try:
        name = input("Enter product name: ").strip()
        company = input("Enter company: ").strip()
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price: "))
        origin = input("Enter country of origin: ").strip()
        return {
            'name': name,
            'company': company,
            'quantity': quantity,
            'price': price,
            'Country of origin': origin
        }
    except ValueError:
        print("Invalid input. Please enter correct values.")
        return None

def restock_inventory(filepath):
    try:
        inventory_display(filepath)
        inv = inventory_read(filepath)
        restock_cart = []
        company = input("Enter the name supplier/company: ")
        if not company:
            print("Company/supplier name is required for invoice.")
            return
        while True:
            product_name = input("Enter product name to restock or add into inventory: ").strip()
            existing_product = check_product(inv, product_name)
            if existing_product:
                quantity = int(input("How much quantaty you want to restock: "))
                existing_product['quantity'] += quantity
                restock_cart.append({
                    'name': existing_product['name'],
                    'company': existing_product['company'],
                    'quantity': quantity,
                    'price': existing_product['price'],
                    'subtotal': quantity * existing_product['price'],
                    'Country of origin': existing_product['Country of origin']
                })
            else:
                new_product_add = input(f"{product_name} not found in inventory.Do you want to add it?").strip()
                if new_product_add.lower() == 'yes':
                    new_product = get_from_user()
                    inventory_add(filepath, new_product)
                    inv.append(new_product)
                    restock_cart.append({
                        'name': new_product['name'],
                        'company': new_product['company'],
                        'quantity': new_product['quantity'],
                        'price': new_product['price'],
                        'subtotal': new_product['quantity'] * new_product['price'],
                        'Country of origin': new_product['Country of origin']
                    })
            restock_more_products = input("Do you want to restock more products?").strip().lower()
            if restock_more_products != 'yes':
                break
        if restock_cart:
            invoice_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            invoice_file = f"restock-invoice{invoice_number}.txt"
            total_amount = sum(item['subtotal'] for item in restock_cart)
            header = f"Restock Invoice from {company}\nDate: {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
            items = [f"{item['name']:20}{item['quantity']:>6}{item['price']:>10.2f}{item['subtotal']:>12.2f}\n" for item in restock_cart]
            footer = "Total Restock Amount:"
            write_invoice(invoice_file, header, items, total_amount, footer)
        write_inventory(filepath, inv)
        print("Inventory updated successfully!")
    except ValueError:
        print("Invalid input. Please enter correct values.")
    except Exception as e:
        print(f"An error occurred: {e}")

def item_sell(filepath):
    inv = inventory_read(filepath)
    item_cart = []
    inventory_display(filepath)
    customer_name = input("Enter the Customer name for billing : ")
    if not customer_name:
        print("Customer name is required for the bill.")
        return
    while True:
        product_name = input("Enter the name of product customer want to buy: ")
        if not product_name:
            print("Please enter Product name to continue.")
            continue
        product = check_product(inv, product_name)
        if not product:
            print(f"{product_name} not found.")
            choice = input("Do you want to try buying another product? (yes/no): ").strip().lower()
            if choice != 'yes':
                break
            else:
                continue
        try:
            quantity = int(input("Enter the quantity you want to buy: "))
            if quantity <= 0:
                print("Quantity must be greater than zero.")
                continue
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            continue
        free_item = quantity // 3
        total_quantity = quantity + free_item
        if product['quantity'] >= total_quantity:
            product['quantity'] -= total_quantity
            sell_price = product['price'] * 2
            item_cart.append({
                'name': product['name'],
                'company': product['company'],
                'quantity': quantity,
                'free_items': free_item,
                'price per piece': sell_price,
                'subtotal': quantity * sell_price,
                'Country of origin': product['Country of origin']
            })
        else:
            print(f"Not enough {product_name} in stock.")
        buy_again = input("Do you want to buy more products? ").strip().lower()
        if buy_again != 'yes':
            break
    if item_cart:
        invoice_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        invoice_file = f"sell-invoice{invoice_number}.txt"
        total_amount = sum(item['subtotal'] for item in item_cart)
        header = f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
        items = [f"{item['name']:15}{item['quantity']:>12}{item['free_items']:>12}{item['price per piece']:>12.2f}{item['subtotal']:>14.2f}\n" for item in item_cart]
        footer = f"Total Amount Payed:\nAll items are billed to: {customer_name}"
        write_invoice(invoice_file, header, items, total_amount, footer)
        write_inventory(filepath, inv)
        print("Invoice has been generated successfully! Check the file for more info", invoice_file)
