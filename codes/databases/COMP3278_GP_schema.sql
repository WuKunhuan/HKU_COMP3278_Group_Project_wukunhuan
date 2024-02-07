
/* Reference: https://lucid.app/lucidchart/a1437aaf-2a11-4ae0-a2da-36595f9dc044/edit?invitationId=inv_1e5076ee-1b9c-43ff-bf35-6d088f7ec0ec&page=0_0# */

DROP DATABASE IF EXISTS `COMP3278_GP`;
CREATE DATABASE `COMP3278_GP`;
USE `COMP3278_GP`;

CREATE TABLE Student(
    student_id INT NOT NULL PRIMARY KEY,
    UID VARCHAR(10) NOT NULL,
    password VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    welcome TEXT,
    email VARCHAR(30) NOT NULL, 
    avatar VARCHAR(100) NOT NULL
);

CREATE TABLE LoginHistory (
    student_id INT NOT NULL,
    history_id INT NOT NULL,
    login_time DATETIME NOT NULL,
    logout_time DATETIME NOT NULL,
    login_duration INT NOT NULL,
    PRIMARY KEY (student_id, history_id),
    FOREIGN KEY (student_id) REFERENCES Student (student_id)
);

CREATE TABLE Course (
    course_id INT NOT NULL PRIMARY KEY, 
    course_code VARCHAR(20) NOT NULL, 
    course_title VARCHAR(100) NOT NULL
); 

CREATE TABLE Student_Course (
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Student (student_id),
    FOREIGN KEY (course_id) REFERENCES Course (course_id)
);

CREATE TABLE Class (
    course_id INT NOT NULL, 
    class_id INT NOT NULL PRIMARY KEY, 
    zoom_link VARCHAR(100) NOT NULL, 
    course_info TEXT, 
    week_day VARCHAR(10) NOT NULL, 
    start_time DATETIME NOT NULL, 
    end_time DATETIME NOT NULL, 
    venue VARCHAR(100) NOT NULL, 
    class_type VARCHAR(50) NOT NULL, 
    FOREIGN KEY (course_id) REFERENCES Course (course_id)
);

CREATE TABLE Exams (
    exam_id INT NOT NULL PRIMARY KEY,
    exam_start_time DATETIME NOT NULL,
    exam_end_time DATETIME NOT NULL,
    course_id INT NOT NULL,
    venue VARCHAR(50) NOT NULL,
    format VARCHAR(50) NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Course (course_id)
);

CREATE TABLE Materials (
    class_id INT NOT NULL,
    material_id INT NOT NULL,
    material_name VARCHAR(100) NOT NULL, 
    material_link TEXT NOT NULL, 
    PRIMARY KEY (class_id, material_id), 
    FOREIGN KEY (class_id) REFERENCES Class (class_id)
);

CREATE TABLE Messages (
    class_id INT NOT NULL,
    message_id INT NOT NULL,
    content TEXT NOT NULL, 
    PRIMARY KEY (class_id, message_id), 
    FOREIGN KEY (class_id) REFERENCES Class (class_id)
);

CREATE TABLE Forums (
    forum_id INT NOT NULL PRIMARY KEY,
    course_id INT NOT NULL,
    forum_info VARCHAR(1000) NOT NULL, 
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

CREATE TABLE Comments (
    comment_id INT NOT NULL, 
    forum_id INT NOT NULL,
    content VARCHAR(1000) NOT NULL, 
    student_id INT NOT NULL,
    post_time DATETIME NOT NULL,
    PRIMARY KEY (comment_id, forum_id), 
    FOREIGN KEY (forum_id) REFERENCES Forums (forum_id), 
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);

CREATE TABLE likes (
    student_id INT NOT NULL, 
    comment_id INT NOT NULL, 
    PRIMARY KEY (comment_id, student_id), 
    FOREIGN KEY (comment_id) REFERENCES Comments (comment_id), 
    FOREIGN KEY (student_id) REFERENCES Student (student_id)
);


