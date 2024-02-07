
/* Reference: https://lucid.app/lucidchart/a1437aaf-2a11-4ae0-a2da-36595f9dc044/edit?invitationId=inv_1e5076ee-1b9c-43ff-bf35-6d088f7ec0ec&page=0_0# */

USE `COMP3278_GP`;

DELETE FROM Exams; 

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('1', '2022-12-14 14:30:00', '2022-12-14 17:30:00', '3', 'CPD-LG.07-10', 'One Cheatsheet');  

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('2', '2022-12-08 09:30:00', '2022-12-08 12:30:00', '4', 'LE4', 'One Cheatsheet'); 



INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('3', '2022-10-10 12:30:00', '2022-10-10 17:30:00', '3', 'MWT1', 'Open Book'); 

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('4', '2022-10-11 10:30:00', '2022-10-11 11:30:00', '3', 'MWT1', 'Closed Book'); 

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('5', '2022-10-05 09:30:00', '2022-10-05 10:30:00', '3', 'MWT1', 'One Cheatsheet'); 

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('6', '2022-10-06 14:30:00', '2022-10-06 15:30:00', '3', 'MWT2', 'Open Book'); 

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('7', '2022-10-12 16:30:00', '2022-10-12 18:30:00', '3', 'MWT2', 'Closed Book'); 

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('8', '2022-10-14 13:30:00', '2022-10-12 14:30:00', '3', 'MWT2', 'One Cheatsheet');

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('9', '2022-10-09 15:30:00', '2022-10-09 17:30:00', '3', 'MWT3', 'Open Book'); 

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('10', '2022-10-07 19:30:00', '2022-10-07 20:30:00', '3', 'MWT3', 'Closed Book'); 

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('11', '2022-10-13 20:30:00', '2022-10-13 21:30:00', '3', 'MWT3', 'One Cheatsheet');

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('12', '2022-10-09 15:30:00', '2022-10-09 17:30:00', '3', 'CPD-LG.08', 'Open Book'); 

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('13', '2022-10-16 19:30:00', '2022-10-16 20:30:00', '3', 'CPD-LG.09', 'Closed Book'); 

INSERT INTO Exams (exam_id, exam_start_time, exam_end_time, course_id, venue, format) VALUES ('14', '2022-10-08 20:30:00', '2022-10-08 21:30:00', '3', 'CPD-LG.10', 'One Cheatsheet');
