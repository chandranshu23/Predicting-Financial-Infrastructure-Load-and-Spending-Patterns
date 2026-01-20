# Predicting-Financial-Infrastructure-Load-and-Spending-Patterns
a capstone project to develop a Big Data system capable of predicting financial infrastructure loads and classifying transaction types in real-time. The project's primary challenge is the execution of a full data engineering and machine learning lifecycle on a single, Linux virtual machine running a pseudo-distributed stack. 




##################################################################################
#
# Flow of Project
#
##################################################################################
Follow The steps to run this in you system

1. Store the three csv files(transaction, users and cards) in to a folder named dataStaging in your shared directory

2. Clone the Project form Git to your home(~) directory and remane it to projectMaster

3. go inside the projectMaster and run dirSetup.shared to create and setup all the directoris in HDFS

#CSV to ORC conversion and Data Cleaning(Bronz layer)
4. Now open the sparkScripts directory and open jupyter notebook there (type jupyter-notebook then enter) 
	a. run convertToOrc_sd254_users first then run user_cleaned
	b. run convertToOrc_sd254_cards first then run cards_cleaned
	c. run convertToOrc_transactions first then transactions_cleaned

#Creation of Hive tables using ORC files(silver Layer)	
5. Now go back to projectMaster Directory and then go to hiveScripts and run them one by one(hive -f scriptName.hql)
	a. run create_cards_silver.hql  
	b. run create_user_silver.hql
	c. run create_transactions_silver.hql  

#Creation of data marts using the hiveTables(Golden Layer)
6 go back to projectMaster and fo to sparkScripts
	a. ...
