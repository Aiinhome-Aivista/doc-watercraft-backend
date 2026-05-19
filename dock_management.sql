-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 72.61.226.68    Database: dock_management
-- ------------------------------------------------------
-- Server version	8.0.45-0ubuntu0.24.04.1

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
-- Table structure for table `bill_details`
--

DROP TABLE IF EXISTS `bill_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill_details` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bill_main_id` int NOT NULL,
  `vessel_id` int DEFAULT NULL,
  `activity_name` varchar(100) DEFAULT NULL,
  `qty` decimal(12,2) DEFAULT NULL,
  `rate` decimal(12,2) DEFAULT NULL,
  `amount` decimal(12,2) DEFAULT NULL,
  `remarks` text,
  `gst_rate` decimal(5,2) DEFAULT NULL,
  `gst_amount` decimal(12,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_bill_main` (`bill_main_id`),
  KEY `fk_bill_vessel` (`vessel_id`),
  CONSTRAINT `fk_bill_main` FOREIGN KEY (`bill_main_id`) REFERENCES `bill_main` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_bill_vessel` FOREIGN KEY (`vessel_id`) REFERENCES `vessels` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill_details`
--

LOCK TABLES `bill_details` WRITE;
/*!40000 ALTER TABLE `bill_details` DISABLE KEYS */;
INSERT INTO `bill_details` VALUES (1,1,1,'Terminal Services',400.00,46.00,18400.00,'',18.00,3312.00,'2026-05-12 06:31:17'),(2,1,1,'Handling service',400.00,170.00,68000.00,'',18.00,12240.00,'2026-05-12 06:31:18'),(3,1,1,'Berthing charges',2.00,3000.00,6000.00,'',18.00,1080.00,'2026-05-12 06:31:19'),(4,1,1,'Mooring charges',4.00,4000.00,16000.00,'',12.00,1920.00,'2026-05-12 06:31:19'),(5,1,1,'Truck entry charges',1.00,100.00,100.00,'',18.00,18.00,'2026-05-12 06:31:19'),(6,1,1,'Weighment charges',1.00,250.00,250.00,'',18.00,45.00,'2026-05-12 06:31:20'),(7,1,1,'Berthing Assistance',2.00,2000.00,4000.00,'',18.00,720.00,'2026-05-12 06:31:20'),(8,2,1,'Terminal Services',400.00,46.00,18400.00,'',18.00,3312.00,'2026-05-12 06:31:39'),(9,2,1,'Handling service',400.00,170.00,68000.00,'',18.00,12240.00,'2026-05-12 06:31:39'),(10,2,1,'Berthing charges',2.00,3000.00,6000.00,'',18.00,1080.00,'2026-05-12 06:31:40'),(11,2,1,'Mooring charges',4.00,4000.00,16000.00,'',12.00,1920.00,'2026-05-12 06:31:40'),(12,2,1,'Truck entry charges',1.00,100.00,100.00,'',18.00,18.00,'2026-05-12 06:31:41'),(13,2,1,'Weighment charges',1.00,250.00,250.00,'',18.00,45.00,'2026-05-12 06:31:41'),(14,2,1,'Berthing Assistance',2.00,2000.00,4000.00,'',18.00,720.00,'2026-05-12 06:31:41'),(15,3,3,'Terminal Services',1300.00,46.00,59800.00,'',18.00,10764.00,'2026-05-12 11:47:47'),(16,3,3,'Handling service',1300.00,170.00,221000.00,'',18.00,39780.00,'2026-05-12 11:47:47'),(17,3,3,'Berthing charges',1.00,3000.00,3000.00,'',18.00,540.00,'2026-05-12 11:47:48'),(18,3,3,'Mooring charges',1.00,4000.00,4000.00,'',12.00,480.00,'2026-05-12 11:47:48'),(19,3,3,'Truck entry charges',1.00,100.00,100.00,'',18.00,18.00,'2026-05-12 11:47:49'),(20,3,3,'Berthing Assistance',1.00,2000.00,2000.00,'',18.00,360.00,'2026-05-12 11:47:49');
/*!40000 ALTER TABLE `bill_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bill_main`
--

DROP TABLE IF EXISTS `bill_main`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill_main` (
  `id` int NOT NULL AUTO_INCREMENT,
  `voucher_number` varchar(50) NOT NULL,
  `bill_date` date NOT NULL,
  `party_id` int NOT NULL,
  `period_start` date DEFAULT NULL,
  `period_end` date DEFAULT NULL,
  `narration` text,
  `bill_base_value` decimal(12,2) DEFAULT '0.00',
  `cgst` decimal(12,2) DEFAULT '0.00',
  `sgst` decimal(12,2) DEFAULT '0.00',
  `igst` decimal(12,2) DEFAULT '0.00',
  `round_off` decimal(12,2) DEFAULT '0.00',
  `total_bill_value` decimal(12,2) DEFAULT '0.00',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `voucher_number` (`voucher_number`),
  KEY `fk_bill_party` (`party_id`),
  CONSTRAINT `fk_bill_party` FOREIGN KEY (`party_id`) REFERENCES `party_masters` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill_main`
--

LOCK TABLES `bill_main` WRITE;
/*!40000 ALTER TABLE `bill_main` DISABLE KEYS */;
INSERT INTO `bill_main` VALUES (1,'BILL-20260512023115','2026-05-12',1,'2026-05-11','2026-05-14','',112750.00,9667.50,9667.50,0.00,0.00,132085.00,'2026-05-12 06:31:17','2026-05-12 06:31:17'),(2,'BILL-20260512023138','2026-05-12',1,'2026-05-11','2026-05-14','',112750.00,9667.50,9667.50,0.00,0.00,132085.00,'2026-05-12 06:31:39','2026-05-12 06:31:39'),(3,'BILL-20260512074745','2026-05-12',1,'2026-05-01','2026-05-13','',289900.00,25971.00,25971.00,0.00,0.00,341842.00,'2026-05-12 11:47:47','2026-05-12 11:47:47');
/*!40000 ALTER TABLE `bill_main` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cargo_operations`
--

DROP TABLE IF EXISTS `cargo_operations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cargo_operations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gate_entry_id` int NOT NULL,
  `vessel_id` int DEFAULT NULL,
  `operation_type` enum('LOADING','UNLOADING') NOT NULL DEFAULT 'UNLOADING',
  `start_datetime` datetime NOT NULL,
  `end_datetime` datetime DEFAULT NULL,
  `compressor_no` varchar(30) DEFAULT NULL,
  `remarks` text,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_gate_entry` (`gate_entry_id`),
  KEY `fk_cargo_vessel` (`vessel_id`),
  CONSTRAINT `cargo_operations_ibfk_1` FOREIGN KEY (`gate_entry_id`) REFERENCES `gate_entries` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `fk_cargo_vessel` FOREIGN KEY (`vessel_id`) REFERENCES `vessels` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargo_operations`
--

LOCK TABLES `cargo_operations` WRITE;
/*!40000 ALTER TABLE `cargo_operations` DISABLE KEYS */;
INSERT INTO `cargo_operations` VALUES (1,1,1,'UNLOADING','2026-05-12 11:48:00','2026-05-12 11:49:00','12234','','2026-05-12 11:49:21','2026-05-12 11:49:54'),(2,3,3,'UNLOADING','2026-05-12 17:13:00','2026-05-12 17:14:00','','','2026-05-12 17:14:09','2026-05-12 17:14:40');
/*!40000 ALTER TABLE `cargo_operations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gate_entries`
--

DROP TABLE IF EXISTS `gate_entries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gate_entries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gate_in_no` varchar(20) NOT NULL COMMENT 'Auto-generated gate-in number',
  `gate_in_datetime` datetime NOT NULL,
  `party_id` int DEFAULT NULL,
  `vehicle_id` int DEFAULT NULL,
  `challan_invoice_no` varchar(50) NOT NULL,
  `weighment_slip_no` varchar(50) DEFAULT NULL,
  `outside_payment_slip` varchar(100) DEFAULT NULL,
  `outside_weight` decimal(10,2) DEFAULT NULL,
  `own_weighbridge` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1=Yes (>=60T, skip WBIN), 0=No (needs WBIN)',
  `direction` varchar(10) DEFAULT NULL,
  `status` enum('PENDING_WBIN','WBIN_DONE','UNLOADING','PENDING_WBOUT','GATE_OUT','COMPLETED') NOT NULL DEFAULT 'PENDING_WBIN',
  `gate_out_datetime` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gate_in_no` (`gate_in_no`),
  KEY `idx_status` (`status`),
  KEY `idx_gate_in_datetime` (`gate_in_datetime`),
  KEY `fk_vehicle` (`vehicle_id`),
  KEY `fk_gate_entries_party` (`party_id`),
  CONSTRAINT `fk_gate_entries_party` FOREIGN KEY (`party_id`) REFERENCES `party_masters` (`id`),
  CONSTRAINT `fk_vehicle` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle_master` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gate_entries`
--

LOCK TABLES `gate_entries` WRITE;
/*!40000 ALTER TABLE `gate_entries` DISABLE KEYS */;
INSERT INTO `gate_entries` VALUES (1,'GIN-2026-00001','2026-05-12 11:36:00',1,1,'CH12345','12345',NULL,40.00,0,'EXPORT','COMPLETED','2026-05-12 11:56:00','2026-05-12 11:43:28','2026-05-12 11:56:47'),(2,'GIN-2026-00002','2026-05-10 14:05:00',2,3,'12012','4101',NULL,45.60,1,'EXPORT','WBIN_DONE',NULL,'2026-05-12 16:57:18','2026-05-12 16:57:18'),(3,'GIN-2026-00003','2026-05-12 17:11:00',2,3,'1200','46452',NULL,NULL,1,'EXPORT','GATE_OUT','2026-05-12 17:14:00','2026-05-12 17:12:41','2026-05-12 17:15:08');
/*!40000 ALTER TABLE `gate_entries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `party_masters`
--

DROP TABLE IF EXISTS `party_masters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `party_masters` (
  `id` int NOT NULL AUTO_INCREMENT,
  `party_name` varchar(150) NOT NULL,
  `party_code` varchar(50) DEFAULT NULL,
  `address` text,
  `state` varchar(100) DEFAULT NULL,
  `country` varchar(100) DEFAULT NULL,
  `pincode` varchar(20) DEFAULT NULL,
  `mobiles` json DEFAULT NULL,
  `emails` json DEFAULT NULL,
    `pan_number` varchar(20) DEFAULT NULL,
    `gst_number` varchar(30) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `party_code` (`party_code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `party_masters`
--

LOCK TABLES `party_masters` WRITE;
/*!40000 ALTER TABLE `party_masters` DISABLE KEYS */;
INSERT INTO `party_masters` (`id`, `party_name`, `party_code`, `address`, `state`, `country`, `pincode`, `mobiles`, `emails`, `pan_number`, `gst_number`, `created_at`, `updated_at`) VALUES (1,'IRC Commercial','IRCC','1 sunyat sen street','West Bengal','India','700001','[\"1234567890\"]','[\"tdlkolkata@yahoo.com\"]',NULL,NULL,'2026-05-12 05:57:08','2026-05-12 05:57:08'),(2,' HAQUE TRADERS','002','8/2B, ABDUL HALIM LANE, TALTAKA, KOLKATA, 743338','WEST BENGAL','INDIA','743338','[\"1234567890\"]','[\"haque@gmail.com\"]',NULL,NULL,'2026-05-12 11:21:59','2026-05-12 11:21:59'),(3,'ABC','345','abh','abc','india','12345','[\"8976567896\"]','[\"abc@gmail.com\"]',NULL,NULL,'2026-05-18 07:42:30','2026-05-18 07:42:30'),(4,'ABC','890654','KOLKATA','WEST BENGAL','INDIA','700101','[\"8756908790\"]','[\"ABC789@gmail.com\"]',NULL,NULL,'2026-05-18 08:02:04','2026-05-18 08:02:04');
/*!40000 ALTER TABLE `party_masters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rate_master`
--

DROP TABLE IF EXISTS `rate_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rate_master` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vessel_id` int NOT NULL,
  `activity` varchar(100) NOT NULL,
  `formula` varchar(20) NOT NULL,
  `rate` decimal(10,2) DEFAULT NULL,
  `gst_rate` decimal(5,2) NOT NULL,
  `min_qty` decimal(10,2) DEFAULT NULL,
  `max_qty` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_rate_master_vessel` (`vessel_id`),
  CONSTRAINT `fk_rate_master_vessel` FOREIGN KEY (`vessel_id`) REFERENCES `vessels` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rate_master`
--

LOCK TABLES `rate_master` WRITE;
/*!40000 ALTER TABLE `rate_master` DISABLE KEYS */;
INSERT INTO `rate_master` VALUES (1,1,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-12 06:01:56'),(2,1,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-12 06:01:57'),(3,1,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-12 06:01:57'),(4,1,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-12 06:01:57'),(5,1,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-12 06:01:58'),(6,1,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-12 06:01:58'),(7,1,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-12 06:01:58'),(8,1,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-12 06:01:59'),(9,1,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-12 06:01:59'),(10,1,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-12 06:01:59'),(11,2,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-12 11:30:36'),(12,2,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-12 11:30:37'),(13,2,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-12 11:30:37'),(14,2,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-12 11:30:37'),(15,2,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-12 11:30:38'),(16,2,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-12 11:30:38'),(17,2,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-12 11:30:38'),(18,2,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-12 11:30:38'),(19,2,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-12 11:30:39'),(20,2,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-12 11:30:39'),(21,3,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-12 11:39:01'),(22,3,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-12 11:39:01'),(23,3,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-12 11:39:02'),(24,3,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-12 11:39:02'),(25,3,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-12 11:39:02'),(26,3,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-12 11:39:02'),(27,3,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-12 11:39:03'),(28,3,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-12 11:39:03'),(29,3,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-12 11:39:03'),(30,3,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-12 11:39:03');
/*!40000 ALTER TABLE `rate_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_access_rights`
--

DROP TABLE IF EXISTS `user_access_rights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_access_rights` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `access_rights` json NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_access_rights_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_access_rights`
--

LOCK TABLES `user_access_rights` WRITE;
/*!40000 ALTER TABLE `user_access_rights` DISABLE KEYS */;
INSERT INTO `user_access_rights` VALUES (1,1,'{\"modules\": [\"DASHBOARD\", \"VESSEL_OPS\", \"VEHICLE_LOGISTICS\", \"WEIGHBRIDGE_TERMINAL\", \"REPORTS_BILLING\", \"SETTINGS\", \"PARTY_MASTER\", \"VEHICLE_MASTER\"], \"gate_operations\": [\"PENDING_WBIN\", \"WBIN_DONE\", \"UNLOADING\", \"PENDING_WBOUT\", \"COMPLETED\", \"GATE_OUT\"], \"vessel_statuses\": [\"PLANNED\", \"BERTHED\", \"MOORED\", \"COMPLETED\"]}','2026-04-23 05:25:30','2026-04-24 12:30:01'),(2,2,'{}','2026-05-12 06:36:44','2026-05-12 06:36:44');
/*!40000 ALTER TABLE `user_access_rights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role` varchar(50) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(150) DEFAULT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `email` varchar(150) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','@admin','123456','admin','7894561230','admin@gmail.com',1,'2026-04-23 05:24:47','2026-04-23 05:24:47'),(2,'user','admin1','1234567','Loading user','12345578900','admin1@gmail.com',1,'2026-05-12 06:36:44','2026-05-12 06:36:44');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle_master`
--

DROP TABLE IF EXISTS `vehicle_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle_master` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vehicle_no` varchar(50) DEFAULT NULL,
  `transporter_name` varchar(100) NOT NULL,
  `active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `vehicle_no` (`vehicle_no`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_master`
--

LOCK TABLES `vehicle_master` WRITE;
/*!40000 ALTER TABLE `vehicle_master` DISABLE KEYS */;
INSERT INTO `vehicle_master` VALUES (1,'WB 05 D 1234','RAM company',1),(2,'WB05 D 1236','ram company',1),(3,'WB12A 5104','HAQUE TRADERS',1),(4,'WB12A 4710','HAQUE TRADERS',1),(5,'WB12A 5410','A',1);
/*!40000 ALTER TABLE `vehicle_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vessels`
--

DROP TABLE IF EXISTS `vessels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vessels` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vessel_auto_id` varchar(20) NOT NULL COMMENT 'Auto-generated e.g. VSL-2024-001',
  `vessel_name` varchar(100) NOT NULL,
  `party_id` int DEFAULT NULL,
  `cargo_type` varchar(100) NOT NULL COMMENT 'e.g. FLYASH, COAL, etc.',
  `quantity` decimal(10,2) NOT NULL COMMENT 'Expected quantity in MT',
  `direction` enum('IMPORT','EXPORT') NOT NULL,
  `status` enum('PLANNED','BERTHED','MOORED','COMPLETED') NOT NULL DEFAULT 'PLANNED',
  `expected_date` date NOT NULL,
  `berthing_datetime` datetime DEFAULT NULL,
  `mooring_datetime` datetime DEFAULT NULL,
  `survey_quantity` decimal(10,2) DEFAULT NULL COMMENT 'Actual quantity per survey report in MT',
  `survey_datetime` datetime DEFAULT NULL,
  `sailing_datetime` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vessel_auto_id` (`vessel_auto_id`),
  KEY `idx_status` (`status`),
  KEY `idx_expected_date` (`expected_date`),
  KEY `idx_party_name` (`party_id`),
  CONSTRAINT `fk_party` FOREIGN KEY (`party_id`) REFERENCES `party_masters` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vessels`
--

LOCK TABLES `vessels` WRITE;
/*!40000 ALTER TABLE `vessels` DISABLE KEYS */;
INSERT INTO `vessels` VALUES (1,'VSL-2026-0001','MV HAQUE -12.05.2026',1,'FLYASH',500.00,'EXPORT','COMPLETED','2026-05-14','2026-05-13 11:32:00','2026-05-13 11:33:00',400.00,'2026-05-13 11:58:00','2026-05-14 11:59:00','2026-05-12 11:31:56','2026-05-12 11:59:42'),(2,'VSL-2026-0002','M.V. TARA - 5',2,'FLYASH',1200.00,'EXPORT','COMPLETED','2026-05-12','2026-05-13 21:01:00','2026-05-13 22:02:00',NULL,NULL,'2026-05-12 17:16:00','2026-05-12 17:00:36','2026-05-12 17:16:56'),(3,'VSL-2026-0003','M.V  PAWANSUTH',1,'COAL',1000.00,'EXPORT','COMPLETED','2026-05-12','2026-05-12 17:09:00','2026-05-12 17:09:00',1300.00,'2026-05-12 17:16:00','2026-05-12 17:16:00','2026-05-12 17:09:01','2026-05-12 17:16:42');
/*!40000 ALTER TABLE `vessels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wbin_records`
--

DROP TABLE IF EXISTS `wbin_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wbin_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gate_entry_id` int NOT NULL,
  `weighment_slip_no` varchar(50) NOT NULL,
  `wbin_datetime` datetime NOT NULL,
  `gross_weight` decimal(10,3) DEFAULT NULL COMMENT 'For EXPORT: loaded truck gross weight in MT',
  `tare_weight` decimal(10,3) DEFAULT NULL COMMENT 'For IMPORT: empty truck tare weight in MT',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gate_entry_id` (`gate_entry_id`),
  KEY `idx_gate_entry` (`gate_entry_id`),
  CONSTRAINT `wbin_records_ibfk_1` FOREIGN KEY (`gate_entry_id`) REFERENCES `gate_entries` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wbin_records`
--

LOCK TABLES `wbin_records` WRITE;
/*!40000 ALTER TABLE `wbin_records` DISABLE KEYS */;
INSERT INTO `wbin_records` VALUES (1,1,'12345','2026-05-12 11:36:00',40.200,NULL,'2026-05-12 11:43:35');
/*!40000 ALTER TABLE `wbin_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wbout_records`
--

DROP TABLE IF EXISTS `wbout_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wbout_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `gate_entry_id` int NOT NULL,
  `weighment_slip_no` varchar(50) NOT NULL,
  `wbout_datetime` datetime NOT NULL,
  `gross_weight` decimal(10,3) DEFAULT NULL COMMENT 'Final gross weight (for IMPORT: loaded)',
  `tare_weight` decimal(10,3) DEFAULT NULL COMMENT 'Final tare weight (for EXPORT: empty)',
  `net_weight` decimal(10,3) GENERATED ALWAYS AS ((case when ((`gross_weight` is not null) and (`tare_weight` is not null)) then (`gross_weight` - `tare_weight`) else NULL end)) STORED COMMENT 'Computed net material quantity in MT',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gate_entry_id` (`gate_entry_id`),
  KEY `idx_gate_entry` (`gate_entry_id`),
  CONSTRAINT `wbout_records_ibfk_1` FOREIGN KEY (`gate_entry_id`) REFERENCES `gate_entries` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wbout_records`
--

LOCK TABLES `wbout_records` WRITE;
/*!40000 ALTER TABLE `wbout_records` DISABLE KEYS */;
INSERT INTO `wbout_records` (`id`, `gate_entry_id`, `weighment_slip_no`, `wbout_datetime`, `gross_weight`, `tare_weight`, `created_at`) VALUES (1,1,'12345','2026-05-12 11:54:00',NULL,14.280,'2026-04-24 16:04:36'),(2,10,'125896','2026-04-25 15:15:00',59.000,NULL,'2026-04-25 15:18:50'),(3,11,'789456','2026-04-25 10:40:00',NULL,55.000,'2026-04-27 10:40:19'),(4,12,'7894566','2026-04-20 11:30:00',NULL,12.000,'2026-04-27 11:30:54'),(5,14,'7895623','2026-04-27 19:31:00',58.000,NULL,'2026-04-27 19:31:16'),(6,2,'789456','2026-04-27 20:01:00',56.000,NULL,'2026-04-27 20:01:12'),(7,3,'46452','2026-05-12 17:14:00',NULL,16.420,'2026-04-28 10:46:01'),(10,4,'64545656','2026-05-04 19:07:00',NULL,12.000,'2026-05-04 19:07:59');
/*!40000 ALTER TABLE `wbout_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'dock_management'
--
/*!50003 DROP PROCEDURE IF EXISTS `sp_create_cargo_operation` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_create_cargo_operation`(
    IN p_gate_entry_id INT,
    IN p_vessel_id INT,
    IN p_operation_type VARCHAR(50),
    IN p_start_datetime DATETIME,
    IN p_end_datetime DATETIME,
    IN p_compressor_no VARCHAR(30),
    IN p_remarks TEXT
)
BEGIN
    DECLARE v_status VARCHAR(50);

    -- =========================
    -- VALIDATION
    -- =========================
    IF NOT EXISTS (
        SELECT 1 FROM gate_entries WHERE id = p_gate_entry_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Gate entry not found';
    END IF;

    IF p_vessel_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'vessel_id required';
    END IF;

    -- =========================
    -- INSERT
    -- =========================
    INSERT INTO cargo_operations (
        gate_entry_id,
        vessel_id,
        operation_type,
        start_datetime,
        end_datetime,
        compressor_no,
        remarks,
        created_at,
        updated_at
    ) VALUES (
        p_gate_entry_id,
        p_vessel_id,
        p_operation_type,
        p_start_datetime,
        p_end_datetime,
        p_compressor_no,
        p_remarks,
        NOW(),
        NOW()
    );

    -- =========================
    -- STATUS LOGIC
    -- =========================
    IF p_start_datetime IS NOT NULL AND p_end_datetime IS NULL THEN
        SET v_status = 'UNLOADING';
    ELSEIF p_end_datetime IS NOT NULL THEN
        SET v_status = 'PENDING_WBOUT';
    ELSE
        SET v_status = NULL;
    END IF;

    IF v_status IS NOT NULL THEN
        UPDATE gate_entries
        SET status = v_status,
            updated_at = NOW()
        WHERE id = p_gate_entry_id;
    END IF;

    -- =========================
    -- RETURN DATA
    -- =========================
    SELECT 
        co.*,
        v.vessel_name,
        v.direction
    FROM cargo_operations co
    LEFT JOIN vessels v ON co.vessel_id = v.id
    WHERE co.id = LAST_INSERT_ID();

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_create_gate_entry` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_create_gate_entry`(
    IN p_party_id INT,
    IN p_vehicle_id INT,
    IN p_challan_invoice_no VARCHAR(50),
    IN p_weighment_slip_no VARCHAR(50),
    IN p_outside_payment_slip VARCHAR(100),
    IN p_outside_weight DECIMAL(10,2),
    IN p_own_weighbridge TINYINT(1),
    IN p_gate_in_datetime DATETIME,
    IN p_direction VARCHAR(10)
)
BEGIN
    DECLARE v_status VARCHAR(20);

    -- ✅ Decide initial status
    IF p_own_weighbridge = 1 THEN
        SET v_status = 'WBIN_DONE';
    ELSE
        SET v_status = 'PENDING_WBIN';
    END IF;

    -- ✅ Insert into updated table
    INSERT INTO gate_entries (
        party_id,
        vehicle_id,
        challan_invoice_no,
        weighment_slip_no,
        outside_payment_slip,
        outside_weight,
        own_weighbridge,
        gate_in_datetime,
        status,
        direction,
        created_at,
        updated_at
    )
    VALUES (
        p_party_id,
        p_vehicle_id,
        p_challan_invoice_no,
        p_weighment_slip_no,
        p_outside_payment_slip,
        p_outside_weight,
        p_own_weighbridge,
        p_gate_in_datetime,
        v_status,
        p_direction,
        NOW(),
        NOW()
    );

    -- ✅ Return inserted row with joins
    SELECT 
        ge.*,
        pm.party_name,
        vm.vehicle_no,
        vm.transporter_name
    FROM gate_entries ge
    LEFT JOIN party_masters pm ON ge.party_id = pm.id
    LEFT JOIN vehicle_master vm ON ge.vehicle_id = vm.id
    WHERE ge.id = LAST_INSERT_ID();

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_create_party` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_create_party`(
    IN p_party_name VARCHAR(150),
    IN p_party_code VARCHAR(50),
    IN p_address TEXT,
    IN p_state VARCHAR(100),
    IN p_country VARCHAR(100),
    IN p_pincode VARCHAR(20),
    IN p_mobiles JSON,
    IN p_emails JSON,
    IN p_pan_number VARCHAR(20),
    IN p_gst_number VARCHAR(30)
)
BEGIN

    -- VALIDATION
    IF p_party_name IS NULL OR p_party_name = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'party_name is required';
    END IF;

    -- DUPLICATE CHECK
    IF EXISTS (
        SELECT 1 FROM party_masters WHERE party_code = p_party_code
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'party_code already exists';
    END IF;

    INSERT INTO party_masters (
        party_name, party_code, address, state, country,
        pincode, mobiles, emails, pan_number, gst_number, created_at, updated_at
    ) VALUES (
        p_party_name, p_party_code, p_address, p_state, p_country,
        p_pincode, p_mobiles, p_emails, p_pan_number, p_gst_number, NOW(), NOW()
    );

    SELECT * FROM party_masters WHERE id = LAST_INSERT_ID();

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_create_wbin` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_create_wbin`(
    IN p_gate_entry_id INT,
    IN p_weighment_slip_no VARCHAR(50),
    IN p_wbin_datetime DATETIME,
    IN p_gross_weight DECIMAL(10,2),
    IN p_tare_weight DECIMAL(10,2)
)
BEGIN
    DECLARE v_status VARCHAR(50);
    DECLARE v_direction VARCHAR(20);
    DECLARE v_vehicle_id INT;

    -- Get Gate Entry Details
    SELECT
        status,
        direction,
        vehicle_id
    INTO
        v_status,
        v_direction,
        v_vehicle_id
    FROM gate_entries
    WHERE id = p_gate_entry_id
    LIMIT 1;

    -- Validation
    IF v_status IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Gate entry not found';
    END IF;

    IF v_vehicle_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Vehicle not assigned';
    END IF;

    IF v_status <> 'PENDING_WBIN' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid status for WBIN';
    END IF;

    IF v_direction = 'EXPORT' AND p_gross_weight IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Gross weight required for EXPORT';
    END IF;

    IF v_direction = 'IMPORT' AND p_tare_weight IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Tare weight required for IMPORT';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM wbin_records
        WHERE gate_entry_id = p_gate_entry_id
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'WBIN already exists';
    END IF;

    -- Insert WBIN Record
    INSERT INTO wbin_records (
        gate_entry_id,
        weighment_slip_no,
        wbin_datetime,
        gross_weight,
        tare_weight,
        created_at
    ) VALUES (
        p_gate_entry_id,
        p_weighment_slip_no,
        p_wbin_datetime,
        p_gross_weight,
        p_tare_weight,
        NOW()
    );

    -- Update Gate Entry
    UPDATE gate_entries
    SET
        status = 'WBIN_DONE',
        weighment_slip_no = p_weighment_slip_no,
        updated_at = NOW()
    WHERE id = p_gate_entry_id;

    -- Return Result
    SELECT
        wr.*,
        ge.gate_in_no,
        ge.vehicle_id,
        vm.vehicle_no,
        ge.direction,
        ge.status
    FROM wbin_records wr
    JOIN gate_entries ge
        ON ge.id = wr.gate_entry_id
    LEFT JOIN vehicle_master vm
        ON vm.id = ge.vehicle_id
    WHERE wr.gate_entry_id = p_gate_entry_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_create_wbout` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_create_wbout`(
    IN p_gate_entry_id INT,
    IN p_weighment_slip_no VARCHAR(50),
    IN p_wbout_datetime DATETIME,
    IN p_gross_weight DECIMAL(10,2),
    IN p_tare_weight DECIMAL(10,2)
)
BEGIN
    DECLARE v_status VARCHAR(50);
    DECLARE v_direction VARCHAR(20);
    DECLARE v_vehicle_id INT;

    -- GET GATE ENTRY DETAILS
    SELECT
        ge.status,
        ge.direction,
        ge.vehicle_id
    INTO
        v_status,
        v_direction,
        v_vehicle_id
    FROM gate_entries ge
    WHERE ge.id = p_gate_entry_id
    LIMIT 1;

    -- VALIDATIONS
    IF v_status IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Gate entry not found';
    END IF;

    IF v_vehicle_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Vehicle not assigned';
    END IF;

    IF v_status NOT IN ('PENDING_WBOUT', 'WBIN_DONE', 'UNLOADING') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid status for WBOUT';
    END IF;

    -- WEIGHT VALIDATION
    IF v_direction = 'EXPORT' AND p_tare_weight IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Tare weight required for EXPORT';
    END IF;

    IF v_direction = 'IMPORT' AND p_gross_weight IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Gross weight required for IMPORT';
    END IF;

    -- INSERT OR UPDATE WBOUT
    IF EXISTS (
        SELECT 1 FROM wbout_records WHERE gate_entry_id = p_gate_entry_id
    ) THEN

        -- UPDATE EXISTING
        UPDATE wbout_records
        SET
            weighment_slip_no = p_weighment_slip_no,
            wbout_datetime = p_wbout_datetime,
            gross_weight = p_gross_weight,
            tare_weight = p_tare_weight
        WHERE gate_entry_id = p_gate_entry_id;

    ELSE

        -- INSERT NEW
        INSERT INTO wbout_records (
            gate_entry_id,
            weighment_slip_no,
            wbout_datetime,
            gross_weight,
            tare_weight,
            created_at
        ) VALUES (
            p_gate_entry_id,
            p_weighment_slip_no,
            p_wbout_datetime,
            p_gross_weight,
            p_tare_weight,
            NOW()
        );

    END IF;

    -- UPDATE GATE ENTRY
    UPDATE gate_entries
    SET
        status = 'GATE_OUT',
        weighment_slip_no = p_weighment_slip_no,
        gate_out_datetime = p_wbout_datetime,
        updated_at = NOW()
    WHERE id = p_gate_entry_id;

    -- RETURN RESULT
    SELECT
        wo.*,
        ge.gate_in_no,
        ge.vehicle_id,
        vm.vehicle_no,
        vm.transporter_name,
        ge.direction,
        ge.status,
        ge.gate_out_datetime
    FROM wbout_records wo
    JOIN gate_entries ge
        ON ge.id = wo.gate_entry_id
    LEFT JOIN vehicle_master vm
        ON vm.id = ge.vehicle_id
    WHERE wo.gate_entry_id = p_gate_entry_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_delete_party` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_delete_party`(
    IN p_id INT
)
BEGIN

    -- CHECK USAGE
    IF EXISTS (SELECT 1 FROM vessels WHERE party_id = p_id) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete: linked with vessels';
    END IF;

    DELETE FROM party_masters WHERE id = p_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_gate_out` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_gate_out`(
    IN p_gate_id INT,
    IN p_gate_out_datetime DATETIME
)
BEGIN
    -- ✅ VALIDATION
    IF p_gate_out_datetime IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'gate_out_datetime required';
    END IF;

    -- ✅ UPDATE
    UPDATE gate_entries
    SET 
        gate_out_datetime = p_gate_out_datetime,
        status = 'COMPLETED',
        updated_at = NOW()
    WHERE id = p_gate_id;

    -- ✅ RETURN UPDATED RECORD
    SELECT 
        ge.*,
        vm.vehicle_no,
        vm.transporter_name
    FROM gate_entries ge
    LEFT JOIN vehicle_master vm ON ge.vehicle_id = vm.id
    WHERE ge.id = p_gate_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_cargo_operation` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_get_cargo_operation`(
    IN p_operation_id INT
)
BEGIN

    SELECT 
        co.id,
        co.gate_entry_id,
        co.vessel_id,
        co.operation_type,
        co.start_datetime,
        co.end_datetime,
        co.compressor_no,
        co.remarks,
        co.created_at,

        v.vessel_name,
        v.direction,

        p.party_name

    FROM cargo_operations co
    LEFT JOIN vessels v ON co.vessel_id = v.id
    LEFT JOIN party_masters p ON v.party_id = p.id
    WHERE co.id = p_operation_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_gate_entries` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_get_gate_entries`(
    IN p_vessel_id INT,
    IN p_status VARCHAR(50),
    IN p_limit INT,
    IN p_offset INT
)
BEGIN

    -- ✅ TOTAL COUNT
    SELECT COUNT(DISTINCT ge.id) AS total
    FROM gate_entries ge
    LEFT JOIN cargo_operations co ON co.gate_entry_id = ge.id
    WHERE
        (p_vessel_id IS NULL OR co.vessel_id = p_vessel_id)
        AND (p_status IS NULL OR ge.status = p_status);

    -- ✅ MAIN DATA (NO DUPLICATION ISSUE)
    SELECT 
        ge.id,
        ge.gate_in_no,
        ge.gate_in_datetime,
        ge.party_id,
        ge.vehicle_id,
        ge.challan_invoice_no,
        ge.weighment_slip_no,
        ge.outside_payment_slip,
        ge.outside_weight,
        ge.own_weighbridge,
        ge.status,
        ge.direction,
        ge.gate_out_datetime,
        ge.created_at,
        ge.updated_at,

        -- ✅ PARTY
        pm.party_name,
        pm.party_code,

        -- ✅ VEHICLE
        vm.vehicle_no,
        vm.transporter_name,

        -- ✅ ONE VESSEL PER GATE ENTRY (latest cargo_operation)
        v.id AS vessel_id,
        v.vessel_name,
        v.berthing_datetime,
        v.mooring_datetime,
        v.direction AS vessel_direction,

        co.id AS cargo_operation_id,
        co.compressor_no

    FROM gate_entries ge

    LEFT JOIN party_masters pm 
        ON pm.id = ge.party_id

    LEFT JOIN vehicle_master vm 
        ON vm.id = ge.vehicle_id

    -- ✅ pick latest cargo_operation per gate_entry
    LEFT JOIN cargo_operations co 
        ON co.id = (
            SELECT c2.id 
            FROM cargo_operations c2
            WHERE c2.gate_entry_id = ge.id
            ORDER BY c2.id DESC
            LIMIT 1
        )

    LEFT JOIN vessels v 
        ON v.id = co.vessel_id

    WHERE
        (p_vessel_id IS NULL OR v.id = p_vessel_id)
        AND (p_status IS NULL OR ge.status = p_status)

    ORDER BY ge.gate_in_datetime DESC
    LIMIT p_limit OFFSET p_offset;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_parties` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_get_parties`()
BEGIN
    SELECT * FROM party_masters ORDER BY id DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_party` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_get_party`(
    IN p_id INT
)
BEGIN
    SELECT * FROM party_masters WHERE id = p_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_get_weighments` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_get_weighments`(
    IN p_gate_entry_id INT
)
BEGIN

    -- =========================
    -- WBIN
    -- =========================
    SELECT 
        wr.* 
    FROM wbin_records wr
    WHERE wr.gate_entry_id = p_gate_entry_id;

    -- =========================
    -- WBOUT
    -- =========================
    SELECT 
        wo.* 
    FROM wbout_records wo
    WHERE wo.gate_entry_id = p_gate_entry_id;

    -- =========================
    -- CARGO OPERATIONS
    -- =========================
    SELECT 
        co.*,
        v.vessel_name,
        v.direction,
        p.party_name
    FROM cargo_operations co
    LEFT JOIN vessels v ON co.vessel_id = v.id
    LEFT JOIN party_masters p ON v.party_id = p.id
    WHERE co.gate_entry_id = p_gate_entry_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_truncate_dock_management_tables` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_truncate_dock_management_tables`()
BEGIN
    -- Disable foreign key checks
    SET FOREIGN_KEY_CHECKS = 0;

    TRUNCATE TABLE cargo_operations;
    TRUNCATE TABLE vessels;
    TRUNCATE TABLE vehicle_master;
    TRUNCATE TABLE gate_entries;
    TRUNCATE TABLE wbin_records;
    TRUNCATE TABLE rate_master;
    TRUNCATE TABLE bill_details;
    TRUNCATE TABLE bill_main;
    TRUNCATE TABLE party_masters;

    -- Enable foreign key checks again
    SET FOREIGN_KEY_CHECKS = 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_update_cargo_operation` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_update_cargo_operation`(
    IN p_operation_id INT,
    IN p_start_datetime DATETIME,
    IN p_end_datetime DATETIME,
    IN p_compressor_no VARCHAR(30),
    IN p_remarks TEXT
)
BEGIN
    DECLARE v_gate_entry_id INT;
    DECLARE v_exists INT DEFAULT 0;

    -- =========================
    -- VALIDATION
    -- =========================
    SELECT COUNT(*)
      INTO v_exists
      FROM cargo_operations
     WHERE id = p_operation_id;

    IF v_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cargo operation not found';
    END IF;

    -- =========================
    -- FETCH gate_entry_id
    -- =========================
    SELECT gate_entry_id
      INTO v_gate_entry_id
      FROM cargo_operations
     WHERE id = p_operation_id
     LIMIT 1;

    -- =========================
    -- UPDATE (only non-null inputs)
    -- =========================
    UPDATE cargo_operations
       SET start_datetime = IFNULL(p_start_datetime, start_datetime),
           end_datetime   = IFNULL(p_end_datetime, end_datetime),
           compressor_no  = IFNULL(p_compressor_no, compressor_no),
           remarks        = IFNULL(p_remarks, remarks),
           updated_at     = NOW()
     WHERE id = p_operation_id;

    -- =========================
    -- STATUS LOGIC
    -- =========================
    -- If end_datetime is provided → move to PENDING_WBOUT
    IF p_end_datetime IS NOT NULL THEN
        UPDATE gate_entries
           SET status = 'PENDING_WBOUT',
               updated_at = NOW()
         WHERE id = v_gate_entry_id;
    ELSEIF p_start_datetime IS NOT NULL THEN
        -- If only start provided (no end) → UNLOADING (or LOADING based on your convention)
        UPDATE gate_entries
           SET status = 'UNLOADING',
               updated_at = NOW()
         WHERE id = v_gate_entry_id;
    END IF;

    -- =========================
    -- RETURN UPDATED RECORD
    -- =========================
    SELECT 
        co.*,
        v.vessel_name,
        v.direction,
        p.party_name
    FROM cargo_operations co
    LEFT JOIN vessels v ON co.vessel_id = v.id
    LEFT JOIN party_masters p ON v.party_id = p.id
    WHERE co.id = p_operation_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sp_update_party` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`aiinhome`@`%` PROCEDURE `sp_update_party`(
    IN p_id INT,
    IN p_party_name VARCHAR(150),
    IN p_party_code VARCHAR(50),
    IN p_address TEXT,
    IN p_state VARCHAR(100),
    IN p_country VARCHAR(100),
    IN p_pincode VARCHAR(20),
    IN p_mobiles JSON,
    IN p_emails JSON,
    IN p_pan_number VARCHAR(20),
    IN p_gst_number VARCHAR(30)
)
BEGIN

    IF NOT EXISTS (SELECT 1 FROM party_masters WHERE id = p_id) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Party not found';
    END IF;

    UPDATE party_masters
    SET 
        party_name = IFNULL(p_party_name, party_name),
        party_code = IFNULL(p_party_code, party_code),
        address = IFNULL(p_address, address),
        state = IFNULL(p_state, state),
        country = IFNULL(p_country, country),
        pincode = IFNULL(p_pincode, pincode),
        mobiles = IFNULL(p_mobiles, mobiles),
        emails = IFNULL(p_emails, emails),
        pan_number = IFNULL(p_pan_number, pan_number),
        gst_number = IFNULL(p_gst_number, gst_number),
        updated_at = NOW()
    WHERE id = p_id;

    SELECT * FROM party_masters WHERE id = p_id;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-18 13:37:54
