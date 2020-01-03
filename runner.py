import tkinter as tk
from Face_Data import *
from mysql_operations import *

def check_database(Position):
    stmt =''
    if Position=="ADMIN":
        stmt='ERP_DATABASE'
    elif Position=='FACULTY':
        stmt='FACULTY_DATABASE'
    else:
        stmt='STUDENT_DATABASE'
    return stmt

def check_login(id,password,Position):
    stmt=check_database(Position)
    my_database=get_login_data(stmt)
    comb=id+password
    if comb in my_database:
        return True
    return False


def main_page():
    message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System", bg="green", fg="white",
                       font=("ArialBold", 30),height=4)
    message.pack(fill="x")  # place(x=80, y=20)
    icon = tk.PhotoImage(file="C:\MiniProject\Attendance_management_system\AMS.png")
    tk.Label(window, image=icon).pack()
    takeImg = tk.Button(window, text="Login Section", command=login_page,fg="white", bg="blue2", width=30, height=5,
                        activebackground="Red",font=('times', 15, ' bold '))  # command=take_img
    takeImg.place(x=90, y=400)
    FA = tk.Button(window, text="Automatic Attendace", command=att_update_page,fg="white", bg="blue2", width=30, height=5,
                   activebackground="Red", font=('times', 15, ' bold '))  # command=subjectchoose
    FA.place(x=690, y=400)

def att_update_page():
    livefeed_attendance()

def error(number):
    if number==1:
        Error = tk.Label(window, text="Login Id is Empty", width=20, fg="black", bg="deep pink", height=2,
                      font=('times', 15, ' bold '))
        Error.place(x=300, y=500)
    if number==2:
        Error = tk.Label(window, text="password is Empty", width=20, fg="black", bg="deep pink", height=2,
                         font=('times', 15, ' bold '))
        Error.place(x=300, y=500)
    if number==3:
        Error = tk.Label(window, text="Invalid Login Id or Password", width=20, fg="black", bg="Red", height=4,
                         font=('times', 15, ' bold '))
        Error.place(x=450, y=550)

def get_Attendance_data(Id,Data,Times):
    Database=desc_attendance()
    my_desc = []
    for idx in Database:
        my_desc.append(idx[0])
    if Data in my_desc and Times==1:
        Data = one_day(Data,Id)
        return Data[0]
    elif Data in my_desc and Times==7:
        my_Dates=[]
        position = my_desc.index(Data)
        while Times!=0:
            if my_desc[position]=="LOGIN_ID":
                break
            Times-=1
            Data = my_desc[position]
            Data = week_data(Data,Id)
            my_Dates.append(Data[0])
            position-=1
        return my_Dates

def view_week(Id,Data):
    import tkinter
    root = tkinter.Tk()
    root.title("weekly ")
    root.configure(background='snow')
    All_Databaase=[]
    All_Databaase.append(["Dates","period 1","period 2","period 3","period 4","period 5","period 6","period 7"])
    represnt=["Absent","Present","N/E"]
    Data = get_Attendance_data(Id,Data,7)
    Dates=get_Dates()
    weekly =[]
    count=0
    days_data =[]
    for day in Data:
        for period in day:
            period = int(period)
            days_data.append(represnt[period])
        days_data.insert(0,Dates[count])
        count+=1
        weekly.append(days_data)
        days_data=[]
    for days in weekly:
        All_Databaase.append(days)
    r = 0
    for col in All_Databaase:
        c = 0
        for row in col:
            label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                  bg="lawn green", text=row, relief=tkinter.RIDGE)
            label.grid(row=r, column=c)
            c += 1
        r += 1
    root.mainloop()

def view_Today(Id,Data):
    import tkinter
    root = tkinter.Tk()
    root.title("Today ")
    root.configure(background='snow')
    All_Databaase=[]
    All_Databaase.append(["period 1","period 2","period 3","period 4","period 5","period 6","period 7"])
    represnt = ["Absent", "Present", "N/E"]
    Data = get_Attendance_data(Id,current_date(),1)
    Data=Data[0]
    Todays_Data =[]
    for period in Data:
        period=int(period)
        Todays_Data.append(represnt[period])
    All_Databaase.append(Todays_Data)
    r = 0
    for col in All_Databaase:
        c = 0
        for row in col:
            label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                  bg="lawn green", text=row, relief=tkinter.RIDGE)
            label.grid(row=r, column=c)
            c += 1
        r += 1
    root.mainloop()

