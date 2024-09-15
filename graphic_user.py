import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

# No se aplican configuraciones de tema ni apariencia para mantener los colores predeterminados

class UserManager:
    def __init__(self, master):
        self.master = master
        self.user_data = {}  # Almacenamiento temporal para usuarios
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        
        # Crear un Frame para centrar los elementos
        self.frame = ctk.CTkFrame(self.master)
        self.frame.grid(row=0, column=0, padx=20, pady=20)
        
        # Aseguramos que el Frame esté centrado
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Crear pantalla de inicio de sesión
        ctk.CTkLabel(self.frame, text="Username:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.username_entry = ctk.CTkEntry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(self.frame, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.password_entry = ctk.CTkEntry(self.frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(self.frame, text="Login", command=self.login_user).grid(row=2, column=0, padx=10, pady=10)
        ctk.CTkButton(self.frame, text="Register", command=self.register_user).grid(row=2, column=1, padx=10, pady=10)

    def clear_screen(self):
        # Limpiar la pantalla
        for widget in self.master.winfo_children():
            widget.destroy()

    def register_user(self):
        # Función para registrar un usuario
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.user_data:
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.user_data[username] = password
            messagebox.showinfo("Success", f"User {username} registered successfully.")
            self.create_login_screen()

    def login_user(self):
        # Función para iniciar sesión
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_data.get(username) == password:
            messagebox.showinfo("Success", "Login successful.")
            self.clear_screen()
            Inventory(self.master, username, self)  # Pasar self para habilitar la funcionalidad de logout
        else:
            messagebox.showerror("Error", "Invalid username or password.")

class Inventory:
    def __init__(self, master, username, user_manager):
        self.master = master
        self.username = username
        self.user_manager = user_manager
        self.inventory = []  # Lista para almacenar los elementos del inventario
        self.transaction_history = []  # Historial de transacciones
        self.create_inventory_screen()

    def create_inventory_screen(self):
        self.clear_screen()

        # Crear un Frame para centrar los elementos
        self.frame = ctk.CTkFrame(self.master)
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        # Aseguramos que el Frame esté centrado
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Crear pantalla de gestión de inventario
        ctk.CTkLabel(self.frame, text=f"Inventory Management - User: {self.username}").grid(row=0, column=0, columnspan=6, pady=10)

        # Widget para mostrar el inventario
        self.tree = ctk.CTkFrame(self.frame)
        self.tree.grid(row=1, column=0, columnspan=6, pady=10)

        self.product_list = ctk.CTkTextbox(self.tree, width=600, height=200)
        self.product_list.pack()

        # Campos de entrada
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

        # Botones de acciones
        ctk.CTkButton(self.frame, text="Add Product", command=self.add_product).grid(row=8, column=0, pady=10, padx=5)
        ctk.CTkButton(self.frame, text="Update Product", command=self.update_product).grid(row=8, column=1, pady=10, padx=5)
        ctk.CTkButton(self.frame, text="Remove Product", command=self.remove_product).grid(row=8, column=2, pady=10, padx=5)
        ctk.CTkButton(self.frame, text="Generate Report", command=self.generate_report).grid(row=8, column=3, pady=10, padx=5)
        ctk.CTkButton(self.frame, text="Log Out", command=self.logout).grid(row=8, column=4, pady=10, padx=5)
        ctk.CTkButton(self.frame, text="Exit", command=self.master.quit).grid(row=8, column=5, pady=10, padx=5)

    def clear_screen(self):
        # Limpiar la pantalla
        for widget in self.master.winfo_children():
            widget.destroy()

    def add_product(self):
        # Función para añadir un producto
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get() or 0)
        price = float(self.price_entry.get() or 0.0)
        supplier = self.supplier_entry.get() or 'N/A'
        min_stock = int(self.min_stock_entry.get() or 0)
        max_stock = int(self.max_stock_entry.get() or 0)

        product = {
            'name': name,
            'quantity': quantity,
            'price': price,
            'supplier': supplier,
            'min_stock': min_stock,
            'max_stock': max_stock
        }

        self.inventory.append(product)
        self.product_list.insert(ctk.END, f"{name}, {quantity}, {price}, {supplier}, {min_stock}, {max_stock}\n")
        self.transaction_history.append(f"Added {name} at {datetime.now()}")
        self.clear_entries()

    def update_product(self):
        # Función para actualizar un producto
        selected_item = self.product_list.get("1.0", ctk.END).splitlines()[0]  # Ejemplo, necesita selección real
        name = self.name_entry.get()
        quantity = int(self.quantity_entry.get() or 0)
        price = float(self.price_entry.get() or 0.0)
        supplier = self.supplier_entry.get() or 'N/A'
        min_stock = int(self.min_stock_entry.get() or 0)
        max_stock = int(self.max_stock_entry.get() or 0)

        updated_product = f"{name}, {quantity}, {price}, {supplier}, {min_stock}, {max_stock}\n"
        self.product_list.delete("1.0", ctk.END)  # Reemplazar con manejo correcto de índices
        self.product_list.insert(ctk.END, updated_product)
        self.transaction_history.append(f"Updated {name} at {datetime.now()}")
        self.clear_entries()

    def remove_product(self):
        # Función para eliminar un producto
        selected_item = self.product_list.get("1.0", ctk.END).splitlines()[0]  # Ejemplo, necesita selección real
        self.product_list.delete("1.0", ctk.END)  # Reemplazar con manejo correcto de índices
        self.transaction_history.append(f"Removed {selected_item.split(',')[0]} at {datetime.now()}")

    def generate_report(self):
        # Función para generar reportes de inventario
        report_window = ctk.CTkToplevel(self.master)
        report_window.title("Inventory Report")
        report_text = ctk.CTkTextbox(report_window, width=400, height=400)
        report_text.pack()
        report_text.insert(ctk.END, "Inventory Report\n\n")
        for product in self.inventory:
            report_text.insert(ctk.END, f"{product['name']} - {product['quantity']} units - ${product['price']} - Supplier: {product['supplier']} - Min Stock: {product['min_stock']} - Max Stock: {product['max_stock']}\n")

    def logout(self):
        # Función para cerrar sesión
        self.user_manager.create_login_screen()  # Llama al método de UserManager para crear la pantalla de inicio de sesión

    def clear_entries(self):
        # Limpiar entradas de datos
        self.name_entry.delete(0, ctk.END)
        self.quantity_entry.delete(0, ctk.END)
        self.price_entry.delete(0, ctk.END)
        self.supplier_entry.delete(0, ctk.END)
        self.min_stock_entry.delete(0, ctk.END)
        self.max_stock_entry.delete(0, ctk.END)

def center_window(root, width=900, height=600):
    # Centrar la ventana en la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    root.geometry(f'{width}x{height}+{position_right}+{position_top}')

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Warehouse Management System")
    center_window(root)  # Centrar la ventana
    UserManager(root)
    root.mainloop()
##deadfasdasdasdasdas