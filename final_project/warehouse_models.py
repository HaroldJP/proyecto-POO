import json
import os
from datetime import datetime, timedelta

# Ensure the data and inventory directories exist
os.makedirs('data/inventory', exist_ok=True)

# User Management Classes
class UserManager:
    def __init__(self, user_file='data/users.json'):
        self.user_file = os.path.join('data', os.path.basename(user_file))
        self.user_data = self.load_users()

    def load_users(self):
        try:
            with open(self.user_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.user_file, 'w') as file:
            json.dump(self.user_data, file, indent=4)

    def register_user(self):
        while True:
            username = input("Enter your username: ").strip()
            if username in self.user_data:
                print("The username already exists.")
            else:
                password = input("Enter your password: ")
                self.user_data[username] = password
                self.save_users()
                print(f"User {username} successfully registered.")
                break

    def login_user(self):
        while True:
            username = input("Enter your username: ").strip()
            if username in self.user_data:
                password = input("Enter your password: ")
                if self.user_data[username] == password:
                    print("Login successful.")
                    return username  # Return the username to identify the user
                else:
                    print("Incorrect password.")
            else:
                print("Username not found.")
            if input("Try again? (yes/no): ").strip().lower() != 'yes':
                break
        return None

# Supplier Class
class Supplier:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info

# Product Classes
class Product:
    def __init__(self, name, quantity, price, supplier=None, min_stock=0, max_stock=None):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.supplier = supplier
        self.min_stock = min_stock
        self.max_stock = max_stock

    def __str__(self):
        return f"Product: {self.name}, Quantity: {self.quantity}, Price: {self.price}, Supplier: {self.supplier.name if self.supplier else 'N/A'}"

    def update_quantity(self, quantity):
        self.quantity = quantity

    def update_price(self, price):
        self.price = price

    def check_stock(self):
        if self.quantity < self.min_stock:
            print(f"Warning: {self.name} is below the minimum stock level!")
        if self.max_stock and self.quantity > self.max_stock:
            print(f"Warning: {self.name} exceeds the maximum stock level!")

class PerishableProduct(Product):
    def __init__(self, name, quantity, price, expiration_date, supplier=None, min_stock=0, max_stock=None):
        super().__init__(name, quantity, price, supplier, min_stock, max_stock)
        self.expiration_date = expiration_date

    def __str__(self):
        return f"Perishable Product: {self.name}, Quantity: {self.quantity}, Price: {self.price}, Expiration Date: {self.expiration_date}, Supplier: {self.supplier.name if self.supplier else 'N/A'}"

class NonPerishableProduct(Product):
    def __init__(self, name, quantity, price, shelf_life, supplier=None, min_stock=0, max_stock=None):
        super().__init__(name, quantity, price, supplier, min_stock, max_stock)
        self.shelf_life = shelf_life

    def __str__(self):
        return f"Non-Perishable Product: {self.name}, Quantity: {self.quantity}, Price: {self.price}, Shelf Life: {self.shelf_life}, Supplier: {self.supplier.name if self.supplier else 'N/A'}"

# Inventory Management Class
class Inventory:
    def __init__(self, username):
        self.username = username
        self.inventory_file = os.path.join('data', 'inventory', f'inventory_{username}.json')
        self.total_inv = self.load_inventory()
        self.transaction_history = []

    def load_inventory(self):
        try:
            with open(self.inventory_file, 'r') as file:
                inventory_data = json.load(file)
                return [self.create_product_from_data(data) for data in inventory_data]
        except FileNotFoundError:
            return []

    def save_inventory(self):
        with open(self.inventory_file, 'w') as file:
            inventory_data = [self.product_to_dict(product) for product in self.total_inv]
            json.dump(inventory_data, file, indent=4)

    def create_product_from_data(self, data):
        if data['type'] == 'PerishableProduct':
            return PerishableProduct(data['name'], data['quantity'], data['price'], 
                                     datetime.strptime(data['expiration_date'], "%Y-%m-%d").date(),
                                     Supplier(data['supplier']['name'], data['supplier']['contact_info']) if data['supplier'] else None,
                                     data['min_stock'], data['max_stock'])
        else:
            return NonPerishableProduct(data['name'], data['quantity'], data['price'], data['shelf_life'],
                                        Supplier(data['supplier']['name'], data['supplier']['contact_info']) if data['supplier'] else None,
                                        data['min_stock'], data['max_stock'])

    def product_to_dict(self, product):
        return {
            'type': 'PerishableProduct' if isinstance(product, PerishableProduct) else 'NonPerishableProduct',
            'name': product.name,
            'quantity': product.quantity,
            'price': product.price,
            'min_stock': product.min_stock,
            'max_stock': product.max_stock,
            'supplier': {'name': product.supplier.name, 'contact_info': product.supplier.contact_info} if product.supplier else None,
            'expiration_date': product.expiration_date.strftime("%Y-%m-%d") if isinstance(product, PerishableProduct) else None,
            'shelf_life': product.shelf_life if isinstance(product, NonPerishableProduct) else None
        }

    def show_inventory(self):
        if not self.total_inv:
            print("Inventory is empty.")
        else:
            for index, product in enumerate(self.total_inv, start=1):
                print(f"{index}. {product}")

    def add_product(self, product):
        self.total_inv.append(product)
        self.transaction_history.append(f"Added {product.name} at {datetime.now()}")
        self.save_inventory()
        print(f"{product.name} added to inventory.")

    def remove_product(self, product_index):
        try:
            removed_product = self.total_inv.pop(product_index)
            self.transaction_history.append(f"Removed {removed_product.name} at {datetime.now()}")
            self.save_inventory()
            print(f"{removed_product.name} removed from inventory.")
        except IndexError:
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def update_product(self, product_index, quantity=None, price=None):
        try:
            product = self.total_inv[product_index]
            if quantity is not None:
                product.update_quantity(quantity)
            if price is not None:
                product.update_price(price)
            self.transaction_history.append(f"Updated {product.name} at {datetime.now()}")
            self.save_inventory()
            print(f"{product.name} updated.")
        except IndexError:
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    def search_product(self, name=None, category=None, min_price=None, max_price=None):
        results = []
        for product in self.total_inv:
            if (name and name.lower() in product.name.lower()) or \
               (category and isinstance(product, category)) or \
               (min_price is not None and product.price >= min_price) or \
               (max_price is not None and product.price <= max_price):
                results.append(product)
        return results

    def generate_report(self, report_type="all"):
        today = datetime.now().date()
        one_month_from_now = today + timedelta(days=30)
        
        if report_type == "all":
            print("Full Inventory Report:")
            self.show_inventory()
        elif report_type == "low_stock":
            print("Low Stock Report:")
            for product in self.total_inv:
                if product.quantity < product.min_stock:
                    print(product)
        elif report_type == "expiring_soon":
            print("Expiring Soon Report:")
            for product in self.total_inv:
                if isinstance(product, PerishableProduct):
                    if today <= product.expiration_date <= one_month_from_now:
                        print(f"Expiring Soon: {product}")
        elif report_type == "expired":
            print("Expired Products Report:")
            for product in self.total_inv:
                if isinstance(product, PerishableProduct) and product.expiration_date < today:
                    print(f"Expired: {product}")
        else:
            print("Invalid report type.")
