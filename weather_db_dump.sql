-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: pogoda_db
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `dane_pogodowe`
--

DROP TABLE IF EXISTS `dane_pogodowe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dane_pogodowe` (
  `id` int NOT NULL AUTO_INCREMENT,
  `miasto_id` int NOT NULL,
  `godzina` datetime DEFAULT NULL,
  `temperatura` decimal(4,1) DEFAULT NULL,
  `odczuwalna` decimal(4,1) DEFAULT NULL,
  `warunki` text,
  `wiatr` varchar(100) DEFAULT NULL,
  `kierunek` text,
  `wilgotnosc` int DEFAULT NULL,
  `opady` varchar(50) DEFAULT NULL,
  `czas_zapisu` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `data` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `miasto_id` (`miasto_id`),
  CONSTRAINT `dane_pogodowe_ibfk_1` FOREIGN KEY (`miasto_id`) REFERENCES `miasta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=751 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dane_pogodowe`
--

LOCK TABLES `dane_pogodowe` WRITE;
/*!40000 ALTER TABLE `dane_pogodowe` DISABLE KEYS */;
INSERT INTO `dane_pogodowe` VALUES (1,1,'2025-04-19 13:00:00',19.0,19.0,'Zachmurzenie częściowe','4 m/s','210° S-SE do N-NW',49,'-','2025-04-19 10:16:18',NULL),(2,1,'2025-04-19 14:00:00',19.0,19.0,'Zachmurzenie całkowite','4 m/s','210° S-SE do N-NW',46,'-','2025-04-19 10:16:18',NULL),(3,1,'2025-04-19 15:00:00',20.0,20.0,'Głównie pochmurno','4 m/s','220° S do N',44,'-','2025-04-19 10:16:18',NULL),(4,1,'2025-04-19 16:00:00',20.0,20.0,'Częściowe zachmurzenie','4 m/s','230° SSW do N-NE',43,'-','2025-04-19 10:16:18',NULL),(5,1,'2025-04-19 17:00:00',20.0,20.0,'Głównie słonecznie','4 m/s','240° SW do N-NE',43,'-','2025-04-19 10:16:18',NULL),(6,1,'2025-04-19 18:00:00',19.0,19.0,'Głównie słonecznie','3 m/s','260° W do N-NE',44,'-','2025-04-19 10:16:18',NULL),(7,1,'2025-04-19 19:00:00',18.0,18.0,'Głównie słonecznie','3 m/s','280° W-NW do N-NE',46,'-','2025-04-19 10:16:18',NULL),(8,1,'2025-04-19 20:00:00',17.0,17.0,'Głównie czyste niebo','3 m/s','300° NW do N',50,'-','2025-04-19 10:16:18',NULL),(9,1,'2025-04-19 21:00:00',15.0,15.0,'Głównie czyste niebo','2 m/s','330° N-NW do N-NE',59,'-','2025-04-19 10:16:18',NULL),(10,1,'2025-04-19 22:00:00',13.0,14.0,'Czyste niebo','1 m/s','20° North-northeast to South-southwest',66,'-','2025-04-19 10:16:18',NULL),(11,1,'2025-04-19 23:00:00',13.0,13.0,'Czyste niebo','2 m/s','60° East-northeast to West-southwest',69,'-','2025-04-19 10:16:18',NULL),(12,1,'2025-04-20 00:00:00',13.0,12.0,'Głównie czyste niebo','2 m/s','70° East-northeast to West-southwest',72,'-','2025-04-19 10:16:18',NULL),(13,1,'2025-04-20 01:00:00',12.0,11.0,'Rozproszone chmury','3 m/s','80° East to West',74,'-','2025-04-19 10:16:18',NULL),(14,1,'2025-04-20 02:00:00',13.0,12.0,'Zachmurzenie częściowe','3 m/s','90° East to West',71,'-','2025-04-19 10:16:18',NULL),(15,1,'2025-04-20 03:00:00',13.0,12.0,'Głównie pochmurno','3 m/s','100° East to West',70,'-','2025-04-19 10:16:18',NULL),(16,1,'2025-04-20 04:00:00',12.0,11.0,'Pochmurno','2 m/s','120° SE do NW',74,'-','2025-04-19 10:16:18',NULL),(17,1,'2025-04-20 05:00:00',12.0,11.0,'Zachmurzenie całkowite','2 m/s','140° SE do NW',75,'-','2025-04-19 10:16:18',NULL),(18,1,'2025-04-20 06:00:00',12.0,11.0,'Zachmurzenie całkowite','2 m/s','140° SE do NW',75,'-','2025-04-19 10:16:18',NULL),(19,1,'2025-04-20 07:00:00',13.0,12.0,'Głównie pochmurno','2 m/s','130° SE do NW',74,'-','2025-04-19 10:16:18',NULL),(20,1,'2025-04-20 08:00:00',14.0,14.0,'Głównie pochmurno','3 m/s','130° SE do NW',68,'-','2025-04-19 10:16:18',NULL),(21,1,'2025-04-20 09:00:00',17.0,17.0,'Głównie pochmurno','3 m/s','140° SE do NW',61,'-','2025-04-19 10:16:18',NULL),(22,1,'2025-04-20 10:00:00',19.0,19.0,'Pochmurno','3 m/s','140° SE do NW',55,'-','2025-04-19 10:16:18',NULL),(23,1,'2025-04-20 11:00:00',20.0,20.0,'Zachmurzenie całkowite','3 m/s','150° SSE do N-NW',50,'-','2025-04-19 10:16:18',NULL),(24,1,'2025-04-20 12:00:00',21.0,21.0,'Zachmurzenie całkowite','2 m/s','160° S-SE do N-NW',45,'-','2025-04-19 10:16:18',NULL),(25,2,'2025-04-19 13:00:00',19.0,19.0,'Rozproszone chmury','1 m/s','60° East-northeast to West-southwest',45,'-','2025-04-19 10:16:21',NULL),(26,2,'2025-04-19 14:00:00',20.0,20.0,'Głównie słonecznie','2 m/s','50° Northeast to Southwest',42,'-','2025-04-19 10:16:21',NULL),(27,2,'2025-04-19 15:00:00',20.0,20.0,'Rozproszone chmury','2 m/s','70° East-northeast to West-southwest',41,'-','2025-04-19 10:16:21',NULL),(28,2,'2025-04-19 16:00:00',20.0,20.0,'Zachmurzenie częściowe','3 m/s','70° East-northeast to West-southwest',41,'-','2025-04-19 10:16:21',NULL),(29,2,'2025-04-19 17:00:00',20.0,20.0,'Głównie pochmurno','4 m/s','80° East to West',43,'-','2025-04-19 10:16:21',NULL),(30,2,'2025-04-19 18:00:00',20.0,20.0,'Głównie pochmurno','3 m/s','80° East to West',45,'-','2025-04-19 10:16:21',NULL),(31,2,'2025-04-19 19:00:00',18.0,18.0,'Zachmurzenie częściowe','3 m/s','80° East to West',48,'-','2025-04-19 10:16:21',NULL),(32,2,'2025-04-19 20:00:00',17.0,17.0,'Sprinkles. Partly cloudy.','3 m/s','80° East to West',54,'0.1  mm (rain)','2025-04-19 10:16:21',NULL),(33,2,'2025-04-19 21:00:00',15.0,15.0,'Sprinkles. Scattered clouds.','2 m/s','90° East to West',63,'0.1  mm (rain)','2025-04-19 10:16:21',NULL),(34,2,'2025-04-19 22:00:00',13.0,13.0,'Czyste niebo','1 m/s','100° East to West',71,'-','2025-04-19 10:16:21',NULL),(35,2,'2025-04-19 23:00:00',12.0,12.0,'Czyste niebo','1 m/s','150° SSE do N-NW',77,'-','2025-04-19 10:16:21',NULL),(36,2,'2025-04-20 00:00:00',11.0,11.0,'Czyste niebo','1 m/s','200° SSW do N-NE',79,'-','2025-04-19 10:16:21',NULL),(37,2,'2025-04-20 01:00:00',10.0,10.0,'Czyste niebo','1 m/s','230° SSW do N-NE',81,'-','2025-04-19 10:16:21',NULL);
/*!40000 ALTER TABLE `dane_pogodowe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `miasta`
--

DROP TABLE IF EXISTS `miasta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `miasta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(50) NOT NULL,
  `wojewodztwo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `miasta`
--

LOCK TABLES `miasta` WRITE;
/*!40000 ALTER TABLE `miasta` DISABLE KEYS */;
INSERT INTO `miasta` VALUES (1,'Warsaw','mazowieckie'),(2,'Krakow','małopolskie'),(3,'Lodz','łódzkie'),(4,'Wroclaw','dolnośląskie'),(5,'Poznan','wielkopolskie'),(6,'Gdansk','pomorskie'),(7,'Szczecin','zachodniopomorskie'),(8,'Bydgoszcz','kujawsko-pomorskie'),(9,'Lublin','lubelskie'),(10,'Katowice','śląskie'),(11,'Gorzow-wielkopolski','lubuskie'),(12,'Zielona-gora','lubuskie'),(13,'Opole','opolskie'),(14,'Rzeszow','podkarpackie'),(15,'Kielce','świętokrzyskie');
/*!40000 ALTER TABLE `miasta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-20 18:24:20
