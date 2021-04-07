DROP DATABASE bbc_scraper;
CREATE DATABASE bbc_scraper;
USE bbc_scraper;

CREATE TABLE `article` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `url` varchar(1000) UNIQUE NOT NULL,
  `title` blob,
  `r_date` tinytext,
  `img` tinytext,
  `txt_id` int,
  `author_id` int,
  `topic_id` int
);

CREATE TABLE `author` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(1000) UNIQUE NOT NULL,
  `title` tinytext
);

CREATE TABLE `topic` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(1000) UNIQUE NOT NULL,
  `url` varchar(1000) UNIQUE NOT NULL
);

CREATE TABLE `txt` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `summary` blob, 
  `article_text` longblob
);

CREATE TABLE `article_tag` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `tag_id` int,
  `article_id` int
);

CREATE TABLE `tag` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(1000) UNIQUE NOT NULL,
  `url` varchar(1000) UNIQUE NOT NULL
);

CREATE TABLE `article_link` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `article_id` int,
  `link_id` int
);

CREATE TABLE `link` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(1000), 
  `url` varchar(1000)
);

ALTER TABLE `article` ADD FOREIGN KEY (`author_id`) REFERENCES `author` (`id`);

ALTER TABLE `article` ADD FOREIGN KEY (`topic_id`) REFERENCES `topic` (`id`);

ALTER TABLE `article` ADD FOREIGN KEY (`txt_id`) REFERENCES `txt` (`id`);

ALTER TABLE `article_tag` ADD FOREIGN KEY (`article_id`) REFERENCES `article` (`id`);

ALTER TABLE `article_tag` ADD FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`);

ALTER TABLE `article_link` ADD FOREIGN KEY (`article_id`) REFERENCES `article` (`id`);

ALTER TABLE `article_link` ADD FOREIGN KEY (`link_id`) REFERENCES `link` (`id`);
