CREATE DATABASE IF NOT EXISTS financial_db;

CREATE EXTERNAL TABLE IF NOT EXISTS financial_db.users_silver (
    person_id STRING,
    current_age INT,
    retirement_age INT,
    birth_year INT,
    birth_month INT,
    gender STRING,
    address STRING,
    apartment STRING,
    city STRING,
    state STRING,
    zipcode STRING,
    latitude DOUBLE,
    longitude DOUBLE,
    per_capita_income_zipcode DECIMAL(10,2),
    yearly_income_person DECIMAL(10,2),
    total_debt DECIMAL(10,2),
    fico_score INT,
    num_credit_cards INT
)
STORED AS ORC
LOCATION '/user/talentum/projectMaster/warehouseDir/users';

