import pandas as pd
import psycopg2
import subprocess

# Establish Connection to DB
try:
    conn = psycopg2.connect(
    host="ec2-18-132-73-146.eu-west-2.compute.amazonaws.com",
    port="5432",
    user="consultants",
    password="WelcomeItc@2022",  
    database="testdb"  
)
    print('Connection Succesful')
except psycopg2.Error as e:
    print('connection error', e)

cursor = conn.cursor()

cursor.execute("SELECT * from ianproducts;")

rows = cursor.fetchall()

# Create DataFrame for available items
products_df = pd.DataFrame(rows, columns=["product_id", "name", "category", "effective_date"])
print(products_df)

#Write to File
products_df.to_csv('psqlProducts.csv', sep=',', index=False)

local_file = 'psqlProducts.csv' 
hdfs_dir = 'ukussept/ian/products'
## Write to HDFS using Subprocess
try:
    # Using subprocess to call HDFS commands
    hdfs_put_command = f'hadoop fs -put -f {local_file} {hdfs_dir}'
    subprocess.run(hdfs_put_command, shell=True, check=True)
    print(f"File successfully uploaded to HDFS")
    
except subprocess.CalledProcessError as e:
        print(f"Failed to upload to HDFS: {e}")

