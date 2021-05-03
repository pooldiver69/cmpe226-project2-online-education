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
        s_name VARCHAR(20) NOT NULL,
        user_id MEDIUMINT NOT NULL,
        primary key (s_id),
        foreign key (user_id) references 
            auth(id) on delete cascade
    )