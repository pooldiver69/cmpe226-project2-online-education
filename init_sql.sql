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
        author_id MEDIUMINT NOT NULL, 
        primary key (c_id),
        foreign key (author_id) references 
            instructor(i_id) on delete cascade
    );

insert into auth values (1, "fake_instructor1@sjsu.edu", "1e4938be29e9cd78075cdaa75decc31a");
insert into auth values (2, "fake_instructor2@sjsu.edu", "1e4938be29e9cd78075cdaa75decc31a");
insert into auth values (3, "fake_instructor3@sjsu.edu", "1e4938be29e9cd78075cdaa75decc31a");

insert into instructor values (1, "fake instructor 1", 1);
insert into instructor values (2, "fake instructor 2", 2);
insert into instructor values (3, "fake instructor 3", 3);

insert into course values (1, "Python Programming", "Mock up course", "Programming", 1);
insert into course values (2, "SQL", "Mock up course", "Data Structure", 2);
insert into course values (3, "Data Engineering", "Mock up course", "Data Structure", 3);