import mysql.connector

#create a database
a = mysql.connector.connect(host = "localhost", user = "root", password = "root")
mycursor = a.cursor()
mycursor.execute("create database if not exists library")

#connet the database
mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="library")
mycursor = mydb.cursor()

#create a table to reserve accounts
mycursor.execute('''create table permission (id int not null auto_increment primary key ,
            name varchar(28) not null, password varchar(12) not null, pm varchar(255) not null)''')

#add items(only administrator) in the table
mycursor.execute("insert into permission set name = 'Eva', password= '123' ,pm = 'administrator'")
mycursor.execute("insert into permission set name = 'John', password= '456' ,pm = 'administrator'")
mycursor.execute("insert into permission set name = 'Marcos', password= '789' ,pm = 'administrator'")
mydb.commit()

#create a table to reserve items of books
mycursor.execute('''create table book (id int not null auto_increment primary key, title varchar(255) not null,
            author varchar(255) not null, topic varchar(255) not null, language varchar(255) not null,
            location varchar(255) not null, total_number int not null, inside_number int not null)''')

#create a table to reserve record of events
mycursor.execute('''create table event_record (id int not null auto_increment primary key, book_id int not null,
            title varchar(255) not null, debit int not null, remark varchar(255), operator varchar(255),
            time datetime not null default now())''')


mydb.close()
