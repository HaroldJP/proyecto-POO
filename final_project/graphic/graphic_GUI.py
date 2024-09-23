import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
import os

# Define the Supplier, Product, PerishableProduct, and NonPerishableProduct classes

class Supplier:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info

class Product:
    def __init__(self, name, quantity, price, supplier, min_stock, max_stock):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.supplier = supplier
        self.min_stock = min_stock
        self.max_stock = max_stock

    def update_quantity(self, quantity):
        self.quantity = quantity

    def update_price(self, price):
        self.price = price

    def check_stock(self):
        if self.quantity < self.min_stock:
            return "Stock below minimum"
        elif self.quantity > self.max_stock:
            return "Stock above maximum"
        return "Stock is within range"

    def to_dict(self):
        return {
            'type': 'Product',
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'supplier': self.supplier.name,
            'contact_info': self.supplier.contact_info,
            'min_stock': self.min_stock,
            'max_stock': self.max_stock
        }

    def __str__(self):
        return f"{self.name}: {self.quantity} units at ${self.price}, Supplier: {self.supplier.name}, contact: {self.supplier.contact_info}"

class PerishableProduct(Product):
    def __init__(self, name, quantity, price, expiration_date, supplier, min_stock, max_stock):
        super().__init__(name, quantity, price, supplier, min_stock, max_stock)
        self.expiration_date = expiration_date

    def is_near_expiration(self, days=7):
        return (self.expiration_date - datetime.now()).days <= days

    def is_expired(self):
        return datetime.now() > self.expiration_date

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'type': 'PerishableProduct',
            'expiration_date': self.expiration_date.strftime('%Y-%m-%d')
        })
        return data

    def __str__(self):
        return super().__str__() + f", Expires on: {self.expiration_date.date()}"

class NonPerishableProduct(Product):
    def __init__(self, name, quantity, price, shelf_life, supplier, min_stock, max_stock):
        super().__init__(name, quantity, price, supplier, min_stock, max_stock)
        self.shelf_life = shelf_life

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'type': 'NonPerishableProduct',
            'shelf_life': self.shelf_life
        })
        return data

    def __str__(self):
        return super().__str__() + f", Shelf life: {self.shelf_life}"

# UserManager class

