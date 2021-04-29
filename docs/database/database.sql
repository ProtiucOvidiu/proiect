Drop table groups_perm_relation;
Drop table user_groups_relation;
Drop table permissions;
Drop table groups;
Drop table users;

CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255),
  `password` varchar(255),
  `full_name` varchar(255),
  `email` varchar(255),
  `phone_number` int(10)
);

CREATE TABLE `groups` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `description` varchar(255)
);

CREATE TABLE `permissions` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `description` varchar(255)
);

CREATE TABLE `user_groups_relation` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `user_id` int,
  `group_id_1` int,
  `group_id_2` int,
  `group_id_3` int
);

CREATE TABLE `groups_perm_relation` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `group_id` int,
  `perm_id_1` int,
  `perm_id_2` int,
  `perm_id_3` int
);

ALTER TABLE `user_groups_relation` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `user_groups_relation` ADD FOREIGN KEY (`group_id_1`) REFERENCES `groups` (`id`);

ALTER TABLE `user_groups_relation` ADD FOREIGN KEY (`group_id_2`) REFERENCES `groups` (`id`);

ALTER TABLE `user_groups_relation` ADD FOREIGN KEY (`group_id_3`) REFERENCES `groups` (`id`);

ALTER TABLE `groups_perm_relation` ADD FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`);

ALTER TABLE `groups_perm_relation` ADD FOREIGN KEY (`perm_id_1`) REFERENCES `permissions` (`id`);

ALTER TABLE `groups_perm_relation` ADD FOREIGN KEY (`perm_id_2`) REFERENCES `permissions` (`id`);

ALTER TABLE `groups_perm_relation` ADD FOREIGN KEY (`perm_id_3`) REFERENCES `permissions` (`id`);
