-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: brc.mysql.database.azure.com    Database: brc
-- ------------------------------------------------------
-- Server version	5.7.32-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `blood_request`
--

DROP TABLE IF EXISTS `blood_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_request` (
  `blood_request_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `blood_group_id` int(11) NOT NULL,
  `blood_qty_ml` decimal(10,0) NOT NULL,
  `is_approved` tinyint(4) NOT NULL DEFAULT '0',
  `donor_id` int(11) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`blood_request_id`),
  KEY `fh_idx` (`user_id`),
  KEY `fh_idx1` (`donor_id`),
  KEY `fh3_idx` (`blood_group_id`),
  KEY `fh_idx1sdsds` (`user_id`),
  KEY `fh3_idx2ewe` (`blood_group_id`),
  CONSTRAINT `fgff` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fh6545gfgf` FOREIGN KEY (`blood_group_id`) REFERENCES `blood_group` (`blood_group_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-05 16:38:16
