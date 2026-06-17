-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 72.61.226.68    Database: dock_management
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.24.04.2

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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill_details`
--

LOCK TABLES `bill_details` WRITE;
/*!40000 ALTER TABLE `bill_details` DISABLE KEYS */;
INSERT INTO `bill_details` VALUES (1,1,1,'Terminal Services',400.00,46.00,18400.00,'',18.00,3312.00,'2026-05-12 06:31:17'),(2,1,1,'Handling service',400.00,170.00,68000.00,'',18.00,12240.00,'2026-05-12 06:31:18'),(3,1,1,'Berthing charges',2.00,3000.00,6000.00,'',18.00,1080.00,'2026-05-12 06:31:19'),(4,1,1,'Mooring charges',4.00,4000.00,16000.00,'',12.00,1920.00,'2026-05-12 06:31:19'),(5,1,1,'Truck entry charges',1.00,100.00,100.00,'',18.00,18.00,'2026-05-12 06:31:19'),(6,1,1,'Weighment charges',1.00,250.00,250.00,'',18.00,45.00,'2026-05-12 06:31:20'),(7,1,1,'Berthing Assistance',2.00,2000.00,4000.00,'',18.00,720.00,'2026-05-12 06:31:20'),(8,2,1,'Terminal Services',400.00,46.00,18400.00,'',18.00,3312.00,'2026-05-12 06:31:39'),(9,2,1,'Handling service',400.00,170.00,68000.00,'',18.00,12240.00,'2026-05-12 06:31:39'),(10,2,1,'Berthing charges',2.00,3000.00,6000.00,'',18.00,1080.00,'2026-05-12 06:31:40'),(11,2,1,'Mooring charges',4.00,4000.00,16000.00,'',12.00,1920.00,'2026-05-12 06:31:40'),(12,2,1,'Truck entry charges',1.00,100.00,100.00,'',18.00,18.00,'2026-05-12 06:31:41'),(13,2,1,'Weighment charges',1.00,250.00,250.00,'',18.00,45.00,'2026-05-12 06:31:41'),(14,2,1,'Berthing Assistance',2.00,2000.00,4000.00,'',18.00,720.00,'2026-05-12 06:31:41'),(15,3,3,'Terminal Services',1300.00,46.00,59800.00,'',18.00,10764.00,'2026-05-12 11:47:47'),(16,3,3,'Handling service',1300.00,170.00,221000.00,'',18.00,39780.00,'2026-05-12 11:47:47'),(17,3,3,'Berthing charges',1.00,3000.00,3000.00,'',18.00,540.00,'2026-05-12 11:47:48'),(18,3,3,'Mooring charges',1.00,4000.00,4000.00,'',12.00,480.00,'2026-05-12 11:47:48'),(19,3,3,'Truck entry charges',1.00,100.00,100.00,'',18.00,18.00,'2026-05-12 11:47:49'),(20,3,3,'Berthing Assistance',1.00,2000.00,2000.00,'',18.00,360.00,'2026-05-12 11:47:49'),(21,4,4,'Terminal Services',500.00,46.00,23000.00,'',18.00,4140.00,'2026-05-18 09:20:00'),(22,4,4,'Handling service',500.00,170.00,85000.00,'',18.00,15300.00,'2026-05-18 09:20:00'),(23,4,4,'Berthing charges',1.00,3000.00,3000.00,'',18.00,540.00,'2026-05-18 09:20:00'),(24,4,4,'Mooring charges',1.00,4000.00,4000.00,'',12.00,480.00,'2026-05-18 09:20:01'),(25,4,4,'Berthing Assistance',1.00,2000.00,2000.00,'',18.00,360.00,'2026-05-18 09:20:01'),(26,5,4,'Terminal Services',500.00,46.00,23000.00,'',18.00,4140.00,'2026-05-18 09:47:31'),(27,5,4,'Handling service',500.00,170.00,85000.00,'',18.00,15300.00,'2026-05-18 09:47:31'),(28,5,4,'Berthing charges',1.00,3000.00,3000.00,'',18.00,540.00,'2026-05-18 09:47:31'),(29,5,4,'Mooring charges',1.00,4000.00,4000.00,'',12.00,480.00,'2026-05-18 09:47:32'),(30,5,4,'Truck entry charges',5.00,100.00,500.00,'',18.00,90.00,'2026-05-18 09:47:32'),(31,5,4,'Berthing Assistance',1.00,2000.00,2000.00,'',18.00,360.00,'2026-05-18 09:47:32');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill_main`
--

