import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# No specific theme or appearance settings are applied to keep default colors

class UserManager:
    def __init__(self, master):
        self.master = master
        self.user_data = {}  # Temporary storage for user data
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        
        # Create a frame to center elements
        self.frame = ctk.CTkFrame(self.master)
        self.frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Ensure the frame is centered
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Create login screen
        ctk.CTkLabel(self.frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.username_entry = ctk.CTkEntry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.password_entry = ctk.CTkEntry(self.frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Buttons for login and registration
        ctk.CTkButton(self.frame, text="Login", command=self.login_user).grid(row=2, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame, text="Register", command=self.register_user).grid(row=2, column=1, padx=10, pady=10)

    def clear_screen(self):
        # Clear all widgets from the current screen
        for widget in self.master.winfo_children():
            widget.destroy()

    def register_user(self):
        # Function to register a new user
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.user_data:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.user_data[username] = password
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

class Inventory:
    def __init__(self, master, username, user_manager):
        self.master = master
        self.username = username
        self.user_manager = user_manager
        self.inventory = []  # List to store inventory items
        self.transaction_history = []  # List to store transaction history
        self.create_inventory_screen()

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

        # Input fields for product details
        ctk.CTkLabel(self.frame, text="Product Name:").grid(row=2, column=0, pady=5, sticky='e')
        self.name_entry = ctk.CTkEntry(self.frame)
        self.name_entry.grid(row=2, column=1, pady=5)

        ctk.CTkLabel(self.frame, text="Quantity:").grid(row=3, column=0, pady=5, sticky='e')
        self.quantity_entry = ctk.CTkEntry(self.frame)
        self.quantity_entry.grid(row=3, column=1, pady=5)

        ctk.CTkLabel(self.frame, text="Price:").grid(row=4, column=0, pady=5, sticky='e')
        self.price_entry = ctk.CTkEntry(self.frame)
        self.price_entry.grid(row=4, column=1, pady=5)

        ctk.CTkLabel(self.frame, text="Supplier:").grid(row=5, column=0, pady=5, sticky='e')
        self.supplier_entry = ctk.CTkEntry(self.frame)
        self.supplier_entry.grid(row=5, column=1, pady=5)

        ctk.CTkLabel(self.frame, text="Min Stock:").grid(row=6, column=0, pady=5, sticky='e')
        self.min_stock_entry = ctk.CTkEntry(self.frame)
        self.min_stock_entry.grid(row=6, column=1, pady=5)

        ctk.CTkLabel(self.frame, text="Max Stock:").grid(row=7, column=0, pady=5, sticky='e')
        self.max_stock_entry = ctk.CTkEntry(self.frame)
        self.max_stock_entry.grid(row=7, column=1, pady=5)

        # Action buttons
        ctk.CTkButton(self.frame, text="Add Product", command=self.add_product).grid(row=8, column=0, pady=10, padx=5)
        ctk.CTkButton(self.frame, text="Update Product", command=self.update_product).grid(row=8, column=1, pady=10, padx=5)
        ctk.CTkButton(self.frame, text="Remove Product", command=self.remove_product).grid(row=8, column=2, pady=10, padx=5)
        ctk.CTkButton(self.frame, text="Generate Report", command=self.generate_report).grid(row=8, column=3, pady=10, padx=5)
        ctk.CTkButton(self.frame, text="Log Out", command=self.logout).grid(row=8, column=4, pady=10, padx=5)
        ctk.CTkButton(self.frame, text="Exit", command=self.master.quit).grid(row=8, column=5, pady=10, padx=5)

    def clear_screen(self):
        # Clear all widgets from the current screen
        for widget in self.master.winfo_children():
            widget.destroy()

    def add_product(self):
        # Function to add a new product to the inventory
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get() or 0)
        price = float(self.price_entry.get() or 0.0)
        supplier = self.supplier_entry.get() or 'N/A'
        min_stock = int(self.min_stock_entry.get() or 0)
        max_stock = int(self.max_stock_entry.get() or 0)

        # Create a dictionary for the product details
        product = {
            'name': name,
            'quantity': quantity,
            'price': price,
            'supplier': supplier,
            'min_stock': min_stock,
            'max_stock': max_stock
        }

        # Add product to the inventory list and update display
        self.inventory.append(product)
        self.product_list.insert(ctk.END, f"{name}, {quantity}, {price}, {supplier}, {min_stock}, {max_stock}\n")
        self.transaction_history.append(f"Added {name} at {datetime.now()}")
        self.clear_entries()

    def update_product(self):
        # Function to update an existing product (example, needs real selection handling)
        selected_item = self.product_list.get("1.0", ctk.END).splitlines()[0]  # Example, needs actual selection
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get() or 0)
        price = float(self.price_entry.get() or 0.0)
        supplier = self.supplier_entry.get() or 'N/A'
        min_stock = int(self.min_stock_entry.get() or 0)
        max_stock = int(self.max_stock_entry.get() or 0)

        # Update the product details (example implementation)
        updated_product = f"{name}, {quantity}, {price}, {supplier}, {min_stock}, {max_stock}\n"
        self.product_list.delete("1.0", ctk.END)  # Replace with correct index handling
        self.product_list.insert(ctk.END, updated_product)
        self.transaction_history.append(f"Updated {name} at {datetime.now()}")
        self.clear_entries()

    def remove_product(self):
        # Function to remove a product (example, needs real selection handling)
        selected_item = self.product_list.get("1.0", ctk.END).splitlines()[0]  # Example, needs actual selection
        self.product_list.delete("1.0", ctk.END)  # Replace with correct index handling
        self.transaction_history.append(f"Removed {selected_item.split(',')[0]} at {datetime.now()}")

    def generate_report(self):
        # Function to generate an inventory report
        report_window = ctk.CTkToplevel(self.master)
        report_window.title("Inventory Report")
        report_text = ctk.CTkTextbox(report_window, width=400, height=400)
        report_text.pack()
        report_text.insert(ctk.END, "Inventory Report\n\n")
        for product in self.inventory:
            report_text.insert(ctk.END, f"{product['name']} - {product['quantity']} units - ${product['price']} - Supplier: {product['supplier']} - Min Stock: {product['min_stock']} - Max Stock: {product['max_stock']}\n")

    def logout(self):
        # Function to log out and return to the login screen
        self.user_manager.create_login_screen()  # Calls the UserManager method to create the login screen

    def clear_entries(self):
        # Clear all input fields in the inventory management screen
        self.name_entry.delete(0, ctk.END)
        self.quantity_entry.delete(0, ctk.END)
        self.price_entry.delete(0, ctk.END)
        self.supplier_entry.delete(0, ctk.END)
        self.min_stock_entry.delete(0, ctk.END)
        self.max_stock_entry.delete(0, ctk.END)

def center_window(root, width=900, height=600):
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
