create database sprint;
use  sprint;
create table users(
id int auto_increment primary key,
username varchar(100) unique not null,
email varchar(100) unique not null,
password_hash varchar(255) not null
);
show tables;
describe users;
select * from users;