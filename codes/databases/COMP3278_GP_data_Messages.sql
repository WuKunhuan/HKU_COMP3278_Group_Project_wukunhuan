
/* Reference: https://lucid.app/lucidchart/a1437aaf-2a11-4ae0-a2da-36595f9dc044/edit?invitationId=inv_1e5076ee-1b9c-43ff-bf35-6d088f7ec0ec&page=0_0# */

/*

CREATE TABLE Messages (
    class_id INT NOT NULL,
    message_id INT NOT NULL,
    content TEXT NOT NULL, 
    PRIMARY KEY (class_id, message_id), 
    FOREIGN KEY (class_id) REFERENCES Class (class_id)
);

*/

USE `COMP3278_GP`;

DELETE FROM Messages; 

INSERT INTO Messages (class_id, message_id, content) VALUES (2, 1, 'Welcome to Artificial Intelligence'); 

INSERT INTO Messages (class_id, message_id, content) VALUES (2, 2, 'I am your lecturer, Dirk. '); 

INSERT INTO Messages (class_id, message_id, content) VALUES (1, 1, 'This is AI\'s tutorial. '); 

INSERT INTO Messages (class_id, message_id, content) VALUES (5, 1, 'Welcome back to DBMS'); 

INSERT INTO Messages (class_id, message_id, content) VALUES (5, 2, 'I am your lecturer, Ping. '); 

