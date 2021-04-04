CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255),
  `password` varchar(255),
  `full_name` varchar(255),
  `email` varchar(255),
  `phone_number` varchar(10),
  `group_id` int,
  `extra_permissions` int
);

CREATE TABLE `groups` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `string_permissions` varchar(255),
  `description` varchar(255)
);

CREATE TABLE `permissions` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `description` varchar(255)
);

ALTER TABLE `users` ADD FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`);
