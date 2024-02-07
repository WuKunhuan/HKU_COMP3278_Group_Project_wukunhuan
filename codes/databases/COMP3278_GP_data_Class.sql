
/* Reference: https://lucid.app/lucidchart/a1437aaf-2a11-4ae0-a2da-36595f9dc044/edit?invitationId=inv_1e5076ee-1b9c-43ff-bf35-6d088f7ec0ec&page=0_0# */

/*

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

*/

USE `COMP3278_GP`;

DELETE FROM Class; 

INSERT INTO Class (course_id, class_id, zoom_link, course_info, week_day, start_time, end_time, venue, class_type) VALUES ('1', '1', 'https://hku.zoom.us/j/97433800177?pwd=T2hSWEdqWitDQ1dUUXJ4MGQ4OENJZz09#success', 'COMP3270 Artificial intelligence', '2', '2022-11-22 12:30:00', '2022-11-22 13:20:00', 'CYCP1', 'Tutorial');

INSERT INTO Class (course_id, class_id, zoom_link, course_info, week_day, start_time, end_time, venue, class_type) VALUES ('1', '2', 'https://hku.zoom.us/j/97433800177?pwd=T2hSWEdqWitDQ1dUUXJ4MGQ4OENJZz09#success', 'COMP3270 Artificial intelligence', '5', '2022-11-25 12:30:00', '2022-11-25 14:20:00', 'CYCP1', 'Lecture');

INSERT INTO Class (course_id, class_id, zoom_link, course_info, week_day, start_time, end_time, venue, class_type) VALUES ('2', '3', 'https://hku.zoom.us/j/94178262634?pwd=Q2pTa1BPYkpiQjBsRVVUQnlpU2pGZz09', 'CCGL9063 How to Make (Sense of) Money', '3', '2022-11-23 12:30:00', '2022-11-23 14:20:00', 'MWT1', 'Lecture');

INSERT INTO Class (course_id, class_id, zoom_link, course_info, week_day, start_time, end_time, venue, class_type) VALUES ('3', '4', 'https://hku.zoom.us/j/96226740999?pwd=ZER1UUdxSVVhQzNXbXFkUDd3WjRBdz09#success', 'COMP3278 Introduction to database management systems', '1', '2022-11-21 14:30:00', '2022-11-21 15:20:00', 'MWT2', 'Tutorial');

INSERT INTO Class (course_id, class_id, zoom_link, course_info, week_day, start_time, end_time, venue, class_type) VALUES ('3', '5', 'https://hku.zoom.us/j/96226740999?pwd=ZER1UUdxSVVhQzNXbXFkUDd3WjRBdz09#success', 'COMP3278 Introduction to database management systems', '4', '2022-11-24 13:30:00', '2022-11-24 15:20:00', 'MWT2', 'Lecture');

INSERT INTO Class (course_id, class_id, zoom_link, course_info, week_day, start_time, end_time, venue, class_type) VALUES ('4', '6', 'https://hku.zoom.us/j/91763757554?pwd=UE9DUTdrakNVTFhMVmF6OXpha2o1dz09#success', 'COMP3297 Software engineering', '2', '2022-11-22 09:30:00', '2022-11-22 10:20:00', 'CYPP2', 'Lecture');

INSERT INTO Class (course_id, class_id, zoom_link, course_info, week_day, start_time, end_time, venue, class_type) VALUES ('4', '7', 'https://hku.zoom.us/j/91763757554?pwd=UE9DUTdrakNVTFhMVmF6OXpha2o1dz09#success', 'COMP3297 Software engineering', '5', '2022-11-25 09:30:00', '2022-11-25 11:20:00', 'CYPP2', 'Lecture');

INSERT INTO Class (course_id, class_id, zoom_link, course_info, week_day, start_time, end_time, venue, class_type) VALUES ('5', '8', 'https://hku.zoom.us/j/94554995634?pwd=dVlFVHI2UWFqMXVDVnMwTXE1UHkrZz09#success', 'COMP3330 Interactive Mobile Application Design and Programming', '1', '2022-11-21 12:30:00', '2022-11-21 14:20:00', 'LE4', 'Lecture');

INSERT INTO Class (course_id, class_id, zoom_link, course_info, week_day, start_time, end_time, venue, class_type) VALUES ('5', '9', 'https://hku.zoom.us/j/94554995634?pwd=dVlFVHI2UWFqMXVDVnMwTXE1UHkrZz09#success', 'COMP3330 Interactive Mobile Application Design and Programming', '2', '2022-11-22 13:30:00', '2022-11-22 14:20:00', 'LE4', 'Tutorial');


INSERT INTO Class (course_id, class_id, zoom_link, course_info, start_time, end_time, week_day, venue, class_type) VALUES ('1', '10', 'https://hku.zoom.us/j/97433800177?pwd=T2hSWEdqWitDQ1dUUXJ4MGQ4OENJZz09#success', 'COMP3270 Artificial intelligence', '2022-11-08 10:30:00','2022-11-08 11:20:00', '1', 'CYCP1', 'Tutorial'); 

INSERT INTO Class (course_id, class_id, zoom_link, course_info, start_time, end_time, week_day, venue, class_type) VALUES ('1', '11', 'https://hku.zoom.us/j/97433800177?pwd=T2hSWEdqWitDQ1dUUXJ4MGQ4OENJZz09#success', 'COMP3270 Artificial intelligence', '2022-11-08 16:30:00','2022-11-08 17:20:00', '1', 'CYCP1', 'Tutorial'); 

INSERT INTO Class (course_id, class_id, zoom_link, course_info, start_time, end_time, week_day, venue, class_type) VALUES ('1', '12', 'https://hku.zoom.us/j/97433800177?pwd=T2hSWEdqWitDQ1dUUXJ4MGQ4OENJZz09#success', 'COMP3270 Artificial intelligence', '2022-11-09 10:30:00','2022-11-09 11:20:00', '2', 'CYCP1', 'Tutorial'); 

INSERT INTO Class (course_id, class_id, zoom_link, course_info, start_time, end_time, week_day, venue, class_type) VALUES ('2', '13', 'https://hku.zoom.us/j/94178262634?pwd=Q2pTa1BPYkpiQjBsRVVUQnlpU2pGZz09', 'CCGL9063 How to Make (Sense of) Money', '2022-11-19 20:30:00','2022-11-19 21:30:00', '1', 'MWT1', 'Lecture'); 

