Steps:-
1)Install Mysql and pycharm(optional) Software on your system.
2)Set up them and download python module such as Tkinter,datetime,pymysql,
cv2(opencv),numpy,pil(pillow).
3)create three new folders in your project folder ,naming Reports,Images,training .
4) create a training.yml file in your training folder.
5)Set up the file extensions like haarcascade_frontalface_default.xml you will find them in your python folder like "C:\\Users\\rohit gupta\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml"(my extension) ,similary for images and reports and change them all over the file.
6)for connecting python to mysql give accurate values to database connectivity like host='localhost',user=your mysql database name(root),password=your password which you have setup during the installation of mysql database.
ex:-con = pymysql.connect(host='localhost',
                      user='root',
                      password='tiger')
In mysql_operations file.
7)Installation and setup procedure are finished ,try running it.
8)The main file to run is runner.py .
9)If any error occur ,try google it and solve it .
							Thank You.
							      Rohit 