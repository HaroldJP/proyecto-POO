from warehouse_models import UserManager, Inventory, Supplier, PerishableProduct, NonPerishableProduct
from datetime import datetime, timedelta
if __name__ == "__main__":
    user_manager = UserManager()
    
    while True:
        print("\nWelcome to the warehouse application. Please choose an option:")
        print("1. Register")
        print("2. Log in")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user_manager.register_user()
        
        elif choice == '2':
            username = user_manager.login_user()
            if username:  # If login is successful
                inventory = Inventory(username)
                
                while True:
                    print("\nInventory Management Menu:")
                    print("1. Add a new product")
                    print("2. Remove a product")
                    print("3. Edit a product")
                    print("4. Show inventory")
                    print("5. Search for a product")
                    print("6. Generate inventory report")
                    print("7. Log out")
                    
                    while True:
                        try:
                            inventory_choice = int(input("Enter your choice: "))
                            if inventory_choice in [1, 2, 3, 4, 5, 6, 7]:
                                break
                            else:
                                print("Invalid choice, please try again.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                    if inventory_choice == 1:
                        while True:
                            product_type = input("Is the product perishable (yes/no)? ").strip().lower()
                            if product_type in ['yes', 'no']:
                                break
                            else:
                                print("Please answer with 'yes' or 'no'.")
                        
                        name = input("Enter product name: ")
                        while True:
                            try:
                                quantity = int(input("Enter product quantity: "))
                                price = float(input("Enter product price: "))
                                min_stock = int(input("Enter minimum stock level: "))
                                max_stock = input("Enter maximum stock level (leave blank for no limit): ")
                                max_stock = int(max_stock) if max_stock else None
                                break
                            except ValueError:
                                print("Invalid input. Please enter numeric values for quantity, price, and stock levels.")
                        
                        supplier_name = input("Enter supplier name: ")
                        supplier_contact = input("Enter supplier contact information: ")
                        supplier = Supplier(supplier_name, supplier_contact)

                        if product_type == 'yes':
                            while True:
                                expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
                                try:
                                    expiration_date_parsed = datetime.strptime(expiration_date, "%Y-%m-%d").date()
                                    break
                                except ValueError:
                                    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
                            product = PerishableProduct(name, quantity, price, expiration_date_parsed, supplier, min_stock, max_stock)
                        else:
                            shelf_life = input("Enter shelf life (e.g., '2 years'): ")
                            product = NonPerishableProduct(name, quantity, price, shelf_life, supplier, min_stock, max_stock)

                        inventory.add_product(product)

                    elif inventory_choice == 2:
                        inventory.show_inventory()
                        try:
                            product_index = int(input("Enter the number of the product to remove: ")) - 1
                            inventory.remove_product(product_index)
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")

                    elif inventory_choice == 3:
                        inventory.show_inventory()
                        try:
                            product_index = int(input("Enter the number of the product to update: ")) - 1
                            quantity = input("Enter the new quantity (leave blank to keep current quantity): ")
                            price = input("Enter the new price (leave blank to keep current price): ")
                            quantity = int(quantity) if quantity else None
                            price = float(price) if price else None
                            inventory.update_product(product_index, quantity, price)
                        except ValueError:
                            print("Invalid input. Please enter valid numbers.")

                    elif inventory_choice == 4:
                        inventory.show_inventory()

                    elif inventory_choice == 5:
                        search_name = input("Enter product name to search (leave blank to skip): ")
                        search_category = input("Enter product category (perishable/non-perishable, leave blank to skip): ").strip().lower()
                        search_category = PerishableProduct if search_category == 'perishable' else NonPerishableProduct if search_category == 'non-perishable' else None
                        min_price = input("Enter minimum price to search (leave blank to skip): ")
                        max_price = input("Enter maximum price to search (leave blank to skip): ")
                        min_price = float(min_price) if min_price else None
                        max_price = float(max_price) if max_price else None

                        results = inventory.search_product(name=search_name, category=search_category, min_price=min_price, max_price=max_price)
                        if results:
                            for product in results:
                                print(product)
                        else:
                            print("No products found matching the search criteria.")

                    elif inventory_choice == 6:
                        print("\nReport Types:")
                        print("1. Full Inventory Report")
                        print("2. Low Stock Report")
                        print("3. Expiring Soon Report")
                        print("4. Expired Products Report")

                        report_choice = input("Enter your choice: ")
                        report_type = "all" if report_choice == '1' else \
                                      "low_stock" if report_choice == '2' else \
                                      "expiring_soon" if report_choice == '3' else \
                                      "expired" if report_choice == '4' else None

                        if report_type:
                            inventory.generate_report(report_type=report_type)
                        else:
                            print("Invalid report type selected.")
                    
                    elif inventory_choice == 7:
                        print("Logging out...")
                        break
            else:
                print("Login failed. Please try again.")
        
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")
