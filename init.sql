-- MySQL Script generated by MySQL Workbench
-- Sun Mar  7 13:02:28 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Articles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Articles` (
  `idArticles` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `title` VARCHAR(45) NULL,
  `date` DATETIME NULL,
  `text` LONGTEXT NULL,
  `image` VARCHAR(200) NULL,
  `url` VARCHAR(200) NULL,
  `topic` VARCHAR(45) NULL,
  `subtopic` VARCHAR(45) NULL,
  PRIMARY KEY (`idArticles`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
