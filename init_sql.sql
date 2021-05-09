-- SJSU CMPE 226 Spring2021TEAM5
drop database if exists cmpe226_project2_online_education;
create database cmpe226_project2_online_education;
use cmpe226_project2_online_education;

create table auth
    (
        id MEDIUMINT NOT NULL AUTO_INCREMENT,
        email VARCHAR(255) NOT NULL UNIQUE,
        pwd VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
    );

create table student
	(
        s_id MEDIUMINT NOT NULL AUTO_INCREMENT, 
        s_name VARCHAR(50) NOT NULL,
        user_id MEDIUMINT NOT NULL,
        primary key (s_id),
        foreign key (user_id) references 
            auth(id) on delete cascade
    );

create table instructor
	(
        i_id MEDIUMINT NOT NULL AUTO_INCREMENT, 
        i_name VARCHAR(50) NOT NULL,
        user_id MEDIUMINT NOT NULL,
        primary key (i_id),
        foreign key (user_id) references 
            auth(id) on delete cascade
    );

create table course
	(
        c_id MEDIUMINT NOT NULL AUTO_INCREMENT, 
        c_name VARCHAR(50) NOT NULL,
        c_description VARCHAR(255) NOT NULL,
        subject VARCHAR(50) NOT NULL,
        price FLOAT(10) NOT NULL,
        author_id MEDIUMINT NOT NULL, 
        primary key (c_id),
        foreign key (author_id) references 
            instructor(i_id) on delete cascade
    );

create table content
	(
        episode_number MEDIUMINT NOT NULL AUTO_INCREMENT, 
        c_id MEDIUMINT NOT NULL, 
        title VARCHAR(50) NOT NULL,
        stored_loc VARCHAR(255) NOT NULL,
        con_description VARCHAR(255) NOT NULL,
        primary key (episode_number, c_id),
        foreign key (c_id) references 
            course(c_id) on delete cascade
    );

create table purchase
	(
        c_id MEDIUMINT NOT NULL, 
        s_id MEDIUMINT NOT NULL, 
        p_price FLOAT(10) NOT NULL,
        purchsed_time TIMESTAMP NOT NULL,
        primary key (c_id, s_id),
        foreign key (s_id) references student(s_id),
        foreign key (c_id) references course(c_id) 
    );

create table review
    (
        c_id MEDIUMINT NOT NULL, 
        s_id MEDIUMINT NOT NULL, 
        star INT(5) NOT NULL,
        r_message VARCHAR(255) NOT NULL,
        created_time TIMESTAMP NOT NULL,
        primary key (c_id, s_id),
        foreign key (s_id) references student(s_id),
        foreign key (c_id) references course(c_id) 
    );

create table question
    (
        q_id MEDIUMINT NOT NULL AUTO_INCREMENT, 
        c_id MEDIUMINT NOT NULL,
        s_id MEDIUMINT NOT NULL, 
        q_message VARCHAR(255) NOT NULL,
        q_created_time TIMESTAMP NOT NULL,
        resolved BOOLEAN NOT NULL,
        primary key (q_id),
        foreign key (c_id) references course(c_id) 
    );

create table answer
    (
        q_id MEDIUMINT NOT NULL, 
        i_id MEDIUMINT NOT NULL,
        a_message VARCHAR(255) NOT NULL,
        a_created_time TIMESTAMP NOT NULL,
        primary key (q_id),
        foreign key (q_id) references question(q_id) 
            on delete cascade
        
    );

insert into auth values (1, "fake_instructor1@sjsu.edu", "bd0dcd7fa592787af69927fc66cba2ec");
insert into auth values (2, "fake_instructor2@sjsu.edu", "bd0dcd7fa592787af69927fc66cba2ec");
insert into auth values (3, "fake_instructor3@sjsu.edu", "bd0dcd7fa592787af69927fc66cba2ec");
insert into auth values (4, "fake_student1@sjsu.edu", "bd0dcd7fa592787af69927fc66cba2ec");
insert into auth values (5, "fake_student2@sjsu.edu", "bd0dcd7fa592787af69927fc66cba2ec");

