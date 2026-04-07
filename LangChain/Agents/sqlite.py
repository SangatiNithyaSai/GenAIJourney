import sqlite3

#connect to sqllite
connection=sqlite3.connect('student.db')

#cursor to execute commands

cursor=connection.cursor()

#table creation

table_info=""" 
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT)
"""

cursor.execute(table_info)
#Insert some records
cursor.execute('''Insert into Student values('krish','Data Science','A',90)''' )
cursor.execute('''Insert into Student values('murali','Data Science','B',80)''' )
cursor.execute('''Insert into Student values('kiran','DevOps','C',100)''' )
cursor.execute('''Insert into Student values('raj','DevOps','A',90)''' )

#Display the records
print("The Inserted records are:")
data=cursor.execute('Select * from Student')
for i in data:
    print(i)

connection.commit()
connection.close()