drop table if exists users;
create table users(
	id integer primary key autoincrement,
	username text not null,
	email text not null,
	password text not null
);

drop table if exists ideas;
create table ideas(
	id integer primary key autoincrement,
	idea text not null,
	brief text not null,
	description text not null,
	username text not null,
	status integer not null
);
