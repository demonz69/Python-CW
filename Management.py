import datetime

# Function to read inventory from a file
def inventory_read(filepath):
    
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

#function to check if product exists in inventory
def check_product(inv,product_name):
    product_check = product_name.strip().lower()
    for product in inv:
        if product['name'].strip().lower() == product_check:
            return product
    return None
    
#function to input from user for new product to be used for restock function
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
    
# Function to add new product to inventory 
def inventory_add(filepath, product):
    with open(filepath, 'a') as file:
        file.write(f"{product['name']},{product['company']},{product['quantity']},{product['price']},{product['Country of origin']}\n")
    print("Inventory updated successfully!")
        
# Function to display products in inventory as a table
def inventory_display(filepath):
    inv = inventory_read(filepath)
    if not inv:
        print("No products in inventory.")
        return

    # header
    print("\n"+"-" * 34 + "Current Inventory" + "-" * 34 +"\n")
    print(f"{'Name':20} {'Company':20} {'Quantity':10} {'Price (Rs)':12} {'Country of Origin':20}")
    print("-" * 85)

    # for every product
    for product in inv:
        print(f"{product['name']:20} {product['company']:20} "
              f"{str(product['quantity']):10} {str(format(product['price'], '.2f')):12} "
              f"{product['Country of origin']:20}")

#function to restock and add new product 
def restock_inventory(filepath):
    try:

        inventory_display(filepath)
        inv=inventory_read(filepath)
        restock_cart = []
        
        company = input("Enter the name supplier/company: ")
        if not company:
            print("Company/supplier name is required for invoice.")
            return
        
      
        while True:
            product_name = input("Enter product name to restock or add into inventory: ").strip()
            print(f"Checking if '{product_name}' exists in inventory...")
            existing_product = check_product(inv,product_name)
            
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
                print(f"Restocked {quantity} {product_name}.")
            else:
                new_product_add= input(f"{product_name} not found in inventory.Do you want to add it?").strip()
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
                else:
                    print(f"{product_name} not added to inventory.")  
                     
            restock_more_products = input("Do you want to restock more products?").strip().lower()
            if restock_more_products != 'yes':
                break  
        # Generate invoice for restocking
        if restock_cart:
            invoice_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            invoice_file = f"restock-invoice:{invoice_number}.txt"
            total_amount = sum(item['subtotal'] for item in restock_cart)

            with open(invoice_file, 'w') as file:
                file.write(f"Restock Invoice from {company}\n")
                file.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
                file.write(f"{'Product':20}{'Qty':>6}{'Price':>10}{'Subtotal':>12}\n")
                for item in restock_cart:
                    file.write(f"{item['name']:20}{item['quantity']:>6}{item['price']:>10.2f}{item['subtotal']:>12.2f}\n")
                file.write("-" * 54 + "\n")
                file.write(f"{'Total Restock Amount:':>44} Rs {total_amount:.2f}\n")
            print(f"Restock invoice has been generated: {invoice_file}")
                 
         # to update inventory  after restock     
        with open(filepath, 'w') as file:
            for product in inv:
                file.write(f"{product['name']},{product['company']},{product['quantity']},{product['price']},{product['Country of origin']}\n")
        print("Inventory updated successfully!")       
            
    except ValueError:
        print("Invalid input. Please enter correct values.")
     
    except Exception as e:
        print(f"An error occurred: {e}")
      
    

# function to sell products
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
            print("Please enter Product name to contunue.")
            continue
       
        # Check if the product exists in the inventory  
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
            sell_price = product['price']*2
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
            print(f"Not enough {product_name} instock.")

            
        buy_again = input("Do you want to buy more products? ").strip().lower()
        if buy_again != 'yes':
            break
            
       
    if item_cart:
        # for invoice creation
        invoice_number = datetime.datetime.now().strftime("%Y%m%d%H%M%S")   
        invoice_file = f"sell-invoice:{invoice_number}.txt"
        total_amount = sum(item['subtotal'] for item in item_cart)
        
        with open(invoice_file, 'w') as file:
            file.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
            file.write(f"{'Product':15}{'Qty':>12}{'Free':>12}{'Price(Rs)':>12}{'Subtotal(Rs)':>15}\n")
            file.write("-" * 66 + "\n")
            for item in item_cart:
                file.write(f"{item['name']:15}{item['quantity']:>12}{item['free_items']:>12}{item['price per piece']:>12.2f}{item['subtotal']:>14.2f}\n")
            file.write("-" * 66 + "\n")
            file.write(f"{'Total Amount Payed: '} Rs {total_amount:.2f}\n") 
            file.write(f"All items are billed to: {customer_name}")
            
        with open(filepath, 'w') as file:
            for product in inv:
                file.write(f"{product['name']},{product['company']},{product['quantity']},{product['price']},{product['Country of origin']}\n")
                
                
        print("Invoice has been generated successfully! check the file for more info", invoice_file)
               
filepath = 'Information.txt'


# main function with all the options
def main_function():

    while True:
        print("\n--- WeCare Management ---")
        print("1. Display Inventory")
        print("2. sell Products")
        print("3. Restock Inventory or Add New Products")
        print("4. close program")

        code = input("Enter your code of operation: ").strip()

        if code == '1':
            inventory_display(filepath)
        elif code == '2':
            item_sell(filepath)
        elif code == '3':
            restock_inventory(filepath)
        elif code == '4':
            break
        else:
            print("Invalid code. Please enter a number between 1 and 4.")


main_function()
            