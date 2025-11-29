-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 29, 2025 at 01:25 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `attendance`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance_records`
--

CREATE TABLE `attendance_records` (
  `id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `status` enum('Present','Absent','Late') NOT NULL,
  `recorded_by` int(11) DEFAULT NULL,
  `period` text NOT NULL,
  `subject` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance_records`
--

INSERT INTO `attendance_records` (`id`, `student_id`, `class_id`, `date`, `time`, `status`, `recorded_by`, `period`, `subject`) VALUES
(9, 12, 10, '2025-10-26', '13:02:32', 'Present', 1, '2nd', 'java'),
(10, 14, 10, '2025-10-26', '00:00:00', 'Absent', NULL, '', ''),
(13, 12, 10, '2025-10-26', '13:27:02', 'Present', 1, '2nd', 'adbms'),
(14, 15, 12, '2025-10-26', '13:31:45', 'Present', 1, '1st', 'java'),
(15, 15, 12, '2025-10-26', '13:32:11', 'Present', 1, '2nd', 'dbms'),
(16, 16, 12, '2025-10-26', '00:00:00', 'Absent', NULL, '', ''),
(17, 18, 15, '2025-10-26', '16:49:06', 'Present', 1, '1st', 'java'),
(18, 19, 16, '2025-10-26', '00:00:00', 'Absent', NULL, '', ''),
(19, 20, 18, '2025-10-26', '16:51:31', 'Present', 1, '1st', 'java'),
(20, 21, 20, '2025-10-27', '00:00:00', 'Absent', NULL, '', ''),
(21, 22, 22, '2025-10-27', '11:24:08', 'Present', 1, '1st', 'java'),
(22, 23, 22, '2025-10-27', '00:00:00', 'Absent', NULL, '', ''),
(23, 24, 24, '2025-10-30', '16:05:41', 'Present', 1, '1', 'AI DBMS java'),
(24, 24, 24, '2025-10-30', '16:25:35', 'Present', 1, '1st', 'imge processing'),
(25, 25, 20, '2025-10-30', '00:00:00', 'Absent', NULL, '', ''),
(26, 26, 28, '2025-10-30', '17:53:26', 'Present', 10, '1st', 'imge processing'),
(27, 29, 28, '2025-10-30', '00:00:00', 'Absent', NULL, '', ''),
(28, 32, 38, '2025-11-08', '16:33:21', 'Present', 11, '1st', 'imge processing'),
(29, 33, 39, '2025-11-08', '00:00:00', 'Absent', NULL, '', ''),
(30, 36, 40, '2025-11-10', '10:55:03', 'Present', 12, '1st', 'imge processing'),
(31, 37, 40, '2025-11-10', '00:00:00', 'Absent', NULL, '', ''),
(32, 36, 40, '2025-11-10', '00:00:00', 'Absent', 12, '2nd', 'cs'),
(33, 37, 40, '2025-11-10', '00:00:00', 'Absent', 12, '1st', 'imge processing'),
(34, 38, 42, '2025-11-10', '00:00:00', 'Absent', 12, '1st', 'CS'),
(35, 36, 40, '2025-11-12', '00:00:00', 'Absent', NULL, '4th', 'imge processing'),
(36, 37, 40, '2025-11-12', '00:00:00', 'Absent', NULL, '4th', 'imge processing'),
(37, 36, 40, '2025-11-12', '00:00:00', 'Absent', NULL, '5th', 'imge processing'),
(38, 36, 40, '2025-11-12', '00:00:00', 'Absent', NULL, '7th', 'cs'),
(39, 36, 40, '2025-11-25', '00:00:00', 'Absent', NULL, '1nd', 'java'),
(40, 40, 47, '2025-11-27', '00:00:00', 'Absent', NULL, '2nd', 'AI');

-- --------------------------------------------------------

--
-- Table structure for table `classes`
--

CREATE TABLE `classes` (
  `id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `academic_year` varchar(10) NOT NULL,
  `teacher_name` varchar(255) NOT NULL,
  `subjects_json` text NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `classes`
--

