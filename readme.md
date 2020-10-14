# Readme


## Create User Table
CREATE TABLE `users`(
 `user_id` int NOT NULL AUTO_INCREMENT,
 `name` varchar(128) NOT NULL,
 `phone` varchar(11) NULL,
 `address` varchar(512),
 PRIMARY KEY(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