def student_login():
    def view_Attendance(Id):
        def back_student_page():
            student_Dashboard(Id)

        def view_student_Today():
            view_Today(Id, current_date())

        def view_student_week():
            view_week(Id, current_date())

        def whole_student_percentage():
            whole_percentage(Id)

        clear()
        message = tk.Label(window, text="                 Attendance Section       ", bg="green", fg="white",
                           font=("ArialBold", 40))
        message.pack(fill="x")

        BACK = tk.Button(window, text="Back ", command=back_student_page, fg="white", bg="green", width=30, height=4,
                         activebackground="Red", font=('times', 15, ' bold '))
        BACK.place(x=20, y=90)
        SubmitButton = tk.Button(window, text="Today", command=view_student_Today, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
        SubmitButton.place(x=600, y=90)
        SubmitButton = tk.Button(window, text="Weekly", command=view_student_week, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
        SubmitButton.place(x=600, y=180)
        SubmitButton = tk.Button(window, text="Percentage", command=whole_student_percentage, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
        SubmitButton.place(x=600, y=270)

        def whole_percentage(Id):
            def back_section():
                student_Dashboard(Id)

            clear()
            message = tk.Label(window, text="                 Percentage Section        ", bg="green", fg="white",
                               font=("ArialBold", 40))

            message.pack(fill="x")  # place(x=80, y=20)
            BACK = tk.Button(window, text="BACK ", command=back_section, fg="white", bg="green", width=30, height=5,
                             activebackground="Red", font=('times', 15, ' bold '))
            BACK.place(x=20, y=200)
            N_E = 0
            PRESENT = 0
            ABSENT = 0
            Database = desc_attend()
            my_desc = []
            my_Data = []
            for idx in Database:
                my_desc.append(idx[0])
            for idx in my_desc:
                if idx != "LOGIN_ID":
                    Data = my_row(idx, Id)
                    my_Data.append(Data[0])
            for row in my_Data:
                for col in row:
                    if col == '0':
                        ABSENT += 1
                    elif col == '1':
                        PRESENT += 1
                    else:
                        N_E += 1

            NAME = tk.Label(window, text=("Roll_no:" + Id), width=20, fg="black", bg="green", height=4,
                            font=('times', 15, ' bold '))
            NAME.place(x=950, y=140)
            NAME = tk.Label(window, text=("No of Not Enter days:" + str(round(N_E))), width=20, fg="black", bg="green",
                            height=4,
                            font=('times', 15, ' bold '))
            NAME.place(x=950, y=350)
            NAME = tk.Label(window, text=("No of period present:" + str(PRESENT)), width=20, fg="black", bg="green",
                            height=4,
                            font=('times', 15, ' bold '))
            NAME.place(x=950, y=420)
            if PRESENT != 0:
                PRESENT /= 7
            if ABSENT != 0:
                ABSENT /= 7
            N_E /= 7
            NAME = tk.Label(window, text=("No of period absent:" + str(ABSENT)), width=20, fg="black", bg="green", height=4,
                            font=('times', 15, ' bold '))
            NAME.place(x=950, y=490)
            NAME = tk.Label(window, text=("No Of present Days" + str(round(PRESENT))), width=20, fg="black", bg="green",
                            height=4,
                            font=('times', 15, ' bold '))
            NAME.place(x=950, y=210)
            NAME = tk.Label(window, text=("No of Absent days:" + str(round(ABSENT))), width=20, fg="black", bg="green",
                            height=4,
                            font=('times', 15, ' bold '))
            NAME.place(x=950, y=280)

            NAME = tk.Label(window, text="Total percentage:0.0", width=20, fg="black", bg="green", height=4,
                            font=('times', 15, ' bold '))
            NAME.place(x=950, y=580)
            if round(PRESENT) == 0:
                NAME = tk.Label(window, text="Total percentage:0.0", width=20, fg="black", bg="green", height=4,
                                font=('times', 15, ' bold '))
                NAME.place(x=950, y=580)
                sql_stmt = "UPDATE FACE_data Set Percentage = 0.0"
            else:
                NAME = tk.Label(window, text=("Total percentage:" + str(((PRESENT) / (PRESENT + ABSENT)) * 100)), width=20,
                                fg="black", bg="green", height=4,
                                font=('times', 15, ' bold '))
                NAME.place(x=950, y=580)
                sql_stmt = "UPDATE FACE_data Set Percentage = " + str(((round(PRESENT)) / (round(PRESENT + ABSENT))) * 100)
            mycommand.execute(sql_stmt)
            con.commit()

    def student_Dashboard(Id):
        def student_view_profile():
            view_person(Id)
        def view_student_attendance():
            view_Attendance(Id)
        clear()
        message = tk.Label(window, text="                 Student Dashboard       ", bg="green", fg="white",
                           font=("ArialBold", 40))
        message.pack(fill="x")

        BACK = tk.Button(window, text="Logout ", command=login_page, fg="white", bg="green", width=30, height=4,
                         activebackground="Red", font=('times', 15, ' bold '))
        BACK.place(x=20, y=90)
        ProfileButton = tk.Button(window, text="View Profile", command=student_view_profile, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
        ProfileButton.place(x=600, y=90)
        ViewButton = tk.Button(window, text="View Attendance", command=view_student_attendance, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
        ViewButton.place(x=600, y=180)
        SemesterButton = tk.Button(window, text="Semester Timings", command=Semester_timings, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
        SemesterButton.place(x=600, y=270)

    def log_in():
        id=Id_txt.get()
        password=password_txt.get()
        if id == '':
            error(1)
        elif password=='':
            error(2)
        elif not check_login(id, password, "STUDENT"):
            error(3)
        else:
            student_Dashboard(id.upper())

    clear()
    message = tk.Label(window, text="                 Student Login        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)
    BACK =tk.Button(window, text="BACK ", command=login_page,fg="white", bg="green", width=30, height=4,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=150)

    ID = tk.Label(window, text="Enter Login ID", width=20, fg="black", bg="deep pink", height=2,
                  font=('times', 15, ' bold '))
    ID.place(x=200, y=300)

    Id_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Id_txt.place(x=550, y=300)

    password = tk.Label(window, text="Enter password", width=20, fg="black", bg="deep pink", height=2,
                            font=('times', 15, ' bold '))
    password.place(x=200, y=400)

    password_txt = tk.Entry(window, width=20, bg="yellow", show="*",fg="red", font=('times', 25, ' bold '))
    password_txt.place(x=550, y=400)

    SubmitButton = tk.Button(window, text="Submit", command=log_in, fg="black", bg="grey",
                                 width=10, height=1, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=950, y=450)

def faculty_login():
    def log_in():
        id=Id_txt.get()
        password=password_txt.get()
        if id == '':
            error(1)
        elif password=='':
            error(2)
        elif not check_login(id, password, "FACULTY"):
            error(3)
        else:
            faculty_Dashboard(id.upper())
    clear()
    message = tk.Label(window, text="                 Faculty Login        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)
    BACK =tk.Button(window, text="BACK ", command=login_page,fg="white", bg="green", width=30, height=4,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=150)

    ID = tk.Label(window, text="Enter Login ID", width=20, fg="black", bg="deep pink", height=2,
                  font=('times', 15, ' bold '))
    ID.place(x=200, y=300)

    Id_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Id_txt.place(x=550, y=300)

    password = tk.Label(window, text="Enter password", width=20, fg="black", bg="deep pink", height=2,
                            font=('times', 15, ' bold '))
    password.place(x=200, y=400)

    password_txt = tk.Entry(window, width=20, bg="yellow", show="*",fg="red", font=('times', 25, ' bold '))
    password_txt.place(x=550, y=400)

    SubmitButton = tk.Button(window, text="Submit", command=log_in, fg="black", bg="grey",
                                 width=10, height=1, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=950, y=450)
def Add_Members():
    clear()
    message = tk.Label(window, text="                 ADD Members        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)
    BACK = tk.Button(window, text="BACK ", command=admin_page, fg="white", bg="green", width=30, height=4,
                     activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20, y=150)
    B1 = tk.Button(window, text="Add Student", command=Add_student,fg="white", bg="blue2", width=30, height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B1.place(x=20,y=400)

    B2 = tk.Button(window, text="Add Faculty", command=Add_Faculty, fg="white", bg="blue2", width=30,
                   height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B2.place(x=420, y=400)

    B3 = tk.Button(window, text="Add Erp Members", command=Add_erp_members, fg="white", bg="blue2", width=30,
                   height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B3.place(x=840, y=400)

def Add_Faculty():
    def submit():
        def Take_Images():
            global unique_id
            unique_id = get_id(unique_id)
            Face_capture(unique_id)
            Acknowledgement = tk.Label(window, text="Succesfully Added", width=20, fg="black", bg="green", height=4,
                                       font=('times', 15, ' bold '))
            Acknowledgement.place(x=20, y=550)
        Faculty_Data = []
        Faculty_Data.append(Name_txt.get())
        Faculty_Data.append(Roll_no_txt.get())
        Faculty_Data.append(Password_txt.get())
        Faculty_Data.append(Position_txt.get())
        Faculty_Data.append(Salary_txt.get())
        Faculty_Data.append(Dept_txt.get())
        Faculty_Data.append('FACULTY')
        Faculty_Data.append('2014')
        Faculty_Database = ["Name", "Roll no", "Password", "Position", "Salary", "Dept", "Status", "year of joining"]
        if check_Student_Data(Faculty_Database, Faculty_Data) == True:
            database = "FACULTY_DATABASE"
            Add_Face_data(Faculty_Data[0], Faculty_Data[1])
            user_id = get_id(Faculty_Data[1])
            global unique_id
            unique_id= user_id
            Images = tk.Button(window, text="TAKE IMAGES", command=Take_Images, fg="white", bg="green", width=30,
                               height=4,
                               activebackground="Red", font=('times', 15, ' bold '))
            Images.place(x=20, y=350)
            insert_default_attendance(Faculty_Data[1])
            string = ""
            for data in Faculty_Data:
                string = string + "'" + data + "',"
            string = string[:-1]
            Faculty_Data = "(" + string + ")"
            insert_Data(database, Faculty_Data)
        else:
            Acknowledgement = tk.Label(window, text="Enter a Valid Data", width=20, fg="black", bg="Red", height=4,
                                       font=('times', 15, ' bold '))
            Acknowledgement.place(x=20, y=550)

    clear()
    message = tk.Label(window, text="                 ADD FACULTY        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)
    BACK = tk.Button(window, text="BACK ", command=Add_Members, fg="white", bg="green", width=30, height=4,
                     activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20, y=150)
    Name = tk.Label(window, text="Name", width=20, fg="black", bg="deep pink", height=2,
                    font=('times', 15, ' bold '))
    Name.place(x=500, y=90)
    Name_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Name_txt.place(x=790, y=90)
    Roll_no = tk.Label(window, text="Roll no", width=20, fg="black", bg="deep pink", height=2,
                       font=('times', 15, ' bold '))
    Roll_no.place(x=500, y=180)
    Roll_no_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Roll_no_txt.place(x=790, y=180)
    Password = tk.Label(window, text="Password", width=20, fg="black", bg="deep pink", height=2,
                        font=('times', 15, ' bold '))
    Password.place(x=500, y=270)
    Password_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Password_txt.place(x=790, y=270)
    Position = tk.Label(window, text="Position", width=20, fg="black", bg="deep pink", height=2,
                    font=('times', 15, ' bold '))
    Position.place(x=500, y=360)
    Position_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Position_txt.place(x=790, y=360)
    Salary = tk.Label(window, text="Salary", width=20, fg="black", bg="deep pink", height=2,
                     font=('times', 15, ' bold '))
    Salary.place(x=500, y=450)
    Salary_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Salary_txt.place(x=790, y=450)
    Dept= tk.Label(window, text="Dept", width=20, fg="black", bg="deep pink", height=2,
                       font=('times', 15, ' bold '))
    Dept.place(x=500, y=540)
    Dept_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Dept_txt.place(x=790, y=540)
    Submit = tk.Button(window, text="Submit", command=submit, fg="black", bg="grey",
                       width=20, height=4, activebackground="Red",
                       font=('times', 15, ' bold '))
    Submit.place(x=820, y=600)


def Add_erp_members():
    def submit():
        def Take_Images():
            Face_capture(unique_id)
            Acknowledgement = tk.Label(window, text="Succesfully Added", width=20, fg="black", bg="green", height=4,
                                       font=('times', 15, ' bold '))
            Acknowledgement.place(x=20, y=550)
        erp_Data = []
        erp_Data.append(Name_txt.get())
        erp_Data.append(Roll_no_txt.get())
        erp_Data.append(Password_txt.get())
        erp_Data.append(Position_txt.get())
        erp_Data.append(Salary_txt.get())
        erp_Data.append(Dept_txt.get())
        erp_Data.append('ADMIN')
        erp_Database = ["Name", "Roll no", "Password", "Position", "Salary", "Dept", "Status"]
        if check_Student_Data(erp_Database, erp_Data) == True:
            database = "ERP_DATABASE"
            string = ""
            Add_Face_data(erp_Data[0], erp_Data[1])
            user_id = get_id(erp_Data[1])
            global unique_id
            unique_id = user_id
            Images = tk.Button(window, text="TAKE IMAGES", command=Take_Images, fg="white", bg="green", width=30,
                               height=4,
                               activebackground="Red", font=('times', 15, ' bold '))
            Images.place(x=20, y=350)
            insert_default_attendance(erp_Data[1])
            string = ""
            for data in erp_Data:
                string = string + "'" + data + "',"
            string = string[:-1]
            erp_Data = "(" + string + ")"
            insert_Data(database, erp_Data)
        else:
            Acknowledgement = tk.Label(window, text="Enter a Valid Data", width=20, fg="black", bg="green", height=4,
                                       font=('times', 15, ' bold '))
            Acknowledgement.place(x=20, y=550)

    def Take_Images():
        Face_capture(unique_id)
        Acknowledgement = tk.Label(window, text="Succesfully Added", width=20, fg="black", bg="green", height=4,
                                   font=('times', 15, ' bold '))
        Acknowledgement.place(x=20, y=550)

    clear()
    message = tk.Label(window, text="                 ADD ADMIN        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)
    BACK = tk.Button(window, text="BACK ", command=Add_Members, fg="white", bg="green", width=30, height=4,
                     activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20, y=150)
    Name = tk.Label(window, text="Name", width=20, fg="black", bg="deep pink", height=2,
                    font=('times', 15, ' bold '))
    Name.place(x=500, y=90)
    Name_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Name_txt.place(x=790, y=90)
    Roll_no = tk.Label(window, text="Roll no", width=20, fg="black", bg="deep pink", height=2,
                       font=('times', 15, ' bold '))
    Roll_no.place(x=500, y=180)
    Roll_no_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Roll_no_txt.place(x=790, y=180)
    Password = tk.Label(window, text="Password", width=20, fg="black", bg="deep pink", height=2,
                        font=('times', 15, ' bold '))
    Password.place(x=500, y=270)
    Password_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Password_txt.place(x=790, y=270)
    Position = tk.Label(window, text="Position", width=20, fg="black", bg="deep pink", height=2,
                    font=('times', 15, ' bold '))
    Position.place(x=500, y=360)
    Position_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Position_txt.place(x=790, y=360)
    Salary = tk.Label(window, text="Salary", width=20, fg="black", bg="deep pink", height=2,
                     font=('times', 15, ' bold '))
    Salary.place(x=500, y=450)
    Salary_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Salary_txt.place(x=790, y=450)
    Dept= tk.Label(window, text="Dept", width=20, fg="black", bg="deep pink", height=2,
                       font=('times', 15, ' bold '))
    Dept.place(x=500, y=540)
    Dept_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Dept_txt.place(x=790, y=540)
    Submit = tk.Button(window, text="Submit", command=submit, fg="black", bg="grey",
                       width=20, height=4, activebackground="Red",
                       font=('times', 15, ' bold '))
    Submit.place(x=820, y=600)


def Add_student():
    def submit():
        def Take_Images():
            global unique_id
            Face_capture(unique_id)
            Acknowledgement = tk.Label(window, text="Succesfully Added", width=20, fg="black", bg="green", height=4,
                                       font=('times', 15, ' bold '))
            Acknowledgement.place(x=20, y=550)

        Student_Data=[]
        Student_Data.append(Name_txt.get())
        Student_Data.append(Roll_no_txt.get())
        Student_Data.append(Password_txt.get())
        Student_Data.append(DEPT_txt.get())
        Student_Data.append(Class_txt.get())
        Student_Data.append(Section_txt.get())
        Student_Data.append('7')
        Student_Data.append('2016')
        Student_Data.append("STUDYING")
        Student_Database = ["Name", "Roll no", "Password", "Dept", "Class", "Section", "Semester", "year of joining",
                            "Status"]
        if check_Student_Data(Student_Database, Student_Data) == True:
            database = "STUDENT_DATABASE"
            Add_Face_data(Student_Data[0], Student_Data[1])
            user_id = get_id(Student_Data[1])
            global  unique_id
            unique_id =  user_id
            Images= tk.Button(window, text="TAKE IMAGES", command=Take_Images,fg="white", bg="green", width=30, height=4,
                   activebackground="Red", font=('times', 15, ' bold '))
            Images.place(x=20, y=350)
            insert_default_attendance(Student_Data[1])
            string = ""
            for data in Student_Data:
                string = string + "'" + data + "',"
            string = string[:-1]
            Student_Data = "(" + string + ")"
            insert_Data(database, Student_Data)
        else:
            Acknowledgement = tk.Label(window, text="Enter a Valid Data", width=20, fg="black", bg="green", height=4,
                                       font=('times', 15, ' bold '))
            Acknowledgement.place(x=20, y=550)

    clear()
    message = tk.Label(window, text="                 ADD STUDENT        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)
    BACK =tk.Button(window, text="BACK ", command=admin_page,fg="white", bg="green", width=30, height=4,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=150)
    Name = tk.Label(window, text="Name", width=20, fg="black", bg="deep pink", height=2,
                  font=('times', 15, ' bold '))
    Name.place(x=500, y=90)
    Name_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Name_txt.place(x=790, y=90)
    Roll_no = tk.Label(window, text="Roll no", width=20, fg="black", bg="deep pink", height=2,
                  font=('times', 15, ' bold '))
    Roll_no.place(x=500, y=180)
    Roll_no_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Roll_no_txt.place(x=790, y=180)
    Password = tk.Label(window, text="Password", width=20, fg="black", bg="deep pink", height=2,
                  font=('times', 15, ' bold '))
    Password.place(x=500, y=270)
    Password_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Password_txt.place(x=790, y=270)
    DEPT = tk.Label(window, text="Dept", width=20, fg="black", bg="deep pink", height=2,
                        font=('times', 15, ' bold '))
    DEPT.place(x=500, y=360)
    DEPT_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    DEPT_txt.place(x=790, y=360)
    CLass= tk.Label(window, text="Class", width=20, fg="black", bg="deep pink", height=2,
                        font=('times', 15, ' bold '))
    CLass.place(x=500, y=450)
    Class_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Class_txt.place(x=790, y=450)
    Section= tk.Label(window, text="Section", width=20, fg="black", bg="deep pink", height=2,
                        font=('times', 15, ' bold '))
    Section.place(x=500, y=540)
    Section_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Section_txt.place(x=790, y=540)
    Submit= tk.Button(window, text="Submit", command=submit, fg="black", bg="grey",
                                 width=20, height=4, activebackground="Red",
                                 font=('times', 15, ' bold '))
    Submit.place(x=820,y=600)

def check_Student_Data(Student_list,Current_list):
    length = len(Current_list)
    for idx in range(length):
        if Current_list[idx]=='':
            print("please Enter a valid "+Student_list[idx] +" for student Database.")
            return False
    return True

def id_check(Data):
    my_id = []
    for row in Data:
        my_id.append(row[1].lower())
    return my_id

def view_person(Id):
    Database = collecting_complete_data()
    person_Data = ''
    for row in Database:
        if row[1].lower() == Id.lower():
            person_Data = row
            break
    if person_Data!='' and len(person_Data) > 8 and person_Data[8] == 'STUDYING':
        NAME = tk.Label(window, text=("STUDENT DETAILS"), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=70)

        NAME = tk.Label(window, text=("Name:"+person_Data[0]), width=20, fg="black", bg="green", height=4,
                                   font=('times', 15, ' bold '))
        NAME.place(x=950, y=140)
        NAME = tk.Label(window, text=("Login Id:"+person_Data[1]), width=20, fg="black", bg="green", height=4,
                                   font=('times', 15, ' bold '))
        NAME.place(x=950, y=210)
        NAME = tk.Label(window, text=("Dept:" + person_Data[3]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=280)
        NAME = tk.Label(window, text=("Class:" + person_Data[4]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=350)
        NAME = tk.Label(window, text=("Section:" + person_Data[5]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=420)
        NAME = tk.Label(window, text=("Semester:" + person_Data[6]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950,y=490)
    elif person_Data != '' and len(person_Data) >= 8 and (person_Data[3] == 'TEACHER' or person_Data[3] == 'FACULTY'):

        NAME = tk.Label(window, text=("FACULTY DETAILS"), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=70)

        NAME = tk.Label(window, text=("Name:"+person_Data[0]), width=20, fg="black", bg="green", height=4,
                                   font=('times', 15, ' bold '))
        NAME.place(x=950, y=140)
        NAME = tk.Label(window, text=("Login Id:"+person_Data[1]), width=20, fg="black", bg="green", height=4,
                                   font=('times', 15, ' bold '))
        NAME.place(x=950, y=210)
        NAME = tk.Label(window, text=("Position:" + person_Data[3]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=280)
        NAME = tk.Label(window, text=("Salary:" + person_Data[4]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=350)
        NAME = tk.Label(window, text=("Dept:" + person_Data[5]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=420)
    elif person_Data != '' and len(person_Data) >= 6 and (person_Data[3] == 'HOD' or person_Data[3] == "ADMIN"):
        if person_Data[3] == "ADMIN":

            NAME = tk.Label(window, text=("ADMIN DETAILS"), width=20, fg="black", bg="green", height=4,
                            font=('times', 15, ' bold '))
            NAME.place(x=950, y=70)
        else:

            NAME = tk.Label(window, text=("HOD DETAILS"), width=20, fg="black", bg="green", height=4,
                            font=('times', 15, ' bold '))
            NAME.place(x=950, y=70)
        NAME = tk.Label(window, text=("Name:" + person_Data[0]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=140)
        NAME = tk.Label(window, text=("Login Id:" + person_Data[1]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=210)
        NAME = tk.Label(window, text=("Position:" + person_Data[3]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=280)
        NAME = tk.Label(window, text=("Salary:" + person_Data[4]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=350)
        NAME = tk.Label(window, text=("Dept:" + person_Data[5]), width=20, fg="black", bg="green", height=4,
                        font=('times', 15, ' bold '))
        NAME.place(x=950, y=420)
    else:
        Acknowledgement = tk.Label(window, text="Enter a Valid Data", width=20, fg="black", bg="green", height=4,
                                   font=('times', 15, ' bold '))
        Acknowledgement.place(x=750, y=600)

def Delete_person(Id):
    sql_stmt = "Delete from "
    Database = collecting_complete_data()
    for idx in Database:
        if Id == idx[1]:
            if idx[-1] == "STUDYING":
                sql_stmt += "student_database where LOGIN_ID ='" + Id + "'"
            elif idx[-1] == 'FACULTY' or idx[-1] == 'TEACHER':
                sql_stmt += "faculty_database where LOGIN_ID ='" + Id + "'"
            else:
                sql_stmt += "erp_database where LOGIN_ID ='" + Id + "'"
            delele_person_Data(sql_stmt)

def Delete_Members():
    def delete_data():
        id=ID_txt.get()
        Id=id.lower()
        Database = collecting_complete_data()
        Database = id_check(Database)
        if Id in Database:
            view_person(Id)
            Delete_person(Id.upper())
            Acknowledgement = tk.Label(window, text="Person Data removed", width=20, fg="white", bg="Red", height=4,
                                       font=('times', 15, ' bold '))
            Acknowledgement.place(x=750, y=600)
        else:
            Acknowledgement = tk.Label(window, text="Enter a Valid Data", width=20, fg="white", bg="Red", height=4,
                                       font=('times', 15, ' bold '))
            Acknowledgement.place(x=750, y=600)

    clear()
    message = tk.Label(window, text="                 Delete Members        ", bg="green", fg="white",
                       font=("ArialBold", 40))
    message.pack(fill="x")
    BACK =tk.Button(window, text="BACK ", command=admin_page,fg="white", bg="green", width=30, height=4,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=90)
    ID = tk.Label(window, text="Enter Person ID", width=20, fg="black", bg="deep pink", height=2,
                     font=('times', 15, ' bold '))
    ID.place(x=400, y=200)
    ID_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    ID_txt.place(x=650, y=200)

    SubmitButton = tk.Button(window, text="Submit", command=delete_data, fg="black", bg="grey",
                                 width=10, height=1, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=750, y=450)




def View_Members():
    def view_Data():
        id = ID_txt.get()
        Id = id.lower()
        view_person(Id)
    clear()
    message = tk.Label(window, text="                 View Members        ", bg="green", fg="white",
                       font=("ArialBold", 40))
    message.pack(fill="x")
    BACK =tk.Button(window, text="BACK ", command=admin_page,fg="white", bg="green", width=30, height=4,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=90)
    ID = tk.Label(window, text="Enter Person ID", width=20, fg="black", bg="deep pink", height=2,
                     font=('times', 15, ' bold '))
    ID.place(x=400, y=200)
    ID_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    ID_txt.place(x=650, y=200)

    SubmitButton = tk.Button(window, text="Submit", command=view_Data, fg="black", bg="grey",
                                 width=10, height=1, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=750, y=450)


def Search_Members():
    clear()
    message = tk.Label(window, text="                 Search Section        ", bg="green", fg="white",
                       font=("ArialBold", 40))
    message.pack(fill="x")
    BACK =tk.Button(window, text="BACK ", command=admin_page,fg="white", bg="green", width=30, height=4,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20, y=90)
    takeImg = tk.Button(window, text="Known Person", command=known_search, fg="white", bg="blue2", width=30, height=5,
                        activebackground="Red",
                        font=('times', 15, ' bold '))  # command=take_img
    takeImg.place(x=90, y=400)

    FA = tk.Button(window, text="Unknown Person", command=unknown_search, fg="white", bg="blue2", width=30,
                   height=5,
                   activebackground="Red", font=('times', 15, ' bold '))  # command=subjectchoose
    FA.place(x=690, y=400)

def unknown_search():
    clear()
    message = tk.Label(window, text="                 Unknown Search        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)

    BACK =tk.Button(window, text="BACK ", command=Search_Members,fg="white", bg="green", width=30, height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=200)

    B1 = tk.Button(window, text="Student Details", command=student_Details,fg="white", bg="blue2", width=30, height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B1.place(x=20,y=400)

    B2 = tk.Button(window, text="Faculty Details", command=faculty_details, fg="white", bg="blue2", width=30,
                   height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B2.place(x=420, y=400)

    B3 = tk.Button(window, text="Erp Details", command=erp_details, fg="white", bg="blue2", width=30,
                   height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B3.place(x=840, y=400)


def erp_details():
    Data = collecting_specific_data("erp_database")
    if Data == []:
        Acknowledgement = tk.Label(window, text="Enter a Valid Data", width=20, fg="white", bg="Red", height=4,
                                   font=('times', 15, ' bold '))
        Acknowledgement.place(x=750, y=600)
    else:
        All_Database = []
        erp_Database = ["Name", "Roll no", "Password", "Position", "Salary", "Dept", "Status"]
        All_Database.append(erp_Database)
        for row in Data:
            All_Database.append(row)
        import tkinter
        root = tkinter.Tk()
        root.title("Erp Details")
        root.configure(background='snow')
        r = 0
        for col in All_Database:
            c = 0
            for row in col:
                label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                      bg="lawn green", text=row, relief=tkinter.RIDGE)
                label.grid(row=r, column=c)
                c += 1
            r += 1
        root.mainloop()


def faculty_details():
    Data = collecting_specific_data("faculty_database")
    if Data == []:
        Acknowledgement = tk.Label(window, text="Enter a Valid Data", width=20, fg="white", bg="Red", height=4,
                                   font=('times', 15, ' bold '))
        Acknowledgement.place(x=750, y=600)
    else:
        All_Database = []
        Faculty_Database = ["Name", "Roll no", "Password", "Position", "Salary", "Dept", "Status", " year of joining"]
        All_Database.append(Faculty_Database)
        for row in Data:
            All_Database.append(row)
        import tkinter
        root = tkinter.Tk()
        root.title("Faculty Details")
        root.configure(background='snow')
        r = 0
        for col in All_Database:
            c = 0
            for row in col:
                label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                      bg="lawn green", text=row, relief=tkinter.RIDGE)
                label.grid(row=r, column=c)
                c += 1
            r += 1
        root.mainloop()

def student_Details():
    Data = collecting_specific_data("student_database")
    if Data == []:
        Acknowledgement = tk.Label(window, text="Enter a Valid Data", width=20, fg="white", bg="Red", height=4,
                                   font=('times', 15, ' bold '))
        Acknowledgement.place(x=750, y=600)
    else:
        All_Database = []

        Student_Database = ["Name", "Roll no", "Password", "Dept", "Class", "Section", "Semester", " ~year of joining",
                            "Status"]
        All_Database.append(Student_Database)
        for row in Data:
            All_Database.append(row)
        import tkinter
        root = tkinter.Tk()
        root.title("Student Details")
        root.configure(background='snow')
        r = 0
        for col in All_Database:
            c = 0
            for row in col:
                label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                      bg="lawn green", text=row, relief=tkinter.RIDGE)
                label.grid(row=r, column=c)
                c += 1
            r += 1
        root.mainloop()


def known_search():
    def view_known_Data():
        id = ID_txt.get()
        Id = id.lower()
        Database = collecting_complete_data()
        Database = id_check(Database)
        if Id in Database:
            view_person(Id)
        else:
            Acknowledgement = tk.Label(window, text="Enter a Valid Data", width=20, fg="black", bg="green", height=4,
                                       font=('times', 15, ' bold '))
            Acknowledgement.place(x=20, y=550)
    clear()
    message = tk.Label(window, text="                 Known Search        ", bg="green", fg="white",
                       font=("ArialBold", 40))
    message.pack(fill="x")
    BACK = tk.Button(window, text="BACK ", command=Search_Members, fg="white", bg="green", width=30, height=4,
                     activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20, y=90)

    ID = tk.Label(window, text="Enter Person ID", width=20, fg="black", bg="deep pink", height=2,
                     font=('times', 15, ' bold '))
    ID.place(x=400, y=200)
    ID_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    ID_txt.place(x=650, y=200)

    SubmitButton = tk.Button(window, text="Submit", command=view_known_Data, fg="black", bg="grey",
                                 width=10, height=1, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=750, y=450)

def convert_format(Data):
    Data=Data.split("/")
    Data=Data[::-1]
    return "-".join(Data)

def check_format(Data_1,Data_2):
    if Data_1.count("/")==2 and Data_2.count("/")==2:
        Data_1=Data_1.split("/")
        Data_2=Data_2.split("/")
        if check_date(Data_1) and check_date(Data_2):
            return True
    return False

def check_date():
    cur_Date=desc_attendance()
    Dates=[]
    for idx in cur_Date:
        Dates.append(idx[0])
    if current_date() in Dates:
        return True
    return False

def Semester_timings():
    clear()
    message = tk.Label(window, text="                 Semester Timings        ", bg="green", fg="white",
                       font=("ArialBold", 40))
    message.pack(fill="x")

    BACK = tk.Button(window, text="BACK ", command=admin_page, fg="white", bg="green", width=30, height=4,
                     activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20, y=90)
    Database =extract_semester_timings()
    if Database==[]:
        Acknowledgement = tk.Label(window, text="No Data Available", width=20, fg="black", bg="green", height=4,
                                   font=('times', 15, ' bold '))
        Acknowledgement.place(x=20, y=550)
    else:
        takeImg = tk.Button(window, text=("Starting Date"+convert_format(Database[0])), command=known_search, fg="white", bg="blue2", width=30,
                            height=5,
                            activebackground="Red",
                            font=('times', 15, ' bold '))  # command=take_img
        takeImg.place(x=200, y=250)

        FA = tk.Button(window, text=("Ending Date"+convert_format(Database[1])), command=unknown_search, fg="white", bg="blue2", width=30,
                       height=5,
                       activebackground="Red", font=('times', 15, ' bold '))  # command=subjectchoose
        FA.place(x=800, y=250)

def view_admin_attendance():
    clear()
    message = tk.Label(window, text="                 Attendance Section        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)

    BACK =tk.Button(window, text="BACK ", command=admin_page,fg="white", bg="green", width=30, height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=200)

    B1 = tk.Button(window, text="Student Attendance", command=student_section,fg="white", bg="blue2", width=30, height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B1.place(x=20,y=400)

    B2 = tk.Button(window, text="Faculty Attendance", command=faculty_section, fg="white", bg="blue2", width=30,
                   height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B2.place(x=420, y=400)
def faculty_section():
    return
def student_section():
    Database=[]
    def report_section():
        clear()
        message = tk.Label(window, text="                 Report Section        ", bg="green", fg="white",
                           font=("ArialBold", 40))

        message.pack(fill="x")  # place(x=80, y=20)

        BACK = tk.Button(window, text="BACK ", command=view_admin_attendance, fg="white", bg="green", width=30,
                         height=5,
                         activebackground="Red", font=('times', 15, ' bold '))
        BACK.place(x=20, y=200)
        B1 = tk.Button(window, text="Show Details", command=select_choice_1, fg="white", bg="blue2",
                       width=30, height=5,
                       activebackground="Red", font=('times', 15, ' bold '))
        B1.place(x=20, y=400)

        B2 = tk.Button(window, text="Report Generation", command=select_choice_2, fg="white", bg="blue2", width=30,
                       height=5,
                       activebackground="Red", font=('times', 15, ' bold '))
        B2.place(x=420, y=400)
    def select_choice_1():
        Database.insert(4,'1')
        choice()
        del Database[4]
    def select_choice_2():
        Database.insert(4,'2')
        choice()
        del Database[4]
    def choice():
        if (Database[3] == "percentage" or Database[3] == "Today_attendance") and Database[0]== "student":
            Data = get_Data_from_Database_1(Database[3], Database[0], Database[1], Database[2])
            if Database[4] == '1':
                if Data==[]:
                    Acknowledgement = tk.Label(window, text="No Data Available", width=20, fg="black", bg="Red",
                                                   height=4,
                                                   font=('times', 15, ' bold '))
                    Acknowledgement.place(x=20, y=550)
                elif Database[3]=="Today_attendance":
                    import tkinter
                    root = tkinter.Tk()
                    root.title("SMEC_Class_"+Database[1]+Database[2]+current_date())
                    root.configure(background='snow')
                    r = 0
                    All_Database =[]
                    MY=["S_no","Roll_no","Name" ,str(current_date())]
                    All_Database.append(MY)
                    for row in Data:
                        All_Database.append(row)

                    for col in All_Database:
                        c = 0
                        for row in col:
                            label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                          bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                    root.mainloop()
                else:
                    import tkinter
                    root = tkinter.Tk()
                    root.title(Database[0] + " percentage")
                    if Data != [] and Data != None:
                        root.configure(background='snow')
                        r = 0
                        All_Database = []
                        All_Database.append(["S_no","Roll_no","Name","Percentage"])
                        for row in Data:
                            All_Database.append(row)
                        for col in All_Database:
                            c = 0
                            for row in col:
                                label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                      bg="lawn green", text=row, relief=tkinter.RIDGE)
                                label.grid(row=r, column=c)
                                c += 1
                            r += 1
                        root.mainloop()
                    else:
                        Acknowledgement = tk.Label(window, text="No Data Available", width=20, fg="black", bg="Red",
                                                   height=4,
                                                   font=('times', 15, ' bold '))
                        Acknowledgement.place(x=20, y=550)
            elif Database[4] == '2':
                with open(
                                                                    "C:\MiniProject\Attendance_management_system\Reports\student_" + Database[3] + "_" + Database[1] + Database[2] + ".csv",
                                                                    'w+')as my_file:
                    my_file.write("\n\n\n")
                    my_file.write(
                        "                                                                                           SMEC                                  \n")
                    my_file.write(" Class : " + Database[1] + Database[2] + "\n")
                    my_file.write("Dept:CSE\n")
                    if Database[3] == "Today_attendance":
                        my_file.write("Date:" + current_date() + "\n")
                        if Data == [] or Data == None:
                            my_file.write("\n" + "No Data Available " + "\n")
                            Acknowledgement = tk.Label(window, text="No Data Available", width=20, fg="black",
                                                           bg="Red",
                                                           height=4,
                                                           font=('times', 15, ' bold '))
                            Acknowledgement.place(x=20, y=550)
                        else:
                            my_file.write("\nS_no,Roll_no,Name," + str(current_date()) + "\n")
                            my_file.write("\n")
                            for row in Data:
                                row = ",".join(row)
                                my_file.write(row)
                                my_file.write("\n\n")
                            my_file.write(
                                "\n\n\nSignature of HOD                                                                        Signature of Principal")
                            Acknowledgement = tk.Label(window, text="Sheet Generated", width=20, fg="black",
                                                       bg="Red",
                                                       height=4,
                                                       font=('times', 15, ' bold '))
                            Acknowledgement.place(x=20, y=550)
                    else:
                        my_file.write(Database[0] + " percentage\n\n")
                        my_file.write("Dept:CSE\n\n")
                        if Data != [] and Data != None:
                            my_file.write("\nS_no,Roll_no,Name,Percentage\n")
                            for row in Data:
                                row = ",".join(row)
                                my_file.write(row)
                                my_file.write("\n\n")
                            my_file.write(
                                "\n\nSignature of HOD                                                                        Signature of Principal\n")
                            Acknowledgement = tk.Label(window, text="Sheet Generated", width=20, fg="black",
                                                       bg="Red",
                                                           height=4,
                                                           font=('times', 15, ' bold '))
                            Acknowledgement.place(x=20, y=550)
                        else:
                            my_file.write("\n\n\nNo Data Available\n\n")
                            Acknowledgement = tk.Label(window, text="No Data Available", width=20, fg="black",
                                                           bg="Red",
                                                           height=4,
                                                           font=('times', 15, ' bold '))
                            Acknowledgement.place(x=20, y=550)
                    my_file.close()
        else:
            Data = get_Data_from_Database_1(Database[3], Database[0], Database[1], Database[2])
            if Database[4] == '1':
                if Data == []:
                    Acknowledgement = tk.Label(window, text="No Data Available", width=20, fg="black", bg="Red",
                                               height=4,
                                               font=('times', 15, ' bold '))
                    Acknowledgement.place(x=20, y=550)
                elif Database[3] == "Today_attendance":
                    import tkinter
                    root = tkinter.Tk()
                    root.title("Faculty_Attendance_" + current_date())
                    root.configure(background='snow')
                    r = 0
                    All_Database = []
                    MY = ["S_no", "Roll_no", "Name", str(current_date())]
                    All_Database.append(MY)
                    for row in Data:
                        All_Database.append(row)
                    for col in All_Database:
                        c = 0
                        for row in col:
                            label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                    root.mainloop()
                else:
                    import tkinter
                    root = tkinter.Tk()
                    root.title(Database[0] + " percentage")
                    if Data != [] and Data != None:
                        root.configure(background='snow')
                        r = 0
                        All_Database = []
                        All_Database.append(["S_no", "Roll_no", "Name", "Percentage"])
                        for row in Data:
                            All_Database.append(row)
                        for col in All_Database:
                            c = 0
                            for row in col:
                                label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                      bg="lawn green", text=row, relief=tkinter.RIDGE)
                                label.grid(row=r, column=c)
                                c += 1
                            r += 1
                        root.mainloop()
                    else:
                        Acknowledgement = tk.Label(window, text="No Data Available", width=20, fg="black", bg="Red",
                                                   height=4,
                                                   font=('times', 15, ' bold '))
                        Acknowledgement.place(x=20, y=550)
            elif Database[4] == '2':
                with open(
                                                                "C:\MiniProject\Attendance_management_system\Reports\student_" + Database[3] + "_" + Database[1] + Database[2] + ".csv",
                        'w+')as my_file:
                    my_file.write("\n\n\n")
                    my_file.write(
                        "                                                                                           SMEC                                  \n")
                    my_file.write(" Class : " + Database[1] + Database[2] + "\n")
                    my_file.write("Dept:CSE\n")
                    if Database[3] == "Today_attendance":
                        my_file.write("Date:" + current_date() + "\n")
                        if Data == [] or Data == None:
                            my_file.write("\n" + "No Data Available " + "\n")
                            Acknowledgement = tk.Label(window, text="No Data Available", width=20, fg="black",
                                                       bg="Red",
                                                       height=4,
                                                       font=('times', 15, ' bold '))
                            Acknowledgement.place(x=20, y=550)
                        else:
                            my_file.write("\nS_no,Roll_no,Name," + str(current_date()) + "\n")
                            my_file.write("\n")
                            for row in Data:
                                row = ",".join(row)
                                my_file.write(row)
                                my_file.write("\n\n")
                            my_file.write(
                                "\n\n\nSignature of HOD                                                                        Signature of Principal")
                            Acknowledgement = tk.Label(window, text="Sheet Generated", width=20, fg="black",
                                                       bg="Red",
                                                       height=4,
                                                       font=('times', 15, ' bold '))
                            Acknowledgement.place(x=20, y=550)
                    else:
                        my_file.write(Database[0] + " percentage\n\n")
                        my_file.write("Dept:CSE\n\n")
                        if Data != [] and Data != None:
                            my_file.write("\nS_no,Roll_no,Name,Percentage\n")
                            for row in Data:
                                row = ",".join(row)
                                my_file.write(row)
                                my_file.write("\n\n")
                            my_file.write(
                                "\n\nSignature of HOD                                                                        Signature of Principal\n")
                            Acknowledgement = tk.Label(window, text="Sheet Generated", width=20, fg="black",
                                                       bg="Red",
                                                       height=4,
                                                       font=('times', 15, ' bold '))
                            Acknowledgement.place(x=20, y=550)
                        else:
                            my_file.write("\n\n\nNo Data Available\n\n")
                            Acknowledgement = tk.Label(window, text="No Data Available", width=20, fg="black",
                                                       bg="Red",
                                                       height=4,
                                                       font=('times', 15, ' bold '))
                            Acknowledgement.place(x=20, y=550)

    def Section_4A():
        Database.insert(0,'student')
        Database.insert(1,'4')
        Database.insert(2,'A')
        view_section("student", "4", "A")

    def Section_4B():
        Database.insert(0,'student')
        Database.insert(1,'4')
        Database.insert(2,'B')
        view_section("student", "4", "B")

    def Section_4C():
        Database.insert(0,'student')
        Database.insert(1,'4')
        Database.insert(2,'C')
        view_section("student", "4", "C")

    def Section_4D():
        Database.insert(0,'student')
        Database.insert(1,'4')
        Database.insert(2,'D')
        view_section("student", "4", "D")

    def report_secton_percentage():
        Database.insert(3,"percentage")
        report_section()

    def report_section_Today():
        Database.insert(3,"Today_attendance")
        report_section()

    def view_section(status, smec_class, section):
        clear()
        message = tk.Label(window, text="                 Choice Section        ", bg="green", fg="white",
                           font=("ArialBold", 40))

        message.pack(fill="x")  # place(x=80, y=20)

        BACK = tk.Button(window, text="BACK ", command=view_admin_attendance, fg="white", bg="green", width=30, height=5,
                         activebackground="Red", font=('times', 15, ' bold '))
        BACK.place(x=20, y=200)
        B1 = tk.Button(window, text="Attendance Percentage", command=report_secton_percentage, fg="white", bg="blue2", width=30, height=5,
                       activebackground="Red", font=('times', 15, ' bold '))
        B1.place(x=20, y=400)

        B2 = tk.Button(window, text="Today Attendance", command=report_section_Today, fg="white", bg="blue2", width=30,
                       height=5,
                       activebackground="Red", font=('times', 15, ' bold '))
        B2.place(x=420, y=400)
    clear()
    message = tk.Label(window, text="                Student  Attendance Section        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)

    BACK =tk.Button(window, text="BACK ", command=view_admin_attendance,fg="white", bg="green", width=30, height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=200)
    SubmitButton = tk.Button(window, text="Class 4A", command=Section_4A, fg="white", bg="blue",
                             width=40, height=3, activebackground="Red",
                             font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=600, y=90)
    SubmitButton = tk.Button(window, text="Class 4B", command=Section_4B, fg="white", bg="blue",
                             width=40, height=3, activebackground="Red",
                             font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=600, y=180)
    SubmitButton = tk.Button(window, text="Class 4C", command=Section_4C, fg="white", bg="blue",
                             width=40, height=3, activebackground="Red",
                             font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=600, y=270)
    SubmitButton = tk.Button(window, text="Class 4D", command=Section_4D, fg="white", bg="blue",
                             width=40, height=3, activebackground="Red",
                             font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=600, y=360)

def admin_page():
    clear()
    message = tk.Label(window, text="                 Admin Section        ", bg="green", fg="white",
                       font=("ArialBold", 40))
    message.pack(fill="x")

    BACK =tk.Button(window, text="Logout ", command=login_page,fg="white", bg="green", width=30, height=4,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=90)
    AddButton = tk.Button(window, text="Add Members", command=Add_Members, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    AddButton.place(x=600, y=90)
    DeleteButton = tk.Button(window, text="Delete Members", command=Delete_Members, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    DeleteButton.place(x=600, y=180)
    SearchButton = tk.Button(window, text="Search Members", command=View_Members, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    SearchButton.place(x=600, y=270)
    ViewButton = tk.Button(window, text="View Members", command=Search_Members, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    ViewButton.place(x=600, y=360)
    SemesterButton = tk.Button(window, text="Semester Timings", command=Semester_timings, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    SemesterButton.place(x=600, y=450)
    SubmitButton = tk.Button(window, text="View Attendance", command=view_admin_attendance, fg="white", bg="blue",
                                 width=40, height=3, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=600, y=540)

def erp_login():
    def log_in():
        id=Id_txt.get()
        password=password_txt.get()
        if id == '':
            error(1)
        elif password=='':
            error(2)
        elif not check_login(id, password, "ADMIN"):
            error(3)
        else:
            admin_page()
    clear()
    message = tk.Label(window, text="                 ERP Login        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)
    BACK =tk.Button(window, text="BACK ", command=login_page,fg="white", bg="green", width=30, height=4,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=150)

    ID = tk.Label(window, text="Enter Login ID", width=20, fg="black", bg="deep pink", height=2,
                  font=('times', 15, ' bold '))
    ID.place(x=200, y=300)

    Id_txt = tk.Entry(window, width=20, bg="yellow", fg="red", font=('times', 25, ' bold '))
    Id_txt.place(x=550, y=300)

    password = tk.Label(window, text="Enter password", width=20, fg="black", bg="deep pink", height=2,
                            font=('times', 15, ' bold '))
    password.place(x=200, y=400)

    password_txt = tk.Entry(window, width=20, bg="yellow",show="*", fg="red", font=('times', 25, ' bold '))
    password_txt.place(x=550, y=400)

    SubmitButton = tk.Button(window, text="Submit", command=log_in, fg="black", bg="grey",
                                 width=10, height=1, activebackground="Red",
                                 font=('times', 15, ' bold '))  # command=clear
    SubmitButton.place(x=950, y=450)



def faculty_Dashboard(id):
    print("here")


def clear():
    for frame in window.winfo_children():
        frame.destroy()


def login_page():
    def clear_main_page():
        clear()
        main_page()
    clear()
    message = tk.Label(window, text="                 Login Section        ", bg="green", fg="white",
                       font=("ArialBold", 40))

    message.pack(fill="x")  # place(x=80, y=20)

    BACK =tk.Button(window, text="BACK ", command=clear_main_page,fg="white", bg="green", width=30, height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    BACK.place(x=20,y=200)

    B1 = tk.Button(window, text="Student Login", command=student_login,fg="white", bg="blue2", width=30, height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B1.place(x=90,y=400)

    B3 = tk.Button(window, text="Erp Login", command=erp_login, fg="white", bg="blue2", width=30,
                   height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B3.place(x=690, y=400)


'''
    B2 = tk.Button(window, text="Faculty Login", command=faculty_login, fg="white", bg="blue2", width=30,
                   height=5,
                   activebackground="Red", font=('times', 15, ' bold '))
    B2.place(x=420, y=400)
'''

#####Window is our Main frame of system
window = tk.Tk()
window.title("FAMS-Face Recognition Based Attendance Management System")

window.geometry('1280x720')
def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)
unique_id=0

if start():
    creating_Database('')
main_page()
window.mainloop()
