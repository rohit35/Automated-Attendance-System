import pymysql
from datetime import date
from runner import get_Attendance_data
con = pymysql.connect(host='localhost',
                      user='root',
                      password='tiger')
mycommand = con.cursor()

def start():
    mycommand.execute("SHOW DATABASES")
    Databases = mycommand.fetchall()
    My_list =[]
    for Database in Databases:
        My_list+=list(Database)
    if 'SMEC_DATABASE' not in My_list and 'smec_database' not in My_list:
        mycommand.execute("CREATE DATABASE SMEC_DATABASE")
        con.commit()
        return True
    return False


def creating_Database(self):
    mycommand.execute("USE SMEC_DATABASE")
    con.commit()
    mycommand.execute("SHOW TABLES")
    Databases = mycommand.fetchall()
    My_list = []
    for Database in Databases:
        My_list += list(Database)
    if My_list == []:
        mysql_stmt = 'CREATE TABLE ERP_DATABASE (NAME VARCHAR(50),LOGIN_ID VARCHAR(50),PASSWORD VARCHAR(255),' \
                     'POSITION VARCHAR(50),SALARY VARCHAR(50),DEPT VARCHAR(10),STATUS VARCHAR(40))'
        mycommand.execute(mysql_stmt)
        mysql_stmt = 'CREATE TABLE STUDENT_DATABASE (NAME VARCHAR(50),LOGIN_ID VARCHAR(50),PASSWORD VARCHAR(255)' \
                     ',DEPT VARCHAR(45),CLASS VARCHAR(40),SECTION VARCHAR(40),SEMESTER VARCHAR(40) ,YEAR_OF_JOINING VARCHAR(40),STATUS VARCHAR(40))'
        mycommand.execute(mysql_stmt)
        mysql_stmt = 'CREATE TABLE FACULTY_DATABASE (NAME VARCHAR(50),LOGIN_ID VARCHAR(50),PASSWORD VARCHAR(255)' \
                     ',POSITION VARCHAR(50),SALARY VARCHAR(50),DEPT VARCHAR(50),STATUS VARCHAR(50),YEAR_OF_JOINING VARCHAR(40))'
        mycommand.execute(mysql_stmt)
        mysql_stmt = "INSERT INTO ERP_DATABASE VALUES ('ADMIN_SMEC' , 'ADMIN_SMEC' ,'ADMIN_SMEC' ,'ADMIN' ,'20000' ,'Everything' ,'WORKING' )"
        mycommand.execute(mysql_stmt)
        con.commit()
        mysql_stmt = 'CREATE TABLE SEMESTER_DATABASE (STARTING_DATE  DATE,ENDING_DATE DATE)'
        mycommand.execute(mysql_stmt)
        con.commit()
        sql_stmt = "create table Face_Data (id INT AUTO_INCREMENT,ROLL_NO VARCHAR(20),NAME VARCHAR(30),Percentage VARCHAR(20),PRIMARY KEY(id))"
        mycommand.execute(sql_stmt)
        con.commit()
        sql_stmt="insert into semester_database values('2019-08-05','2019-11-25')"
        mycommand.execute(sql_stmt)
        con.commit()
        sql_stmt = 'create table Attendance_database(LOGIN_ID varchar(50),'
        sql_stmt +=semester_date_update()
        mycommand.execute(sql_stmt)
        con.commit()





def get_login_data(database):
    mycommand.execute("USE smec_database")
    con.commit()
    stmt="SELECT * FROM "+database
    mycommand.execute(stmt)
    Databases = mycommand.fetchall()
    my_data =[]
    for data in Databases:
        my_data.append(data[1]+data[2])
    return my_data

def insert_Data(Database,Values):
    sql_stmt = "INSERT INTO "+Database +' values '+Values
    mycommand.execute(sql_stmt)
    con.commit()

def collecting_specific_data(Database):
    sql_stmt = "select * from "+Database
    mycommand.execute(sql_stmt)
    My_Data =[]
    Database=mycommand.fetchall()
    for idx in Database:
        My_Data.append(list(idx))
    return My_Data