LOCK TABLES `bill_main` WRITE;
/*!40000 ALTER TABLE `bill_main` DISABLE KEYS */;
INSERT INTO `bill_main` VALUES (1,'BILL-20260512023115','2026-05-12',1,'2026-05-11','2026-05-14','',112750.00,9667.50,9667.50,0.00,0.00,132085.00,'2026-05-12 06:31:17','2026-05-12 06:31:17'),(2,'BILL-20260512023138','2026-05-12',1,'2026-05-11','2026-05-14','',112750.00,9667.50,9667.50,0.00,0.00,132085.00,'2026-05-12 06:31:39','2026-05-12 06:31:39'),(3,'BILL-20260512074745','2026-05-12',1,'2026-05-01','2026-05-13','',289900.00,25971.00,25971.00,0.00,0.00,341842.00,'2026-05-12 11:47:47','2026-05-12 11:47:47'),(4,'BILL-20260518051959','2026-05-18',5,'2026-05-17','2026-05-18','',117000.00,10410.00,10410.00,0.00,0.00,137820.00,'2026-05-18 09:20:00','2026-05-18 09:20:00'),(5,'BILL-20260518054730','2026-05-18',5,'2026-05-17','2026-05-18','',117500.00,10455.00,10455.00,0.00,0.00,138410.00,'2026-05-18 09:47:31','2026-05-18 09:47:31');
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
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargo_operations`
--

LOCK TABLES `cargo_operations` WRITE;
/*!40000 ALTER TABLE `cargo_operations` DISABLE KEYS */;
INSERT INTO `cargo_operations` VALUES (1,1,1,'UNLOADING','2026-05-12 11:48:00','2026-05-12 11:49:00','12234','','2026-05-12 11:49:21','2026-05-12 11:49:54'),(2,3,3,'UNLOADING','2026-05-12 17:13:00','2026-05-12 17:14:00','','','2026-05-12 17:14:09','2026-05-12 17:14:40'),(3,7,4,'UNLOADING','2026-05-18 15:10:00','2026-05-18 15:13:00','E01','','2026-05-18 15:11:03','2026-05-18 15:13:44'),(4,8,4,'UNLOADING','2026-05-18 15:11:00','2026-05-18 15:13:00','E02','','2026-05-18 15:11:24','2026-05-18 15:14:00'),(5,6,4,'UNLOADING','2026-05-18 15:11:00','2026-05-18 15:14:00','E03','','2026-05-18 15:11:44','2026-05-18 15:14:13'),(6,5,4,'UNLOADING','2026-05-18 15:12:00','2026-05-18 15:14:00','E04','','2026-05-18 15:12:22','2026-05-18 15:14:26'),(7,4,4,'UNLOADING','2026-05-18 15:12:00','2026-05-18 15:14:00','E05','','2026-05-18 15:12:58','2026-05-18 15:14:38'),(9,17,7,'LOADING','2026-05-19 21:35:00','2026-05-19 21:36:00','678','34','2026-05-19 21:36:20','2026-05-19 21:36:36'),(10,18,7,'LOADING','2026-05-19 21:37:00','2026-05-19 21:38:00','234','23','2026-05-19 21:38:08','2026-05-19 21:38:22'),(11,20,9,'LOADING','2026-05-19 22:25:00','2026-05-19 22:25:00','888','555','2026-05-19 22:25:43','2026-05-19 22:26:02'),(12,19,9,'LOADING','2026-05-20 10:10:00','2026-05-20 10:10:00','55','88','2026-05-20 10:10:44','2026-05-20 10:10:56'),(13,22,9,'LOADING','2026-05-20 10:19:00','2026-05-20 10:19:00','5888','899','2026-05-20 10:19:31','2026-05-20 10:19:49'),(14,25,10,'UNLOADING','2026-06-01 13:13:00','2026-06-01 13:45:00','12345','','2026-06-01 13:15:19','2026-06-01 13:15:49'),(15,28,11,'UNLOADING','2026-03-29 11:17:00','2026-06-01 16:03:00','1234569','','2026-06-01 16:01:33','2026-06-01 16:03:49'),(16,35,7,'LOADING','2026-06-04 15:54:00','2026-06-04 17:00:00','C1','','2026-06-04 15:55:31','2026-06-04 15:56:01'),(17,41,11,'UNLOADING','2026-06-05 17:34:00','2026-06-05 17:36:00','','','2026-06-05 17:35:39','2026-06-05 17:37:24'),(18,43,11,'UNLOADING','2026-06-06 08:46:00','2026-06-06 08:46:00','','','2026-06-06 08:46:34','2026-06-06 08:46:53'),(19,45,11,'UNLOADING','2026-03-30 10:43:00','2026-03-30 11:08:00','','','2026-06-06 13:27:36','2026-06-06 13:28:25'),(20,46,11,'UNLOADING','2026-03-30 10:40:00','2026-03-30 11:09:00','','','2026-06-06 13:36:45','2026-06-06 13:37:36'),(21,2,11,'UNLOADING','2026-06-06 16:20:00',NULL,'','','2026-06-06 16:21:25','2026-06-06 16:21:25');
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
  `own_weighbridge` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1=Yes (>=60T, skip WBIN), 0=No (needs WBIN)',
  `direction` varchar(10) DEFAULT NULL,
  `status` enum('PENDING_WBIN','WBIN_DONE','UNLOADING','PENDING_WBOUT','GATE_OUT','COMPLETED') NOT NULL DEFAULT 'PENDING_WBIN',
  `gate_out_datetime` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `outside_gross_weight` decimal(10,2) DEFAULT NULL,
  `outside_tare_weight` decimal(10,2) DEFAULT NULL,
  `outside_net_weight` decimal(10,2) GENERATED ALWAYS AS ((case when ((`outside_gross_weight` is not null) and (`outside_tare_weight` is not null)) then (`outside_gross_weight` - `outside_tare_weight`) else NULL end)) STORED,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gate_in_no` (`gate_in_no`),
  KEY `idx_status` (`status`),
  KEY `idx_gate_in_datetime` (`gate_in_datetime`),
  KEY `fk_vehicle` (`vehicle_id`),
  KEY `fk_gate_entries_party` (`party_id`),
  CONSTRAINT `fk_gate_entries_party` FOREIGN KEY (`party_id`) REFERENCES `party_masters` (`id`),
  CONSTRAINT `fk_vehicle` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle_master` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gate_entries`
--

