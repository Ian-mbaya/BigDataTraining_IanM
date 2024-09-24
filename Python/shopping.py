import pandas as pd

# DataFrame for item stock with Sr.no column
data = {
    "Sr.no": [1, 2, 3],
    "Item": ["Biscuits", "Cereals", "Chicken"],
    "Quantity": [5, 10, 20],
    "Cost/Item": [20.5, 90, 100]
}

# Create DataFrame for available items
df = pd.DataFrame(data)

# Initialize total cost and DataFrame for purchased items
total_cost = 0
purchased_items_df = pd.DataFrame(columns=["Sr.no", "Item", "Qty", "TotalCost"])

while True:
    try:
        # Display items from the DataFrame
        print("\n----------------Items In Store-------------------")
        print("S.No\tItem\tQty\tCost/Item")
        print(df.to_string(index=False))
        
        # Input item selection by Sr.no
        itemPurchased = int(input("\nEnter the Sr.no of the item you want to purchase (1:Biscuit, 2:Cereal, 3:Chicken): "))

        # Check if Sr.no exists in the DataFrame
        if itemPurchased not in df['Sr.no'].values:
            print(f"Invalid Sr.no. Please select from the available options: {df['Sr.no'].values}.")
            continue

        # Access the selected item row from the DataFrame using Sr.no
        selected_item = df[df['Sr.no'] == itemPurchased].iloc[0]
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
        df.loc[df['Sr.no'] == itemPurchased, 'Quantity'] = available_quantity - quantity

        total_item_cost = quantity * item_cost
        total_cost += total_item_cost

        # Add purchased items to the purchased_items_df
        new_purchase = pd.DataFrame([[itemPurchased, item_name, quantity, total_item_cost]], 
                                    columns=["Sr.no", "Item", "Qty", "TotalCost"])
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
    elif 15 <= distance <= 30:
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