INSERT INTO `classes` (`id`, `teacher_id`, `name`, `academic_year`, `teacher_name`, `subjects_json`, `description`, `created_at`) VALUES
(23, 7, 'II Mca', '2025 Batch', 'divya', '[\"imge processing\"]', NULL, '2025-10-29 05:50:55'),
(28, 10, 'I MCA', '2025 Batch', 'sanjana', '[\"imge processing\",\"AI\"]', NULL, '2025-10-30 11:33:11'),
(36, 10, 'II Mca', '2025 Batch', 'sanjana', '[\"imge processing\"]', NULL, '2025-10-30 12:13:42'),
(37, 10, 'II bca', '2025 Batch', 'sanjana', '[\"cs\"]', NULL, '2025-10-30 12:14:10'),
(38, 11, 'II Mca', '2025 Batch', 'test', '[\"imge processing\",\"java\"]', NULL, '2025-11-08 10:51:22'),
(39, 11, 'I MCA', '2024-2024 ', 'test', '[\"cs\",\"AI\"]', NULL, '2025-11-08 10:51:52'),
(40, 12, 'II Mca', '2024 Batch', 'Riya', '[\"java\"]', NULL, '2025-11-10 05:11:02'),
(41, 12, 'I Mca', '2024-2024 ', 'Riya', '[\"imge processing\",\"AI\"]', NULL, '2025-11-10 05:11:39'),
(43, 12, 'II MBA', '2025 Batch', 'Riya', '[\"imge processing\"]', NULL, '2025-11-12 15:08:11'),
(44, 12, 'II MBA-A', '2025 -26 B', 'Riya', '[\"java\"]', NULL, '2025-11-12 15:08:33'),
(46, 12, 'I BBA', '2025 Batch', 'Riya', '[\"Logistics\",\"Business Studies\"]', NULL, '2025-11-25 12:46:47'),
(47, 12, 'I Mba', '2025 Batch', 'Riya', '[\"AI\"]', NULL, '2025-11-27 10:49:53');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `class_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `student_id_number` varchar(50) NOT NULL,
  `parent_email` varchar(255) NOT NULL,
  `image_path` text DEFAULT NULL,
  `face_embedding` blob DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`id`, `class_id`, `name`, `student_id_number`, `parent_email`, `image_path`, `face_embedding`, `created_at`) VALUES
(22, 22, 'sanjana', '5028', 'raosanjanar@gmail.com', 'uploads\\f02043ed73dc4de998a3e79b9d51dd6b.jpg', 0x3ab206be3bd5623d8c02683dec149fbd45f73abdf8155cbce33935bddc3184bd5b7c2b3e6429f8bdcf1a023ebabab43b8d0ee3bd4fac373ca81babbcf6e6a23d057d91bdff1df7bd7d8f20bdac324dbd59eb2f3de8a6213d9da7343bfaad4e3d1f6d0cbeeab287be34f996bdad51c8bc6e46fe3a7e478bbd464b0e3da555643d9fee4abe1b3d10bd3a57b1bb4c4de03d26f4ddbc6d58aabcbfb2cd3d6836d43ab55e2cbec15d7fbd08fac93d987a163ed3fbcb3d12562a3d065fe33b5751b4bddcd1653d267027be4137553d09d4e03d148ec23abddfac3d80dc4d3d04a8d9bded60c93c7e3c5f3d2b85d9bd0c4b7b3cedc6c23c652f72bcc6b401bd4e490fbd8ce72a3e45ee963dd70494bd174068bdc9200d3e1df5c7bd88c869bc7e768f3d2f3498bdc8251ebebfe747be3dafba3cdd1e8e3e2e4fda3d2f160fbd3f21c13de42c3abdcf400dbdccfa21bc34f7b13d0e197dbdecfbac3d34a8c83c0a6ef23d67ad163eaff86e3df90b7dbbc009183eca9e31bce4c81d3d6cba073dd19f963d0be9b7bdc4b626bdd4af11bea0d22fbd7f94023d374c1b3db1d4c43b8021cb3d809503bef57b0f3eeb9f823cd6b81ebd52fcc1bb820f393d801819bda2ab58bdb247873d16240abe8730ec3dea9eb13d57c60a3b336d0e3e1ad2ae3dba156f3d90979d3c830b09bd3386dfbd803680bcc57e823d50981bbdddb1913dc635863c, '2025-10-27 05:52:40'),
(23, 22, 'sharanya', '5029', 'raosanjanar@gmail.com', 'uploads\\c799dec692304e928768fe691ce1408e.jpg', 0xa020c3bd93977b3d72dcb13d03f489bc3bad77bd54bd82bd436bf8bc3c6017bdcf88223e530eb8bda407cc3d10e25a3c4264d2bdff7cbcbc4ebd1abc7b0fde3db5ea93bd3b3dcebd9bfa12bc90d907bdc22b783d158c2e3d5388be3d33e4243d4692e6bde76c92be5d0f14bd6535c0bd3cbd313c89b520bdd8ef2fbc5f1d1f3d06fc3abef6de4abd90a82abc646a5a3d19f696bb92bff1bbb37d1a3e42af9f3c9f8352bedcc995bce85d593d0290113e7d51023e9f7bdb3c50490e3d5ba2a1bd0118993ddce524be4ac069bcb760533d1792853d8a5b3abbf20d3f3d0c3fdabd28363e3dc06d873c4f0228be533f6f3ce1d9013cbdd01ebd983d71bbd9c38c3cefff4e3e4533283d306d40bdda830bbd1034033ed0590dbec6aaba3c058db93d77a010bd723105beaab24dbef6ab29bda1c5893e25497f3d2e5fb8bd239ca33d1b568cbd8a965cbc42793fb921a6cf3df54cabbdabd1b23d2a600dbd77fcd43cd0be1f3ee84a88bbd61aa73c19d9273e2bfe113d609e8e3d068d133d6e1f483ce118c5bd6a5f11bd5277f4bd5e7a82bc06f71ebdded5f1bcc2501c3900d07a3d71f14bbe40c3943d0ff6e7bc73f7acbd519700bdea65383d7da2cbbce3f686bde755573da67815be09f2c63da6dc0c3e0b3b7bbc8433143eed1b313d0074e43c3305a2bcf998e2bb5190c5bdb1c510bccd53863d3b20b9bd42ba883d960f8e3c, '2025-10-27 05:53:12'),
(26, 28, 'sanjana', 'BCA202501', 'raosanjanar@gmail.com', 'uploads\\efb506c4b4014465b43161c6e7733067.jpg', 0x3ab206be3bd5623d8c02683dec149fbd45f73abdf8155cbce33935bddc3184bd5b7c2b3e6429f8bdcf1a023ebabab43b8d0ee3bd4fac373ca81babbcf6e6a23d057d91bdff1df7bd7d8f20bdac324dbd59eb2f3de8a6213d9da7343bfaad4e3d1f6d0cbeeab287be34f996bdad51c8bc6e46fe3a7e478bbd464b0e3da555643d9fee4abe1b3d10bd3a57b1bb4c4de03d26f4ddbc6d58aabcbfb2cd3d6836d43ab55e2cbec15d7fbd08fac93d987a163ed3fbcb3d12562a3d065fe33b5751b4bddcd1653d267027be4137553d09d4e03d148ec23abddfac3d80dc4d3d04a8d9bded60c93c7e3c5f3d2b85d9bd0c4b7b3cedc6c23c652f72bcc6b401bd4e490fbd8ce72a3e45ee963dd70494bd174068bdc9200d3e1df5c7bd88c869bc7e768f3d2f3498bdc8251ebebfe747be3dafba3cdd1e8e3e2e4fda3d2f160fbd3f21c13de42c3abdcf400dbdccfa21bc34f7b13d0e197dbdecfbac3d34a8c83c0a6ef23d67ad163eaff86e3df90b7dbbc009183eca9e31bce4c81d3d6cba073dd19f963d0be9b7bdc4b626bdd4af11bea0d22fbd7f94023d374c1b3db1d4c43b8021cb3d809503bef57b0f3eeb9f823cd6b81ebd52fcc1bb820f393d801819bda2ab58bdb247873d16240abe8730ec3dea9eb13d57c60a3b336d0e3e1ad2ae3dba156f3d90979d3c830b09bd3386dfbd803680bcc57e823d50981bbdddb1913dc635863c, '2025-10-30 12:17:55'),
(27, 31, 'sharanya', 'BCA202502', 'raosanjanar@gmail.com', 'uploads\\0537d45d551f472fba5f7a76f437a4f6.jpg', 0xa020c3bd93977b3d72dcb13d03f489bc3bad77bd54bd82bd436bf8bc3c6017bdcf88223e530eb8bda407cc3d10e25a3c4264d2bdff7cbcbc4ebd1abc7b0fde3db5ea93bd3b3dcebd9bfa12bc90d907bdc22b783d158c2e3d5388be3d33e4243d4692e6bde76c92be5d0f14bd6535c0bd3cbd313c89b520bdd8ef2fbc5f1d1f3d06fc3abef6de4abd90a82abc646a5a3d19f696bb92bff1bbb37d1a3e42af9f3c9f8352bedcc995bce85d593d0290113e7d51023e9f7bdb3c50490e3d5ba2a1bd0118993ddce524be4ac069bcb760533d1792853d8a5b3abbf20d3f3d0c3fdabd28363e3dc06d873c4f0228be533f6f3ce1d9013cbdd01ebd983d71bbd9c38c3cefff4e3e4533283d306d40bdda830bbd1034033ed0590dbec6aaba3c058db93d77a010bd723105beaab24dbef6ab29bda1c5893e25497f3d2e5fb8bd239ca33d1b568cbd8a965cbc42793fb921a6cf3df54cabbdabd1b23d2a600dbd77fcd43cd0be1f3ee84a88bbd61aa73c19d9273e2bfe113d609e8e3d068d133d6e1f483ce118c5bd6a5f11bd5277f4bd5e7a82bc06f71ebdded5f1bcc2501c3900d07a3d71f14bbe40c3943d0ff6e7bc73f7acbd519700bdea65383d7da2cbbce3f686bde755573da67815be09f2c63da6dc0c3e0b3b7bbc8433143eed1b313d0074e43c3305a2bcf998e2bb5190c5bdb1c510bccd53863d3b20b9bd42ba883d960f8e3c, '2025-10-30 12:18:15'),
(29, 28, 'sharanya', 'BCA202503', 'raosanjanar@gmail.com', 'uploads\\19946212bc4648eb86d2f6a68ed5e1db.jpg', 0xa020c3bd93977b3d72dcb13d03f489bc3bad77bd54bd82bd436bf8bc3c6017bdcf88223e530eb8bda407cc3d10e25a3c4264d2bdff7cbcbc4ebd1abc7b0fde3db5ea93bd3b3dcebd9bfa12bc90d907bdc22b783d158c2e3d5388be3d33e4243d4692e6bde76c92be5d0f14bd6535c0bd3cbd313c89b520bdd8ef2fbc5f1d1f3d06fc3abef6de4abd90a82abc646a5a3d19f696bb92bff1bbb37d1a3e42af9f3c9f8352bedcc995bce85d593d0290113e7d51023e9f7bdb3c50490e3d5ba2a1bd0118993ddce524be4ac069bcb760533d1792853d8a5b3abbf20d3f3d0c3fdabd28363e3dc06d873c4f0228be533f6f3ce1d9013cbdd01ebd983d71bbd9c38c3cefff4e3e4533283d306d40bdda830bbd1034033ed0590dbec6aaba3c058db93d77a010bd723105beaab24dbef6ab29bda1c5893e25497f3d2e5fb8bd239ca33d1b568cbd8a965cbc42793fb921a6cf3df54cabbdabd1b23d2a600dbd77fcd43cd0be1f3ee84a88bbd61aa73c19d9273e2bfe113d609e8e3d068d133d6e1f483ce118c5bd6a5f11bd5277f4bd5e7a82bc06f71ebdded5f1bcc2501c3900d07a3d71f14bbe40c3943d0ff6e7bc73f7acbd519700bdea65383d7da2cbbce3f686bde755573da67815be09f2c63da6dc0c3e0b3b7bbc8433143eed1b313d0074e43c3305a2bcf998e2bb5190c5bdb1c510bccd53863d3b20b9bd42ba883d960f8e3c, '2025-10-30 12:22:24'),
(32, 38, 'sanjana', 'BCA2025010', 'raosanjanar@gmail.com', 'uploads\\f2569d83454147e1ae5bf76b0f639bf4.jpg', 0x3ab206be3bd5623d8c02683dec149fbd45f73abdf8155cbce33935bddc3184bd5b7c2b3e6429f8bdcf1a023ebabab43b8d0ee3bd4fac373ca81babbcf6e6a23d057d91bdff1df7bd7d8f20bdac324dbd59eb2f3de8a6213d9da7343bfaad4e3d1f6d0cbeeab287be34f996bdad51c8bc6e46fe3a7e478bbd464b0e3da555643d9fee4abe1b3d10bd3a57b1bb4c4de03d26f4ddbc6d58aabcbfb2cd3d6836d43ab55e2cbec15d7fbd08fac93d987a163ed3fbcb3d12562a3d065fe33b5751b4bddcd1653d267027be4137553d09d4e03d148ec23abddfac3d80dc4d3d04a8d9bded60c93c7e3c5f3d2b85d9bd0c4b7b3cedc6c23c652f72bcc6b401bd4e490fbd8ce72a3e45ee963dd70494bd174068bdc9200d3e1df5c7bd88c869bc7e768f3d2f3498bdc8251ebebfe747be3dafba3cdd1e8e3e2e4fda3d2f160fbd3f21c13de42c3abdcf400dbdccfa21bc34f7b13d0e197dbdecfbac3d34a8c83c0a6ef23d67ad163eaff86e3df90b7dbbc009183eca9e31bce4c81d3d6cba073dd19f963d0be9b7bdc4b626bdd4af11bea0d22fbd7f94023d374c1b3db1d4c43b8021cb3d809503bef57b0f3eeb9f823cd6b81ebd52fcc1bb820f393d801819bda2ab58bdb247873d16240abe8730ec3dea9eb13d57c60a3b336d0e3e1ad2ae3dba156f3d90979d3c830b09bd3386dfbd803680bcc57e823d50981bbdddb1913dc635863c, '2025-11-08 10:53:36'),
(33, 39, 'sharanya', 'BCA2025012', 'raosanjanar@gmail.com', 'uploads\\f92063d65999475f9932d4efd4b6d36f.jpg', 0xa020c3bd93977b3d72dcb13d03f489bc3bad77bd54bd82bd436bf8bc3c6017bdcf88223e530eb8bda407cc3d10e25a3c4264d2bdff7cbcbc4ebd1abc7b0fde3db5ea93bd3b3dcebd9bfa12bc90d907bdc22b783d158c2e3d5388be3d33e4243d4692e6bde76c92be5d0f14bd6535c0bd3cbd313c89b520bdd8ef2fbc5f1d1f3d06fc3abef6de4abd90a82abc646a5a3d19f696bb92bff1bbb37d1a3e42af9f3c9f8352bedcc995bce85d593d0290113e7d51023e9f7bdb3c50490e3d5ba2a1bd0118993ddce524be4ac069bcb760533d1792853d8a5b3abbf20d3f3d0c3fdabd28363e3dc06d873c4f0228be533f6f3ce1d9013cbdd01ebd983d71bbd9c38c3cefff4e3e4533283d306d40bdda830bbd1034033ed0590dbec6aaba3c058db93d77a010bd723105beaab24dbef6ab29bda1c5893e25497f3d2e5fb8bd239ca33d1b568cbd8a965cbc42793fb921a6cf3df54cabbdabd1b23d2a600dbd77fcd43cd0be1f3ee84a88bbd61aa73c19d9273e2bfe113d609e8e3d068d133d6e1f483ce118c5bd6a5f11bd5277f4bd5e7a82bc06f71ebdded5f1bcc2501c3900d07a3d71f14bbe40c3943d0ff6e7bc73f7acbd519700bdea65383d7da2cbbce3f686bde755573da67815be09f2c63da6dc0c3e0b3b7bbc8433143eed1b313d0074e43c3305a2bcf998e2bb5190c5bdb1c510bccd53863d3b20b9bd42ba883d960f8e3c, '2025-11-08 10:53:59'),
(36, 40, 'sanjana', 'MCA5028', 'raosanjanar@gmail.com', 'uploads\\7aece17bf065499b86675641f30932d3.jpg', 0x3ab206be3bd5623d8c02683dec149fbd45f73abdf8155cbce33935bddc3184bd5b7c2b3e6429f8bdcf1a023ebabab43b8d0ee3bd4fac373ca81babbcf6e6a23d057d91bdff1df7bd7d8f20bdac324dbd59eb2f3de8a6213d9da7343bfaad4e3d1f6d0cbeeab287be34f996bdad51c8bc6e46fe3a7e478bbd464b0e3da555643d9fee4abe1b3d10bd3a57b1bb4c4de03d26f4ddbc6d58aabcbfb2cd3d6836d43ab55e2cbec15d7fbd08fac93d987a163ed3fbcb3d12562a3d065fe33b5751b4bddcd1653d267027be4137553d09d4e03d148ec23abddfac3d80dc4d3d04a8d9bded60c93c7e3c5f3d2b85d9bd0c4b7b3cedc6c23c652f72bcc6b401bd4e490fbd8ce72a3e45ee963dd70494bd174068bdc9200d3e1df5c7bd88c869bc7e768f3d2f3498bdc8251ebebfe747be3dafba3cdd1e8e3e2e4fda3d2f160fbd3f21c13de42c3abdcf400dbdccfa21bc34f7b13d0e197dbdecfbac3d34a8c83c0a6ef23d67ad163eaff86e3df90b7dbbc009183eca9e31bce4c81d3d6cba073dd19f963d0be9b7bdc4b626bdd4af11bea0d22fbd7f94023d374c1b3db1d4c43b8021cb3d809503bef57b0f3eeb9f823cd6b81ebd52fcc1bb820f393d801819bda2ab58bdb247873d16240abe8730ec3dea9eb13d57c60a3b336d0e3e1ad2ae3dba156f3d90979d3c830b09bd3386dfbd803680bcc57e823d50981bbdddb1913dc635863c, '2025-11-10 05:13:10'),
(37, 40, 'sharanya', 'MCA5030', 'raosanjanar@gmail.com', 'uploads\\8a7cc047b14f464297aaf7e533b7dcb5.jpg', 0xa020c3bd93977b3d72dcb13d03f489bc3bad77bd54bd82bd436bf8bc3c6017bdcf88223e530eb8bda407cc3d10e25a3c4264d2bdff7cbcbc4ebd1abc7b0fde3db5ea93bd3b3dcebd9bfa12bc90d907bdc22b783d158c2e3d5388be3d33e4243d4692e6bde76c92be5d0f14bd6535c0bd3cbd313c89b520bdd8ef2fbc5f1d1f3d06fc3abef6de4abd90a82abc646a5a3d19f696bb92bff1bbb37d1a3e42af9f3c9f8352bedcc995bce85d593d0290113e7d51023e9f7bdb3c50490e3d5ba2a1bd0118993ddce524be4ac069bcb760533d1792853d8a5b3abbf20d3f3d0c3fdabd28363e3dc06d873c4f0228be533f6f3ce1d9013cbdd01ebd983d71bbd9c38c3cefff4e3e4533283d306d40bdda830bbd1034033ed0590dbec6aaba3c058db93d77a010bd723105beaab24dbef6ab29bda1c5893e25497f3d2e5fb8bd239ca33d1b568cbd8a965cbc42793fb921a6cf3df54cabbdabd1b23d2a600dbd77fcd43cd0be1f3ee84a88bbd61aa73c19d9273e2bfe113d609e8e3d068d133d6e1f483ce118c5bd6a5f11bd5277f4bd5e7a82bc06f71ebdded5f1bcc2501c3900d07a3d71f14bbe40c3943d0ff6e7bc73f7acbd519700bdea65383d7da2cbbce3f686bde755573da67815be09f2c63da6dc0c3e0b3b7bbc8433143eed1b313d0074e43c3305a2bcf998e2bb5190c5bdb1c510bccd53863d3b20b9bd42ba883d960f8e3c, '2025-11-10 05:13:35'),
(38, 42, 'shreya', 'BCA1020', 'raosanjanar@gmail.com', 'uploads\\79be267164cf4e1dbaf5e7d4abec145e.jpg', 0x970728bde945ac3dd3c7533ddac08bbdb655cdbde97058bd26eda1bd84f7aebd2fb1d53d09b5a9bd86f7093e039a80bdd12829be7940e3bbf93a66bd23bc1a3e96f51cbe0bb1bbbdd090b2bb555c8d3cc8ef943ddaed783c26ba143cf0bc053d56cd86bd68a098be958733bdd621c3bc1b55d8bc60e281bbe5ba60bcc7b0923d0150e7bd8bf193bc84a2f43cea999b3da1bae43c37fe36bdfdd7bc3dc200ab3c200463bec073dd3c307db03d1226263e7bd6013e1d0aa53c5c00033dd2c3b8bd7f28e43ddbc71cbee82599bc50b1953dfcc39a3d049810bda475243d9ed3cbbd37b0433c42958f3d243303be866bb7bca9b3a63d9efe55bdebff58bc5ad4a6bd7a8e1b3ed6adf33c0fc7b7bda19192bdf91dce3de7a0b3bd454f2cbd2062953c0e8fa4bdb371edbdce6a63be28b31ebd46258f3eac6d7a3d7e6bf6bd6b1c773d612702bdd0f09abb411f283d64eed93deed38fbb3d6a363dd417b9bd01fc6abb825d283e37987bbd103c283d4b6e303e80793e3c7620873de90a3abcdb641e3c0acaf6bd8ed12d3b345314be257c0abd03d806bda19b5fba3bdbbcbcd4d38a3d2db41dbe5dca703d7e4a4e3ad945babcbd1fbb3a25481d3bc6a9f3bc7a2893bdfecd9a3d889e02bebba4363d7145fa3d51117a3db673c23de3feb13d0ee0e13b5c88993b194617bd1b8a10beb8edfbbceb05703d40ae7abda2e5cb3c529770ba, '2025-11-10 05:15:33'),
(40, 47, 'priya', '123456', 'raosanjanar@gmail.com', 'uploads\\a46c7ce2554e4a48a98e675e9edaf255.jpg', 0xfffaeabd370b33bcf98c193d49478ebd8063bdbdcd7e0cbc0e548bbda70389bdba4f2a3e7e2bf0bdd96c923dea79dfbce1e124be8425f33c319c6ebc1e9fa93d3c97d8bd31e5dbbdf3a0193c517990bd5855c23cae20723da15aa63cd6c0b63c7dd7f9bd28f788be7a2ab2bdeb4bc3bcef21843c3a3199bd6195e23c8f353d3d2ae734be871e6c3bf430773c9c07d93d674469bd726677bdab5fc43dd2fcf43bc5fa35bed0cab1bd4285bf3d39b3e93d4782dc3d6de4813d55d867bce86392bd78efd13dcd7c3cbeb4e20d3d8835e93d50541c3c6cca583db564c63c0e0c0abefdef083cda2c8c3d22b0e0bd0967f73c6271223df2622fbd02d584bc1557493c7bd72f3ef6df8f3d0c70a1bde38cb2bd827e073efeddfebd9f3fdaba24aaa73dd4af8dbdf4c620be52cd36be80d1cc3abd22843e2911cc3ca0ed2c3c168c893d1ea11bbdfe248dbb1e92f1bc84a0a63d71069ebd259d203d7bb7ccbc08927c3d5b36393e5ce384bcc0f80a3c7e73133e9d7682bcf2c94f3d43b9bf3c9f22c43d95b5d9bda70820bd8e51c0bd30fd5ebd54c6903d515791bcbca8823c72b9cc3d887b12be687d0e3e12c8c0bb33a95fbde181dd3b77ee74ba4c9959bd1f5352bd0fc7a73d3bd52dbe6186063ea76dd13d1bf8bf3c1ff4263e0d7b483da40f7a3dd9d2d13a234dd3bcfefaa3bd693020bdf597dc3ccaff86bb65ac803c4cb6823c, '2025-11-27 10:50:47');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `name` varchar(255) NOT NULL,
  `teacher_subjects` varchar(512) NOT NULL,
  `phone` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `name`, `teacher_subjects`, `phone`) VALUES
(10, 'sanjana', 'sanjana@gmail.com', '$2b$12$8qFnK/96u0zF1Dipruvty.BmMDTzrUnEXIIZwweuwzOhKllrBShB6', 'sanjana', '', ''),
(12, 'Riya', 'riya@gmail.com', '$2b$12$PD6iOl2rQa9Q4T1bkpj4Iun2PMMYcVN.LdgWVRj8J0NXWTbnQSnLm', 'Riya', '', ''),
(13, 'Sanjana', 'raosanjanar@gmail.com', '$2b$12$BfKOu7cvBsAl9BhqLyj4FOYUoZCi98pRo8xu/KmWXBIPPpTHAh7Ra', 'sanjana ', '', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance_records`
--
ALTER TABLE `attendance_records`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_session_attendance` (`student_id`,`class_id`,`date`,`period`,`subject`) USING HASH,
  ADD KEY `recorded_by` (`recorded_by`);

--
-- Indexes for table `classes`
--
ALTER TABLE `classes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teacher_id` (`teacher_id`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `student_id_number` (`student_id_number`),
  ADD KEY `class_id` (`class_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance_records`
--
ALTER TABLE `attendance_records`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `classes`
--
ALTER TABLE `classes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
