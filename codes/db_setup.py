
import os, time, datetime, pickle, sys, cv2, math, sqlite3
import mysql.connector


class COMP3278_GP_db: 

    def __init__(self):

        os.system("clear")
        self.conn = mysql.connector.connect(host="localhost", user="root_0", passwd="123456")
        self.cursor = self.conn.cursor()

        all_database_files = [
            "databases/COMP3278_GP_schema.sql", 
            "databases/COMP3278_GP_data_Student.sql", 
            "databases/COMP3278_GP_data_LoginHistory.sql", 
            "databases/COMP3278_GP_data_Course.sql", 
            "databases/COMP3278_GP_data_Student_Course.sql", 
            "databases/COMP3278_GP_data_Class.sql", 
            "databases/COMP3278_GP_data_Exams.sql", 
            "databases/COMP3278_GP_data_Materials.sql", 
            "databases/COMP3278_GP_data_Messages.sql", 
            "databases/COMP3278_GP_data_Forums.sql", 
            "databases/COMP3278_GP_data_Comments.sql", 
            "databases/COMP3278_GP_data_likes.sql"
        ]

        # Compile database files. 
        for file in all_database_files:
            # print ("\n")
            # print (f"File: {file}")
            file_read = open(file, "r")

            sql = ""; status = "normal"; 
            space = 0; comment = ""
            for line in file_read.readlines():
                for char in line: 
                    if (status == "escape"):
                        status = "normal"
                        space = 0
                        comment = ""
                        if (char == "("):
                            space = 2; 
                        sql += char
                        pass
                    if (char == ";" and status == "normal"): 
                        status = "execute"
                        print (f"[sql] {sql}")
                        self.cursor.execute (sql)
                        sql = ""
                    elif (char == " " or char == '\n'): 
                        if (status == "normal"): 
                            space += 1; 
                            if (space < 2): 
                                sql += " "
                        pass
                    elif (char == "/"): 
                        if (comment == "*" and status == "comment"):
                            status = "normal"
                        else: 
                            comment = "/"
                    elif (char == "*"): 
                        if (comment == "/" and status == "normal"):
                            status = "comment"
                        else: 
                            comment = "*"

                    else: 
                        if (char == "\\"):
                            if (status == "normal"):
                                status = "escape"
                        if (status == "execute"): 
                            status = "normal"
                        if (status == "normal"): 
                            space = 0
                            comment = ""
                            if (char == "("):
                                space = 2; 
                            sql += char
                            
            file_read.close()

