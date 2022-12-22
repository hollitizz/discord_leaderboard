DROP TABLE IF EXISTS `leaderboard_msgs`;
CREATE TABLE `leaderboard_msgs` (
	`msg_id` TEXT
);

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
	`user_id` VARCHAR(30) NOT NULL UNIQUE,
	`is_displayed` BOOLEAN DEFAULT TRUE,
	PRIMARY KEY (`user_id`)
);

DROP TABLE IF EXISTS `accounts`;
CREATE TABLE `accounts` (
    `user_id` VARCHAR(30) NOT NULL,
	`summoner_name` TEXT NOT NULL,
	`tier` INT DEFAULT 0,
	`rank` INT DEFAULT 0,
	`lp` INT DEFAULT 0,
	`league_id` TEXT NOT NULL
);