CREATE TABLE IF NOT EXISTS `sbl` (
  `sbl_id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `sbl_db` VARCHAR(100) NOT NULL,
  `sbl_domain` VARCHAR(255),
  `sbl_url` TEXT NOT NULL,
  `sbl_global` TINYINT(1) NOT NULL DEFAULT FALSE,
  `sbl_timestamp` VARCHAR(20)
);