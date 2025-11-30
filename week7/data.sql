-- MySQL dump 10.13  Distrib 8.0.35, for Win64 (x86_64)
--
-- Host: localhost    Database: website
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `follower_count` int unsigned NOT NULL DEFAULT '0',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,'test2','test@test.com','test',0,'2025-11-16 00:13:52'),(2,'member01','member01@wehelp.tw','wehelp',0,'2025-11-16 00:13:54'),(3,'member02','member02@wehelp.tw','wehelp',0,'2025-11-16 00:13:54'),(4,'member03','member03@wehelp.tw','wehelp',0,'2025-11-16 00:13:54'),(5,'member04','member04@wehelp.tw','wehelp',0,'2025-11-16 00:13:54'),(6,'郭千明','abc@abc.com','$argon2id$v=19$m=65536,t=3,p=4$KsjAaGkmKRk/AwKxb54YPA$bY456cExoevvPsFohm0nP0lmedRGIgrRLDoo4ogC3Ms',0,'2025-11-23 16:24:48'),(7,'Kaitlyn Wu','kaitastic26o@icloud.com','$argon2id$v=19$m=65536,t=3,p=4$EXWkxIUrNXgG8v//BqTsng$vvisRO/t0qZVOfhkApduoNCYTWLdoOVSiakAgCUKE9s',0,'2025-11-30 22:54:54'),(8,'User11','11@11.con','$argon2id$v=19$m=65536,t=3,p=4$c6crzGe/oLSi88ScesqQDQ$4PbQ93qizGf/yPCQTl8CxTI/QDs8nhjIGrUbs9rnMss',0,'2025-12-01 01:29:05'),(9,'vul3196','momo341323172@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$nnzxzRMe7fnSMf/VSdFIsg$oKQLpqUykUBJgbLDhPRCvXYzvUd1LUpnvVu/8l/DcT0',0,'2025-12-01 01:29:58');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int unsigned NOT NULL,
  `content` text NOT NULL,
  `like_count` int unsigned NOT NULL DEFAULT '0',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,1,'member01@wehelp.tw calling',1,'2025-11-16 16:00:27'),(2,2,'member02@wehelp.tw calling',2,'2025-11-16 16:00:36'),(3,3,'member03@wehelp.tw calling',3,'2025-11-16 16:00:43'),(4,5,'member05@wehelp.tw calling',5,'2025-11-16 16:00:50'),(5,4,'member04@wehelp.tw calling',4,'2025-11-16 16:00:57'),(6,2,'I caught a cold and kept sneezing. Feel dizzy and fatigue.',76,'2025-11-16 16:01:06'),(7,6,'231',0,'2025-11-23 16:25:31'),(8,6,'555',0,'2025-11-30 22:42:42'),(9,7,'888',0,'2025-11-30 22:55:11'),(10,9,'teat1',0,'2025-12-01 01:30:25');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `search_log`
--

DROP TABLE IF EXISTS `search_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `search_log` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `target_id` int unsigned NOT NULL,
  `executor_id` int unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `search_log`
--

LOCK TABLES `search_log` WRITE;
/*!40000 ALTER TABLE `search_log` DISABLE KEYS */;
INSERT INTO `search_log` VALUES (1,1,6,'2025-11-30 22:46:07'),(2,1,6,'2025-11-30 22:48:06'),(3,6,7,'2025-11-30 22:55:15'),(4,6,7,'2025-11-30 22:55:15'),(5,5,7,'2025-11-30 22:55:17'),(6,6,9,'2025-12-01 01:30:48'),(7,6,9,'2025-12-01 01:30:49'),(8,6,9,'2025-12-01 01:30:50'),(9,6,9,'2025-12-01 01:30:50'),(10,6,9,'2025-12-01 01:30:51');
/*!40000 ALTER TABLE `search_log` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-01  2:05:35
