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



