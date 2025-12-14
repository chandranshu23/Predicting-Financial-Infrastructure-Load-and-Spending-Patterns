--This script is to create the transaction table for the silver layer of the madallion architecture of our data
--Author: Saurav Dani
--created: 26-11-2025

-- Database Selection
CREATE DATABASE IF NOT EXISTS financial_db;
USE financial_db;

--Droping table if it already exists
DROP TABLE IF EXISTS transactions_silver;

--Creating the external table
CREATE EXTERNAL TABLE transactions_silver (
    user_id INT,
    card_id INT,
    amount DECIMAL(10,2),
    use_chip STRING,
    merchant_name STRING,  -- Changed to STRING to fix decoding error
    merchant_city STRING,
    merchant_state STRING,
    zip STRING,
    mcc INT,
    errors STRING,
    is_fraud STRING,
    transaction_timestamp TIMESTAMP
)
PARTITIONED BY (year INT, month INT)
STORED AS ORC
LOCATION '/user/talentum/projectMaster/warehouseDir/transactions';

-- Repair partitions to discover new data
MSCK REPAIR TABLE transactions_silver;
