from operation import restock_inventory, item_sell
from read import inventory_display

filepath = 'Information.txt'

def main_function():

    """
    The main function that runs the WeCare Inventory Management System.
    Displays a menu to perform operations such as displaying inventory,
    selling products, restocking inventory, or exiting the program.
    
    Returns:
        None
    """

    while True:
        try:
            print("\n--- WeCare Management ---")
            print("1. Display Inventory")
            print("2. sell Products")
            print("3. Restock Inventory or Add New Products")
            print("4. close program")
            code = input("\n"+"Enter your code of operation: ").strip()
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

        except FileNotFoundError:
            print("Error: Inventory file not found. Please check the file path.")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

main_function()
