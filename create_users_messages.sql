create table users (
	id int primary key auto_increment,
	display_name varchar(100) not null,
	email varchar(255) not null,
	password_hash varchar(40) not null,
	address varchar(255),
	lat decimal(10,6),
	long decimal(10,6),
	listen_radius_miles decimal(5,3),
	created_at datetime not null,
	modified_at datetime not null
);

create table messages (
	id int primary key auto_increment,
	original_msg_id int, -- null for original
	author_id int not null,
	subject varchar(255),
	body text,
	created_at datetime not null,
	modified_at datetime not null
);
