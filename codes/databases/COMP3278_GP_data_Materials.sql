
/* Reference: https://lucid.app/lucidchart/a1437aaf-2a11-4ae0-a2da-36595f9dc044/edit?invitationId=inv_1e5076ee-1b9c-43ff-bf35-6d088f7ec0ec&page=0_0# */


/*

CREATE TABLE Materials (
    class_id INT NOT NULL,
    material_id INT NOT NULL,
    material_name VARCHAR(100) NOT NULL, 
    material_link TEXT NOT NULL, 
    PRIMARY KEY (class_id, material_id), 
    FOREIGN KEY (class_id) REFERENCES Class (class_id)
);

*/


USE `COMP3278_GP`;

DELETE FROM Materials; 

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('1', '1', 'Tutorial Slide', 'https://docs.google.com/presentation/d/1bWCKHpZW4kisv0NzPcP8RBhVhTke6GoX/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('2', '1', 'Lecture Slide', 'https://docs.google.com/presentation/d/11i9LwJX_QuYV2iPjxLu5JTfeumtOVplP/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('3', '1', 'Lecture Slide 1', 'https://docs.google.com/presentation/d/11i9LwJX_QuYV2iPjxLu5JTfeumtOVplP/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('3', '2', 'Lecture Slide 2', 'https://docs.google.com/presentation/d/11i9LwJX_QuYV2iPjxLu5JTfeumtOVplP/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('4', '1', 'Tutorial Slide', 'https://docs.google.com/presentation/d/1bWCKHpZW4kisv0NzPcP8RBhVhTke6GoX/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('5', '1', 'Lecture Slide 1', 'https://docs.google.com/presentation/d/11i9LwJX_QuYV2iPjxLu5JTfeumtOVplP/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('5', '2', 'Lecture Slide 2', 'https://docs.google.com/presentation/d/11i9LwJX_QuYV2iPjxLu5JTfeumtOVplP/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('6', '1', 'Lecture Slide', 'https://docs.google.com/presentation/d/11i9LwJX_QuYV2iPjxLu5JTfeumtOVplP/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('7', '1', 'Lecture Slide', 'https://docs.google.com/presentation/d/11i9LwJX_QuYV2iPjxLu5JTfeumtOVplP/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('8', '1', 'Lecture Slide', 'https://docs.google.com/presentation/d/11i9LwJX_QuYV2iPjxLu5JTfeumtOVplP/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');

INSERT INTO Materials (class_id, material_id, material_name, material_link) VALUES ('9', '1', 'Tutorial Slide', 'https://docs.google.com/presentation/d/1bWCKHpZW4kisv0NzPcP8RBhVhTke6GoX/edit?usp=sharing&ouid=114100705181186664487&rtpof=true&sd=true');
