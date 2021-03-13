use mydb;
CREATE TABLE `article` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `url` int UNIQUE NOT NULL,
  `title` tinytext,
  `r_date` date,
  `img` tinytext,
  `txt_id` int,
  `author_id` int,
  `section_id` int
);

CREATE TABLE `author` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` tinytext UNIQUE NOT NULL,
  `title` tinytext
);

CREATE TABLE `section` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` tinytext UNIQUE NOT NULL,
  `url` tinytext UNIQUE NOT NULL
);

CREATE TABLE `txt` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `summary` text,
  `article_text` text
);

CREATE TABLE `article_label` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `label_id` int,
  `article_id` int
);

CREATE TABLE `label` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` tinytext UNIQUE NOT NULL,
  `url` tinytext UNIQUE NOT NULL
);

CREATE TABLE `article_link` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `article_id` int,
  `link_id` int
);

CREATE TABLE `link` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `url` tinytext
);

ALTER TABLE `article` ADD FOREIGN KEY (`author_id`) REFERENCES `author` (`id`);

ALTER TABLE `article` ADD FOREIGN KEY (`section_id`) REFERENCES `section` (`id`);

ALTER TABLE `article` ADD FOREIGN KEY (`txt_id`) REFERENCES `txt` (`id`);

ALTER TABLE `article_label` ADD FOREIGN KEY (`article_id`) REFERENCES `article` (`id`);

ALTER TABLE `article_label` ADD FOREIGN KEY (`label_id`) REFERENCES `label` (`id`);

ALTER TABLE `article_link` ADD FOREIGN KEY (`article_id`) REFERENCES `article` (`id`);

ALTER TABLE `article_link` ADD FOREIGN KEY (`link_id`) REFERENCES `link` (`id`);
