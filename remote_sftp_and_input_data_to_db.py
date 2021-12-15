import mysql.connector
import csv
import pysftp
import datetime


#get the date
datefull = datetime.datetime.now()
getdate=datefull.strftime("PullOut-%d-%m-%y")


#connect to sftp server
myHostname = "192.168.1.5"
myUsername = "root"
myPassword = "Prasetya1"

with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
    print("Connection succesfully stablished ... ")

    # Remote path - file path
    remoteFilePath = '/storage/backup/GraphReport_20211214_PullOut.txt'

    # Path to save the file
    localFilePath = '/Users/ekaprasetya/Downloads/python/' + str(getdate) + ".txt"
    sftp.get(remoteFilePath, localFilePath)


#connect to database
mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = "root",
	database = "testdb"
	)

my_cursor = mydb.cursor()

#my_cursor.execute("LOAD DATA INFILE '/Users/ekaprasetya/Downloads/testingye.txt' INTO TABLE testdb.users FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n'(@col1,@col2,@col3,@col4) set name=@col1,email=@col2,age=@col3;")

#query = "LOAD DATA INFILE '/Users/ekaprasetya/Downloads/testingye.txt' INTO TABLE users FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n' IGNORE 1 LINES (@1,@2,@3,@4) SET name=@1, email=@2, age=@3, user_id=NULL "
query = "LOAD DATA INFILE '" + str(localFilePath) + "' INTO TABLE users FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n' IGNORE 1 LINES (@1,@2,@3,@4) SET name=@1, email=@2, age=@3, user_id=NULL "

my_cursor.execute( query )
mydb.commit()
