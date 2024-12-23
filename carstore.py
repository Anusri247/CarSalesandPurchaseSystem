import mysql.connector

# Database Connection
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="123456789",  # Replace with your MySQL password
            database="carsalespurchasedb",
            auth_plugin="mysql_native_password"  # Ensure this database exists
        )
        print("Database connection successful!")
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")
        return None

# Admin Functions
def add_car():
    conn = connect_to_db()
    if conn is None:
        print("Cannot proceed without a database connection.")
        return

    cursor = conn.cursor()

    brand = input("Enter car brand: ")
    model = input("Enter car model: ")
    year = int(input("Enter manufacturing year: "))
    color = input("Enter car color: ")
    price = float(input("Enter car price: "))

    query = """INSERT INTO car_inventory (brand, model, year, color, price)
               VALUES (%s, %s, %s, %s, %s)"""
    data = (brand, model, year, color, price)

    cursor.execute(query, data)
    conn.commit()
    print("Car added successfully!")
    conn.close()

def view_inventory():
    conn = connect_to_db()
    if conn is None:
        print("Cannot proceed without a database connection.")
        return

    cursor = conn.cursor()
    query = "SELECT * FROM car_inventory"
    cursor.execute(query)
    rows = cursor.fetchall()

    print("\nCar Inventory:")
    print(f"{'Car ID':<8} {'Brand':<15} {'Model':<15} {'Year':<6} {'Color':<10} {'Price':<10}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<8} {row[1]:<15} {row[2]:<15} {row[3]:<6} {row[4]:<10} {row[5]:<10.2f}")

    conn.close()

# Customer Functions
def buy_car():
    conn = connect_to_db()
    cursor = conn.cursor()

    car_id = int(input("Enter the Car ID to purchase: "))
    customer_name = input("Enter your name: ")
    customer_phone = input("Enter your phone: ")

    # Insert customer details and the car ID they are purchasing
    query_customer = """INSERT INTO customers (name, phone, car_id, transaction_type)
                        VALUES (%s, %s, %s, 'purchase')"""
    cursor.execute(query_customer, (customer_name, customer_phone, car_id))
    conn.commit()

    # Delete the purchased car from the inventory
    query_remove_car = "DELETE FROM car_inventory WHERE car_id = %s"
    cursor.execute(query_remove_car, (car_id,))
    conn.commit()

    print(f"Transaction for Car ID {car_id} and Customer {customer_name} recorded successfully.")
    conn.close()

# Menus
def admin_menu():
    while True:
        print("\nAdmin Menu")
        print("1. Add Car")
        print("2. View Inventory")
        print("3. View Customers (Transactions)")  # View customers and their transaction details
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_car()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            view_customers()  # View customers with their transactions
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")

def view_customers():
    conn = connect_to_db()
    if conn is None:
        print("Cannot proceed without a database connection.")
        return

    cursor = conn.cursor()
    query = "SELECT customer_id, name, phone FROM customers"
    cursor.execute(query)
    rows = cursor.fetchall()

    print("\nCustomers List:")
    print(f"{'Customer ID':<15} {'Name':<20} {'Phone':<15}")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]:<15} {row[1]:<20} {row[2]:<15}")

    conn.close()



def customer_menu():
    while True:
        print("\nCustomer Menu")
        print("1. View Available Cars")
        print("2. Buy a Car")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_inventory()
        elif choice == "2":
            buy_car()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Try again.")

def main_menu():
    while True:
        print("\n" + "-" * 30)
        print("CAR SALES AND PURCHASE SYSTEM".upper())
        print("-" * 30)
        print("1. Admin")
        print("2. Customer")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            admin_menu()
        elif choice == "2":
            customer_menu()
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Try again.")


def clear_and_add_data():
    conn = connect_to_db()
    if conn is None:
        print("Cannot proceed without a database connection.")
        return

    cursor = conn.cursor()

    # Delete all cars from the inventory and all customers
    cursor.execute("DELETE FROM car_inventory;")
    cursor.execute("DELETE FROM customers;")
    print("All cars and customers removed from the system!")

    # Reset auto-increment for car_inventory and customers
    cursor.execute("ALTER TABLE car_inventory AUTO_INCREMENT = 1;")
    cursor.execute("ALTER TABLE customers AUTO_INCREMENT = 1;")

    # Insert new cars
    cars = [
        ('BMW', 'M4', 2023, 'Black', 7499999.99),
        ('Mercedes', 'AMG GT', 2023, 'Silver', 7580000.00),
        ('Audi', 'R8', 2023, 'Red', 13200000.00),
        ('Ferrari', '488 GTB', 2023, 'Yellow', 25700000.00),
        ('Lamborghini', 'Huracan Evo', 2023, 'Green', 29000000.00)
    ]
    cursor.executemany("INSERT INTO car_inventory (brand, model, year, color, price) VALUES (%s, %s, %s, %s, %s)", cars)

    # Insert new customers
    customers = [
        ('John Doe', '1234567890'),
        ('Jane Smith', '9876543210'),
        ('Alice Brown', '5556667777')
    ]
    cursor.executemany("INSERT INTO customers (name, phone) VALUES (%s, %s)", customers)

    conn.commit()
    print("New cars and customers added to the system!")

    conn.close()


# Call this function to clear and add new data
clear_and_add_data()

# Run the Program
if __name__ == "__main__":
    main_menu()
