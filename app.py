import streamlit as st
import mysql.connector
from mysql.connector import pooling
from decimal import Decimal
import base64

# Function to add background from local file
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)),
                    url("data:image/jpeg;base64,{encoded_string}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Apply background
add_bg_from_local('images/dbms_bg.jpg')

# Custom CSS for button
button_css = """
<style>
    .stButton > button {
        color: white;
        background-color: #4CAF50; /* Green */
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
</style>
"""
st.markdown(button_css, unsafe_allow_html=True)



# Database connection pool
def create_connection_pool():
    return mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        host="localhost",
        user="root",
        password="sinch123",  # Your database password
        database="SM_MANAGEMENT"
    )

connection_pool = create_connection_pool()

# Check user credentials
def check_credentials(username, password, role):
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    if role == "Admin":
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
    else:
        cursor.execute("SELECT * FROM customer WHERE FNAME=%s AND LNAME=%s", (username, password))
    user = cursor.fetchone()
    connection.close()
    return user

# Login function
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    role = st.sidebar.radio("Role", ["Admin", "Customer"])

    if st.sidebar.button("Login"):
        user = check_credentials(username, password, role)
        if user:
            st.session_state["user"] = user
            st.session_state["role"] = role
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password")

# Format data for display
def format_data(data):
    for item in data:
        for key, value in item.items():
            if isinstance(value, Decimal):
                item[key] = float(value)
            elif hasattr(value, 'isoformat'):
                item[key] = value.isoformat()
    return data

# Admin dashboard
def admin_dashboard():
    # Custom title with smaller font size using HTML
    st.markdown("<h3 style='text-align: center;'>Here you can perform CRUD Operation!!</h3>", unsafe_allow_html=True)

    # Dropdown menu for CRUD operations
    operation = st.selectbox("Select Operation", ["Add", "Update", "Delete", "View"])
    table = st.selectbox("Select Table", ["Customer", "Employee", "Shopping Cart", "Store", "Product", "Payment"])

    if operation == "Add":
        add_entry(table)
    elif operation == "Update":
        update_entry(table)
    elif operation == "Delete":
        delete_entry(table)
    elif operation == "View":
        view_entries(table)

# Function to add an entry to a table
def add_entry(table):
    st.subheader(f"Add {table}")
    with st.form(key=f'add_{table.lower()}_form'):
        if table == "Customer":
            fname = st.text_input("First Name")
            lname = st.text_input("Last Name")
            ph_no = st.text_input("Phone Number")
            c_id = st.number_input("Customer ID", min_value=1)
            submit_button = st.form_submit_button("Add Customer")
            if submit_button:
                connection = connection_pool.get_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO customer (FNAME, LNAME, PH_NO, C_ID) 
                    VALUES (%s, %s, %s, %s)
                """, (fname, lname, ph_no, c_id))
                connection.commit()
                connection.close()
                st.success("Customer added successfully!")
        elif table == "Employee":
            emp_id = st.number_input("Employee ID", min_value=1)
            ename = st.text_input("Name")
            hire_date = st.date_input("Hire Date")
            salary = st.number_input("Salary", format="%.2f")
            dob = st.date_input("Date of Birth")
            age = st.number_input("Age", min_value=0)
            submit_button = st.form_submit_button("Add Employee")
            if submit_button:
                connection = connection_pool.get_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO employee (EMP_ID, ENAME, HIRE_DATE, SALARY, DOB, AGE) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (emp_id, ename, hire_date, salary, dob, age))
                connection.commit()
                connection.close()
                st.success("Employee added successfully!")
        elif table == "Shopping Cart":
            cart_id = st.number_input("Cart ID", min_value=1)
            c_id = st.number_input("Customer ID", min_value=1)
            status = st.text_input("Status")
            total_price = st.number_input("Total Price", format="%.2f")
            creation_date = st.date_input("Creation Date")
            submit_button = st.form_submit_button("Add Shopping Cart")
            if submit_button:
                connection = connection_pool.get_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO shopping_cart (CART_ID, C_ID, STATUS, TOTAL_PRICE, CREATION_DATE) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (cart_id, c_id, status, total_price, creation_date))
                connection.commit()
                connection.close()
                st.success("Shopping Cart added successfully!")
        elif table == "Store":
            store_id = st.number_input("Store ID", min_value=1)
            name = st.text_input("Store Name")
            location = st.text_input("Location")
            manager_id = st.number_input("Manager ID", min_value=1)
            submit_button = st.form_submit_button("Add Store")
            if submit_button:
                connection = connection_pool.get_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO store (STORE_ID, NAME, LOCATION, MANAGER_ID) 
                    VALUES (%s, %s, %s, %s)
                """, (store_id, name, location, manager_id))
                connection.commit()
                connection.close()
                st.success("Store added successfully!")
        elif table == "Product":
            product_id = st.number_input("Product ID", min_value=1)
            pname = st.text_input("Product Name")
            description = st.text_input("Description")
            price = st.number_input("Price", format="%.2f")
            category = st.text_input("Category")
            stock = st.number_input("Stock", min_value=0)
            submit_button = st.form_submit_button("Add Product")
            if submit_button:
                connection = connection_pool.get_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO product (P_ID, PNAME, DESCRIPTION, PRICE, CATEGORY, STOCK) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (product_id, pname, description, price, category, stock))
                connection.commit()
                connection.close()
                st.success("Product added successfully!")
        elif table == "Payment":
            payment_id = st.number_input("Payment ID", min_value=1)
            c_id = st.number_input("Customer ID", min_value=1)
            emp_id = st.number_input("Employee ID", min_value=1)
            pay_method = st.text_input("Payment Method")
            total_amount = st.number_input("Total Amount", format="%.2f")
            submit_button = st.form_submit_button("Add Payment")
            if submit_button:
                connection = connection_pool.get_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO payment (PAY_ID, C_ID, EMP_ID, PAY_METHOD, TOTAL_AMOUNT) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (payment_id, c_id, emp_id, pay_method, total_amount))
                connection.commit()
                connection.close()
                st.success("Payment added successfully!")

