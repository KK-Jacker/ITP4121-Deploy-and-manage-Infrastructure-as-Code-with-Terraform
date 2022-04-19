-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql:3306
-- Generation Time: Feb 17, 2022 at 08:26 AM
-- Server version: 8.0.26
-- PHP Version: 7.4.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `default_schema`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE dec8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `donor`
--

CREATE TABLE `donor` (
  `_user_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `user_face_index` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `user_type_face_index` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `equipment`
--

CREATE TABLE `equipment` (
  `_equipment_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int NOT NULL,
  `description` varchar(250) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `meta` varchar(200) COLLATE dec8_bin DEFAULT NULL,
  `batch_id` varchar(50) COLLATE dec8_bin DEFAULT NULL,
  `donor_id` int NOT NULL,
  `equipment_type_id` int NOT NULL,
  `status` enum('not_selected','selected','pending','completed') COLLATE dec8_bin DEFAULT NULL,
  `has_receipt` tinyint(1) DEFAULT NULL,
  `_receipt_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `receipt_total` float DEFAULT NULL,
  `receipt_date` datetime DEFAULT NULL,
  `receipt_merchant_name` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `receipt_reject_reason` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `admin_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `equipment_application`
--

CREATE TABLE `equipment_application` (
  `time` datetime DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `address` varchar(220) COLLATE dec8_bin DEFAULT NULL,
  `_thanks_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `_thanks_message` varchar(500) COLLATE dec8_bin DEFAULT NULL,
  `thankfulness` float DEFAULT NULL,
  `happiness` float DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int NOT NULL,
  `status` enum('waiting_for_teacher_approval','teacher_rejected','pending','in_progress','donated','completed_without_receipt','donated_waiting_for_receipt','completed_with_receipt','completed_receipt_rejected') COLLATE dec8_bin DEFAULT NULL,
  `equipment_type_id` int NOT NULL,
  `student_id` int NOT NULL,
  `donor_id` int DEFAULT NULL,
  `equipment_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `equipment_type`
--

CREATE TABLE `equipment_type` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int NOT NULL,
  `name` varchar(50) COLLATE dec8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int NOT NULL,
  `message` varchar(100) COLLATE dec8_bin NOT NULL,
  `from_student` tinyint(1) NOT NULL,
  `equipment_application_id` int DEFAULT NULL,
  `repair_application_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `model_base`
--

CREATE TABLE `model_base` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `region`
--

CREATE TABLE `region` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int NOT NULL,
  `name` varchar(64) COLLATE dec8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `repair_application`
--

CREATE TABLE `repair_application` (
  `time` datetime DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `address` varchar(220) COLLATE dec8_bin DEFAULT NULL,
  `_thanks_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `_thanks_message` varchar(500) COLLATE dec8_bin DEFAULT NULL,
  `thankfulness` float DEFAULT NULL,
  `happiness` float DEFAULT NULL,
  `_equipment_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int NOT NULL,
  `title` varchar(100) COLLATE dec8_bin NOT NULL,
  `description` varchar(250) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `status` enum('pending','repairing','repaired','completed') COLLATE dec8_bin NOT NULL,
  `student_id` int NOT NULL,
  `volunteer_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `school`
--

CREATE TABLE `school` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` bigint NOT NULL,
  `name_en` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `name_zh_Hant` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `address_en` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `address_zh_Hant` varchar(150) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `url` varchar(200) COLLATE dec8_bin NOT NULL,
  `phone_number` varchar(20) COLLATE dec8_bin NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `category` enum('AIDED_PRIMARY_SCHOOLS','AIDED_SECONDARY_SCHOOLS','AIDED_SPECIAL_SCHOOLS','CAPUT_SECONDARY_SCHOOLS','DIRECT_SUBSIDY_SCHEME_PRIMARY_SCHOOLS','DIRECT_SUBSIDY_SCHEME_SECONDARY_SCHOOLS','ENGLISH_SCHOOLS_FOUNDATION_PRIMARY','ENGLISH_SCHOOLS_FOUNDATION_SECONDARY','GOVERNMENT_PRIMARY_SCHOOLS','GOVERNMENT_SECONDARY_SCHOOLS','INTERNATIONAL_SCHOOLS_PRIMARY','INTERNATIONAL_SCHOOLS_SECONDARY','KINDERGARTEN_CUM_CHILD_CARE_CENTRES','KINDERGARTENS','PRIVATE_PRIMARY_SCHOOLS','PRIVATE_SECONDARY_SCHOOLS_DAY_EVENING') COLLATE dec8_bin NOT NULL,
  `region_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `story`
--

CREATE TABLE `story` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `id` int NOT NULL,
  `title` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `title_zh_Hant` varchar(100) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `title_en` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_bin,
  `content_zh_Hant` text CHARACTER SET utf8 COLLATE utf8_bin,
  `content_en` text CHARACTER SET utf8 COLLATE utf8_bin,
  `urgency` float DEFAULT NULL,
  `_story_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `approved` tinyint(1) DEFAULT NULL,
  `student_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `_user_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `user_face_index` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `user_type_face_index` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `_id_card_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `id_card_face_index` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `id` int NOT NULL,
  `home_address` varchar(250) COLLATE dec8_bin NOT NULL,
  `id_card_number` varchar(8) COLLATE dec8_bin NOT NULL,
  `teacher_email` varchar(50) COLLATE dec8_bin DEFAULT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `teacher_id` int DEFAULT NULL,
  `_status` enum('not_activated','student_activated_wait_for_teacher_approval','student_not_activated_and_teacher_approved','activated') COLLATE dec8_bin DEFAULT NULL,
  `school_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `teacher`
--

CREATE TABLE `teacher` (
  `_user_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `user_face_index` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `user_type_face_index` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `_id_card_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `id_card_face_index` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `id` int NOT NULL,
  `school_id` bigint NOT NULL,
  `office_phone_number` varchar(20) COLLATE dec8_bin DEFAULT NULL,
  `_status` enum('not_activated','teacher_activated_wait_for_admin_approval','teacher_not_activated_and_admin_approved','admin_rejected','activated') COLLATE dec8_bin DEFAULT NULL,
  `admin_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `user_type` varchar(10) COLLATE dec8_bin DEFAULT NULL,
  `id` int NOT NULL,
  `username` varchar(20) COLLATE dec8_bin NOT NULL,
  `first_name` varchar(50) COLLATE dec8_bin NOT NULL,
  `last_name` varchar(50) COLLATE dec8_bin NOT NULL,
  `first_name_zh_hant` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `last_name_zh_hant` varchar(50) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `_email` varchar(50) COLLATE dec8_bin NOT NULL,
  `gender` enum('MALE','FEMALE') COLLATE dec8_bin DEFAULT NULL,
  `dateOfBirth` date NOT NULL,
  `region_id` int NOT NULL,
  `phone_number` varchar(20) COLLATE dec8_bin NOT NULL,
  `password_hash` varchar(128) COLLATE dec8_bin NOT NULL,
  `activated` tinyint(1) DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `volunteer`
--

CREATE TABLE `volunteer` (
  `_user_photo` varchar(150) COLLATE dec8_bin DEFAULT NULL,
  `user_face_index` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `user_type_face_index` varchar(100) COLLATE dec8_bin DEFAULT NULL,
  `id` int NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=dec8 COLLATE=dec8_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `donor`
--
ALTER TABLE `donor`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `equipment`
--
ALTER TABLE `equipment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `donor_id` (`donor_id`),
  ADD KEY `equipment_type_id` (`equipment_type_id`);

--
-- Indexes for table `equipment_application`
--
ALTER TABLE `equipment_application`
  ADD PRIMARY KEY (`id`),
  ADD KEY `donor_id` (`donor_id`),
  ADD KEY `equipment_id` (`equipment_id`),
  ADD KEY `equipment_type_id` (`equipment_type_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `equipment_type`
--
ALTER TABLE `equipment_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_equipment_type_name` (`name`);

--
-- Indexes for table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `equipment_application_id` (`equipment_application_id`),
  ADD KEY `repair_application_id` (`repair_application_id`);

--
-- Indexes for table `region`
--
ALTER TABLE `region`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_region_name` (`name`);

--
-- Indexes for table `repair_application`
--
ALTER TABLE `repair_application`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `volunteer_id` (`volunteer_id`);

--
-- Indexes for table `school`
--
ALTER TABLE `school`
  ADD PRIMARY KEY (`id`),
  ADD KEY `region_id` (`region_id`);

--
-- Indexes for table `story`
--
ALTER TABLE `story`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `ix_story_urgency` (`urgency`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`id`),
  ADD KEY `school_id` (`school_id`),
  ADD KEY `teacher_id` (`teacher_id`),
  ADD KEY `idx_location` (`latitude`,`longitude`);

--
-- Indexes for table `teacher`
--
ALTER TABLE `teacher`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`),
  ADD KEY `school_id` (`school_id`),
  ADD KEY `ix_teacher_office_phone_number` (`office_phone_number`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_user__email` (`_email`),
  ADD UNIQUE KEY `ix_user_username` (`username`),
  ADD KEY `region_id` (`region_id`),
  ADD KEY `ix_user_first_name` (`first_name`),
  ADD KEY `ix_user_first_name_zh_hant` (`first_name_zh_hant`),
  ADD KEY `ix_user_last_name` (`last_name`),
  ADD KEY `ix_user_last_name_zh_hant` (`last_name_zh_hant`),
  ADD KEY `ix_user_phone_number` (`phone_number`);

--
-- Indexes for table `volunteer`
--
ALTER TABLE `volunteer`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_volunteer_location` (`latitude`,`longitude`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `equipment`
--
ALTER TABLE `equipment`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `equipment_application`
--
ALTER TABLE `equipment_application`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `equipment_type`
--
ALTER TABLE `equipment_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `message`
--
ALTER TABLE `message`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `region`
--
ALTER TABLE `region`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `repair_application`
--
ALTER TABLE `repair_application`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `school`
--
ALTER TABLE `school`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `story`
--
ALTER TABLE `story`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admin`
--
ALTER TABLE `admin`
  ADD CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`);

--
-- Constraints for table `donor`
--
ALTER TABLE `donor`
  ADD CONSTRAINT `donor_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`);

--
-- Constraints for table `equipment`
--
ALTER TABLE `equipment`
  ADD CONSTRAINT `equipment_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`),
  ADD CONSTRAINT `equipment_ibfk_2` FOREIGN KEY (`donor_id`) REFERENCES `donor` (`id`),
  ADD CONSTRAINT `equipment_ibfk_3` FOREIGN KEY (`equipment_type_id`) REFERENCES `equipment_type` (`id`);

--
-- Constraints for table `equipment_application`
--
ALTER TABLE `equipment_application`
  ADD CONSTRAINT `equipment_application_ibfk_1` FOREIGN KEY (`donor_id`) REFERENCES `donor` (`id`),
  ADD CONSTRAINT `equipment_application_ibfk_2` FOREIGN KEY (`equipment_id`) REFERENCES `equipment` (`id`),
  ADD CONSTRAINT `equipment_application_ibfk_3` FOREIGN KEY (`equipment_type_id`) REFERENCES `equipment_type` (`id`),
  ADD CONSTRAINT `equipment_application_ibfk_4` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`);

--
-- Constraints for table `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `message_ibfk_1` FOREIGN KEY (`equipment_application_id`) REFERENCES `equipment_application` (`id`),
  ADD CONSTRAINT `message_ibfk_2` FOREIGN KEY (`repair_application_id`) REFERENCES `repair_application` (`id`);

--
-- Constraints for table `repair_application`
--
ALTER TABLE `repair_application`
  ADD CONSTRAINT `repair_application_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  ADD CONSTRAINT `repair_application_ibfk_2` FOREIGN KEY (`volunteer_id`) REFERENCES `volunteer` (`id`);

--
-- Constraints for table `school`
--
ALTER TABLE `school`
  ADD CONSTRAINT `school_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`);

--
-- Constraints for table `story`
--
ALTER TABLE `story`
  ADD CONSTRAINT `story_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`);

--
-- Constraints for table `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `student_ibfk_2` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`),
  ADD CONSTRAINT `student_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`);

--
-- Constraints for table `teacher`
--
ALTER TABLE `teacher`
  ADD CONSTRAINT `teacher_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`),
  ADD CONSTRAINT `teacher_ibfk_2` FOREIGN KEY (`id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `teacher_ibfk_3` FOREIGN KEY (`school_id`) REFERENCES `school` (`id`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`);

--
-- Constraints for table `volunteer`
--
ALTER TABLE `volunteer`
  ADD CONSTRAINT `volunteer_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