insert into instructor values (1, "fake instructor 1", 1);
insert into instructor values (2, "fake instructor 2", 2);
insert into instructor values (3, "fake instructor 3", 3);

insert into student values (1, "fake instructor 1", 1);
insert into student values (2, "fake instructor 2", 2);
insert into student values (3, "fake instructor 3", 3);
insert into student values (4, "fake student 1", 4);
insert into student values (5, "fake student 2", 5);

insert into course values (1, "Python Programming", "Mock up course", "Programming", 0, 1);
insert into course values (2, "SQL", "Mock up course", "Data Structure", 9.99, 2);
insert into course values (3, "Data Engineering", "Mock up course", "Data Structure", 14.99, 3);

insert into content values (1, 1, "Python 1", "video1.mp4", "Mock up content");
insert into content values (2, 1, "Python 2", "video2.mp4", "Mock up content");
insert into content values (3, 1, "Python 3", "video1.mp4","Mock up content");

insert into content values (1, 2, "SQL 1", "video1.mp4", "Mock up content");
insert into content values (2, 2, "SQL 2", "video2.mp4", "Mock up content");
insert into content values (3, 2, "SQL 3", "video1.mp4","Mock up content");

insert into content values (1, 3, "Data Engineering 1", "video1.mp4", "Mock up content");
insert into content values (2, 3, "Data Engineering 2", "video2.mp4", "Mock up content");


insert into purchase values (1, 4, 0,' 2021-05-08 01:54:53');


create view purchase_history_view AS
SELECT c.c_id, c.c_description AS c_des, c.c_name AS cname, c.subject AS sub,
i.i_name AS instr_name, p.purchsed_time , p.p_price AS pri, p.s_id AS stu_id
FROM course AS c, purchase AS p, instructor AS i
WHERE c.c_id = p.c_id AND i.i_id = c.author_id;


create view course_view AS
SELECT course.c_name AS courseName, course.c_description AS Description, course.subject AS subj, course.c_id,
instructor.i_name AS InstructorName, course.price AS coursePrice
FROM course, instructor
WHERE course.author_id = instructor.i_id;

select * from course_view;


create view course_detail AS
SELECT c.c_id, c.c_name, k.title
FROM course AS c, content AS k
WHERE c.c_id = k.c_id;




DELIMITER //
create procedure FreeCourse(IN courseID INT, OUT onSale VARCHAR(20))
BEGIN
   DECLARE currPrice FLOAT(10);

   select price into currPrice
   from course
   where c_id = courseID;

   IF currPrice = 0 THEN
       SET onSale = 'YES';
   ELSE
       SET onSale = 'NO';
   END IF;
END;
//
DELIMITER ;


call FreeCourse(1, @t);
call FreeCourse(2, @z);
call FreeCourse(3, @s);
Select @t;
Select @z;
Select @s;



DELIMITER //
create procedure addEpisode(IN lastEPISODE_ID INT, IN course_id INT, IN numberUpload INT)
BEGIN
   DECLARE EPISODE_ID INT;
   DECLARE inStr VARCHAR(20);
   DECLARE MAX_EPISODE INT;
   SET EPISODE_ID = lastEPISODE_ID + 1;
   SET inStr = '';
   SET MAX_EPISODE = lastEPISODE_ID + numberUpload;
   WHILE EPISODE_ID <= MAX_EPISODE DO
       IF course_id = 2 THEN
           SET inStr = CONCAT("SQL ",EPISODE_ID);
           insert into content values (EPISODE_ID, course_id, inStr, "video1.mp4","Mock up content");
       END IF;
       IF course_id = 1 THEN
           SET inStr = CONCAT("Python ",EPISODE_ID);
           insert into content values (EPISODE_ID, course_id, inStr, "video1.mp4","Mock up content");
       END IF;
       IF course_id = 3 THEN
           SET inStr = CONCAT("Data Engineering ",EPISODE_ID);
           insert into content values (EPISODE_ID, course_id, inStr, "video2.mp4","Mock up content");
       END IF;
       SET EPISODE_ID = EPISODE_ID + 1;
   END WHILE;
END;
//
DELIMITER //

call addEpisode(3, 2, 4);
call addEpisode(2, 3, 1);

