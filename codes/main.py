

import time, datetime, pickle, sys, os, cv2, math
import mysql.connector
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

def print_sql(sql, data): 
    print(f"[sql]")
    print(f"{sql}")
    print ("")
    print(f"[data]")
    for item in data: 
        print (item)
    print("\n")

class StackedWindow(QMainWindow):

    def __init__(self):
        super(StackedWindow, self).__init__()
    def activate(self): pass
    def deactivate(self): pass

class PortalPage(StackedWindow):

    def __init__(self):

        # Load face train data
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("facial_login_data/train.yml")
        with open("facial_login_data/labels.pickle", "rb") as f:
            self.labels = pickle.load(f)
            self.labels = {v: k for k, v in self.labels.items()}
        self.face_cascade = cv2.CascadeClassifier(\
            'facial_login_data/haarcascade/haarcascade_frontalface_default.xml')

        # Load the UI
        super(PortalPage, self).__init__()
        loadUi("Portal.ui", self)

        self.ExitButton.clicked.connect(lambda: leave())
        current_time = time.localtime()

    def face_update(self):

        # Capture and read a new image
        self.cap = cv2.VideoCapture(0)
        flag, self.image = self.cap.read()
       
        # Displays the face on UI
        h, w = self.image.shape[:2]
        l = int((w - h) / 2)
        square_image = self.image[:, l:l + h]
        square_image = cv2.flip(square_image, 1)
        square_image = cv2.resize(square_image, (550, 550))
        square_image = cv2.cvtColor(square_image, cv2.COLOR_BGR2RGB)
        show_image = QtGui.QImage(square_image.data, square_image.shape[1], square_image.shape[0],
                                  QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(show_image)
        self.CameraArea.setPixmap(pixmap)

class FacialLoginPage(StackedWindow):

    def __init__(self):

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("facial_login_data/train.yml")
        with open("facial_login_data/labels.pickle", "rb") as f:
            self.labels = pickle.load(f)
            self.labels = {v: k for k, v in self.labels.items()}
        self.face_cascade = cv2.CascadeClassifier(\
            'facial_login_data/haarcascade/haarcascade_frontalface_default.xml')
        
        super(FacialLoginPage, self).__init__()
        loadUi("FacialLogin.ui", self)
        self.labels = {'face_id_in_string': -1}
        self.image = None

        # Update the face on the Login Page every 50 seconds
        self.timer = QtCore.QTimer(); 
        self.timer.start(50); 
        self.timer.timeout.connect(self.face_update); 

        # Bind the buttons to the page changing events
        self.pwd_LoginButton.clicked.connect(lambda: switch_to(PWDLOGIN))
        self.ExitButton.clicked.connect(lambda: leave())
        self.VerifyButton.clicked.connect(self.verify_id)

        self.hint_label.setText(
'''
<html>
<head/>
<body>
<p>
    <span style=" color:#646464;">Please keep your face displayed in the circle and click </span>
    <span style=" font-weight:600; color:#646464;">Verify</span>
</p>
</body>
</html>
'''
        )
        
        # Open the camera
        self.cap = cv2.VideoCapture()
        self.cap.open(0, cv2.CAP_DSHOW)

    def face_update(self):

        # Reset the update timer
        self.timer.start(50); 

        # Capture and read a new image
        self.cap = cv2.VideoCapture(0)
        flag, self.image = self.cap.read()
       
        # Displays the face on UI
        h, w = self.image.shape[:2]
        l = int((w - h) / 2)
        square_image = self.image[:, l:l + h]
        square_image = cv2.flip(square_image, 1)
        square_image = cv2.resize(square_image, (400, 400))
        square_image = cv2.cvtColor(square_image, cv2.COLOR_BGR2RGB)
        show_image = QtGui.QImage(square_image.data, square_image.shape[1], square_image.shape[0],
                                  QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(show_image)
        self.CameraArea.setPixmap(pixmap)

    def verify_id(self):

        # Capture and read a new image
        flag, self.image = self.cap.read()
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)

        # Use Confidence Level to detect the current user
        self.user_id = -1
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            idx, conf = self.recognizer.predict(roi_gray)
            if conf >= 90: self.user_id = int(self.labels[idx])

        # User detected
        if self.user_id != -1:
            self.hint_label.setText(
'''
<html>
<head/>
<body>
<p align="center">
    <span style=" font-weight:600; color:#646464;">Login Successfully!</span>
    <br/>
</p>
</body>
</html>
'''
            )
            self.cap.release()
            WINDOWS[FORUM] = ForumPage(self.user_id)
            WINDOWS[EXAM] = ExamPage(self.user_id)
            WINDOWS[EMAIL] = EmailPage(self.user_id)
            switch_to(HOME)

        # User not detected
        else:
            self.hint_label.setText(
'''
<html>
<head/>
<body>
<p align="center">
    <span style=" font-weight:600; color:#646464;">Unrecognized!</span>
    <br/>
    <span style=" color:#646464;">Please adjust your posture and try again</span>
</p>
</body>
</html>
'''
        )

class PwdLoginPage(StackedWindow):

    def __init__(self):
        super(PwdLoginPage, self).__init__()
        self.uid = ""
        self.pwd = ""
        loadUi("PwdLogin.ui", self)
        self.slot_init()

    def slot_init(self):
        self.ExitButton.clicked.connect(lambda: leave())
        self.LoginButton.clicked.connect(self.check_pwd)

    def activate(self):
        self.hint_label.setText(
            '<html><head/><body><p><span style=" color:#646464;">Please enter your UID and Password and click </span><span style=" font-weight:600; color:#646464;">Login</span></p></body></html>'
        )
        pass

    def deactivate(self):
        pass

    def check_pwd(self):
        self.uid = self.uid_text.toPlainText()
        self.pwd = self.pwd_text.toPlainText()
        sql = "SELECT Password FROM Student WHERE UID='%s'" % self.uid
        database.cursor.execute(sql)
        result = database.cursor.fetchall()
        pwd = result[0][0] if result else "PWD"

        if self.pwd == pwd:
            self.hint_label.setText(
                '<html><head/><body><p align="center"><span style=" font-weight:600; color:#646464;">Login Successfully!</span><span style=" font-weight:600; color:#646464;"><br/></p></body></html>'
            )
            time.sleep(2)
            self.deactivate()
            # WINDOWS[HOME] = HomePage(self.user_id)
            # WINDOWS[PROFILE] = ProfilePage(self.user_id)
            # WINDOWS[ONECLASS] = OneClassPage(self.user_id)
            # WINDOWS[TIMETABLE] = TimetablePage(self.user_id)
            # WINDOWS[FORUM] = ForumPage(self.user_id)
            # WINDOWS[EXAM] = ExamPage(self.user_id)
            # WINDOWS[EMAIL] = EmailPage(self.user_id)
            # WINDOWS[LINK] = LinkPage(self.user_id)
            switch_to(HOME)

        else:
            self.hint_label.setText(
                '<html><head/><body><p align="center"><span style=" font-weight:600; color:#646464;">Login Failed!</span><span style=" font-weight:600; color:#646464;"><br/></span><span style=" color:#646464;">Please check your UID and Password and try again</span></p></body></html>'
            )

class HomePage(StackedWindow):

    def __init__(self, user_id, database):
        super(HomePage, self).__init__()
        loadUi("Home.ui", self)
        self.user_id = user_id
        self.database = database
        self.name = ''
        self.last_login_time = ''
        self.this_login_time = 'this this'
        self.login_history = []
        self.login_history_labels = []
        self.ProfileButton.clicked.connect(lambda: switch_to(PROFILE))
        self.ClassButton.clicked.connect(lambda: switch_to(ONECLASS))
        self.ExitButton.clicked.connect(leave)

        self.update_login_time()

        self.loginHintLabel.setText('')
        self.get_data()
        self.set_content()

    def create_label(self, height):
        new_label = QtWidgets.QLabel(self.historyScrollAreaWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(new_label.sizePolicy().hasHeightForWidth())
        new_label.setSizePolicy(sizePolicy)
        new_label.setMinimumSize(QtCore.QSize(0, height))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI")
        font.setPointSize(12)
        new_label.setFont(font)
        return new_label

    def sql_name(self):
        return "select name from Student where student_id = '%s'" % self.user_id
    
    def sql_history(self):
        return "select login_time from LoginHistory where student_id = '%s'" % self.user_id

    def get_data(self):
        sql = self.sql_name()
        database.cursor.execute(sql)
        result = database.cursor.fetchall()
        self.name = result[0][0]

        sql = self.sql_history()
        database.cursor.execute(sql)
        result = database.cursor.fetchall()
        self.login_history = result

        if len(result) > 1:
            self.last_login_time = result[0][0]
        else:
            self.last_login_time = 'No record'


    def set_content(self):
        self.welcome_label.setText(
            f'<html><head/><body><p><span style=" color:#003780;">Welcome back, {self.name}!</span></p></body></html>')
        self.LoginTimeLabel.setText(
            f'<html><head/><body><p><span style=" font-size:12pt; color:#646464;">Login time:<br/>{self.this_login_time}</span></p></body></html>')
        for label in self.login_history_labels:
            self.verticalLayout_4.removeWidget(label)
        self.login_history_labels = []
        for i, history in enumerate(self.login_history[1:]):
            label = self.create_label(height=40)
            label.setText(f'<html><head/><body><p>{history[0]}</p></body></html>')
            self.verticalLayout_4.insertWidget(i, label)
            self.login_history_labels.append(label)
        if len(self.login_history) == 1:
            self.loginHintLabel.setText(
                '<html><head/><body><p><span style=" font-weight:600; color:#003780;">No record!</span></p></body></html>')
        else:
            self.loginHintLabel.setText('')

    def update_login_time(self):
        now = time.localtime()
        year = str(now.tm_year).zfill(4)
        mon = str(now.tm_mon).zfill(2)
        mday = str(now.tm_mday).zfill(2)
        hour = str(now.tm_hour).zfill(2)
        min = str(now.tm_min).zfill(2)
        sec = str(now.tm_sec).zfill(2)
        now_str = f'{year}-{mon}-{mday} {hour}:{min}:{sec}'
        self.this_login_time = now_str

        sql = "select COUNT(*) from loginhistory where student_id = '%s'" % self.user_id
        database.cursor.execute(sql)
        result = database.cursor.fetchall()
        new_id = result[0][0] + 1

        sql = f'''
insert into LoginHistory values ({self.user_id}, {new_id}, \'{now_str}\', \'{now_str}\', 0); 
        '''
        print ("[sql]", sql)

        database.cursor.execute(sql)
        database.conn.commit()

class ProfilePage(StackedWindow):

    def __init__(self, user_id, database):

        super(ProfilePage, self).__init__()
        loadUi("Profile.ui", self)
        self.user_id = user_id
        self.database = database
        self.name = 'nnn'
        self.email = 'eee'
        self.last_login_time = 'qqq'
        self.home_button.clicked.connect(lambda: switch_to(HOME))
        self.get_data()
        self.set_content()

    def get_data(self):

        sql = f'''
SELECT name
FROM Student
WHERE student_id = {self.user_id}; 
        '''

        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()
        print_sql(sql, result)

        self.name = result[0][0]

        sql = f'''
SELECT email
FROM Student
WHERE student_id = {self.user_id}  
        '''

        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()
        print_sql(sql, result)


        self.email = result[0][0] 
        sql = f'''
SELECT Loginhistory.login_time
FROM Student,Loginhistory
WHERE Student.student_id = {self.user_id} 
AND Loginhistory.student_id = Student.student_id;
        
        '''
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()
        print_sql(sql, result)

        print(result)
        if len(result) >= 1:
            self.last_login_time = result[-1][0]
        else:
            self.last_login_time = 'No record'

    def set_content(self):
        self.uid_value.setText(
            f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.user_id}</span></p></body></html>')
        self.name_value.setText(
            f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.name}</span></p></body></html>')
        self.email_value.setText(
            f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.email}</span></p></body></html>')
        self.login_value.setText(
            f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.last_login_time}</span></p></body></html>')

class OneClassPage(StackedWindow):

    def __init__(self, user_id, course_id, database):

        super(OneClassPage, self).__init__()
        self.user_id = user_id
        self.database = database
        now = time.localtime()

        year = str(now.tm_year).zfill(4)
        mon = str(now.tm_mon).zfill(2)
        mday = str(now.tm_mday).zfill(2)
        hour = str(now.tm_hour).zfill(2)
        min = str(now.tm_min).zfill(2)
        sec = str(now.tm_sec).zfill(2)
        now_str = f'{year}-{mon}-{mday} {hour}:{min}:{sec}'
        self.this_login_time = now_str
        loadUi("OneClass.ui", self)

        self.course_id = course_id
        self.course_info = 'cym TUE'

        self.timetable_button.clicked.connect(lambda: switch_to(TIMETABLE))
        self.email_button.clicked.connect(lambda: switch_to(EMAIL))
        self.home_button.clicked.connect(lambda: switch_to(HOME))
        self.activate()

    def sql_getclassIn1Hour(self):
        return "select class_id from Class,Student_Course where Student_Course.student_id = '%s' and Student_Course.course_id = Class.course_id and Date_SUB(Class.start_time, INTERVAL 1 HOUR) <= '%s' and Date_ADD(Class.start_time, INTERVAL 12 HOUR) >= '%s' " % ( self.user_id, self.this_login_time, self.this_login_time)

    def activate(self):
        sql = self.sql_getclassIn1Hour()
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()
        if len(result) == 0:
            # switch_to(TIMETABLE)
            pass
        self.get_data()
        self.set_content()

    def sql_oneclass_info(self):
        return "select Right(Class.start_time,8), Class.venue from Class,Student_Course,Course where Course.course_id = Class.course_id and Student_Course.student_id = '%s' and Student_Course.course_id = Class.course_id and Date_SUB(Class.start_time, INTERVAL 1 HOUR) <= '%s' and Date_ADD(Class.start_time, INTERVAL 12 HOUR) >= '%s'" % (self.user_id, self.this_login_time, self.this_login_time)

    def get_data(self):

        sql = f'''
SELECT Course.course_code, Course.course_title, Course.course_id, Class.venue
FROM Class, Student_Course, Course
WHERE Course.course_id = Class.course_id
    AND Student_Course.student_id = {self.user_id}
    AND Student_Course.course_id = Class.course_id
    AND Date_SUB(Class.start_time, INTERVAL 1 HOUR) <= \'{self.this_login_time}\'
    AND Date_ADD(Class.start_time, INTERVAL 12 HOUR) >= \'{self.this_login_time}\'; 
        '''
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()
        print_sql(sql, result)

        if len(result) > 0:
            self.course_id = f"{result[0][0]} {result[0][1]}"  # to be done
        else:
            self.course_id = -1

        sql = self.sql_oneclass_info()
        self.database.cursor.execute(sql)
        result = self.database.cursor.fetchall()
        print_sql(sql, result); 

        if len(result) > 0:
            self.course_info = f"{result[0][0]} {result[0][1]}"
        else:
            self.course_info = ''

    def set_content(self):
        self.id_value.setText(
            f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.course_id}</span></p></body></html>')
        self.info_value.setText(
            f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.course_info}</span></p></body></html>')

class TimetablePage(StackedWindow):

    def __init__(self, user_id, database):

        super(TimetablePage, self).__init__()
        loadUi("Timetable.ui", self)
        self.classes = []
        self.user_id = user_id
        self.exam_button.clicked.connect(lambda: switch_to(EXAM))
        self.forum_button.clicked.connect(lambda: switch_to(FORUM))
        self.home_button.clicked.connect(lambda: switch_to(HOME))
        self.get_data()
        self.set_content()


    def get_data(self):

        sql = f'''

select Course.course_code, Course.course_title, Right(Class.start_time,8), Right(Class.end_time,8), Class.week_day

From Course, Class, Student_Course
where Course.course_id = Class.course_id
and Class.course_id = Student_Course.course_id
and Student_Course.student_id = {self.user_id}
ORDER BY Class.week_day
;
        
        '''

        database.cursor.execute(sql)
        result = database.cursor.fetchall()
        print_sql(sql, result)

        self.classes = result  # to be done


    def set_content(self):
        #Course.course_name, Right(Class.start_time,8), Right(Class.end_time,8), Class.weekday
        week = []
        for i in range(len(self.classes)):
            if self.classes[i][4] == '1':
                week.append('Monday')
            if self.classes[i][4] == '2':
                week.append('Tuesday')
            if self.classes[i][4] == '3':
                week.append('Wednesday')
            if self.classes[i][4] == '4':
                week.append('Thursday')
            if self.classes[i][4] == '5':
                week.append('Friday')

        if len(self.classes) > 0:
            self.class1_label.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[0][0]}</span></p></body></html>')
            self.class1_value.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{week[0]}</span></p></body></html>')
            self.class1_value_2.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[0][2]}</span></p></body></html>')
        if len(self.classes) > 1:
            self.class2_label.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[1][0]}</span></p></body></html>')
            self.class2_value.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{week[1]}</span></p></body></html>')
            self.class2_value_2.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[1][2]}</span></p></body></html>')

        if len(self.classes) > 2:
            self.class3_label.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[2][0]}</span></p></body></html>')
            self.class3_value.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{week[2]}</span></p></body></html>')
            self.class3_value_2.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[2][2]}</span></p></body></html>')
        if len(self.classes) > 3:
            self.class4_label.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[3][0]}</span></p></body></html>')
            self.class4_value.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{week[3]}</span></p></body></html>')
            self.class4_value_2.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[3][2]}</span></p></body></html>')

        if len(self.classes) > 4:
            self.class5_label.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[4][0]}</span></p></body></html>')
            self.class5_value.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{week[4]}</span></p></body></html>')
            self.class5_value_2.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[4][2]}</span></p></body></html>')
        if len(self.classes) > 5:
            self.class6_label.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[5][0]}</span></p></body></html>')
            self.class6_value.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{week[5]}</span></p></body></html>')
            self.class6_value_2.setText(
                f'<html><head/><body><p><span style=" font-size:22pt; font-weight:400; color:#476089;">{self.classes[5][2]}</span></p></body></html>')

