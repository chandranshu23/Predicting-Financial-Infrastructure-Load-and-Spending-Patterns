-- Table for the Silver Layer (Medallion Architecture)
-- Author: Pratiksha Bajpai
-- Created: 04-12-2025

CREATE DATABASE IF NOT EXISTS financial_db;
USE financial_db;

DROP TABLE IF EXISTS cards_silver;

CREATE EXTERNAL TABLE cards_silver (
    `user` INT,
    card_index INT,
    card_brand STRING,
    card_type STRING,
    card_number STRING,            -- Changed to STRING to match Spark
    cvv STRING,                    -- Changed to STRING to match Spark
    has_chip STRING,
    cards_issued INT,
    credit_limit DECIMAL(10,2),
    year_pin_last_changed INT, 
    card_on_dark_web STRING,
    acct_opened_month INT,
    acct_opened_year INT,
    expires_month INT,
    expires_year INT
)
STORED AS ORC
LOCATION '/user/talentum/projectMaster/warehouseDir/cards'
TBLPROPERTIES ('orc.compress'='SNAPPY');