# Function to update an entry in a table
def update_entry(table):
    st.subheader(f"Update {table}")
    id_to_update = st.number_input(f"{table} ID to Update", min_value=1)
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    
    if table == "Customer":
        cursor.execute("SELECT * FROM customer WHERE C_ID=%s", (id_to_update,))
        entry = cursor.fetchone()
        if entry:
            with st.form(key=f'update_{table.lower()}_form'):
                fname = st.text_input("First Name", entry["FNAME"])
                lname = st.text_input("Last Name", entry["LNAME"])
                ph_no = st.text_input("Phone Number", entry["PH_NO"])
                submit_button = st.form_submit_button("Update Customer")
                if submit_button:
                    cursor.execute("""
                        UPDATE customer 
                        SET FNAME=%s, LNAME=%s, PH_NO=%s 
                        WHERE C_ID=%s
                    """, (fname, lname, ph_no, id_to_update))
                    connection.commit()
                    st.success("Customer updated successfully!")
        else:
            st.error("Customer not found")
    
    elif table == "Employee":
        cursor.execute("SELECT * FROM employee WHERE EMP_ID=%s", (id_to_update,))
        entry = cursor.fetchone()
        if entry:
            with st.form(key=f'update_{table.lower()}_form'):
                ename = st.text_input("Name", entry["ENAME"])
                hire_date = st.date_input("Hire Date", entry["HIRE_DATE"])
                salary = st.number_input("Salary", format="%.2f", value=float(entry["SALARY"]))
                dob = st.date_input("Date of Birth", entry["DOB"])
                age = st.number_input("Age", min_value=0, value=entry["AGE"])
                submit_button = st.form_submit_button("Update Employee")
                if submit_button:
                    cursor.execute("""
                        UPDATE employee 
                        SET ENAME=%s, HIRE_DATE=%s, SALARY=%s, DOB=%s, AGE=%s 
                        WHERE EMP_ID=%s
                    """, (ename, hire_date, salary, dob, age, id_to_update))
                    connection.commit()
                    st.success("Employee updated successfully!")
        else:
            st.error("Employee not found")

    elif table == "Shopping Cart":
        cursor.execute("SELECT * FROM shopping_cart WHERE CART_ID=%s", (id_to_update,))
        entry = cursor.fetchone()
        if entry:
            with st.form(key=f'update_{table.lower()}_form'):
                c_id = st.number_input("Customer ID", min_value=1, value=entry["C_ID"])
                status = st.text_input("Status", entry["STATUS"])
                total_price = st.number_input("Total Price", format="%.2f", value=float(entry["TOTAL_PRICE"]))
                creation_date = st.date_input("Creation Date", entry["CREATION_DATE"])
                submit_button = st.form_submit_button("Update Shopping Cart")
                if submit_button:
                    cursor.execute("""
                        UPDATE shopping_cart 
                        SET C_ID=%s, STATUS=%s, TOTAL_PRICE=%s, CREATION_DATE=%s 
                        WHERE CART_ID=%s
                    """, (c_id, status, total_price, creation_date, id_to_update))
                    connection.commit()
                    st.success("Shopping Cart updated successfully!")
        else:
            st.error("Shopping Cart not found")

    elif table == "Store":
        cursor.execute("SELECT * FROM store WHERE STORE_ID=%s", (id_to_update,))
        entry = cursor.fetchone()
        if entry:
            with st.form(key=f'update_{table.lower()}_form'):
                name = st.text_input("Store Name", entry["NAME"])
                location = st.text_input("Location", entry["LOCATION"])
                manager_id = st.number_input("Manager ID", min_value=1, value=entry["MANAGER_ID"])
                submit_button = st.form_submit_button("Update Store")
                if submit_button:
                    cursor.execute("""
                        UPDATE store 
                        SET NAME=%s, LOCATION=%s, MANAGER_ID=%s 
                        WHERE STORE_ID=%s
                    """, (name, location, manager_id, id_to_update))
                    connection.commit()
                    st.success("Store updated successfully!")
        else:
            st.error("Store not found")

    elif table == "Product":
        cursor.execute("SELECT * FROM product WHERE P_ID=%s", (id_to_update,))
        entry = cursor.fetchone()
        if entry:
            with st.form(key=f'update_{table.lower()}_form'):
                pname = st.text_input("Product Name", entry["PNAME"])
                description = st.text_input("Description", entry["DESCRIPTION"])
                price = st.number_input("Price", format="%.2f", value=float(entry["PRICE"]))
                category = st.text_input("Category", entry["CATEGORY"])
                stock = st.number_input("Stock", min_value=0, value=entry["STOCK"])
                submit_button = st.form_submit_button("Update Product")
                if submit_button:
                    cursor.execute("""
                        UPDATE product 
                        SET PNAME=%s, DESCRIPTION=%s, PRICE=%s, CATEGORY=%s, STOCK=%s 
                        WHERE P_ID=%s
                    """, (pname, description, price, category, stock, id_to_update))
                    connection.commit()
                    st.success("Product updated successfully!")
        else:
            st.error("Product not found")

    elif table == "Payment":
        cursor.execute("SELECT * FROM payment WHERE PAY_ID=%s", (id_to_update,))
        entry = cursor.fetchone()
        if entry:
            with st.form(key=f'update_{table.lower()}_form'):
                c_id = st.number_input("Customer ID", min_value=1, value=entry["C_ID"])
                emp_id = st.number_input("Employee ID", min_value=1, value=entry["EMP_ID"])
                pay_method = st.text_input("Payment Method", entry["PAY_METHOD"])
                total_amount = st.number_input("Total Amount", format="%.2f", value=float(entry["TOTAL_AMOUNT"]))
                submit_button = st.form_submit_button("Update Payment")
                if submit_button:
                    cursor.execute("""
                        UPDATE payment 
                        SET C_ID=%s, EMP_ID=%s, PAY_METHOD=%s, TOTAL_AMOUNT=%s 
                        WHERE PAY_ID=%s
                    """, (c_id, emp_id, pay_method, total_amount, id_to_update))
                    connection.commit()
                    st.success("Payment updated successfully!")
        else:
            st.error("Payment not found")
    
    connection.close()