class UserManager:
    def __init__(self, master, user_file='users.json'):
        self.master = master
        self.user_file = user_file
        self.user_data = self.load_users()
        self.create_login_screen()

    def load_users(self):
        try:
            with open(self.user_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.user_file, 'w') as file:
            json.dump(self.user_data, file)

    def create_login_screen(self):
        self.clear_screen()
        
        # Create a frame to center elements
        self.frame = ctk.CTkFrame(self.master)
        self.frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Ensure the frame is centered
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Create login screen
        ctk.CTkLabel(self.frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.username_entry = ctk.CTkEntry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        ctk.CTkLabel(self.frame, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.password_entry = ctk.CTkEntry(self.frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Buttons for login and registration
        ctk.CTkButton(self.frame, text="Login", command=self.login_user).grid(row=2, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame, text="Register", command=self.register_user).grid(row=2, column=1, padx=10, pady=10)
        ctk.CTkButton(self.frame, text="Change Password", command=self.create_change_password_screen).grid(row=3, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame, text="Delete User", command=self.create_delete_user_screen).grid(row=3, column=1, padx=10, pady=10)

    def clear_screen(self):
        # Clear all widgets from the current screen
        for widget in self.master.winfo_children():
            widget.destroy()

    def register_user(self):
        # Function to register a new user
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Check password length and if it contains at least one number
        if len(password) < 5 or len(password) > 10:
            messagebox.showerror("Error", "Password must be between 5 and 10 characters long.")
        elif not any(char.isdigit() for char in password):
            messagebox.showerror("Error", "Password must contain at least one number.")
        elif username in self.user_data:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.user_data[username] = password
            self.save_users()
            messagebox.showinfo("Success", f"User {username} registered successfully.")
            self.create_login_screen()

    def login_user(self):
        # Function to log in an existing user
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_data.get(username) == password:
            messagebox.showinfo("Success", "Login successful.")
            self.clear_screen()
            Inventory(self.master, username, self)  # Pass self to enable logout functionality
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def create_change_password_screen(self):
        self.clear_screen()

        # Create a frame to center elements
        self.frame = ctk.CTkFrame(self.master)
        self.frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Ensure the frame is centered
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Create change password screen
        ctk.CTkLabel(self.frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.username_entry = ctk.CTkEntry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Old Password:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.old_password_entry = ctk.CTkEntry(self.frame, show='*')
        self.old_password_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="New Password:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.new_password_entry = ctk.CTkEntry(self.frame, show='*')
        self.new_password_entry.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkButton(self.frame, text="Change Password", command=self.change_password).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        ctk.CTkButton(self.frame, text="Back", command=self.create_login_screen).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def change_password(self):
        username = self.username_entry.get()
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        if self.user_data.get(username) == old_password:
            self.user_data[username] = new_password
            self.save_users()
            messagebox.showinfo("Success", "Password changed successfully.")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "Invalid username or old password.")

    def create_delete_user_screen(self):
        self.clear_screen()

        # Create a frame to center elements
        self.frame = ctk.CTkFrame(self.master)
        self.frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Ensure the frame is centered
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Create delete user screen
        ctk.CTkLabel(self.frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.username_entry = ctk.CTkEntry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.password_entry = ctk.CTkEntry(self.frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(self.frame, text="Delete User", command=self.delete_user).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        ctk.CTkButton(self.frame, text="Back", command=self.create_login_screen).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def delete_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_data.get(username) == password:
            del self.user_data[username]
            self.save_users()
            messagebox.showinfo("Success", f"User {username} deleted successfully.")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

# Inventory class

class Inventory:
    def __init__(self, master, username, user_manager, inventory_file='inventory.json'):
        self.master = master
        self.username = username
        self.user_manager = user_manager
        self.inventory_file = inventory_file
        self.inventory = self.load_inventory()  # Load inventory from file
        self.transaction_history = []  # List to store transaction history
        self.create_inventory_screen()

    def load_inventory(self):
        # Load inventory from a JSON file
        if os.path.exists(self.inventory_file):
            with open(self.inventory_file, 'r') as file:
                data = json.load(file)
                return [self.create_product_from_dict(item) for item in data]
        return []

    def save_inventory(self):
        # Save inventory to a JSON file
        with open(self.inventory_file, 'w') as file:
            json.dump([product.to_dict() for product in self.inventory], file)

    def create_product_from_dict(self, data):
        # Create product instances from dictionary data
        supplier = Supplier(data['supplier'], "contact@example.com")  # Simplified for demonstration
        if data['type'] == 'PerishableProduct':
            expiration_date = datetime.strptime(data['expiration_date'], '%Y-%m-%d')
            return PerishableProduct(data['name'], data['quantity'], data['price'], expiration_date, supplier, data['min_stock'], data['max_stock'])
        elif data['type'] == 'NonPerishableProduct':
            return NonPerishableProduct(data['name'], data['quantity'], data['price'], data['shelf_life'], supplier, data['min_stock'], data['max_stock'])
        else:
            return Product(data['name'], data['quantity'], data['price'], supplier, data['min_stock'], data['max_stock'])

    def create_inventory_screen(self):
        self.clear_screen()

        # Create a frame to center elements
        self.frame = ctk.CTkFrame(self.master)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        # Ensure the frame is centered
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Inventory management screen
        ctk.CTkLabel(self.frame, text=f"Inventory Management - User: {self.username}").grid(row=0, column=0, columnspan=6, pady=10)

        # Widget to display inventory
        self.tree = ctk.CTkFrame(self.frame)
        self.tree.grid(row=1, column=0, columnspan=6, pady=10)

        self.product_list = ctk.CTkTextbox(self.tree, width=600, height=200)
        self.product_list.pack()

        # Display loaded inventory
        for product in self.inventory:
            self.product_list.insert(ctk.END, f"{product}\n")

        # Input fields for product details
        ctk.CTkLabel(self.frame, text="Product Name:").grid(row=2, column=0, pady=5, sticky='e')
        self.name_entry = ctk.CTkEntry(self.frame)
        self.name_entry.grid(row=2, column=1, pady=5)
        self.name_entry.bind("<FocusOut>", self.autocomplete_product_details)

        ctk.CTkLabel(self.frame, text="Quantity:").grid(row=2, column=2, pady=5, sticky='e')
        self.quantity_entry = ctk.CTkEntry(self.frame)
        self.quantity_entry.grid(row=2, column=3, pady=5)

        ctk.CTkLabel(self.frame, text="Price:").grid(row=3, column=0, pady=5, sticky='e')
        self.price_entry = ctk.CTkEntry(self.frame)
        self.price_entry.grid(row=3, column=1, pady=5)

        ctk.CTkLabel(self.frame, text="Supplier:").grid(row=3, column=2, pady=5, sticky='e')
        self.supplier_entry = ctk.CTkEntry(self.frame)
        self.supplier_entry.grid(row=3, column=3, pady=5)

        ctk.CTkLabel(self.frame, text="Contact of Distributor:").grid(row=4, column=0, pady=5, sticky='e')
        self.distributor_contact_entry = ctk.CTkEntry(self.frame)
        self.distributor_contact_entry.grid(row=4, column=1, pady=5)

        ctk.CTkLabel(self.frame, text="Min Stock:").grid(row=4, column=2, pady=5, sticky='e')
        self.min_stock_entry = ctk.CTkEntry(self.frame)
        self.min_stock_entry.grid(row=4, column=3, pady=5)

        ctk.CTkLabel(self.frame, text="Max Stock:").grid(row=5, column=0, pady=5, sticky='e')
        self.max_stock_entry = ctk.CTkEntry(self.frame)
        self.max_stock_entry.grid(row=5, column=1, pady=5)

        # Additional input for product type and expiration/shelf life
        self.product_type_var = ctk.StringVar(value="Non-Perishable")
        ctk.CTkLabel(self.frame, text="Product Type:").grid(row=5, column=2, pady=5, sticky='e')
        product_type_menu = ctk.CTkOptionMenu(self.frame, values=["Non-Perishable", "Perishable"], variable=self.product_type_var, command=self.toggle_expiration_entry)
        product_type_menu.grid(row=5, column=3, pady=5)

        ctk.CTkLabel(self.frame, text="Expiration Date (YYYY-MM-DD) / Shelf Life:").grid(row=6, column=0, pady=5, sticky='e')
        self.expiration_entry = ctk.CTkEntry(self.frame)
        self.expiration_entry.grid(row=6, column=1, pady=5)

        # Initialize expiration entry state
        self.toggle_expiration_entry("Non-Perishable")

        # Action buttons
        ctk.CTkButton(self.frame, text="Add Product", command=self.add_product).grid(row=10, column=0, pady=5, padx=5)
        ctk.CTkButton(self.frame, text="Update Product", command=self.update_product).grid(row=10, column=1, pady=5, padx=5)
        ctk.CTkButton(self.frame, text="Remove Product", command=self.remove_product).grid(row=10, column=2, pady=5, padx=5)
        ctk.CTkButton(self.frame, text="Generate Report", command=self.generate_report).grid(row=10, column=3, pady=5, padx=5)
        ctk.CTkButton(self.frame, text="Search Product", command=self.search_product).grid(row=10, column=4, pady=5, padx=5)
        ctk.CTkButton(self.frame, text="Log Out", command=self.logout).grid(row=10, column=5, pady=5, padx=5)
        ctk.CTkButton(self.frame, text="Exit", command=self.master.quit).grid(row=10, column=6, pady=5, padx=5)

    def toggle_expiration_entry(self, selected_type):
        # Enable or disable the expiration date entry based on product type
        if selected_type == "Perishable":
            self.expiration_entry.configure(state='normal')
        else:
            self.expiration_entry.configure(state='disabled')
            self.expiration_entry.delete(0, ctk.END)  # Clear the field if disabled

    def clear_screen(self):
        # Clear all widgets from the current screen
        for widget in self.master.winfo_children():
            widget.destroy()

    def autocomplete_product_details(self, event):
        # Function to autocomplete product details based on the product name
        name = self.name_entry.get()
        for product in self.inventory:
            if product.name == name:
                self.quantity_entry.delete(0, ctk.END)
                self.quantity_entry.insert(0, product.quantity)
                self.price_entry.delete(0, ctk.END)
                self.price_entry.insert(0, product.price)
                self.supplier_entry.delete(0, ctk.END)
                self.supplier_entry.insert(0, product.supplier.name)
                self.distributor_contact_entry.delete(0, ctk.END)
                self.distributor_contact_entry.insert(0, product.supplier.contact_info)
                self.min_stock_entry.delete(0, ctk.END)
                self.min_stock_entry.insert(0, product.min_stock)
                self.max_stock_entry.delete(0, ctk.END)
                self.max_stock_entry.insert(0, product.max_stock)
                if isinstance(product, PerishableProduct):
                    self.product_type_var.set("Perishable")
                    self.expiration_entry.configure(state='normal')
                    self.expiration_entry.delete(0, ctk.END)
                    self.expiration_entry.insert(0, product.expiration_date.strftime('%Y-%m-%d'))
                else:
                    self.product_type_var.set("Non-Perishable")
                    self.expiration_entry.configure(state='normal')
                    self.expiration_entry.delete(0, ctk.END)
                    self.expiration_entry.insert(0, product.shelf_life)
                break

    def add_product(self):
        # Function to add a new product to the inventory
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get() or 0)
        price = float(self.price_entry.get() or 0.0)
        supplier_name = self.supplier_entry.get() or 'N/A'
        supplier = Supplier(supplier_name, "contact@example.com")  # Simplified for demonstration
        min_stock = int(self.min_stock_entry.get() or 0)
        max_stock = int(self.max_stock_entry.get() or 0)
        product_type = self.product_type_var.get()
        expiration_or_shelf_life = self.expiration_entry.get()

        if product_type == "Perishable":
            expiration_date = datetime.strptime(expiration_or_shelf_life, "%Y-%m-%d")
            product = PerishableProduct(name, quantity, price, expiration_date, supplier, min_stock, max_stock)
        else:
            product = NonPerishableProduct(name, quantity, price, expiration_or_shelf_life, supplier, min_stock, max_stock)

        # Add product to the inventory list and update display
        self.inventory.append(product)
        self.product_list.insert(ctk.END, f"{product}\n")
        self.transaction_history.append(f"Added {name} at {datetime.now()}")
        self.clear_entries()
        self.save_inventory()  # Save inventory after adding a product

    def update_product(self):
        # Function to update an existing product
        selected_item = self.product_list.get("1.0", ctk.END).splitlines()[0]  # Example, needs actual selection
        selected_name = selected_item.split(":")[0]  # Extract the product name from the selected item

        # Find the product in the inventory
        for product in self.inventory:
            if product.name == selected_name:
                # Update the product details
                product.name = self.name_entry.get() or product.name
                product.quantity = int(self.quantity_entry.get() or product.quantity)
                product.price = float(self.price_entry.get() or product.price)
                supplier_name = self.supplier_entry.get() or product.supplier.name
                product.supplier = Supplier(supplier_name, "contact@example.com")  # Simplified for demonstration
                product.min_stock = int(self.min_stock_entry.get() or product.min_stock)
                product.max_stock = int(self.max_stock_entry.get() or product.max_stock)
                product_type = self.product_type_var.get()
                expiration_or_shelf_life = self.expiration_entry.get()

                if product_type == "Perishable" and isinstance(product, PerishableProduct):
                    product.expiration_date = datetime.strptime(expiration_or_shelf_life, "%Y-%m-%d")
                elif product_type == "Non-Perishable" and isinstance(product, NonPerishableProduct):
                    product.shelf_life = expiration_or_shelf_life

                # Update the display
                self.product_list.delete("1.0", ctk.END)
                for prod in self.inventory:
                    self.product_list.insert(ctk.END, f"{prod}\n")

                self.transaction_history.append(f"Updated {product.name} at {datetime.now()}")
                self.clear_entries()
                self.save_inventory()  # Save inventory after updating a product
                break

    def remove_product(self):
        # Function to remove a product
        selected_item = self.product_list.get("1.0", ctk.END).splitlines()[0]  # Example, needs actual selection
        selected_name = selected_item.split(":")[0]  # Extract the product name from the selected item

        # Find and remove the product from the inventory
        self.inventory = [product for product in self.inventory if product.name != selected_name]

        # Update the display
        self.product_list.delete("1.0", ctk.END)
        for product in self.inventory:
            self.product_list.insert(ctk.END, f"{product}\n")

        self.transaction_history.append(f"Removed {selected_name} at {datetime.now()}")
        self.save_inventory()  # Save inventory after removing a product

    def search_product(self):
        # Function to search for products by name
        search_window = ctk.CTkToplevel(self.master)
        search_window.title("Search Product")
        ctk.CTkLabel(search_window, text="Enter product name to search:").pack(pady=10)
        search_entry = ctk.CTkEntry(search_window)
        search_entry.pack(pady=10)
        result_text = ctk.CTkTextbox(search_window, width=400, height=300)
        result_text.pack(pady=10)

        def perform_search():
            search_name = search_entry.get().lower()
            results = [str(product) for product in self.inventory if search_name in product.name.lower()]
            result_text.delete("1.0", ctk.END)
            if results:
                result_text.insert(ctk.END, "\n".join(results))
            else:
                result_text.insert(ctk.END, "No products found.")

        ctk.CTkButton(search_window, text="Search", command=perform_search).pack(pady=10)

    def generate_report(self):
        # Function to generate an inventory report
        report_window = ctk.CTkToplevel(self.master)
        report_window.title("Inventory Report")
        report_text = ctk.CTkTextbox(report_window, width=400, height=400)
        report_text.pack()
        report_text.insert(ctk.END, "Inventory Report\n\n")
        for product in self.inventory:
            report_text.insert(ctk.END, f"{product}\n")

        # Report for products low on stock
        report_text.insert(ctk.END, "\nLow Stock Products:\n")
        low_stock_products = [str(product) for product in self.inventory if product.quantity < product.min_stock]
        report_text.insert(ctk.END, "\n".join(low_stock_products) if low_stock_products else "None\n")

        # Report for perishable products near expiration
        report_text.insert(ctk.END, "\nProducts Near Expiration:\n")
        near_expiry = [str(product) for product in self.inventory if isinstance(product, PerishableProduct) and product.is_near_expiration()]
        report_text.insert(ctk.END, "\n".join(near_expiry) if near_expiry else "None\n")

        # Report for expired products
        report_text.insert(ctk.END, "\nExpired Products:\n")
        expired = [str(product) for product in self.inventory if isinstance(product, PerishableProduct) and product.is_expired()]
        report_text.insert(ctk.END, "\n".join(expired) if expired else "None\n")

    def logout(self):
        # Function to log out and return to the login screen
        self.user_manager.create_login_screen()  # Calls the UserManager method to create the login screen

    def clear_entries(self):
        # Clear all input fields in the inventory management screen
        self.name_entry.delete(0, ctk.END)
        self.quantity_entry.delete(0, ctk.END)
        self.price_entry.delete(0, ctk.END)
        self.supplier_entry.delete(0, ctk.END)
        self.distributor_contact_entry.delete(0, ctk.END)
        self.min_stock_entry.delete(0, ctk.END)
        self.max_stock_entry.delete(0, ctk.END)
        self.expiration_entry.delete(0, ctk.END)

def center_window(root, width=900, height=700):
    # Function to center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    root.geometry(f'{width}x{height}+{position_right}+{position_top}')

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Warehouse Management System")
    center_window(root)  # Center the main window
    UserManager(root)    # Create the initial UserManager screen
    root.mainloop()      # Start the main event loop