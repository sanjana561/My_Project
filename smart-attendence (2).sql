-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 24, 2025 at 11:17 AM
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
-- Database: `smart-attendence`
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
  `status` varchar(20) NOT NULL,
  `recorded_by` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance_records`
--

INSERT INTO `attendance_records` (`id`, `student_id`, `class_id`, `date`, `time`, `status`, `recorded_by`, `created_at`) VALUES
(10, 17, 3, '2025-10-24', '12:10:41', 'Present', 7, '2025-10-24 06:40:41'),
(11, 17, 3, '2025-10-27', '12:33:34', 'Present', 7, '2025-10-27 07:02:54'),
(12, 18, 3, '2025-10-24', '00:00:00', 'Absent', NULL, '2025-10-24 07:50:03'),
(13, 18, 3, '2025-10-24', '00:00:00', 'Absent', NULL, '2025-10-24 08:00:33');

-- --------------------------------------------------------

--
-- Table structure for table `classes`
--

CREATE TABLE `classes` (
  `id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `classes`
--

INSERT INTO `classes` (`id`, `teacher_id`, `name`, `description`, `created_at`) VALUES
(3, 7, '2nd BCA', 'BCA 2nd year-2025', '2025-09-01 07:13:56'),
(4, 7, '3rd BCA', 'BCA 3rd year-2025', '2025-09-01 09:43:04');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `student_id_number` varchar(50) NOT NULL,
  `face_embedding` blob DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `image_path` text NOT NULL,
  `parent_email` varchar(230) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `class_id`, `name`, `student_id_number`, `face_embedding`, `created_at`, `image_path`, `parent_email`) VALUES
