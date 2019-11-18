DROP DATABASE IF EXISTS `gatorbarter`;

CREATE DATABASE `gatorbarter`;
USE `gatorbarter`;

CREATE TABLE `user` (
	`u_id` bigint NOT NULL AUTO_INCREMENT,
	`u_email` varchar(128) NOT NULL,
	`u_pass` TEXT(256) NOT NULL,
	`u_is_admin` int NOT NULL DEFAULT '0',
	`u_created_ts` TIMESTAMP NULL DEFAULT NULL,
	`u_updated_ts` TIMESTAMP NULL DEFAULT NULL,
	`u_fname` varchar(128) NOT NULL,
	`u_lname` varchar(128) NOT NULL,
	`u_status` int NOT NULL DEFAULT '1',
	PRIMARY KEY (`u_id`)
);

CREATE TABLE `category` (
	`c_id` bigint NOT NULL AUTO_INCREMENT,
	`c_name` varchar(128) NOT NULL,
	`c_status` int NOT NULL,
	PRIMARY KEY (`c_id`)
);

CREATE TABLE `item` (
	`i_id` bigint NOT NULL AUTO_INCREMENT,
	`i_title` varchar(256) NOT NULL,
	`i_desc` TEXT,
	`i_price` double NOT NULL DEFAULT '0',
	`i_is_tradable` int NOT NULL DEFAULT '0',
	`i_u_id` bigint NOT NULL,
	`i_created_ts` TIMESTAMP NULL DEFAULT NULL,
	`i_updated_ts` TIMESTAMP NULL DEFAULT NULL,
	`i_sold_ts` TIMESTAMP NULL DEFAULT NULL,
	`i_status` int NOT NULL DEFAULT '1',
	`i_c_id` bigint NOT NULL DEFAULT '0',
	PRIMARY KEY (`i_id`)
);

CREATE TABLE `item_image` (
	`ii_id` bigint NOT NULL AUTO_INCREMENT,
	`ii_image` blob,
	`ii_url` TEXT,
	`ii_i_id` bigint NOT NULL,
	`ii_status` int NOT NULL DEFAULT '1',
	PRIMARY KEY (`ii_id`)
);

CREATE TABLE `message` (
	`m_id` bigint NOT NULL AUTO_INCREMENT,
	`m_text` TEXT,
	`m_sender_id` bigint NOT NULL,
	`m_receiver_id` bigint NOT NULL,
	`m_item_id` bigint NOT NULL,
	`m_sent_ts` TIMESTAMP NULL DEFAULT NULL,
	PRIMARY KEY (`m_id`)
);


INSERT INTO `user`(u_email, u_pass, u_fname,  u_lname, u_is_admin ) VALUES ("jsmith@mail.sfsu.edu", "$5$rounds=535000$nuXafy8TPvKtl4Vz$kcAMJ5u/WgzQzl4fRqUMecwm3gEFr0GyM7GBZe/Mlo4","Joe", "Smith", 0);
INSERT INTO `user`(u_email, u_pass, u_fname,  u_lname, u_is_admin ) VALUES ("jstevens@mail.sfsu.edu", "$5$rounds=535000$8LT7xqCFxQLiFJpm$lPXqv6/NFGyQ..ICUwA.lhi3vibEC/XLIoKOY/wkOM8","Jane", "Stevens", 0);
INSERT INTO `user`(u_email, u_pass, u_fname,  u_lname, u_is_admin ) VALUES ("ealderson@mail.sfsu.edu", "$5$rounds=535000$6vzQgodnzXsTn/Bw$ZmM6r8CJql6A6GWZ4LGaOquF5qYsxA76Lhlb2y8ICkC","Elliot", "Alderson", 1);
INSERT INTO `user`(u_email, u_pass, u_fname,  u_lname, u_is_admin ) VALUES ("jhenry@mail.sfsu.edu", "$5$rounds=535000$TyeHSqrmIQ1LZdsU$uObTUjAFzRXjJBZ9q6pbizU/XRPzCxkoAoqWGsc885A","Jack", "Henry", 0);
INSERT INTO `user`(u_email, u_pass, u_fname,  u_lname, u_is_admin ) VALUES ("sadams@mail.sfsu.edu", "$5$rounds=535000$kx8rJDsweerxoAos$9wg3wB8hcabQQDLU70Mc5w28w0I2l3Fi3EHNEgrJUA8","Sam", "Adams", 0);
INSERT INTO `user`(u_email, u_pass, u_fname,  u_lname, u_is_admin ) VALUES ("rhendricks@mail.sfsu.edu", "$5$rounds=535000$TbmxAKoHrnHX9/pt$fzowOSWjtlxqZI9gFm4ESBMfmbl6iD37197rp.0lQ58","Richard", "Hendricks", 1);