class ForumPage(StackedWindow):

    def __init__(self, user_id, forum_id, course_id, database):

        super(ForumPage, self).__init__()
        loadUi("Forum.ui", self)

        # Button listeners
        self.OrderByAscend.clicked.connect(lambda: self.update_ascend_descend("OrderByAscend"))
        self.OrderByDescend.clicked.connect(lambda: self.update_ascend_descend("OrderByDescend"))
        self.BackButton.clicked.connect(lambda: switch_to(TIMETABLE))
        self.HomeButton.clicked.connect(lambda: switch_to(HOME))
        self.SearchButton.clicked.connect(lambda: self.update_search())
        self.Comment1LikeButton.clicked.connect(lambda: self.update_like(1))
        self.Comment2LikeButton.clicked.connect(lambda: self.update_like(2))
        self.Comment3LikeButton.clicked.connect(lambda: self.update_like(3))
        self.PreviousPageButton.clicked.connect(lambda: self.update_page(-1))
        self.NextPageButton.clicked.connect(lambda: self.update_page(1))
        self.ForumPostButton.clicked.connect(lambda: self.post_comment())

        self.user_id = user_id
        self.database = database

        self.forum_id = forum_id
        self.course_id = course_id
        self.student = 0
        self.students = []

        self.keyword = ""
        self.from_date = datetime.datetime.now() - datetime.timedelta(hours=720); 
        self.to_date = datetime.datetime.now(); 
        self.order_by = 0
        self.order_ascend_descend = 0
        self.comments = []
        self.comments_likes = []
        self.comments_display = []
        self.comments_display_likes = []

        self.page = 1

        self.forum_post = ""

        self.run_sql(); 
        self.create_ui(True)

    def update_search(self):
        
        self.student = self.StudentSelect.currentIndex()
        self.keyword = self.KeywordText.text()
        self.from_date = self.FromDate.dateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.to_date = self.ToDate.dateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.order_by = self.OrderBySelect.currentIndex()
        self.run_sql(); 
        self.create_ui(False); 

    def update_like(self, comment):
        
        print ("self.name: ", self.name)
        print ("self.comments_display_likes[comment - 1]: ", self.comments_display_likes[comment - 1])
        if (self.name in self.comments_display_likes[comment - 1]): 
            # Remove like
            sql = f'''
DELETE FROM likes
WHERE student_id = {self.user_id} AND
        comment_id = {self.comments_display[comment - 1][3]}; 
        '''
            print (sql)
            database.cursor.execute(sql)
        
        else: 
            # add like
            sql = f'''
INSERT INTO likes (student_id, comment_id) VALUES ({self.user_id}, {self.comments_display[comment - 1][3]}); 
        '''
            print (sql)
            database.cursor.execute(sql)
        self.run_sql(); 
        self.create_ui(False); 

    def update_page(self, page):
        if (self.page <= 1 and page == -1): 
            return
        elif (self.page >= math.ceil(len(self.comments) * 1.0 / 3) and page == 1):
            return
        else: self.page += page
        self.run_sql(); 
        self.create_ui(False); 

    def update_ascend_descend(self, order): 
        if (order == "OrderByAscend"): 
            self.order_ascend_descend = 0
        else: 
            self.order_ascend_descend = 1
        self.run_sql(); 
        self.create_ui(False); 

    def post_comment(self): 

        sql = f'''
SELECT MAX(comment_id)
FROM Comments
    '''
        print (sql)
        database.cursor.execute(sql)
        max_comment_id = database.cursor.fetchall()
        print_sql(sql, max_comment_id)

        # os.system("clear")
        max_comment_id = max_comment_id[0][0]
        post_time = datetime.datetime.now()

        # print ("max_comment_id: ", max_comment_id)
        # print ("self.forum_id: ", self.forum_id)
        # print ("self.user_id: ", self.user_id)
        # print ("self.ForumPostText.text(): ", self.ForumPostText.text())
        # print ("post_time: ", post_time)

        sql = f'''
INSERT INTO Comments (comment_id, forum_id, student_id, content, post_time) VALUES 
({max_comment_id + 1}, {self.forum_id}, {self.user_id}, \"{self.ForumPostText.text()}\", \"{post_time}\"); 
        '''
        print (sql)
        database.cursor.execute(sql)

        self.run_sql(); 
        self.create_ui(False); 

    def run_sql(self):

        sql = f'''
SELECT name
FROM Student
WHERE student_id = {self.user_id}; 
        '''
        database.cursor.execute(sql)
        self.name = database.cursor.fetchall()[0]
        print_sql (sql, self.name)
        self.name = self.name[0]

        sql = f'''
SELECT student_id, name
FROM Student; 
        '''
        database.cursor.execute(sql)
        students = database.cursor.fetchall()
        print_sql (sql, students)

        students.remove((self.user_id, self.name))
        students_modified = []
        students_dictionary = {}

        students_dictionary[self.name] = 1
        for s in students:
            if (s[1] in students_dictionary): 
                students_dictionary[s[1]] += 1
            else: students_dictionary[s[1]] = 1
            if (students_dictionary[s[1]] == 1): 
                students_modified.append((s[0], s[1]), )
            else: 
                students_modified.append((s[0], f"{s[1]}({students_dictionary[s[1]]})"), )

        students_modified = sorted(students_modified)
        students_modified.insert(0, (self.user_id, self.name))
        students_modified.insert(0, (None, "ALL"))
        self.students = students_modified

        self.comments = []
        self.comments_likes = []


        sql = f'''
SELECT S.avatar, S.student_id, S.name, Com.comment_id, Com.content, Com.post_time, C.course_code, COUNT(*)
FROM Student S, Comments Com, Course C, Forums F, likes l
WHERE Com.student_id = S.student_id AND
        Com.forum_id = F.forum_id AND
        F.course_id = C.course_id AND
        l.comment_id = Com.comment_id AND 
        Com.post_time > \"{self.from_date}\" AND 
        Com.post_time < \"{self.to_date}\"
        '''
        if (self.student != 0):
            sql += f" AND\n        S.student_id = {self.students[self.student][0]}"
        if (self.keyword != ""):
            keywords = self.keyword.split(' ')
            sql += " AND (\n"
            for i in range (len(keywords)): 
                sql += f"            (Com.content LIKE '%{keywords[i]}%')"
                if (i != len(keywords) - 1): sql += " AND \n"
                else: sql += "\n        )\n"
        else: sql += "\n"
        sql += "GROUP BY S.avatar, S.student_id, S.name, Com.comment_id, Com.content, Com.post_time, C.course_code"
        order_by_list = ["Com.post_time", "COUNT(*)", "S.name", "C.course_code"]
        sql += f"\nORDER BY {order_by_list[self.order_by]}"
        if (self.order_ascend_descend == 1):
            sql += " DESC \n"; 
        else:
            sql += " \n";
        database.cursor.execute(sql)
        self.comments = database.cursor.fetchall()
        print_sql(sql, self.comments)


        # Manually left outer join
        # There is a bug, because the left outer join
        # generate None instead of Null values

        sql = '''
SELECT DISTINCT comment_id
FROM likes
        '''
        database.cursor.execute(sql)
        liked_comments = database.cursor.fetchall()
        print_sql(sql, liked_comments)


        sql = f'''
SELECT S.avatar, S.student_id, S.name, Com.comment_id, Com.content, Com.post_time, C.course_code
FROM Student S, Comments Com, Course C, Forums F, likes l
WHERE Com.student_id = S.student_id AND
        Com.forum_id = F.forum_id AND
        F.course_id = C.course_id AND
        Com.comment_id NOT IN (
SELECT DISTINCT comment_id
FROM likes
        ) AND 
        Com.post_time > \"{self.from_date}\" AND 
        Com.post_time < \"{self.to_date}\"
        '''
        if (self.student != 0):
            sql += f" AND\n        S.student_id = {self.students[self.student][0]}"
        if (self.keyword != ""):
            keywords = self.keyword.split(' ')
            sql += " AND (\n"
            for i in range (len(keywords)): 
                sql += f"            (Com.content LIKE '%{keywords[i]}%')"
                if (i != len(keywords) - 1): sql += " AND \n"
                else: sql += "\n        )\n"
        else: sql += "\n"
        sql += "GROUP BY S.avatar, S.student_id, S.name, Com.comment_id, Com.content, Com.post_time, C.course_code"
        order_by_list = ["Com.post_time", "COUNT(*)", "S.name", "C.course_code"]
        sql += f"\nORDER BY {order_by_list[self.order_by]}"
        if (self.order_ascend_descend == 1):
            sql += " DESC \n"; 
        else:
            sql += " \n";
        database.cursor.execute(sql)
        comments_nolike = database.cursor.fetchall()
        print_sql(sql, comments_nolike)
        for i in range (len(comments_nolike)): 
            result = list(comments_nolike[i])
            result.append(0)
            comments_nolike[i] = tuple(result)


        # Merge the results
        for i in comments_nolike: 
            self.comments.append(i)

        # Re-sort
        if (self.order_by == 0): 
            if (self.order_ascend_descend == 1):
                self.comments.sort(key = lambda x: x[5], reverse=True)
            else: 
                self.comments.sort(key = lambda x: x[5], reverse=False)
        elif (self.order_by == 1): 
            if (self.order_ascend_descend == 1):
                self.comments.sort(key = lambda x: x[7], reverse=True)
            else: 
                self.comments.sort(key = lambda x: x[7], reverse=False)
        elif (self.order_by == 2): 
            if (self.order_ascend_descend == 1):
                self.comments.sort(key = lambda x: x[2], reverse=True)
            else: 
                self.comments.sort(key = lambda x: x[2], reverse=False)
        elif (self.order_by == 3): 
            if (self.order_ascend_descend == 1):
                self.comments.sort(key = lambda x: x[6], reverse=True)
            else: 
                self.comments.sort(key = lambda x: x[6], reverse=False)


        # print (self.comments)

        for comment in range (len(self.comments)):

            sql = f'''
SELECT S.name
FROM Student S, Comments C, likes l
WHERE S.student_id = l.student_id AND
        l.comment_id = C.comment_id AND
        C.comment_id = \'{self.comments[comment][3]}\'
            '''

            database.cursor.execute(sql)
            likes = database.cursor.fetchall()
            print_sql (sql, likes)

            self.comments_likes.append(likes)

    def create_ui(self, set_time):

        # default autofill
        self.OrderBySelect.setCurrentIndex(self.order_by)
        self.StudentSelect.setCurrentIndex(self.student)
        self.KeywordText.setText(self.keyword)
        self.ForumPostText.setText(self.forum_post)

        if (set_time): 
            self.FromDate.setDateTime(self.from_date)
            self.ToDate.setDateTime(self.to_date)
        else: 
            # print("from date: ", self.from_date)
            # print("to date: ", self.to_date)
            pass

        self.StudentSelect.clear()
        self.StudentSelect.addItem (f"{self.students[0][1]}")
        self.StudentSelect.addItem (f"{self.students[1][1]} (me)")
        for i in range (2, len(self.students), 1):
            self.StudentSelect.addItem (f"{self.students[i][1]}")
        self.StudentSelect.setCurrentIndex(self.student)

        print ("total comments:", len(self.comments))
        if (len(self.comments) < self.page * 3): 
            self.comments_display = self.comments[3 * (self.page - 1): len(self.comments)]
            self.comments_display_likes = self.comments_likes[3 * (self.page - 1): len(self.comments)]
        else:
            self.comments_display = self.comments[3 * (self.page - 1): 3 * (self.page)]
            self.comments_display_likes = self.comments_likes[3 * (self.page - 1): 3 * (self.page)]
        # print ("self.comments:", self.comments)
        print ("self.comments_display:", self.comments_display)
        print ("self.comments_display_likes:", self.comments_display_likes)

        avatars = []
        names = []
        post_dates = []
        contents = []
        likes = []
        courses = []
        for i in range (len(self.comments_display)):
            avatars.append(self.comments_display[i][0])
            names.append(self.comments_display[i][2])
            post_dates.append(self.comments_display[i][5])
            contents.append(self.comments_display[i][4])
            courses.append(self.comments_display[i][6])
            likes.append(self.comments_display_likes[i])
        for i in range (len(likes)): 
            for j in range (len(likes[i])): 
                likes[i][j] = likes[i][j][0]
        
        # print ("avatars: ", avatars)
        # print ("names: ", names)
        # print ("post_dates: ", post_dates)
        # print ("contents: ", contents)
        # print ("likes: ", likes)
    
        # Main content
        if (len(self.comments_display) == 0): 
            self.NoCommentFound.setText ("No comments found! ")
        else: 
            self.NoCommentFound.setText ("")

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for i in range (1, 4, 1): 
            if (i - 1 < len(self.comments_display)): 
                style = ""
                style += "QPushButton {background: rgb(255, 255, 255); background-image : url(resources/"
                style += avatars[i - 1]; 
                style += "); background-repeat: no-repeat; background-position: center; border-radius: 50px; }"
                exec (f"self.Avatar{i}.setStyleSheet(\"{style}\")")
                exec (f"self.Avatar{i}Name.setText(\"{names[i - 1]}\")")
                day_post = post_dates[i - 1].day; month_post = months[post_dates[i - 1].month - 1]; year_post = post_dates[i - 1].year
                exec (f"self.PostDate{i}.setText(\"{day_post} {month_post} {year_post}\")")
                exec (f"self.Avatar{i}Comment.setText(\"{contents[i - 1]}\")")
                style = "QLabel{background-color: white; color: rgb(0, 0, 0); padding: 10px; font-style: oblique;}"

                exec (f"self.Avatar{i}Comment.setStyleSheet(\"{style}\")")
                exec (f"self.Avatar{i}Comment.setWordWrap(True)")
                if (len(likes[i - 1]) <= 1): 
                    exec (f"self.Comment{i}LikeLabel.setText(\"{len(likes[i - 1])} like\")")
                else: 
                    exec (f"self.Comment{i}LikeLabel.setText(\"{len(likes[i - 1])} likes\")")
                exec (f"self.Comment{i}Course.setText(\"{courses[i - 1]}\")")
                
                style_1 = ""
                style_1 += "QPushButton{background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"
                style_1 += "QPushButton:hover{background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"
                style_1 += "QPushButton:clicked{background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"
                style_2 = ""
                style_2 += "QPushButton{background: rgb(243, 169, 169); background-repeat: no-repeat; background-position: center;}"
                style_2 += "QPushButton:hover{background: rgb(212, 148, 148); background-repeat: no-repeat; background-position: center;}"
                style_2 += "QPushButton:clicked{background: rgb(182, 127, 127); background-repeat: no-repeat; background-position: center;}"
                # print ("user: ", self.name)
                # print ("liked_users: ", likes[i - 1])
                if (self.name in likes[i - 1]): 
                    exec (f"self.Comment{i}LikeButton.setStyleSheet(\"{style_2}\")")
                    exec (f"self.Comment{i}LikeButton.setText(\"Liked\")")
                else:
                    exec (f"self.Comment{i}LikeButton.setStyleSheet(\"{style_1}\")")
                    exec (f"self.Comment{i}LikeButton.setText(\"Like\")")
            else: 
                style = "QPushButton{background: rgb(255, 255, 255, 0); }"
                exec (f"self.Avatar{i}.setStyleSheet(\"{style}\")")
                exec (f"self.Avatar{i}Name.setText(\"\")")
                exec (f"self.PostDate{i}.setText(\"\")")
                exec (f"self.Avatar{i}Comment.setText(\"\")")
                style = "QLabel{background: rgb(255, 255, 255, 0); }"
                exec (f"self.Avatar{i}Comment.setStyleSheet(\"{style}\")")
                exec (f"self.Comment{i}LikeLabel.setText(\"\")")
                exec (f"self.Comment{i}LikeButton.setText(\"\")")
                style = "QPushButton{background: rgb(255, 255, 255, 0); }"
                exec (f"self.Comment{i}LikeButton.setStyleSheet(\"{style}\")")
                exec (f"self.Comment{i}LikeButton.setText(\"\")")
                exec (f"self.Comment{i}Course.setText(\"\")")

        # Ascend && Descend button
        style1 = ""; style2 = ""
        if (self.order_ascend_descend == 0): 
            style1 += "QPushButton {background: rgb(234, 234, 128); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:hover {background: rgb(205, 205, 112); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:clicked {background: rgb(186, 186, 96); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"; 
        else:
            style2 += "QPushButton {background: rgb(234, 234, 128); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:hover {background: rgb(205, 205, 112); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:clicked {background: rgb(186, 186, 96); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}";             
        self.OrderByAscend.setStyleSheet(style1)
        self.OrderByDescend.setStyleSheet(style2)

        # Previous && Next button
        style1 = ""; style2 = ""
        print ("total pages: ", math.ceil(len(self.comments) * 1.0 / 3))
        if (math.ceil(len(self.comments) * 1.0 / 3) <= 1): 
            style1 += "QPushButton {background: rgb(255, 255, 255, 0.3); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton {background: rgb(255, 255, 255, 0.3); background-repeat: no-repeat; background-position: center;}"; 
        elif (self.page == 1): 
            style1 += "QPushButton {background: rgb(255, 255, 255, 0.3); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"; 
        elif (self.page == math.ceil(len(self.comments) * 1.0 / 3)): 
            style2 += "QPushButton {background: rgb(255, 255, 255, 0.3); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"; 
        else: 
            style1 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"; 
        self.PreviousPageButton.setStyleSheet(style1)
        self.NextPageButton.setStyleSheet(style2)

        # page number
        if (math.ceil(len(self.comments) * 1.0 / 3) <= 1): 
            self.PageLabel.setText (f"Page {self.page} of 1")
        else: 
            self.PageLabel.setText (f"Page {self.page} of {math.ceil(len(self.comments) * 1.0 / 3)}")

