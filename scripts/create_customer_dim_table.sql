-- SQL cell
CREATE TABLE IF NOT EXISTS CustomerDim (
    CustomerID INT,
    CustomerName STRING,
    Address STRING,
    EffectiveStartDate DATE,
    EffectiveEndDate DATE,
    IsCurrent INT
);
