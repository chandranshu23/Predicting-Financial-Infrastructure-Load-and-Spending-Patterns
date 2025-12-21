-- this table is to create cards table for the silver layer of the madallion arcitecture of our data
--Autor: Pratiksha Bajpai
--Created: 04-12-2025

--Database Selection
Create Database if not exists financial_db;
use financial_db;

-- Drop table if it already table
DROP table if exists cards_silver;

-- Creating the schema for the cards hive table
create external Table cards_silver (
	`user` INT,
	card_index INT,
	card_brand STRING,
	card_type STRING,
	card_number INT,
	expires STRING,
	cvv INT,
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
LOCATION '/user/talentum/projectMaster/warehouseDir/cards';


	
	
