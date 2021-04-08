CREATE TABLE `users` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255) unique not null,
  `password` varchar(255) not null,
  `full_name` varchar(255) not null,
  `email` varchar(255) unique not null,
  `phone_number` varchar(10) not null,
  `group_id` int not null,
  `extra_permissions` int
);

CREATE TABLE `groups` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) not null,
  `string_permissions` varchar(255) not null,
  `description` varchar(255) 
);

CREATE TABLE `permissions` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255) not null,
  `description` varchar(255)
);

ALTER TABLE `users` ADD FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`);
