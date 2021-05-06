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
        price FLOAT(10) NOT NULL,
        purchsed_time TIMESTAMP NOT NULL,
        primary key (c_id, s_id),
        foreign key (s_id) references student(s_id),
        foreign key (c_id) references course(c_id) 
    );

insert into auth values (1, "fake_instructor1@sjsu.edu", "1e4938be29e9cd78075cdaa75decc31a");
insert into auth values (2, "fake_instructor2@sjsu.edu", "1e4938be29e9cd78075cdaa75decc31a");
insert into auth values (3, "fake_instructor3@sjsu.edu", "1e4938be29e9cd78075cdaa75decc31a");

insert into instructor values (1, "fake instructor 1", 1);
insert into instructor values (2, "fake instructor 2", 2);
insert into instructor values (3, "fake instructor 3", 3);

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