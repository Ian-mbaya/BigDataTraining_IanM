import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# Establish database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="mydatabase"  
)

# Cursor object
mycursor = mydb.cursor()

# Fetch data from the products table
mycursor.execute("SELECT `Sr_no`, `Item`, `Quantity`, `Cost` FROM products")
rows = mycursor.fetchall()

# Create DataFrame for available items
df = pd.DataFrame(rows, columns=["Sr_no", "Item", "Quantity", "Cost/Item"])

# Initialize total cost and DataFrame for purchased items
total_cost = 0
purchased_items_df = pd.DataFrame(columns=["Sr_no", "Item", "Qty", "TotalCost"])

while True:
    try:
        # Display items from the DataFrame
        print("\n----------------Items In Store-------------------")
        print("S.No\tItem\tQty\tCost/Item")
        print(df.to_string(index=False))
        
        # Input item selection by Sr_no
        itemPurchased = int(input("\nEnter the Sr_no of the item you want to purchase: "))

        # Check if Sr_no exists in the DataFrame
        if itemPurchased not in df['Sr_no'].values:
            print(f"Invalid Sr_no. Please select from the available options: {df['Sr_no'].values}.")
            continue

        # Access the selected item row from the DataFrame using Sr_no
        selected_item = df[df['Sr_no'] == itemPurchased].iloc[0]
        item_name = selected_item['Item']
        available_quantity = selected_item['Quantity']
        item_cost = selected_item['Cost/Item']

        # Input quantity
        quantity = int(input(f"How many {item_name} packets do you want to purchase: "))

        if quantity <= 0:
            print("Invalid quantity. Please enter a positive number.")
            continue

        # Check stock availability
        if quantity > available_quantity:
            print(f"Available quantity of {item_name} is {available_quantity}.")
            continue

        # Update stock in the DataFrame
        df.loc[df['Sr_no'] == itemPurchased, 'Quantity'] = available_quantity - quantity

        total_item_cost = quantity * item_cost
        total_cost += total_item_cost

        # Add purchased items to the purchased_items_df
        new_purchase = pd.DataFrame([[itemPurchased, item_name, quantity, total_item_cost]], 
                                     columns=["Sr_no", "Item", "Qty", "TotalCost"])
        purchased_items_df = pd.concat([purchased_items_df, new_purchase], ignore_index=True)

        print(f"{quantity} packets of {item_name} added to cart. Total cost so far: {total_cost}")

        cont = input("Do you want to continue shopping? Y/N: ").lower()
        if cont == 'n':
            break

    except ValueError:
        print("Invalid input. Please enter a valid Product number.")

# Delivery charge based on distance
try:
    distance = int(input("Enter the distance from the store (5/10/15/30): "))
    delivery_charge = 0
    if distance <= 15:
        delivery_charge = 50
        print("Delivery charge of 50 Rs will be levied.")
    elif 15 < distance <= 30:
        delivery_charge = 100
        print("Delivery charge of 100 Rs will be levied.")
    else:
        print("No delivery beyond 30KMS.")
except ValueError:
    print("Invalid distance. Please enter a valid number.")

# Customer details
name = input("Enter your name: ")
address = input("Enter your address: ")

# Final Bill Calculation
final_total = total_cost + delivery_charge

# Printing the bill
print("\n----------------------Bill---------------------------")
print(purchased_items_df.to_string(index=False))
print(f"\nTotal items cost: {total_cost:.2f}")
print(f"Total Bill Amount: Total items cost + Delivery Charge is: {final_total}")
print(f"Name: {name}")
print(f"Address: {address}")
print("Have a nice day!!")

# Display remaining quantities in store
print("\n----------------Remaining Quantity In Store-------------------")
print("S.No\tItem\tQty\tCost/Item")
print(df.to_string(index=False))

# Update remaining quantities in the DB
for index, row in df.iterrows():
    sr_no = row['Sr_no']
    new_quantity = row['Quantity']
    
    update_query = """
    UPDATE products
    SET Quantity = %s
    WHERE Sr_no = %s
    """
    
    # Execute the query with new values
    mycursor.execute(update_query, (new_quantity, sr_no))

# Commit the changes to the database
#mydb.commit()

# Store purchased_items_df in the database
# Create a connection for writing to the database
engine = create_engine('mysql+mysqlconnector://root:1234@localhost/mydatabase')
purchased_items_df.to_sql(name='purchased_items', con=engine, if_exists='append', index=False)

# Close the cursor and connection
mycursor.close()
mydb.close()
