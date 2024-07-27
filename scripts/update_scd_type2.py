# Python cell
from pyspark.sql import functions as F
from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder.appName("SCDType2").getOrCreate()

# Define the function to apply SCD Type-2 logic
def update_scd_type2(customer_id, customer_name, address):
    current_date = F.current_date()
    
    # Check if the record already exists
    existing_record = spark.sql(f"""
        SELECT * 
        FROM CustomerDim 
        WHERE CustomerID = {customer_id} 
        AND IsCurrent = 1
    """)
    
    if existing_record.count() > 0:
        # Update the existing record
        spark.sql(f"""
            UPDATE CustomerDim
            SET EffectiveEndDate = DATE_SUB('{current_date}', 1),
                IsCurrent = 0
            WHERE CustomerID = {customer_id} 
            AND IsCurrent = 1
        """)
    
    # Insert the new record
    spark.sql(f"""
        INSERT INTO CustomerDim (CustomerID, CustomerName, Address, EffectiveStartDate, EffectiveEndDate, IsCurrent)
        VALUES ({customer_id}, '{customer_name}', '{address}', '{current_date}', '9999-12-31', 1)
    """)

# Example usage
update_scd_type2(1, 'John Doe', 'Ajmer')
update_scd_type2(4, 'David Richard', 'Mumbai')
update_scd_type2(3, 'Bob Smith', 'Chennai')
update_scd_type2(5, 'Eva Dsouza', 'Mumbai')