(17, 3, 'shanila', '434531', 0x00000020bcd4bebf000000803d25a23f00000020c62ea33f000000e05d2372bf000000002d33b3bf00000060fa9d95bf00000020f2b698bf000000c0984bb9bf00000080a0efcb3f000000803078c8bf00000000104fc23f00000080843f9a3f000000e0c8a8c8bf000000203555a33f000000c03e2ba8bf000000a0cdcec13f0000000090dcb7bf00000000581fc4bf00000000f150623f00000000ccd1babf00000000f0ac953f00000000f2392abf00000080dfb7a53f00000040066cb13f000000e00f5acdbf000000e03ebbd2bf000000605422b2bf000000c08526c0bf000000209132a5bf000000c04ba5b2bf000000807260963f000000403c2da43f0000008002fec3bf00000000a87aa93f000000406029b03f000000809156b93f00000040a5a47b3f000000c0b27d7d3f0000004098fcce3f000000003d307fbf000000e09837cebf000000004deebcbf000000a0d19bc13f0000004014a8c93f000000808781c13f0000000099e7a53f000000008e4f8a3f000000404573c1bf000000c0ff36bf3f00000080a7b1cebf000000200d35a63f0000000017c3b33f00000020f95cb23f00000040f81bb53f000000403d599c3f000000603877c8bf00000040881ea23f0000002003ffaa3f000000009a66c3bf000000a0ea00a53f000000800f52953f00000040e21fb0bf0000004082d4b6bf000000e01581a73f000000a01eacd23f000000006eaabd3f000000600685c1bf000000406619b9bf000000e076ffce3f00000040e4c1cdbf000000c033f1a7bf000000e08edcbb3f000000a0f412adbf00000040390ccabf000000c0f121d0bf000000802cfbb1bf00000040ed0cdc3f00000000a8dbc53f000000e08b3dbcbf00000040db46af3f00000020ea37bdbf000000009db8653f00000040f7ef953f000000402528c13f00000080e791b6bf00000060e139a43f000000801fc278bf000000a0837aa83f00000000af6ed03f000000607aae893f0000008086c2a0bf000000a08264c43f00000020227d9f3f000000601e28ba3f0000000005fa423f00000000b5ecad3f000000e06175bebf0000008002c3acbf000000800070c3bf000000607fd5b6bf00000060f04083bf00000080f632993f000000204b8eac3f000000805ecfc33f00000000446cd3bf00000060d4c0c93f00000000f8cf7abf000000407717b9bf000000c07d379f3f00000080a623c33f000000c01533a8bf000000e0041ba8bf000000605063bc3f000000006afcd0bf00000060aafcc43f000000005ddcc53f0000002021b6a03f000000801c2bc83f000000c0e881ad3f0000006064a4ae3f000000a0658a9f3f00000040390ba9bf00000060bec1c7bf000000a0461aabbf00000000d002243f000000c02925bbbf000000c03b36b43f000000c09d6b953f, '2025-10-24 06:37:53', 'uploads\\5c2b60d3502a4c1992421a4208dd8e29.jpg', 'shanilamk14@gmail.com'),
(18, 3, 'zamiya', '2343513', 0x00000040ffffbdbf0000000019dabd3f000000204666af3f000000c0a616aebf00000040e3ed9abf000000406c37b5bf000000a052389dbf000000e0fa62b8bf00000060d3edc93f000000207575c5bf000000604fc8c63f000000e0241db6bf000000c06aabcebf000000e0b043a93f000000a0903395bf000000a07919c03f000000003037bfbf000000c04a6ac6bf00000080e6e2abbf000000c0928992bf00000060340db33f00000060a3e674bf000000c0e60f8a3f00000040bc85ba3f000000a07313babf000000205b3cd7bf000000c002cdb8bf000000c0c2f2b4bf000000000e1a5dbf000000006195adbf00000080a94b973f00000040026b913f000000e0529cccbf000000802fb5a6bf0000008054996a3f000000c03007ac3f000000604ab9803f000000c0c31a863f00000060e4d9cc3f00000000040d92bf000000c055cbd1bf00000060ae52babf000000a02db4ba3f000000e0268ecd3f00000080803bc03f000000c0e2a0b33f000000809ec598bf000000400e24bfbf000000805bf0ac3f000000801cd1d0bf000000a0d1cfb03f000000c02a0cc33f000000a0a036a53f00000080c0fdbb3f00000080d296943f000000c021f2c7bf00000040249ca63f000000a09a0db43f000000e0bfe6c6bf000000a0b99eaf3f00000020a8adb53f000000c0f35db7bf00000040911ea4bf00000040798488bf000000a045fcd53f000000e066eebd3f000000e077d5c0bf000000e0d6feb5bf000000a0a5c5cc3f00000080c6e9c8bf000000c0d04d9bbf000000c0545db03f0000004076d4b2bf000000409cf5c5bf000000c0d0f3d1bf00000000a8228cbf0000002041add83f00000060e55cc33f000000c09a46c3bf000000e0a903b93f000000c0e21dc0bf000000e06642883f000000c0995ba83f00000040e6b5c23f00000000fe13b7bf000000c0fbe5bd3f000000208085a3bf000000406f3ca43f0000002027f2c83f00000000aa459d3f00000080ea878bbf00000020a2edcd3f00000000982f88bf00000060846bb63f000000e0f306b63f0000004037a9a83f000000e00847bfbf000000e0ab94c0bf00000040fbd2cebf0000004090d4b1bf00000000c21b82bf0000002017cb8d3f000000e08eb78dbf00000040a761c43f00000080a892cabf000000a0f7dbc43f000000406159713f000000201e39adbf000000c04aa470bf00000040395bc03f00000000e59d85bf000000a08055c1bf00000000c5a2bb3f00000000e6e0c6bf00000060ec25c53f00000080baf0be3f000000e04a40a63f000000000ef3c43f00000060c711b53f000000a05bb7ba3f000000000088413f000000407828a5bf000000203a61c8bf000000e00aa394bf000000a0a688b43f000000801c7ea1bf000000c05c24b93f000000e00f649b3f, '2025-10-24 06:40:21', 'uploads\\bf258d4870254eefb3398d50e7b5cd66.jpg', 'zamiashafi30@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `email`, `name`, `created_at`) VALUES
(7, 'zam', '$2b$12$sWH8dQOnCTO4Ja9eKqKIbOiZeDBFL8fdcGuQY5OfOGIqtuZyFBFZa', 'zamiashafi30@gmail.com', 'Zamiya mariyamma', '2025-09-01 06:58:04');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance_records`
--
ALTER TABLE `attendance_records`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `class_id` (`class_id`),
  ADD KEY `recorded_by` (`recorded_by`);

--
-- Indexes for table `classes`
--
ALTER TABLE `classes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teacher_id` (`teacher_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `student_id_number` (`student_id_number`),
  ADD KEY `class_id` (`class_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance_records`
--
ALTER TABLE `attendance_records`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `classes`
--
ALTER TABLE `classes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance_records`
--
ALTER TABLE `attendance_records`
  ADD CONSTRAINT `attendance_records_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_records_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `attendance_records_ibfk_3` FOREIGN KEY (`recorded_by`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `classes`
--
ALTER TABLE `classes`
  ADD CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