LOCK TABLES `gate_entries` WRITE;
/*!40000 ALTER TABLE `gate_entries` DISABLE KEYS */;
INSERT INTO `gate_entries` (`id`, `gate_in_no`, `gate_in_datetime`, `party_id`, `vehicle_id`, `challan_invoice_no`, `weighment_slip_no`, `outside_payment_slip`, `own_weighbridge`, `direction`, `status`, `gate_out_datetime`, `created_at`, `updated_at`, `outside_gross_weight`, `outside_tare_weight`) VALUES (1,'GIN-2026-00001','2026-05-12 11:36:00',1,1,'CH12345','12345',NULL,0,'EXPORT','COMPLETED','2026-05-12 11:56:00','2026-05-12 11:43:28','2026-05-12 11:56:47',NULL,NULL),(2,'GIN-2026-00002','2026-05-10 14:05:00',2,3,'12012','4101',NULL,1,'EXPORT','UNLOADING',NULL,'2026-05-12 16:57:18','2026-06-06 16:21:25',NULL,NULL),(3,'GIN-2026-00003','2026-05-12 17:11:00',2,3,'1200','46452',NULL,1,'EXPORT','COMPLETED','2026-05-18 16:05:00','2026-05-12 17:12:41','2026-05-18 16:05:27',NULL,NULL),(4,'GIN-2026-00004','2026-05-18 14:38:00',5,6,'A1234','001',NULL,1,'EXPORT','COMPLETED','2026-05-18 15:16:00','2026-05-18 14:40:25','2026-05-18 15:16:32',NULL,NULL),(5,'GIN-2026-00005','2026-05-18 14:40:00',5,7,'B1234','002',NULL,1,'EXPORT','COMPLETED','2026-05-18 15:16:00','2026-05-18 14:41:38','2026-05-18 15:16:23',NULL,NULL),(6,'GIN-2026-00006','2026-05-18 14:41:00',5,8,'C1234','003',NULL,1,'EXPORT','COMPLETED','2026-05-18 15:16:00','2026-05-18 14:44:56','2026-05-18 15:16:15',NULL,NULL),(7,'GIN-2026-00007','2026-05-18 14:45:00',5,9,'D1234','004',NULL,1,'EXPORT','COMPLETED','2026-05-18 15:15:00','2026-05-18 14:45:45','2026-05-18 15:16:01',NULL,NULL),(8,'GIN-2026-00008','2026-05-18 14:45:00',5,10,'E1234','005',NULL,1,'EXPORT','COMPLETED','2026-05-18 15:16:00','2026-05-18 14:46:33','2026-05-18 15:16:08',NULL,NULL),(9,'GIN-2026-00009','2026-05-12 12:28:00',9,11,'983','44486',NULL,1,'EXPORT','WBIN_DONE',NULL,'2026-05-18 15:44:21','2026-05-18 15:44:21',NULL,NULL),(10,'GIN-2026-00010','2026-05-13 00:20:00',9,12,'94096','44488',NULL,1,'EXPORT','WBIN_DONE',NULL,'2026-05-18 15:45:20','2026-05-18 15:45:20',NULL,NULL),(11,'GIN-2026-00011','2026-05-12 22:36:00',9,13,'92689','72018',NULL,1,'EXPORT','WBIN_DONE',NULL,'2026-05-18 15:46:23','2026-05-18 15:46:23',NULL,NULL),(12,'GIN-2026-00012','2026-05-12 22:40:00',9,14,'92688','72014',NULL,1,'EXPORT','WBIN_DONE',NULL,'2026-05-18 15:47:44','2026-05-18 15:47:44',NULL,NULL),(13,'GIN-2026-00013','2026-05-13 00:01:00',9,15,'94097','44555',NULL,1,'EXPORT','WBIN_DONE',NULL,'2026-05-18 15:48:57','2026-05-18 15:48:57',NULL,NULL),(14,'GIN-2026-00014','2026-05-11 13:52:00',9,16,'94078','44390',NULL,1,'EXPORT','WBIN_DONE',NULL,'2026-05-18 15:50:10','2026-05-18 15:50:10',NULL,NULL),(15,'GIN-2026-00015','2026-05-11 14:32:00',9,15,'94079','44393',NULL,1,'EXPORT','WBIN_DONE',NULL,'2026-05-18 15:52:12','2026-05-18 15:52:12',NULL,NULL),(16,'GIN-2026-00016','2026-05-11 14:13:00',9,19,'94080','44396',NULL,1,'EXPORT','WBIN_DONE',NULL,'2026-05-18 15:55:15','2026-05-18 15:55:15',NULL,NULL),(17,'GIN-2026-00017','2026-05-19 06:36:00',9,1,'5','5',NULL,0,'IMPORT','COMPLETED','2026-05-19 21:36:00','2026-05-19 06:36:33','2026-05-19 21:37:05',NULL,NULL),(18,'GIN-2026-00018','2026-05-19 11:26:00',9,2,'123456','123456',NULL,0,'IMPORT','COMPLETED','2026-05-19 21:38:00','2026-05-19 11:32:15','2026-05-19 21:38:54',55.00,13.00),(19,'GIN-2026-00019','2026-05-19 17:48:00',14,1,'556','8899',NULL,0,'IMPORT','COMPLETED','2026-05-20 10:11:00','2026-05-19 17:49:12','2026-05-20 10:11:16',5578.00,556.00),(20,'GIN-2026-00020','2026-05-19 21:25:00',16,1,'654321','6789',NULL,0,'IMPORT','COMPLETED','2026-05-08 22:27:00','2026-05-19 21:25:51','2026-05-19 22:27:42',8.00,5.00),(21,'GIN-2026-00021','2026-05-20 10:14:00',16,3,'55','555',NULL,0,'EXPORT','WBIN_DONE',NULL,'2026-05-20 10:14:42','2026-05-20 10:15:04',266.00,666.00),(22,'GIN-2026-00022','2026-05-20 10:16:00',16,2,'5555','7789',NULL,0,'IMPORT','COMPLETED','2026-05-17 10:20:00','2026-05-20 10:17:17','2026-05-20 10:20:34',6658.00,996.00),(23,'GIN-2026-00023','2026-05-23 16:33:00',16,1,'546464','4464646',NULL,0,'IMPORT','PENDING_WBIN',NULL,'2026-05-23 16:35:55','2026-05-23 16:35:55',55.00,12.00),(24,'GIN-2026-00024','2026-06-01 13:02:00',16,1,'dfdfdsf','slip1234',NULL,0,'IMPORT','PENDING_WBIN',NULL,'2026-06-01 13:04:48','2026-06-01 13:04:48',50.00,30.00),(25,'GIN-2026-00025','2026-06-01 13:05:00',15,2,'dfsdfds','slip123456er',NULL,0,'EXPORT','COMPLETED','2026-06-01 13:16:00','2026-06-01 13:06:09','2026-06-01 13:16:36',50.00,31.00),(26,'GIN-2026-00026','2026-06-01 14:02:00',17,20,'38557','40350',NULL,0,'IMPORT','WBIN_DONE',NULL,'2026-06-01 14:06:36','2026-06-01 14:08:40',56.72,16.20),(27,'GIN-2026-00027','2026-03-29 08:58:00',17,20,'38557','40350',NULL,0,'EXPORT','PENDING_WBIN',NULL,'2026-06-01 15:29:10','2026-06-01 15:29:10',56.72,16.20),(28,'GIN-2026-00028','2026-06-01 15:31:00',17,21,'38563','40355',NULL,1,'EXPORT','COMPLETED','2026-06-01 16:05:00','2026-06-01 15:54:40','2026-06-01 16:05:35',60.14,16.08),(29,'GIN-2026-00029','2026-03-29 12:53:00',17,23,'38572','40378',NULL,1,'EXPORT','WBIN_DONE',NULL,'2026-06-01 16:27:24','2026-06-01 16:27:24',61.24,17.02),(30,'GIN-2026-00030','2026-03-29 10:35:00',17,22,'38570','40374',NULL,0,'EXPORT','PENDING_WBIN',NULL,'2026-06-01 16:40:32','2026-06-01 16:40:32',54.88,17.68),(31,'GIN-2026-00031','2026-03-29 12:53:00',17,23,'38572','40378',NULL,0,'EXPORT','PENDING_WBIN',NULL,'2026-06-01 16:47:53','2026-06-01 16:47:53',61.24,17.02),(32,'GIN-2026-00032','2026-03-29 04:25:00',17,24,'38581','40411',NULL,0,'EXPORT','PENDING_WBIN',NULL,'2026-06-01 16:53:33','2026-06-01 16:53:33',61.14,16.62),(33,'GIN-2026-00033','2026-03-29 12:53:00',17,23,'38572','40378',NULL,0,'EXPORT','PENDING_WBIN',NULL,'2026-06-01 17:50:30','2026-06-01 17:50:30',61.24,16.02),(34,'GIN-2026-00034','2026-03-29 21:42:00',17,21,'38587','40437',NULL,0,'EXPORT','PENDING_WBIN',NULL,'2026-06-04 11:49:50','2026-06-04 11:49:50',59.52,16.00),(35,'GIN-2026-00035','2026-06-04 15:11:00',17,2,'123456','123456',NULL,0,'IMPORT','PENDING_WBOUT',NULL,'2026-06-04 15:12:24','2026-06-04 15:56:01',15.00,15.00),(36,'GIN-2026-00036','2026-06-04 15:53:00',9,2,'321','321',NULL,0,'EXPORT','PENDING_WBIN',NULL,'2026-06-04 15:54:14','2026-06-04 15:54:14',55.00,15.00),(37,'GIN-2026-00037','2026-03-29 18:14:00',17,1,'123','567',NULL,0,'IMPORT','PENDING_WBIN',NULL,'2026-06-04 18:14:48','2026-06-04 18:14:48',15.00,15.00),(38,'GIN-2026-00038','2026-06-04 18:20:00',13,2,'123','12356',NULL,0,'EXPORT','PENDING_WBIN',NULL,'2026-06-04 18:21:39','2026-06-04 18:21:39',100.00,20.00),(39,'GIN-2026-00039','2026-06-05 11:25:00',16,1,'4444','4444',NULL,0,'IMPORT','PENDING_WBIN',NULL,'2026-06-05 11:26:20','2026-06-05 11:26:20',55.00,15.00),(40,'GIN-2026-00040','2026-06-05 12:11:00',16,2,'222',NULL,'2222',0,'IMPORT','PENDING_WBIN',NULL,'2026-06-05 12:12:03','2026-06-05 12:12:03',56.00,15.00),(41,'GIN-2026-00041','2026-06-05 17:32:00',17,28,'38586',NULL,'40448',1,'EXPORT','PENDING_WBOUT',NULL,'2026-06-05 17:34:25','2026-06-05 17:37:24',78.02,19.26),(42,'GIN-2026-00042','2026-03-29 17:48:00',17,23,'38593','40444','40444',0,'EXPORT','WBIN_DONE',NULL,'2026-06-05 17:54:32','2026-06-05 18:30:49',60.00,NULL),(43,'GIN-2026-00043','2026-03-30 06:01:00',17,33,'38596','40446','40446',0,'EXPORT','GATE_OUT','2026-06-06 08:47:00','2026-06-06 08:41:47','2026-06-06 08:47:48',59.40,NULL),(44,'GIN-2026-00044','2026-03-30 07:50:00',17,22,'38600','40479',NULL,0,'EXPORT','WBIN_DONE',NULL,'2026-06-06 11:12:08','2026-06-06 11:16:56',NULL,NULL),(45,'GIN-2026-00045','2026-03-30 08:00:00',17,36,'38598','40478','40478',1,'EXPORT','COMPLETED','2026-03-30 11:14:00','2026-06-06 13:24:14','2026-06-06 13:50:26',55.88,17.60),(46,'GIN-2026-00046','2026-03-30 08:05:00',17,24,'38602','40480','40480',0,'EXPORT','COMPLETED','2026-03-30 11:15:00','2026-06-06 13:33:21','2026-06-06 13:54:36',59.52,16.54);
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
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `pan_number` varchar(20) DEFAULT NULL,
  `gst_number` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `party_code` (`party_code`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `party_masters`
--

LOCK TABLES `party_masters` WRITE;
/*!40000 ALTER TABLE `party_masters` DISABLE KEYS */;
INSERT INTO `party_masters` VALUES (1,'IRC Commercial','IRCC','1 sunyat sen street','West Bengal','India','700001','[\"1234567890\"]','[\"tdlkolkata@yahoo.com\"]','2026-05-12 05:57:08','2026-05-12 05:57:08',NULL,NULL),(2,' HAQUE TRADERS','002','8/2B, ABDUL HALIM LANE, TALTAKA, KOLKATA, 743338','WEST BENGAL','INDIA','743338','[\"1234567890\"]','[\"haque@gmail.com\"]','2026-05-12 11:21:59','2026-05-12 11:21:59',NULL,NULL),(3,'ABC','345','abh','abc','india','12345','[\"8976567896\"]','[\"abc@gmail.com\"]','2026-05-18 07:42:30','2026-05-18 07:42:30',NULL,NULL),(4,'ABC','890654','KOLKATA','WEST BENGAL','INDIA','700101','[\"8756908790\"]','[\"ABC789@gmail.com\"]','2026-05-18 08:02:04','2026-05-18 08:02:04',NULL,NULL),(5,'NMPL ','005','KOLKATA, 7000012','WEST BENGAL','INDIA','700012','[\"8456301470\"]','[\"nmpl@gmail.com\"]','2026-05-18 09:03:45','2026-05-18 09:03:45',NULL,NULL),(6,'k','p','l','i','l','721626','[\"9565689635\"]','[\"p@gmail.com\"]','2026-05-18 09:46:20','2026-05-18 09:46:20',NULL,NULL),(7,'l','india','lohjghjg','ll','i','721426','[\"8123456789\"]','[\"p@gmail.com\"]','2026-05-18 09:49:31','2026-05-18 09:49:31',NULL,NULL),(8,'cba','006','kolkata','wb','in','720001','[\"1234567896\"]','[\"k@gmail.com\"]','2026-05-18 09:54:08','2026-05-18 09:54:08',NULL,NULL),(9,'ICM PVT LTD','007','KOLKATA','WEST BENGAL','INDIA','700012','[\"8402460211\"]','[\"icm@.co.in\"]','2026-05-18 10:02:29','2026-05-18 10:02:29',NULL,NULL),(10,'k','45','kolkata','up','i','710003','[\"0123456789\"]','[\"l@gmail.com\"]','2026-05-19 01:44:54','2026-05-19 01:44:54',NULL,NULL),(11,'o','55','AP','MP','i','78965','[\"1234567890\"]','[\"V@gmail.com\"]','2026-05-19 05:56:55','2026-05-19 05:56:55',NULL,NULL),(13,'ABCD','12335','Tantigeriya, Midnapur, Paschim Medinipur , 721102','West Bengal','India','721102','[\"9945789630\"]','[\"dasman22@gmail.com\"]','2026-05-19 06:35:26','2026-05-19 06:35:26',NULL,NULL),(14,'k','l','up','up','i','700021','[\"0123456789\"]','[\"g@gmail.com\"]','2026-05-19 12:15:20','2026-05-19 12:15:20','5596963','855963'),(15,'k','a','kolkata','Wb','in','720001','[\"0123456789\"]','[\"l@gmail.com\"]','2026-05-19 12:36:00','2026-05-19 15:22:00','785GHK','558638547K'),(16,'1','2','3','4','5','687654','[\"9876554321\"]','[\"k@hmail.com\"]','2026-05-19 15:53:43','2026-05-19 15:53:43','7','8'),(17,'IRC Commercial Pvt. Ltd.','IRC','Kolkata','west bengal','India','700001','[\"1234567890\"]','[\"irc@gmail.com\"]','2026-06-01 08:03:23','2026-06-01 08:03:23',NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rate_master`
--

LOCK TABLES `rate_master` WRITE;
/*!40000 ALTER TABLE `rate_master` DISABLE KEYS */;
INSERT INTO `rate_master` VALUES (1,1,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-12 06:01:56'),(2,1,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-12 06:01:57'),(3,1,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-12 06:01:57'),(4,1,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-12 06:01:57'),(5,1,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-12 06:01:58'),(6,1,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-12 06:01:58'),(7,1,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-12 06:01:58'),(8,1,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-12 06:01:59'),(9,1,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-12 06:01:59'),(10,1,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-12 06:01:59'),(11,2,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-12 11:30:36'),(12,2,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-12 11:30:37'),(13,2,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-12 11:30:37'),(14,2,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-12 11:30:37'),(15,2,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-12 11:30:38'),(16,2,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-12 11:30:38'),(17,2,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-12 11:30:38'),(18,2,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-12 11:30:38'),(19,2,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-12 11:30:39'),(20,2,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-12 11:30:39'),(21,3,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-12 11:39:01'),(22,3,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-12 11:39:01'),(23,3,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-12 11:39:02'),(24,3,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-12 11:39:02'),(25,3,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-12 11:39:02'),(26,3,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-12 11:39:02'),(27,3,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-12 11:39:03'),(28,3,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-12 11:39:03'),(29,3,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-12 11:39:03'),(30,3,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-12 11:39:03'),(31,4,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-18 09:05:41'),(32,4,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-18 09:05:41'),(33,4,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-18 09:05:41'),(34,4,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-18 09:05:42'),(35,4,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-18 09:05:42'),(36,4,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-18 09:05:42'),(37,4,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-18 09:05:42'),(38,4,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-18 09:05:43'),(39,4,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-18 09:05:43'),(40,4,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-18 09:05:43'),(41,5,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-18 10:05:54'),(42,5,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-18 10:05:55'),(43,5,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-18 10:05:55'),(44,5,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-18 10:05:55'),(45,5,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-18 10:05:55'),(46,5,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-18 10:05:56'),(47,5,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-18 10:05:56'),(48,5,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-18 10:05:56'),(49,5,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-18 10:05:56'),(50,5,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-18 10:05:56'),(51,6,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-18 10:06:48'),(52,6,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-18 10:06:48'),(53,6,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-18 10:06:49'),(54,6,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-18 10:06:49'),(55,6,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-18 10:06:49'),(56,6,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-18 10:06:50'),(57,6,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-18 10:06:50'),(58,6,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-18 10:06:50'),(59,6,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-18 10:06:50'),(60,6,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-18 10:06:51'),(61,7,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-19 16:03:38'),(62,7,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-19 16:03:38'),(63,7,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-19 16:03:38'),(64,7,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-19 16:03:38'),(65,7,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-19 16:03:38'),(66,7,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-19 16:03:38'),(67,7,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-19 16:03:38'),(68,7,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-19 16:03:38'),(69,7,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-19 16:03:38'),(70,7,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-19 16:03:39'),(71,8,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-19 16:12:49'),(72,8,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-19 16:12:49'),(73,8,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-19 16:12:49'),(74,8,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-19 16:12:49'),(75,8,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-19 16:12:49'),(76,8,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-19 16:12:49'),(77,8,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-19 16:12:49'),(78,8,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-19 16:12:50'),(79,8,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-19 16:12:50'),(80,8,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-19 16:12:50'),(81,9,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-05-19 16:54:03'),(82,9,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-05-19 16:54:03'),(83,9,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-05-19 16:54:03'),(84,9,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-05-19 16:54:03'),(85,9,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-05-19 16:54:03'),(86,9,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-05-19 16:54:03'),(87,9,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-05-19 16:54:04'),(88,9,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-05-19 16:54:04'),(89,9,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-05-19 16:54:04'),(90,9,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-05-19 16:54:04'),(91,10,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-06-01 07:37:40'),(92,10,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-06-01 07:37:40'),(93,10,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-06-01 07:37:41'),(94,10,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-06-01 07:37:41'),(95,10,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-06-01 07:37:41'),(96,10,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-06-01 07:37:41'),(97,10,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-06-01 07:37:42'),(98,10,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-06-01 07:37:42'),(99,10,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-06-01 07:37:42'),(100,10,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-06-01 07:37:42'),(101,11,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-06-01 08:13:09'),(102,11,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-06-01 08:13:09'),(103,11,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-06-01 08:13:09'),(104,11,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-06-01 08:13:09'),(105,11,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-06-01 08:13:10'),(106,11,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-06-01 08:13:10'),(107,11,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-06-01 08:13:10'),(108,11,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-06-01 08:13:10'),(109,11,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-06-01 08:13:11'),(110,11,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-06-01 08:13:11'),(111,12,'Terminal Services','Logic1',46.00,18.00,0.00,0.00,'2026-06-04 13:32:36'),(112,12,'Handling service','Logic1',170.00,18.00,0.00,0.00,'2026-06-04 13:32:36'),(113,12,'Berthing charges','Logic3',3000.00,18.00,0.00,0.00,'2026-06-04 13:32:36'),(114,12,'Mooring charges','Logic4',4000.00,12.00,0.00,0.00,'2026-06-04 13:32:37'),(115,12,'Truck entry charges','Logic2',100.00,18.00,0.00,0.00,'2026-06-04 13:32:37'),(116,12,'Weighment charges','Logic6',250.00,18.00,0.00,0.00,'2026-06-04 13:32:37'),(117,12,'Parking charges','Logic7',100.00,5.00,0.00,0.00,'2026-06-04 13:32:37'),(118,12,'Berthing Assistance','Logic5',2000.00,18.00,1.00,1400.00,'2026-06-04 13:32:38'),(119,12,'Berthing Assistance','Logic5',4000.00,18.00,1401.00,2100.00,'2026-06-04 13:32:38'),(120,12,'Berthing Assistance','Logic5',5500.00,18.00,2101.00,10000.00,'2026-06-04 13:32:38');
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_access_rights`
--

LOCK TABLES `user_access_rights` WRITE;
/*!40000 ALTER TABLE `user_access_rights` DISABLE KEYS */;
INSERT INTO `user_access_rights` VALUES (1,1,'{\"modules\": [\"DASHBOARD\", \"VESSEL_OPS\", \"VEHICLE_LOGISTICS\", \"WEIGHBRIDGE_TERMINAL\", \"REPORTS_BILLING\", \"SETTINGS\", \"PARTY_MASTER\", \"VEHICLE_MASTER\"], \"gate_operations\": [\"PENDING_WBIN\", \"WBIN_DONE\", \"UNLOADING\", \"PENDING_WBOUT\", \"COMPLETED\", \"GATE_OUT\"], \"vessel_statuses\": [\"PLANNED\", \"BERTHED\", \"MOORED\", \"COMPLETED\"]}','2026-04-23 05:25:30','2026-04-24 12:30:01'),(2,2,'{}','2026-05-12 06:36:44','2026-05-12 06:36:44'),(3,3,'{\"modules\": [\"VEHICLE_MASTER\", \"VEHICLE_LOGISTICS\", \"DASHBOARD\"], \"gate_operations\": [\"GATE_OUT\", \"COMPLETED\"], \"vessel_statuses\": []}','2026-06-06 08:11:17','2026-06-06 08:12:40'),(4,4,'{\"modules\": [\"DASHBOARD\", \"VEHICLE_LOGISTICS\"], \"gate_operations\": [\"WBIN_DONE\", \"PENDING_WBIN\", \"PENDING_WBOUT\"], \"vessel_statuses\": []}','2026-06-06 08:26:58','2026-06-06 08:28:39'),(5,5,'{\"modules\": [\"VEHICLE_LOGISTICS\", \"DASHBOARD\"], \"gate_operations\": [\"UNLOADING\"], \"vessel_statuses\": []}','2026-06-06 08:29:32','2026-06-06 08:30:11'),(6,6,'{\"modules\": [\"VESSEL_OPS\"], \"gate_operations\": [], \"vessel_statuses\": [\"PLANNED\", \"BERTHED\", \"MOORED\", \"COMPLETED\"]}','2026-06-06 08:30:57','2026-06-06 08:31:53'),(7,7,'{\"modules\": [\"DASHBOARD\", \"PARTY_MASTER\", \"VEHICLE_MASTER\", \"REPORTS_BILLING\", \"VESSEL_OPS\", \"VEHICLE_LOGISTICS\"], \"gate_operations\": [\"PENDING_WBIN\", \"WBIN_DONE\", \"UNLOADING\", \"PENDING_WBOUT\", \"GATE_OUT\", \"COMPLETED\"], \"vessel_statuses\": [\"PLANNED\", \"BERTHED\", \"MOORED\", \"COMPLETED\"]}','2026-06-06 08:34:40','2026-06-06 08:35:25');
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','@admin','123456','admin','7894561230','admin@gmail.com',1,'2026-04-23 05:24:47','2026-04-23 05:24:47'),(2,'user','admin1','1234567','Loading user','12345578900','admin1@gmail.com',1,'2026-05-12 06:36:44','2026-05-12 06:36:44'),(3,'user','ABC','1234','GATE','1234567890','ABC@GMAIL.COM',1,'2026-06-06 08:11:17','2026-06-06 08:11:17'),(4,'user','WB','1234','WB','1234567890','WB@GMAIL.COM',1,'2026-06-06 08:26:57','2026-06-06 08:26:57'),(5,'user','OP','1234','OPERATIONS','1234567890','OP@GMAIL.COM',1,'2026-06-06 08:29:32','2026-06-06 08:29:32'),(6,'user','SHIP','1234','SHIP','1234567890','SHIP@GMAIL.COM',1,'2026-06-06 08:30:57','2026-06-06 08:30:57'),(7,'user','BACKOFFICE','1234','BACKOFFICE','1234567890','BACKOFFICE@GMAIL.COM',1,'2026-06-06 08:34:39','2026-06-06 08:34:39');
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
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle_master`
--

LOCK TABLES `vehicle_master` WRITE;
/*!40000 ALTER TABLE `vehicle_master` DISABLE KEYS */;
INSERT INTO `vehicle_master` VALUES (1,'WB 05 D 1234','RAM company',1),(2,'WB05 D 1236','ram company',1),(3,'WB12A 5104','HAQUE TRADERS',1),(4,'WB12A 4710','HAQUE TRADERS',1),(5,'WB12A 5410','A',1),(6,'WB01 A1234','NMPL',1),(7,'WB01 B1234','RAM',1),(8,'WB01 C1234','RAM',1),(9,'WB01 D1234','NMPL',1),(10,'WB01 E1234','NMPL',1),(11,'WB25K9779','A',1),(12,'WB25J6068','A',1),(13,'WB15L2635','A',1),(14,'WB29A9184','A',1),(15,'WB25K8226','A',1),(16,'WB25K7665','B',1),(19,'WB25J6068.','B',1),(20,'WB210776','speedways',1),(21,'WB11D1805','kamakhya roadways',1),(22,'WB210893','speedways',1),(23,'WB29C3313','maa tara roadways',1),(24,'WB11D1797','Transporter1',1),(28,'NL01AE9196','Transporter3',1),(33,'WB29C2670','TRANSPORTER',1),(36,'WB272846','transporter',1);
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
  `is_generated` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `vessel_auto_id` (`vessel_auto_id`),
  KEY `idx_status` (`status`),
  KEY `idx_expected_date` (`expected_date`),
  KEY `idx_party_name` (`party_id`),
  CONSTRAINT `fk_party` FOREIGN KEY (`party_id`) REFERENCES `party_masters` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vessels`
--

LOCK TABLES `vessels` WRITE;
/*!40000 ALTER TABLE `vessels` DISABLE KEYS */;
INSERT INTO `vessels` VALUES (1,'VSL-2026-0001','MV HAQUE -12.05.2026',1,'FLYASH',500.00,'EXPORT','COMPLETED','2026-05-14','2026-05-13 11:32:00','2026-05-13 11:33:00',400.00,'2026-05-13 11:58:00','2026-05-14 11:59:00','2026-05-12 11:31:56','2026-05-12 11:59:42'),(2,'VSL-2026-0002','M.V. TARA - 5',2,'FLYASH',1200.00,'EXPORT','COMPLETED','2026-05-12','2026-05-13 21:01:00','2026-05-13 22:02:00',NULL,NULL,'2026-05-12 17:16:00','2026-05-12 17:00:36','2026-05-12 17:16:56'),(3,'VSL-2026-0003','M.V  PAWANSUTH',1,'COAL',1000.00,'EXPORT','COMPLETED','2026-05-12','2026-05-12 17:09:00','2026-05-12 17:09:00',1300.00,'2026-05-12 17:16:00','2026-05-12 17:16:00','2026-05-12 17:09:01','2026-05-12 17:16:42'),(4,'VSL-2026-0004','M.V. NMPL - 1',5,'FLYASH',1600.00,'EXPORT','COMPLETED','2026-05-18','2026-05-18 06:00:00','2026-05-18 14:37:00',500.00,'2026-05-18 14:47:00','2026-05-18 15:49:00','2026-05-18 14:35:41','2026-05-18 14:49:14'),(5,'VSL-2026-0005','M.V. RAMISHA -1',9,'FLYASH',1200.00,'EXPORT','COMPLETED','2026-05-12','2026-05-12 06:00:00','2026-05-12 17:45:00',NULL,NULL,'2026-05-18 16:03:00','2026-05-18 15:35:54','2026-05-18 16:03:32'),(6,'VSL-2026-0006','M.V NAWSIHN HOSSAIN - 1',9,'FLYASH',1250.00,'EXPORT','COMPLETED','2026-05-11','2026-05-11 06:00:00','2026-05-11 16:50:00',NULL,NULL,'2026-05-18 16:03:00','2026-05-18 15:36:48','2026-05-18 16:03:20'),(7,'VSL-2026-0007','RRR',16,'COAL',5.00,'IMPORT','COMPLETED','2026-05-19','2026-05-19 21:33:00','2026-05-19 21:34:00',0.03,'2026-05-19 21:34:00','2026-05-19 21:34:00','2026-05-19 21:33:38','2026-05-19 21:35:05'),(8,'VSL-2026-0008','GHG',15,'FLYASH',6.00,'EXPORT','COMPLETED','2026-06-23','2026-05-19 21:43:00','2026-05-19 21:43:00',NULL,NULL,'2026-05-19 21:43:00','2026-05-19 21:42:49','2026-05-19 21:43:21'),(9,'VSL-2026-0009','ppp',15,'bbb',545.00,'IMPORT','COMPLETED','2026-05-09','2026-05-19 22:24:00',NULL,NULL,NULL,'2026-05-19 22:24:00','2026-05-19 22:24:03','2026-05-19 22:24:43'),(10,'VSL-2026-0010','mv1234/1.6.26',15,'flysasj',500.00,'EXPORT','COMPLETED','2026-06-01','2026-06-01 13:07:00','2026-06-01 13:09:00',50.00,'2026-06-01 13:19:00','2026-06-01 13:20:00','2026-06-01 13:07:40','2026-06-01 13:21:19'),(11,'VSL-2026-0011','M.V.GULSHAN-2/29.03.26',17,'FLYASH',1096.00,'EXPORT','MOORED','2026-06-01','2026-03-29 06:00:00','2026-06-06 16:27:00',NULL,NULL,NULL,'2026-06-01 13:43:08','2026-06-06 16:27:30'),(12,'VSL-2026-0012','BH Durga ',1,'Oil',586.00,'IMPORT','PLANNED','2026-06-04',NULL,NULL,NULL,NULL,NULL,'2026-06-04 19:02:36','2026-06-04 19:02:36');
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wbin_records`
--

LOCK TABLES `wbin_records` WRITE;
/*!40000 ALTER TABLE `wbin_records` DISABLE KEYS */;
INSERT INTO `wbin_records` VALUES (1,1,'12345','2026-05-12 11:36:00',40.200,NULL,'2026-05-12 11:43:35'),(2,17,'5','2026-05-19 06:36:00',NULL,5555.000,'2026-05-19 06:36:39'),(3,18,'123456','2026-05-19 11:32:00',NULL,12.000,'2026-05-19 11:33:04'),(4,19,'8899','2026-05-19 20:42:00',NULL,4.000,'2026-05-19 20:42:13'),(5,20,'6789','2026-05-19 21:26:00',NULL,3.000,'2026-05-19 21:26:16'),(6,21,'555','2026-05-20 10:14:00',555.000,NULL,'2026-05-20 10:15:04'),(7,22,'7789','2026-05-20 10:17:00',NULL,88.000,'2026-05-20 10:17:36'),(8,25,'slip123456er','2026-06-01 13:06:00',50.500,NULL,'2026-06-01 13:06:37'),(9,26,'40350','2026-06-01 14:07:00',NULL,16.200,'2026-06-01 14:08:40'),(10,35,'123456','2026-06-04 15:54:00',NULL,12.000,'2026-06-04 15:54:46'),(11,42,'40444','2026-06-05 17:57:00',60.940,NULL,'2026-06-05 18:30:49'),(12,43,'40446','2026-06-06 08:43:00',59.400,NULL,'2026-06-06 08:45:55'),(13,44,'40479','2026-03-30 07:50:00',53.620,NULL,'2026-06-06 11:16:56'),(14,46,'40480','2026-06-06 13:34:00',59.520,NULL,'2026-06-06 13:35:30');
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wbout_records`
--

LOCK TABLES `wbout_records` WRITE;
/*!40000 ALTER TABLE `wbout_records` DISABLE KEYS */;
INSERT INTO `wbout_records` (`id`, `gate_entry_id`, `weighment_slip_no`, `wbout_datetime`, `gross_weight`, `tare_weight`, `created_at`) VALUES (1,1,'12345','2026-05-12 11:54:00',NULL,14.280,'2026-04-24 16:04:36'),(2,10,'125896','2026-04-25 15:15:00',59.000,NULL,'2026-04-25 15:18:50'),(3,11,'789456','2026-04-25 10:40:00',NULL,55.000,'2026-04-27 10:40:19'),(4,12,'7894566','2026-04-20 11:30:00',NULL,12.000,'2026-04-27 11:30:54'),(5,14,'7895623','2026-04-27 19:31:00',58.000,NULL,'2026-04-27 19:31:16'),(6,2,'789456','2026-04-27 20:01:00',56.000,NULL,'2026-04-27 20:01:12'),(7,3,'46452','2026-05-12 17:14:00',NULL,16.420,'2026-04-28 10:46:01'),(10,4,'001','2026-05-18 15:15:00',NULL,17.490,'2026-05-04 19:07:59'),(11,7,'004','2026-05-18 15:14:00',NULL,15.200,'2026-05-18 15:15:00'),(12,8,'005','2026-05-18 15:15:00',NULL,14.520,'2026-05-18 15:15:11'),(13,6,'003','2026-05-18 15:15:00',NULL,17.510,'2026-05-18 15:15:23'),(14,5,'002','2026-05-18 15:15:00',NULL,18.410,'2026-05-18 15:15:34'),(15,17,'5','2026-05-19 21:36:00',3.000,NULL,'2026-05-19 21:36:55'),(16,18,'123456','2026-05-19 21:38:00',6.000,NULL,'2026-05-19 21:38:36'),(17,20,'6789','2026-05-19 22:26:00',6.000,NULL,'2026-05-19 22:27:06'),(18,19,'8899','2026-05-20 10:11:00',6.000,NULL,'2026-05-20 10:11:08'),(19,22,'7789','2026-05-20 10:19:00',92.000,NULL,'2026-05-20 10:20:15'),(20,25,'slip123456er','2026-06-01 13:15:00',NULL,29.000,'2026-06-01 13:16:22'),(21,28,'40355','2026-06-01 16:04:00',NULL,16.080,'2026-06-01 16:05:08'),(22,43,'40446','2026-06-06 08:47:00',NULL,16.780,'2026-06-06 08:47:48'),(23,45,'40478','2026-03-30 11:14:00',NULL,17.600,'2026-06-06 13:29:31'),(24,46,'40480','2026-03-30 11:15:00',NULL,16.540,'2026-06-06 13:52:28');
/*!40000 ALTER TABLE `wbout_records` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

--
-- Temporary view structure for view `v_vessel_billing`
--

DROP TABLE IF EXISTS `v_vessel_billing`;
/*!50001 DROP VIEW IF EXISTS `v_vessel_billing`*/;
/*!50001 CREATE VIEW `v_vessel_billing` AS 
SELECT 
    v.id AS vessel_id,
    v.vessel_auto_id,
    v.vessel_name,
    v.party_id,
    pm.party_name,
    v.cargo_type,
    v.quantity,
    v.direction,
    v.status,
    v.expected_date,
    v.berthing_datetime,
    v.mooring_datetime,
    v.survey_quantity,
    v.survey_datetime,
    v.sailing_datetime,
    COALESCE(SUM(bd.amount), 0) AS total_base_amount,
    COALESCE(SUM(bd.gst_amount), 0) AS total_gst_amount,
    COALESCE(SUM(bd.amount + bd.gst_amount), 0) AS grand_total_amount,
    CASE 
        WHEN SUM(bd.amount) > 0 THEN 'BILLED'
        ELSE 'PENDING'
    END AS billing_status
FROM vessels v
LEFT JOIN party_masters pm ON v.party_id = pm.id
LEFT JOIN bill_details bd ON v.id = bd.vessel_id
GROUP BY v.id, pm.party_name */;

-- Dump completed on 2026-06-08 14:45:52