def collecting_complete_data():
    sql_stmt="Select * from student_database"
    mycommand.execute(sql_stmt)
    stu_Database=mycommand.fetchall()
    sql_stmt="Select * from faculty_database"
    mycommand.execute(sql_stmt)
    faculty_Database=mycommand.fetchall()
    sql_stmt="Select * from erp_database"
    mycommand.execute(sql_stmt)
    erp_Database=mycommand.fetchall()
    Database =[]
    for idx in stu_Database:
        Database.append(list(idx))
    for idx in faculty_Database:
        Database.append(list(idx))
    for idx in erp_Database:
        Database.append(list(idx))
    return Database

def delele_person_Data(sql_stmt):
    mycommand.execute(sql_stmt)
    con.commit()


def insert_semester_date(stmt):
    mycommand.execute(stmt)
    con.commit()


def Add_Face_data(name,roll_no):
    sql_stmt ="insert into Face_Data (ROLL_NO , NAME) values ('"+roll_no+" ',' "+name+"')"
    mycommand.execute(sql_stmt)
    con.commit()

def get_id(Roll_no):
    mycommand.execute("Select id from Face_Data where ROLL_NO='"+Roll_no+"'")
    Data=mycommand.fetchall()
    My_ids=[]
    for idx in Data:
        My_ids+=list(idx)
    return My_ids[0]

def delete_semester_timings():
    mycommand.execute("Delete from semester_database")
    con.commit()

def extract_semester_data():
    mycommand.execute("select * from semester_database")
    Data =mycommand.fetchall()
    Data=str(Data)[:-3]
    return Data


def extract_semester_timings():
    Data = extract_semester_data()
    Data=Data[15:].split(", datetime.date")
    for idx in range(len(Data)):
        Data[idx]=Data[idx][:-1]
        Data[idx]=Data[idx][1:]
        Data[idx]= Data[idx].replace(",","/")
    return Data
def semester_date_update(starting_date='2019/ 8/ 5',ending_date='2019/ 11/ 25'):
    Data = extract_semester_timings()
    month=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    year = int(Data[0][0:4])
    if leap_year(year):
        month[1]=29
    if Data[0]==starting_date and Data[1]==ending_date:
        cur_date =5
        cur_month=8
        cur_year=2019
    stmt=""
    while(cur_year<=int(Data[1][0:4])):
        while(cur_month<=int(Data[1][5:8])):
            while(cur_date<=month[cur_month] and cur_date<=int(Data[1][9:])):
                stmt+=dates(cur_year,cur_month,cur_date)+" varchar(7) ,"
                cur_date+=1
            cur_date=1
            cur_month+=1
        cur_year+=1
        cur_month=1
        cur_date=1
    stmt=stmt[:-1]
    sql_stmt =stmt+")"
    return sql_stmt

def dates(year,month,day):
    string =''
    string+=str(day)+"_"+str(month)+"_"+str(year)
    return string

def leap_year(year):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return True
    return False

def update_attendance(sql_stmt):
    mycommand.execute(sql_stmt)
    con.commit()


def current_date():
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    d1=d1.replace("/","_")
    if d1[0]=='0':
        d1=d1[1:]
    return d1

def get_face_database():
    mycommand.execute("use smec_database")
    mycommand.execute("select * from face_data")
    Face_Data =mycommand.fetchall()
    Database ={}
    for row in Face_Data:
        no = int(row[0])
        Data  =row[1]+":"+row[2]
        Database[no]=Data
    return Database

def update_absent(id,Today_Date):
    Data =get_Attendance_data(id, Today_Date, 1)
    if Data[0].count("2")==7:
        sql_stmt = "UPDATE Attendance_database Set "+ current_date() +" ='0000000'"
        mycommand.execute(sql_stmt)
        con.commit()

def desc_attendance():
    mycommand.execute("use smec_database")
    mycommand.execute("desc attendance_database")
    Database =mycommand.fetchall()
    return Database

def update_idx(Data,period):
    for idx in Data:
        update(idx,period)

def update(id,period):
    update_absent(id,current_date())
    period = period
    Day = one_day(current_date(),id)
    Day=list(Day[0])[0]
    Day = Day[0:period-1]+'1'+Day[period:]
    Day="'"+Day+"'"
    sql_stmt="UPDATE Attendance_database Set "+ current_date() +" ="+Day+" where LOGIN_ID ='"+id+"'"
    mycommand.execute(sql_stmt)
    con.commit()

