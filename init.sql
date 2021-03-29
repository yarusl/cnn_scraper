DROP DATABASE nytimes;
CREATE DATABASE nytimes;
use nytimes;

CREATE TABLE `article` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `url` tinytext UNIQUE NOT NULL,
  `title` tinytext,
  `r_date` tinytext,
  `img` tinytext,
  `txt_id` int,
  `topic_id` int
);

CREATE TABLE `topic` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` tinytext UNIQUE NOT NULL,
  `url` tinytext UNIQUE NOT NULL
);

CREATE TABLE `txt` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `summary` text,
  `article_text` text UNIQUE NOT NULL
);

CREATE TABLE `article_author` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `author_id` int,
  `article_id` int
);

CREATE TABLE `author` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` tinytext UNIQUE NOT NULL
);

CREATE TABLE `article_link` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `article_id` int,
  `link_id` int
);

CREATE TABLE `link` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` tinytext,
  `url` tinytext
);

ALTER TABLE `article` ADD FOREIGN KEY (`topic_id`) REFERENCES `topic` (`id`);

ALTER TABLE `article` ADD FOREIGN KEY (`txt_id`) REFERENCES `txt` (`id`);

ALTER TABLE `article_author` ADD FOREIGN KEY (`article_id`) REFERENCES `article` (`id`);

ALTER TABLE `article_author` ADD FOREIGN KEY (`author_id`) REFERENCES `author` (`id`);

ALTER TABLE `article_link` ADD FOREIGN KEY (`article_id`) REFERENCES `article` (`id`);

ALTER TABLE `article_link` ADD FOREIGN KEY (`link_id`) REFERENCES `link` (`id`);
