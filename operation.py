from read import inventory_read, inventory_display, check_product
from write import inventory_add, write_inventory, write_invoice,display_invoice
import datetime
VAT_RATE = 0.13


# function to get input from user
def get_from_user():
    """
    Prompt the user to enter product details (name, company, quantity, price, origin).
    Returns a dictionary with the product information.
    """
    try:
        while True:
            name = input("Enter product name: ").replace(" ", "").strip()
            if name:
                break
            print("Product name cannot be empty.")

        while True:
            company = input("Enter company: ").replace(" ", "").strip()
            if company:
                break
            print("Company name cannot be empty.")

        while True:
            quantity = int(input("Enter quantity: ").strip())
            try:
                if quantity >= 0:
                    break
                else:
                    print("Quantity cannot be negative.")
            except ValueError:
                print("Price must be a number.")

        while True:
            price = float(input("Enter price of product(RS): ").strip())
            try:
                if price >= 0:
                    break
                else:
                    print("Price must be non-negative.")
            except ValueError:
                print("Price must be a number.")

        while True:
            origin = input("Enter country of origin: ").strip()
            if origin.replace(" ", "").isalpha():
                break
            print("Country of origin must contain only letters.")

        return {
            'name': name,
            'company': company,
            'quantity': quantity,
            'price': price,
            'Country of origin': origin
        }

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
# Function to add restock 
def restock_inventory(filepath):
    """
    Function to handle inventory restocking by adding new stock to existing products or adding new products.
    Generates an invoice for the restocked items.
    """
    try:
        inventory_display(filepath)
        inv = inventory_read(filepath)
        restock_cart = []

        while True:
            product_name = input("Enter product name to restock or add into inventory: ").strip()
            existing_product = check_product(inv, product_name)

            if existing_product:
              while True:
                try:     
                    quantity = int(input("How much quantaty you want to restock: "))
                    if quantity >= 0:
                        break
                    else:
                        print("Quantity cannot be negative.")
                except ValueError:
                    print("Enter a valid quantity")    
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
                new_product_add = input(f"{product_name} not found in inventory.Do you want to add it?(yes/no)").strip()
                if new_product_add.lower() == 'yes':
                    new_product = get_from_user()
                    if new_product:
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
            restock_more_products = input("Do you want to restock more products?(Yes/no): ").strip().lower()
            if restock_more_products != 'yes':
                break
        if restock_cart:
            invoice_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            invoice_file = f"invoice_restock{invoice_number}.txt"
            total_amount = sum(item['subtotal'] for item in restock_cart)
            vat_amount = VAT_RATE *total_amount
            final_amount_with_vat = total_amount + vat_amount
            date_sell = (f"\nRestock Date: {datetime.datetime.now().strftime('%Y-%m-%d')}"+"\n")
            header = (f"{'Product':15} {'supplyer':15} {'Quantity':12} {'Price (Rs)':12} {'Sub-Total':15} {'Country of origin':18} \n")
            items = [f"{item['name']:15} {item['company']:15} {item['quantity']:<12} {item['price']:<12.2f} {item['subtotal']:<14.2f} {item['Country of origin']:<18}\n" for item in restock_cart]
            footer = (
                f"Subtotal: Rs {total_amount:.2f}\n"
                f"Total Amount Payed with 13% VAT: Rs {final_amount_with_vat:.2f}\n"
            )
            write_invoice(invoice_file, date_sell ,header,items, footer)
            write_inventory(filepath, inv)
            display_invoice(invoice_file)
            print("Invoice has been generated & Inventory updated successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

# Function to sell items
def item_sell(filepath):
    """
    Function to handle the sale of items, generate invoices, and update inventory.
    Handles customer information, product selection, and applies offers.
    """
    inv = inventory_read(filepath)
    item_cart = []
    inventory_display(filepath)
    while True:
        customer_name = input("Enter the Customer name for billing (or type 'cancel' to exit): ").strip()
        if customer_name.lower() == 'cancel':
            print("Billing process cancelled.")
            return 
        if not customer_name:
            print("Customer name cannot be empty.")
            continue
        if not customer_name.replace(" ", "").isalpha():
            print("Please enter a valid name.")
            continue
        break

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
        while True:
            try:
                quantity = int(input("Enter the quantity you want to buy: "))
                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                else:
                    break
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
        buy_again = input("Do you want to buy more products?(yes/no) ").strip().lower()
        if buy_again != 'yes':
            break
    if item_cart:
        invoice_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        invoice_file = f"invoice_sell{invoice_number}.txt"
        total_amount = sum(item['subtotal'] for item in item_cart)
        vat_amount = VAT_RATE*total_amount
        final_amount_with_vat = total_amount + vat_amount
        date_sell = (f"\nSell Date: {datetime.datetime.now().strftime('%Y-%m-%d')}"+"\n\n")
        header = (f"{'Product':15} {'supplyer':15} {'Quantity':12} {'Free items':12}{'Price (Rs)':12} {'Sub-Total':15} \n")
        items = [f"{item['name']:15} {item['company']:15} {item['quantity']:<12} {item['free_items']:<12} {item['price per piece']:<12.2f} {item['subtotal']:<14.2f}\n" for item in item_cart]
        footer = (
                f"Subtotal: Rs {total_amount:.2f}\n"
                f"Total Amount Payed with 13% VAT: Rs {final_amount_with_vat:.2f}\n"
                f"All items are billed to: {customer_name}"
            )
        write_invoice(invoice_file, date_sell ,header,items, footer)
        write_inventory(filepath, inv)
        display_invoice(invoice_file)
        print("Invoice has been generated successfully!")