def delete_entry(table):
    st.subheader(f"Delete {table}")
    id_to_delete = st.number_input(f"{table} ID to Delete", min_value=1)
    
    if st.button("Delete Entry"):
        connection = connection_pool.get_connection()
        cursor = connection.cursor()
        
        # Define the primary key column for each table
        primary_keys = {
            "Customer": "C_ID",
            "Employee": "EMP_ID",
            "Shopping Cart": "CART_ID",
            "Store": "STORE_ID",
            "Product": "P_ID",
            "Payment": "PAY_ID"
        }
        
        if table in primary_keys:
            primary_key = primary_keys[table]
            cursor.execute(f"DELETE FROM {table.lower().replace(' ', '_')} WHERE {primary_key}=%s", (id_to_delete,))
            connection.commit()
            st.success(f"{table} deleted successfully!")
        else:
            st.error("Invalid table selected")
        
        connection.close()


# Function to view all entries in a table
def view_entries(table):
    st.subheader(f"View All {table}")
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table.replace(' ', '_').lower()}")
    entries = cursor.fetchall()
    entries = format_data(entries)
    st.dataframe(entries)  # Display data in a table format
    connection.close()

# Customer dashboard
def customer_dashboard():
    st.title("Customer Dashboard")

    # Fetch shopping cart data
    customer_id = st.session_state["user"]["C_ID"]
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM shopping_cart WHERE C_ID=%s", (customer_id,))
    shopping_carts = cursor.fetchall()
    shopping_carts = format_data(shopping_carts)
    st.subheader("Your Shopping Carts")
    st.write(shopping_carts)

 # Fetch payments data
    cursor.execute("SELECT * FROM payment WHERE C_ID=%s", (customer_id,))
    payments = cursor.fetchall()
    payments = format_data(payments)

    st.subheader("Your Payments")
    st.write(payments)

    connection.close()

# Main function
def main():
    st.title("Supermarket Management System")

    if "user" not in st.session_state:
        st.session_state["user"] = None

    if st.session_state["user"] is None:
        login()
    else:
        if st.session_state["role"] == "Admin":
            admin_dashboard()
        else:
            customer_dashboard()

if __name__ == "__main__":
    main()