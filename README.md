# proyecto-POO

# Inventory Management System

This repository contains a simple inventory management system built in Python. The system manages user authentication, product details, and inventory operations for both perishable and non-perishable products.

## Mermaid

```mermaid
classDiagram
    class UserManager {
        -user_file : string
        -user_data : dict
        +__init__(user_file)
        +load_users() dict
        +save_users()
        +register_user()
        +login_user() bool
    }

    class Supplier {
        -name : string
        -contact_info : string
        +__init__(name, contact_info)
    }

    class Product {
        -name : string
        -quantity : int
        -price : float
        -supplier : Supplier
        -min_stock : int
        -max_stock : int
        +__init__(name, quantity, price, supplier, min_stock, max_stock)
        +update_quantity(quantity)
        +update_price(price)
        +check_stock()
        +__str__() string
    }

    class PerishableProduct {
        -expiration_date : datetime
        +__init__(name, quantity, price, expiration_date, supplier, min_stock, max_stock)
        +__str__() string
    }

    class NonPerishableProduct {
        -shelf_life : string
        +__init__(name, quantity, price, shelf_life, supplier, min_stock, max_stock)
        +__str__() string
    }

    class Inventory {
        -total_inv : list
        -transaction_history : list
        +__init__()
        +show_inventory()
        +add_product(Product)
        +remove_product(product_index)
        +update_product(product_index, quantity, price)
        +search_product(name, category, min_price, max_price) list
        +generate_report(report_type)
    }

    UserManager "1" --> "1..*" Product : uses
    Product <|-- PerishableProduct : extends
    Product <|-- NonPerishableProduct : extends
    Supplier "1" --> "1..*" Product : supplies
    Inventory "1" --> "1..*" Product : manages
```

## Overview

The code is organized into several classes, each with specific responsibilities:

1. **User Management**:
    - `UserManager`: Handles user registration and login, with credentials stored in a JSON file.

2. **Product Management**:
    - `Product`: A base class representing a generic product with attributes like name, quantity, price, supplier, and stock levels.
    - `PerishableProduct`: Inherits from `Product`, adding an expiration date.
    - `NonPerishableProduct`: Inherits from `Product`, adding a shelf life.

3. **Supplier Management**:
    - `Supplier`: Represents a supplier with a name and contact information.

4. **Inventory Management**:
    - `Inventory`: Manages the list of products in stock, including adding, removing, updating, and searching products. It also handles the generation of various inventory reports.

## Detailed Class Breakdown

### UserManager
This class manages user accounts. Users are stored in a `users.json` file, and the class provides methods to load, save, register, and authenticate users.

- **Attributes**:
  - `user_file`: The file where user data is stored.
  - `user_data`: A dictionary holding user credentials.

- **Methods**:
  - `load_users`: Loads user data from the JSON file.
  - `save_users`: Saves user data to the JSON file.
  - `register_user`: Allows new users to register.
  - `login_user`: Authenticates existing users.

### Supplier
The `Supplier` class holds basic information about suppliers, including their name and contact information.

### Product
A base class representing a product in the warehouse.

- **Attributes**:
  - `name`, `quantity`, `price`, `supplier`, `min_stock`, `max_stock`: Basic attributes describing the product.
  
- **Methods**:
  - `update_quantity`: Updates the product's quantity.
  - `update_price`: Updates the product's price.
  - `check_stock`: Checks if the product is within the stock limits.

### PerishableProduct
This class represents products that have an expiration date, extending the base `Product` class.

- **Attributes**:
  - Inherits from `Product`.
  - `expiration_date`: The date after which the product is no longer usable.

### NonPerishableProduct
This class represents products with a shelf life, also extending the base `Product` class.

- **Attributes**:
  - Inherits from `Product`.
  - `shelf_life`: The duration for which the product can be stored.

### Inventory
The `Inventory` class manages the warehouse's stock of products.

- **Attributes**:
  - `total_inv`: A list of products currently in inventory.
  - `transaction_history`: A log of all transactions performed on the inventory.

- **Methods**:
  - `show_inventory`: Displays all products in the inventory.
  - `add_product`: Adds a new product to the inventory.
  - `remove_product`: Removes a product from the inventory by index.
  - `update_product`: Updates the quantity and/or price of a product.
  - `search_product`: Searches for products based on name, category, or price range.
  - `generate_report`: Generates various types of reports, including full inventory, low stock, expiring soon, and expired products.

## Application Workflow

1. **User Registration/Login**:
   - Users can register or log in to access the warehouse management features.
   
2. **Inventory Management**:
   - After logging in, users can add, remove, edit, and search for products.
   - They can also generate inventory reports, including:
     - Full inventory
     - Low stock levels
     - Products expiring soon
     - Expired products

3. **Reports**:
   - The system can generate different types of inventory reports, which are crucial for managing stock levels and ensuring that perishable goods are handled properly.
