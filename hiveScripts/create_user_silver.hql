-- This script is to create the users table for the silver layer of the Medallion architecture of our data
-- Author: Muddasar Sayyad
-- Created: 26-11-2025

-- Creating database if not already present
CREATE DATABASE IF NOT EXISTS financial_db;

-- Creating the external table for user-level demographic and financial information
CREATE EXTERNAL TABLE IF NOT EXISTS financial_db.users_silver (
    person_id STRING,                         -- Unique identifier for each person
    current_age INT,                          -- Current age of the user
    retirement_age INT,                       -- Target retirement age for the user
    birth_year INT,                           -- Birth year value
    birth_month INT,                          -- Birth month value
    gender STRING,                            -- Gender of the user
    address STRING,                           -- Primary address of the user
    apartment STRING,                         -- Apartment or unit number (if applicable)
    city STRING,                              -- City of residence
    state STRING,                             -- State of residence
    zipcode STRING,                           -- Postal ZIP code
    latitude DOUBLE,                          -- GPS latitude coordinate of residence
    longitude DOUBLE,                         -- GPS longitude coordinate of residence
    per_capita_income_zipcode DECIMAL(10,2),  -- Average per-capita income of the ZIP code area
    yearly_income_person DECIMAL(10,2),       -- Total yearly income of the user
    total_debt DECIMAL(10,2),                 -- Total debt amount held by the user
    fico_score INT,                           -- User credit score indicator
    num_credit_cards INT                      -- Number of active credit cards owned
)
STORED AS ORC                                  -- Optimized columnar storage format
LOCATION '/user/talentum/projectMaster/warehouseDir/users';

