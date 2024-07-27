# Azure Databricks SCD Type-2 Implementation

This repository contains an implementation of Slowly Changing Dimension (SCD) Type-2 on the `CustomerDim` table using Azure Databricks.


## Introduction

This assignment demonstrates how to implement Slowly Changing Dimension (SCD) Type-2 on the `CustomerDim` table in Azure Databricks. SCD Type-2 allows tracking historical data changes by maintaining multiple versions of records.



### SCD Type 2 Overview

SCD Type 2 is a technique used to maintain historical versions of records in a dimension table. This approach allows you to track the complete history of changes for each record. When an update occurs, the existing record is marked as inactive, and a new record is inserted with the updated information. This new record will have the current values and is marked as active.

### Key Concepts

- **Historical Records:** Maintain past versions of records to track changes over time.
- **Current Records:** Identify the most recent version of a record.
- **Effective Dates:** Use `EffectiveStartDate` and `EffectiveEndDate` to specify the time range during which the record is valid.
- **Flags:** Use the `IsCurrent` flag to indicate whether a record is the current version.


### How It Works

1. **Initial Load:**
   - When the dimension table is first populated, each record has an `EffectiveStartDate`, an `EffectiveEndDate` set to a high value (e.g., `9999-12-31`), and an `IsCurrent` flag set to `1` (true).

2. **Inserting New Records:**
   - When a new record is inserted with a unique identifier (e.g., `CustomerID`), it is treated as a new entry with the current date as the `EffectiveStartDate`.

3. **Updating Existing Records:**
   - When an update is made to an existing record, the current version of the record is marked as inactive by setting its `EffectiveEndDate` to the current date minus one day and the `IsCurrent` flag to `0` (false).
   - A new record is then inserted with the updated information, the current date as the `EffectiveStartDate`, a high value for the `EffectiveEndDate`, and the `IsCurrent` flag set to `1` (true).

### Example

Consider the `CustomerDim` table with the following initial records:

| CustomerID | CustomerName  | Address      | EffectiveStartDate | EffectiveEndDate | IsCurrent |
|------------|---------------|--------------|--------------------|------------------|-----------|
| 1          | John Doe      | 123 Main St  | 2023-01-01         | 9999-12-31       | 1         |
| 2          | Alice Johnson | 456 Elm St   | 2023-01-01         | 9999-12-31       | 1         |
| 3          | Bob Smith     | 789 Oak St   | 2023-01-01         | 9999-12-31       | 1         |

After an update, suppose John Doe's address changes to "Ajmer" on `2023-09-11`. The table will now look like this:

| CustomerID | CustomerName  | Address      | EffectiveStartDate | EffectiveEndDate | IsCurrent |
|------------|---------------|--------------|--------------------|------------------|-----------|
| 1          | John Doe      | 123 Main St  | 2023-01-01         | 2023-09-10       | 0         |
| 1          | John Doe      | Ajmer        | 2023-09-11         | 9999-12-31       | 1         |
| 2          | Alice Johnson | 456 Elm St   | 2023-01-01         | 9999-12-31       | 1         |
| 3          | Bob Smith     | 789 Oak St   | 2023-01-01         | 9999-12-31       | 1         |

In this way, SCD Type 2 allows the tracking of historical data changes, preserving the complete history of each record.

### Use Cases

SCD Type 2 is commonly used in scenarios where it is essential to maintain historical accuracy for analysis and reporting, such as:

- Customer information changes in CRM systems.
- Product details in inventory management systems.
- Employee information in HR systems.

By using SCD Type 2, organizations can ensure that they have a complete history of their data, which is crucial for accurate reporting and analysis.