INSERT INTO `category`(c_name, c_status ) VALUES ("Electronic",1);
INSERT INTO `category`(c_name, c_status ) VALUES ("Furniture",1);
INSERT INTO `category`(c_name, c_status ) VALUES ("Other",1);

INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id, i_status ) VALUES ("Computer Keyboard Title", "Computer Keyboard Description Electronic",9.99, 1, 1, 0 );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id, i_created_ts ) VALUES ("Computer Monitor Title", "Computer Monitor Item Description Electronic",9.99, 1, 1, "2019-11-13 19:13:30" );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id) VALUES ("Computer Mouse Title", "Computer Mouse Description Electronic",9.99, 1, 1 );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id, i_created_ts ) VALUES ("Laptop Title", "Laptop Description Electronic",9.99, 1, 1, "2019-11-13 19:15:30" );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id ) VALUES ("Network Switch Title", "Network Switch Description Electronic",9.99, 1, 1 );

INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id, i_status ) VALUES ("Black Chair Title", "Black Chair Description Furniture",9.99, 1, 2, 0 );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id, i_created_ts ) VALUES ("Black Couch Title", "Black Couch Description Furniture",9.99, 1, 2, "2019-11-13 19:16:30" );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id ) VALUES ("Night Stand Title", "Night Stand Description Furniture",9.99, 1, 2 );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id, i_created_ts ) VALUES ("Orange Couch Title", "Orange Couch Description Furniture",9.99, 1, 2, "2019-11-13 19:11:30" );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id ) VALUES ("Yellow Chair Title", "Yellow Chair Description Furniture",9.99, 1, 2 );


INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id, i_status ) VALUES ("Books Title", "Books Description Other",9.99, 1, 3, 0 );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id ) VALUES ("Cactus Title", "Cactus Description Other",9.99, 1, 3 );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id, i_created_ts ) VALUES ("Globe Title", "Globe Description Other",9.99, 1, 3, "2019-11-13 20:10:30" );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id ) VALUES ("Pink Rose Title", "Pink Rose Description Other",9.99, 1, 3 );
INSERT INTO `item`(i_title, i_desc, i_price,  i_u_id, i_c_id ) VALUES ("Yellow Coffee Cup Title", "Yellow Coffee Cup Description Other",9.99, 1, 3 );

INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Electronic/ComputerKeyboard_medium.jpg", 1);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Electronic/ComputerMonitor_medium.jpg", 2);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Electronic/ComputerMouse_medium.jpg", 3);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Electronic/Laptop_medium.jpg", 4);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Electronic/NetworkSwitch_medium.jpg", 5);

INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Furniture/BlackChair_medium.jpg", 6);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Furniture/BlackCouch_medium.jpg", 7);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Furniture/NightStand_medium.jpg", 8);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Furniture/OrangeCouch_medium.jpg", 9);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Furniture/YellowChair_medium.jpg", 10);

INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Other/Books_medium.jpg", 11);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Other/Cactus_medium.jpg", 12);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Other/Globe_medium.jpeg", 13);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Other/PinkRose_medium.jpg", 14);
INSERT INTO `item_image`(ii_url, ii_i_id ) VALUES ("/static/images/Other/YellowCoffeeCup_medium.jpg", 15);

INSERT INTO `message`(m_text, m_sender_id, m_receiver_id, m_item_id, m_sent_ts  ) VALUES ("Hello, I am interested in the Black Couch\n Please reach out to me.\n- Jane Stevens", 2, 1, 7, "2019-11-14 12:16:30");
