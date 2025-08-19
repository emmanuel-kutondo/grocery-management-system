#!/usr/bin/env python3
import csv
import os
from datetime import datetime
now = datetime.now()

FILENAME = "grocery_products.csv"

grocery_products = {}

def load_from_csv(filename=FILENAME):
    """Load grocery products from CSV """
    global grocery_products
    if not os.path.exists(filename):
        return
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        grocery_products = {
            int(row['id']): {
                'name': row['name'],
                'quantity': float(row['quantity']),
                'units': row['units'],
                'unit_price': float(row['price/units'])
            }
            for row in reader
        }

def save_to_csv(filename=FILENAME):
    """Save grocery products to a CSV file permanently."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'quantity', 'units', 'price/units'])
        for product_id, details in grocery_products.items():
            writer.writerow([
                product_id,
                details['name'],
                details['quantity'],
                details['units'],
                details['unit_price']
            ])

def get_available_products():
    """Display all available products in the inventory"""
    if not grocery_products:
        print("No products available in store.")
    else:
        print("\n=== Available Products ===")
        print(f"{'ID':<5}{'Name':<20}{'Quantity':<10}{'Units':<10}{'Price/Unit':<10}")
        for product_id, details in grocery_products.items():
            print(
                f"{product_id:<5}{details['name']:<20}{details['quantity']:<10}{details['units']:<10}sh {details['unit_price']:<10.2f}"
            )
            total_value = 0
        for product_id, details in grocery_products.items():
             total_value += details['quantity'] * details['unit_price']
        print(f"\nTotal products value: sh{total_value:.2f}")


def register_item():
    """Register a new product"""
    print("\n=== Register New Product ===")
    global grocery_products
    try:
        name = input("Enter name of item(or '0' to go back): ").strip()
        if name.lower() == '0':
            return
        if not name:
            print("Error: Name cannot be empty!")
            return None
        for details in grocery_products.values():
            if details["name"].lower() == name.lower():
                print(f"Error: product '{name}' already exists in the inventory.")
                return None

        quantity = input("Enter quantity of the item(0r '0' to go back: ").strip()
        if quantity.lower() == '0':
            return
        if not quantity.replace('.', '', 1).isdigit() or float(quantity) <= 0:
            print("Error: Quantity must be a positive number!")
            return None
        quantity = float(quantity) if '.' in quantity else int(quantity)

        units = input("Enter unit (e.g., kg, g, l, pieces)(or '0' to go back: ").strip().lower()
        if units.lower() == '0':
            return
        if not units:
            print("Error: Unit cannot be empty!")
            return None


        unit_price = input("Enter price per unit(or '0' to go back): ").strip()
        if unit_price.lower() == '0':
            return
        if not unit_price.replace('.', '', 1).isdigit() or float(unit_price) <= 0:
            print("Error: Price must be a positive number!")
            return None
        unit_price = float(unit_price)

        product_id = max(grocery_products.keys(), default=0) + 1
        grocery_products[product_id] = {
            'name': name,
            'quantity': quantity,
            'units': units,
            'unit_price': unit_price
        }
        save_to_csv()  # auto-save
        print(f"\nAdded successfully: Product '{name}' added with ID {product_id}!")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_product():
    """Update a product"""
    print("\n___Update Product___")
    item_id = input("Enter the ID of item to update(or '0' to go back): ")
    if item_id.lower() == '0':
        return
    if not item_id.isdigit() or int(item_id) not in grocery_products:
        print("Error: Invalid product ID!")
        return

    product_id = str(item_id)
    details = grocery_products[product_id]

    print(f"Current details: {details}")

    try:
        name = input("Enter new name (leave blank to keep current)(or '0' to go back): ").strip()
        if name.lower() == '0':
            return
        if name:
            details["name"] = name

        quantity = input("Enter new quantity (leave blank to keep current)(or '0' to go back): ").strip()
        if quantity.lower() == '0':
            return
        if quantity:
            if not quantity.replace('.', '', 1).isdigit() or float(quantity) <= 0:
                print("Error: Quantity must be a positive number!")
                return
            details["quantity"] = float(quantity) if '.' in quantity else int(quantity)

        units = input("Enter new units (leave blank to keep current)(or '0' to go back): ").strip().lower()
        if units.lower() == '0':
            return
        if units:
            details["units"] = units

        unit_price = input("Enter new price (leave blank to keep current)(or '0' to goback): ").strip()
        if unit_price.lower() == '0':
            return
        if unit_price:
            if not unit_price.replace('.', '', 1).isdigit() or float(unit_price) <= 0:
                print("Error: Price must be a positive number!")
                return
            details["unit_price"] = float(unit_price)

        save_to_csv()  # auto-save
        print(f"Product ID {product_id} updated successfully!")
    except Exception as e:
        print(f"An error has occurred: {e}")

def delete_item():
    """Delete a product by name"""
    print("\n___Delete Item___")
    item_name = input("Enter item name to delete(or '0' to go back): ").strip().lower()
    if item_name.lower() == '0':
        return
    for product_id, details in list(grocery_products.items()):
        if details["name"].lower() == item_name:
            del grocery_products[product_id]
            save_to_csv()  # auto-save
            print(f"Item '{item_name}' removed successfully.")
            return
    print("Item not found")

def restock_item():
    """Restock an existing product"""
    print("\n==== Restock a Product ====")
    if not grocery_products:
        print("No products in the system yet.")
        return
    name = input("Enter product name to restock(or '0' to go back): ").strip().lower()
    if name == '0':
        return
    for product_id ,product in grocery_products.items():
        if product['name'].lower() == name:
            print(f"Current stock: {product['quantity']} {product['units']}")
            quantity = input("Enter quantity to add (or '0' to fo back): ").strip()
            if quantity.lower() == '0':
                return
            if not quantity.replace('.', '', 1).isdigit() or float(quantity)<=0:
                print("Invalid quantity.")
                return
            product['quantity'] += float(quantity)
            save_to_csv()
            print(f" '{product['name']}' restocked.New quantity: {product['quantity']} {product['units']}")
            return
            print("product not found.")

def search_item():
    """Search for a product by name"""
    print("\n--- Search for a Product ---")
    if not grocery_products:
        print("No products in the system.")
        return

    name = input("Enter the product name(or '0' to go back): ").strip().lower()
    if name.lower() == '0':
        return
    found = False
    for product_id, product in grocery_products.items():
        if name in product['name'].lower():
            print("\nProduct Found:")
            print("ID:", product_id)
            print("Name:", product['name'])
            print("Quantity:", product['quantity'], product['units'])
            print("Price per unit:", product['unit_price'])
            found = True
    if not found:
        print("No product found with that name.")

def sell_product():
    """sell products and update inventory"""
    print("\n=== sell a product===")
    if not grocery_products:
        print("No products available to sell.")
        return

    total_sale = 0
    sold_items = []

    while True:
        name = input("Enter the product name to sell (or '0' to end sale):").strip().lower()
        if name == '0':
            break

        found = False
        for product_id, product in grocery_products.items():
            if product['name'].lower() == name:
                found = True

                quantity = input("Enter quantity to sell (or '0' to cancel this item): ").strip()
                if quantity == '0':
                    break
                if not quantity.replace('.', '', 1).isdigit() or float(quantity) < 1:
                    print("Error: Quantity must be a positive number!")
                    break
                quantity = float(quantity)
                if quantity > product['quantity']:

                    break

                total_price = quantity * product['unit_price']
                product['quantity'] -= quantity
                total_sale += total_price

                sold_items.append(
                    {'name': product['name'], 'quantity_sold': quantity, 'unit_price': product['unit_price'],
                     'units': product['units'], 'total_price': total_price})

                break

        if not found:
            print("Product not found. Please try again.")

    if sold_items:
        save_to_csv()  # Save inventory changes
        print("\n=== RECEIPT ===")
        print("TITANS GROCERY STORE")
        for item in sold_items:
            print(
                f"- {item['name']}: {item['quantity_sold']} {item['units']} @ sh{item['unit_price']} = sh{item['total_price']:.2f}")
        print(f"TOTAL: sh{total_sale:.2f}")
        print("Date/Time:", now.strftime("%d-%m-%Y, %H:%M"))
        print("THANK YOU FOR SHOPPING WITH US!")
        print("========================")
    else:
        print("No items were sold.")



#===== Main Menu =====
if __name__ == "__main__":
    load_from_csv()  # load saved data on startup
    while True:
        print("\nGrocery Management System")
        print("1. Add new product")
        print("2. View all products")
        print("3. Delete item")
        print("4. Update item")
        print("5. Restock item")
        print("6. Search item")
        print("7. sell product")
        print("8. Exit...")

        choice = input("Enter your choice: ")

        if choice == '1':
            register_item()
        elif choice == '2':
            get_available_products()
        elif choice == '3':
            delete_item()
        elif choice == '4':
            update_product()
        elif choice == '5':
            restock_item()
        elif choice == '6':
            search_item()
        elif choice == '7':
            sell_product()
        elif choice == '8':
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Please try again.")