class ExamPage(StackedWindow):

    def __init__(self, user_id, database):

        super(ExamPage, self).__init__()
        loadUi("Exam.ui", self)

        # Button listeners
        self.OrderByAscend.clicked.connect(lambda: self.update_ascend_descend("OrderByAscend"))
        self.OrderByDescend.clicked.connect(lambda: self.update_ascend_descend("OrderByDescend"))
        self.SearchButton.clicked.connect(lambda: self.update_search())
        self.PreviousPageButton.clicked.connect(lambda: self.update_page(-1))
        self.NextPageButton.clicked.connect(lambda: self.update_page(1))
        self.BackButton.clicked.connect(lambda: switch_to(TIMETABLE))
        self.HomeButton.clicked.connect(lambda: switch_to(HOME))

        self.user_id = user_id
        self.database = database

        self.keyword = ""
        self.order_by = 0
        self.order_ascend_descend = 0
        self.exams = []
        self.exams_display = []
        self.page = 1
        self.run_sql(); 
        self.create_ui()

    def update_page(self, page):
        if (self.page <= 1 and page == -1): 
            return
        elif (self.page >= math.ceil(len(self.exams) * 1.0 / 12) and page == 1):
            return
        else: self.page += page
        self.run_sql(); 
        self.create_ui(); 

    def update_ascend_descend(self, order): 
        if (order == "OrderByAscend"): 
            self.order_ascend_descend = 0
        else: 
            self.order_ascend_descend = 1
        self.run_sql(); 
        self.create_ui(); 
    
    def update_search (self):
        self.keyword = self.KeywordText.text()
        self.order_by = self.OrderBySelect.currentIndex()
        self.run_sql(); 
        self.create_ui(); 
        
    def run_sql(self):

        sql = f'''
SELECT S.name, C.course_code, C.course_title, E.exam_start_time, E.exam_end_time, E.venue, E.format
FROM Student S, Student_Course SC, Course C, Exams E 
WHERE S.student_id = SC.student_id AND 
        SC.course_id = C.course_id AND 
        C.course_id = E.course_id AND 
        S.student_id = {self.user_id}'''

        if (self.keyword != ""):
            keywords = self.keyword.split(' ')
            sql += " AND (\n"
            for i in range (len(keywords)): 
                sql += f"            (C.course_code LIKE '%{keywords[i]}%' OR C.course_title LIKE '%{keywords[i]}%' OR E.venue LIKE '%{keywords[i]}%' OR E.format LIKE '%{keywords[i]}%')"
                if (i != len(keywords) - 1): sql += " AND \n"
                else: sql += "\n        )\n"
        else: sql += "\n"
        
        order_by_list = ["E.exam_start_time", "C.course_code", "C.course_title", "E.venue", "E.format"]
        sql += f"ORDER BY {order_by_list[self.order_by]}"
        if (self.order_ascend_descend == 1):
            sql += " DESC; \n"; 
        else:
            sql += "; \n"; 

        database.cursor.execute(sql)
        self.exams = database.cursor.fetchall()
        print_sql (sql, self.exams)
    
    def create_ui(self):

        # default autofill
        self.OrderBySelect.setCurrentIndex(self.order_by)
        self.KeywordText.setText(self.keyword)

        # Ascend && Descend button
        style1 = ""; style2 = ""
        if (self.order_ascend_descend == 0): 
            style1 += "QPushButton {background: rgb(234, 234, 128); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:hover {background: rgb(205, 205, 112); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:clicked {background: rgb(186, 186, 96); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"; 
        else:
            style2 += "QPushButton {background: rgb(234, 234, 128); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:hover {background: rgb(205, 205, 112); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:clicked {background: rgb(186, 186, 96); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}";             
        self.OrderByAscend.setStyleSheet(style1)
        self.OrderByDescend.setStyleSheet(style2)

        # Previous && Next button
        style1 = ""; style2 = ""
        print ("total pages: ", math.ceil(len(self.exams) * 1.0 / 12))
        if (math.ceil(len(self.exams) * 1.0 / 12) <= 1): 
            style1 += "QPushButton {background: rgb(255, 255, 255, 0.3); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton {background: rgb(255, 255, 255, 0.3); background-repeat: no-repeat; background-position: center;}"; 
        elif (self.page == 1): 
            style1 += "QPushButton {background: rgb(255, 255, 255, 0.3); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"; 
        elif (self.page == math.ceil(len(self.exams) * 1.0 / 12)): 
            style2 += "QPushButton {background: rgb(255, 255, 255, 0.3); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"; 
        else: 
            style1 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style1 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton {background: rgb(255, 255, 255); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:hover {background: rgb(224, 224, 224); background-repeat: no-repeat; background-position: center;}"; 
            style2 += "QPushButton:clicked {background: rgb(192, 192, 192); background-repeat: no-repeat; background-position: center;}"; 
        self.PreviousPageButton.setStyleSheet(style1)
        self.NextPageButton.setStyleSheet(style2)

        # Page number
        if (math.ceil(len(self.exams) * 1.0 / 12) <= 1): 
            self.PageLabel.setText (f"Page {self.page} of 1")
        else: 
            self.PageLabel.setText (f"Page {self.page} of {math.ceil(len(self.exams) * 1.0 / 12)}")

        if (len(self.exams) < self.page * 12): 
            self.exams_display = self.exams[(self.page - 1) * 12:len(self.exams)]
        else: 
            self.exams_display = self.exams[(self.page - 1) * 12:(self.page) * 12]

        # Main content
        if (len(self.exams_display) == 0): 
            self.NoExamFound.setText ("No satisfied exams found! ")
        else: 
            self.NoExamFound.setText ("")

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for exam in range (12): 
            if (exam < len(self.exams_display)): 
                exam_0 = self.exams_display[exam]; 
                exec (f"self.Date{exam+1}Label.setText (f\"{months[exam_0[3].month - 1]} {exam_0[3].day}\")")
                hour_start = exam_0[3].hour; minute_start = exam_0[3].minute; apm_start = "am"
                if (hour_start >= 12): apm_start = "pm"
                if (hour_start > 12): hour_start -= 12
                hour_end = exam_0[4].hour; minute_end = exam_0[4].minute; apm_end = "am"
                if (hour_end >= 12): apm_end = "pm"
                if (hour_end > 12): hour_end -= 12
                exec (f"self.Time{exam+1}Label.setText (f\"{hour_start}.{minute_start}{apm_start} - {hour_end}.{minute_end}{apm_end}\")")
                exec (f"self.CourseCode{exam+1}Label.setText (\"{exam_0[1]}\")")
                exec (f"self.CourseTitle{exam+1}Label.setText (\"{exam_0[2]}\")")
                exec (f"self.Venue{exam+1}Label.setText (\"{exam_0[5]}\")")
                exec (f"self.Format{exam+1}Label.setText (\"{exam_0[6]}\")")
            else: 
                exec (f"self.Date{exam+1}Label.setText (f\"\")")
                exec (f"self.Time{exam+1}Label.setText (f\"\")")
                exec (f"self.CourseCode{exam+1}Label.setText (\"\")")
                exec (f"self.CourseTitle{exam+1}Label.setText (\"\")")
                exec (f"self.Venue{exam+1}Label.setText (\"\")")
                exec (f"self.Format{exam+1}Label.setText (\"\")")

class EmailPage(StackedWindow): 

    def __init__(self, user_id, class_id, database):

        super(EmailPage, self).__init__()
        loadUi("Email.ui", self)

        # basics
        self.user_id = user_id; 
        self.class_id = class_id; 
        self.name = ""
        self.email = ""
        self.database = database; 

        # ui placeholders
        self.course_info_text = ""
        self.classroom_text = ""
        self.zoom_link_text = ""
        self.message_text = ""
        self.material_text = ""
        self.email_text = ""
        self.student = 0
        self.students = []

        # sql results
        self.main_info = []
        self.materials = []
        self.messages = []

        self.run_sql(); 
        self.create_ui(); 

    def update_email(self):

        self.student = self.EmailStudentSelect.currentIndex()
        sql = f'''
SELECT email
FROM Student
WHERE student_id = {self.students[self.student][0]}
        '''
        database.cursor.execute(sql)
        self.email_text = database.cursor.fetchall()[0]
        print_sql (sql, self.email_text)
        self.email_text = self.email_text[0]
        self.EmailText.setText(self.email_text)
        self.SendEmailButton.setText("Send Email")

        self.run_sql(); 
        self.create_ui(); 

    def send_email(self):

        # Reference: https://zhuanlan.zhihu.com/p/89868804

        if (self.SendEmailButton.text() == "Send Email"): 

            import smtplib
            import email
            from email.mime.text import MIMEText
            from email.mime.image import MIMEImage
            from email.mime.multipart import MIMEMultipart
            from email.header import Header

            mail_host = "smtp.163.com"
            mail_sender = "COMP3278@163.com"
            mail_license = "VXJPSHBKJWNQMFTL"

            self.email_text = self.EmailText.text()
            mail_receivers = self.email_text

            mm = MIMEMultipart('related')
            subject_content = f"[Course Information] {self.course_info_text}"
            mm["From"] = "COMP3278<COMP3278@163.com>"

            i = self.email_text.index('@')
            mm["To"] = [f"{self.email_text[0:i]}<{self.email_text}>"]

            mm["Subject"] = Header(subject_content,'utf-8')

            body_content = ""

            body_content += "[Course Information] \n"
            body_content += self.course_info_text
            body_content += "\n\n"

            body_content += "[Classroom] \n"
            body_content += self.classroom_text
            body_content += "\n\n"

            body_content += "[Zoom Link] \n"
            body_content += self.zoom_link_text
            body_content += "\n\n"

            body_content += "[Messages] \n"
            body_content += self.message_text
            body_content += "\n\n"

            body_content += "[Materials] \n"
            body_content += self.material_text
            body_content += "\n\n"

            body_content += "Best regards, \n"
            body_content += "    COMP3278 Team\n"
            message_text = MIMEText(body_content, "plain", "utf-8")

            mm.attach(message_text)

            # smtp_server = smtplib.SMTP()
            # smtp_server.connect(mail_host, 25)  
            # smtp_server.set_debuglevel(1)
            # smtp_server.login(mail_sender, mail_license)

            # smtp_server = smtplib.SMTP_SSL('smtp.163.com', 465)
            # smtp_server.ehlo()
            # smtp_server.login("COMP3278", "COMP3278gp")

            try: 
                
                print ("0")
                print ("1")
                smtp_server = smtplib.SMTP()
                print ("2")
                # The connection here is timing out. 
                smtp_server.connect(mail_host, 25) 
                print ("3")
                smtp_server.login(mail_sender, mail_license)
                print ("4")
                print (f"Ready to send the email to {self.email_text}. ")
                smtp_server.sendmail(mail_sender, mail_receivers, mm.as_string())
                print ("5")
                smtp_server.quit()

                style_1 = ""
                style_1 += "QPushButton{background: rgb(243, 169, 169); background-repeat: no-repeat; background-position: center;}"
                style_1 += "QPushButton:hover{background: rgb(212, 148, 148); background-repeat: no-repeat; background-position: center;}"
                style_1 += "QPushButton:clicked{background: rgb(182, 127, 127); background-repeat: no-repeat; background-position: center;}"
                self.SendEmailButton.setStyleSheet(style_1)
                self.SendEmailButton.setText("Email Sent!")
            except Exception as ex: 
                print (ex)

    def run_sql(self):

        sql = f'''
SELECT name, email
FROM Student
WHERE student_id = {self.user_id}; 
        '''
        database.cursor.execute(sql)
        result = database.cursor.fetchall()[0]
        print_sql (sql, result)
        self.name = result[0]
        self.email = result[1]

        sql = f'''
SELECT student_id, name, email
FROM Student; 
        '''
        database.cursor.execute(sql)
        students = database.cursor.fetchall()
        print_sql (sql, students)

        students.remove((self.user_id, self.name, self.email))
        students_modified = []
        students_dictionary = {}

        students_dictionary[self.name] = 1
        for s in students:
            if (s[1] in students_dictionary): 
                students_dictionary[s[1]] += 1
            else: students_dictionary[s[1]] = 1
            if (students_dictionary[s[1]] == 1): 
                students_modified.append((s[0], s[1]), )
            else: 
                students_modified.append((s[0], f"{s[1]}({students_dictionary[s[1]]})"), )

        students_modified = sorted(students_modified)
        students_modified.insert(0, (self.user_id, self.name))
        self.students = students_modified


        sql = f'''
SELECT Cou.course_code, Cou.course_title, Cla.course_info, Cla.venue, Cla.zoom_link
FROM Course Cou, Class Cla
WHERE Cla.class_id = {self.class_id} AND 
        Cla.course_id = Cou.course_id; 
        '''
        database.cursor.execute(sql)
        self.main_info = database.cursor.fetchall()
        print_sql (sql, self.main_info)
        self.main_info = self.main_info[0]

        sql = f'''
SELECT Mes.content
FROM Messages Mes, Class Cla
WHERE Mes.class_id = Cla.class_id AND
        Cla.class_id = {self.class_id}; 
        '''
        database.cursor.execute(sql)
        self.messages = database.cursor.fetchall()
        print_sql (sql, self.messages)

        sql = f'''
SELECT Mat.material_name, Mat.material_link
FROM Materials Mat, Class Cla
WHERE Mat.class_id = Cla.class_id AND
        Cla.class_id = {self.class_id}; 
        '''
        database.cursor.execute(sql)
        self.materials = database.cursor.fetchall()
        print_sql (sql, self.materials)

    def create_ui(self):

        self.EmailStudentSelect.clear()
        self.EmailStudentSelect.addItem (f"{self.students[0][1]} (me)")
        for i in range (1, len(self.students), 1):
            self.EmailStudentSelect.addItem (f"{self.students[i][1]}")
        self.EmailStudentSelect.setCurrentIndex(self.student)

        self.course_info_text = f"{self.main_info[0]} {self.main_info[1]}"
        self.CourseContent.setText(self.course_info_text)
        
        self.classroom_text = f"{self.main_info[3]}"
        self.ClassroomContent.setText(self.classroom_text)

        self.zoom_link_text = f"{self.main_info[4]}"
        self.ZoomContent.setText(self.zoom_link_text)

        text = ""
        self.MessageContent.setWordWrap(True)
        for i in range (len(self.messages)): 
            text += self.messages[i][0]; 
            if (i != len(self.messages) - 1): 
                text += '\n'

        self.message_text = text
        self.MessageContent.setText(self.message_text)

        text = ""
        self.MaterialContent.setWordWrap(True)
        for i in range (len(self.materials)): 
            text += self.materials[i][0]; 
            text += " ("; 
            text += self.materials[i][1]; 
            text += ") "
            if (i != len(self.materials) - 1): 
                text += '\n'

        self.material_text = text
        self.MaterialContent.setText(self.material_text)

        self.ClassroomContent.setWordWrap(True)
        self.BackButton.clicked.connect(lambda: switch_to(5))
        self.HomeButton.clicked.connect(lambda: switch_to(0))
        self.EmailConfirm.clicked.connect(lambda: self.update_email())
        self.SendEmailButton.clicked.connect(lambda: self.send_email())

def switch_to(idx):
    cur_win = main_win.currentWidget()
    cur_win.deactivate()
    main_win.removeWidget(cur_win)
    main_win.addWidget(WINDOWS[idx])
    main_win.currentWidget().activate()

def leave():
    database.cursor.close()
    conn.close()
    exit(0)

if __name__ == "__main__":

    PORTAL = 0
    FACIALLOGIN = 1
    PWDLOGIN = 2
    HOME = 3
    PROFILE = 4
    ONECLASS = 5
    TIMETABLE = 6
    FORUM = 7
    EXAM = 8
    EMAIL = 9
    WIDTH = 1200
    HEIGHT = 800
    
    import db_setup
    database = db_setup.COMP3278_GP_db()
    app = QApplication(sys.argv)
    # WINDOWS = [PortalPage(), FacialLoginPage(), PwdLoginPage(),
    #           HomePage(user_id, database), ProfilePage(1, database), 
    #           OneClassPage(1, 3, database), TimetablePage(user_id),
    #           ForumPage(2, 5, 3, database), ExamPage(2, database), EmailPage(2, 5, database)]
    WINDOWS = [PortalPage(), FacialLoginPage(), PwdLoginPage(),
            HomePage(1, database), ProfilePage(1, database), 
            OneClassPage(1, 3, database), TimetablePage(1, database),
            ForumPage(1, 5, 3, database), ExamPage(1, database), EmailPage(1, 5, database)]

    main_win = QStackedWidget()
    main_win.setFixedWidth(WIDTH)
    main_win.setFixedHeight(HEIGHT)
    main_win.setWindowTitle('')

    # main_win.addWidget(WINDOWS[PORTAL])
    main_win.addWidget(WINDOWS[PORTAL])

    activity_records = []
    main_win.show()
    sys.exit(app.exec_())

