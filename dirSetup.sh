#!/bin/bash

#########################################################################################################################################################################################################
# #dirSetup.sh																								#
# This automation script is written to create the necessary dir structure on our linux fs and HDFS necessary for our Credit Card Fraud Detection and Financial Load Forecasting Project 		#
# #Usage: ./dirSetup.sh																							#
# #Prerequisite: None																							#
# #Author: Chandranshu Amola																						#
# #Created: 2025-11-17																							#
#########################################################################################################################################################################################################



#defining a function to perform error handling anywhere in the script
function error_handle(){
	if  [ $? -ne 0 ]; then
		echo "$1"
	fi
}

#Checking if the usage of the script is correct, if not gracefully exiting the script while displaying error message
if [ $# -ne 0 ]; then
	echo "Incorrect usage of shell script! correct usage is : ./dirSetup.sh"
	exit 1
fi

#Defining required variables and paths for this shell scripts
hdfsHome="/user/talentum"
projectHome="/projectMaster"
sparkDir="sparkScripts"
cleanedDir="cleanedData"
warehouseDir="warehouseDir"
hiveDir="hiveScripts"
airflowDAGs="airflowDAGs"
dataStaging="dataStaging"

#creating the dir structre on local file system first
# Deleting directories if they already exits on linux home

if [ -d "${HOME}${projectHome}" ]; then
	rm -rf "${HOME}${projectHome}"
	error_handle "Error Occured while cleaning already existing directories! please try again."
fi

#creating dir
mkdir -p "${HOME}${projectHome}/"{${sparkDir},${cleanedDir},${warehouseDir},${hiveDir},${airflowDAGs},${dataStaging}}
error_handle "Error occured while creating dir structure on Linux fs! please try again."

#checking for hdfs connection
hdfs dfs -ls > /dev/null
error_handle "Cant establish Connection to HDFS and Hadoop! please try again later!"

#checking the dir structure on HDFS file system if exists
if hdfs dfs -test -e "${hdfsHome}${projectHome}"; then
	hdfs dfs -rm -rf "${hdfsHome}${projectHome}"
	error_handle "Encountered error while cleaning existing hdfs dir structure"
fi

#creating dir structure on HDFS
hdfs dfs -mkdir -p "${hdfsHome}${projectHome}/"{${sparkDir},${cleanedDir},${warehouseDir},${hiveDir},${airflowDAGs},${dataStaging}}
error_handle "Error occured while creating dir structure on HDFS fs! please try again."

echo "--------------------- Finished Setting up directory structure for the project ---------------------"