def one_day(Data,Id):
    sql_stmt ="select " + Data + " from attendance_database where LOGIN_ID='" + Id + "'"
    mycommand.execute(sql_stmt)
    Data = mycommand.fetchall()
    return Data

def week_data(Data,Id):
    mycommand.execute("select " + Data + " from attendance_database where LOGIN_ID='" + Id + "'")
    Data = mycommand.fetchone()
    return Data
def desc_attend():
    mycommand.execute("desc attendance_database")
    Database =mycommand.fetchall()
    return Database
def my_row(idx,Id):
    mycommand.execute("select " + idx + " from attendance_database where LOGIN_ID='" + Id + "'")
    Data = mycommand.fetchone()
    return Data

def get_period():
    from datetime import datetime
    now = datetime.now()
    if now > now.replace(hour=9,minute=19) and now <now.replace(hour=10,minute=10):
        return 1
    elif now > now.replace(hour=10,minute=10) and now <now.replace(hour=11,minute=0):
        return 2
    elif now > now.replace(hour=11,minute=1) and now <now.replace(hour=11,minute=51):
        return 3
    elif now > now.replace(hour=11,minute=51) and now <now.replace(hour=12,minute=41):
        return 4
    elif now > now.replace(hour=13,minute=20) and now <now.replace(hour=14,minute=11):
        return 5
    elif now > now.replace(hour=15,minute=11) and now <now.replace(hour=15,minute=0):
        return 6
    else:
        return 7

def get_Data_from_Database_1(reason,status,smec_class,section):
    mycommand.execute("use smec_database")
    con.commit()
    if (status =="student"):
        mycommand.execute("Select LOGIN_ID ,NAME from student_database where CLASS='"+smec_class+"' AND SECTION='"+section+"'")
    else:
        mycommand.execute("select LOGIN_ID,NAME from faculty_database ")
    Data=mycommand.fetchall()
    count=1
    My_Database=[]
    for row in Data:
        my_row=[]
        my_row.append(str(count))
        for col in row:
            my_row.append(col)
        My_Database.append(my_row)
        my_row=[]
        count+=1
    if reason=="percentage":
        for row in My_Database:
            mycommand.execute("select Percentage from face_data where ROLL_NO='"+row[1]+"'")
            per=mycommand.fetchone()
            if per[0]!=None:
                my_row.append(per[0])
            else:
                my_row.append("0")
        for idx in range(len(My_Database)):
            Data = My_Database[idx]
            Data.append(my_row[idx])
            My_Database[idx]=Data
        return My_Database
    else:
        my_row=[]
        for row in My_Database:
            sql_stmt="select "+current_date()+ " from attendance_database where LOGIN_ID ='"+row[1]+"'"
            mycommand.execute(sql_stmt)
            per = mycommand.fetchone()
            my_row.append(per[0])
        for idx in range(len(My_Database)):
            Data = My_Database[idx]
            if '1' in my_row[idx]:
                Data.append("present")
            elif '0' in my_row[idx]:
                Data.append("Absent")
            else:
                Data.append("N/E")
            My_Database[idx]=Data
        return My_Database

def check_date_format():
    cur_Date=desc_attendance()
    Dates=[]
    for idx in cur_Date:
        Dates.append(idx[0])
    if current_date() in Dates:
        return True
    return False

def insert_default_attendance(Id):
    mycommand.execute("desc Attendance_database")
    Attendance_Data = mycommand.fetchall()
    Data = []
    for row in Attendance_Data:
        Data.append(row[0])
    for idx in range(len(Data)):
        if Data[idx] == 'LOGIN_ID':
            Id = "'" + Id + "'"
            Data[idx] = Id
        else:
            Data[idx] = "'2222222'"
    Data = "(" + ",".join(Data) + ")"
    sql_stmt = "INSERT INTO Attendance_database values " + Data
    return update_attendance(sql_stmt)

def get_Dates():
    cur_Date=desc_attendance()
    Dates=[]
    for idx in cur_Date:
        Dates.append(idx[0])
    My_Data=[]
    My_Data.append(current_date())
    n=6
    pos= Dates.index(current_date())-1
    while n!=0:
        n-=1
        My_Data.append(Dates[pos])
        pos-=1
    return My_Data
