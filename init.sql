drop database nytimes;
create database nytimes;
use nytimes;

CREATE TABLE `article` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `url` tinytext UNIQUE NOT NULL,
  `title` tinytext,
  `r_date` tinytext,
  `img` tinytext,
  `txt_id` int,
  `topic_id` int,
  `meta_id` int
);

CREATE TABLE `topic` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `name` tinytext UNIQUE NOT NULL,
  `url` tinytext UNIQUE NOT NULL
);

CREATE TABLE `txt` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `summary` blob,
  `article_text` blob UNIQUE NOT NULL
);

CREATE TABLE `article_author` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `author_id` int,
  `article_id` int
);

CREATE TABLE `meta` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `url` varchar(1000),
  `section` varchar(1000),
  `subsection` varchar(1000),
  `abstract` varchar(1000)
);

CREATE TABLE `label` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `label_type` varchar(100),
  `label_content` varchar(1000)
);

CREATE TABLE `article_label` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `label_id` int,
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

ALTER TABLE `article` ADD FOREIGN KEY (`meta_id`) REFERENCES `meta` (`id`);

ALTER TABLE `article_author` ADD FOREIGN KEY (`article_id`) REFERENCES `article` (`id`);

ALTER TABLE `article_author` ADD FOREIGN KEY (`author_id`) REFERENCES `author` (`id`);

ALTER TABLE `article_link` ADD FOREIGN KEY (`article_id`) REFERENCES `article` (`id`);

ALTER TABLE `article_link` ADD FOREIGN KEY (`link_id`) REFERENCES `link` (`id`);

ALTER TABLE `article_label` ADD FOREIGN KEY (`article_id`) REFERENCES `article` (`id`);

ALTER TABLE `article_label` ADD FOREIGN KEY (`label_id`) REFERENCES `label` (`id`);
