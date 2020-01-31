import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",passwd="")
db = mydb.cursor()
db.execute("create database inventory")
db.execute("use inventory")
db.execute("create table inventory(itm_id varchar(5) ,name varchar(25),stock int(10),avaib char(1),cost int(10));")
db.execute("create table user(username varchar(16),password varchar(15),admin char(1));")
db.execute("insert into user values('admin','admin','y');")
mydb.commit()