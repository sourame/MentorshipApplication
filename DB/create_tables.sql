-- User Table
CREATE TABLE `User` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `street1` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `ethinicity` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

--Mentor Table
CREATE TABLE `Mentor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `communication_type` varchar(50) NOT NULL,
  `pref_ethinicity` varchar(50) DEFAULT NULL,
  `pref_timestart` time DEFAULT NULL,
  `pref_timeend` time DEFAULT NULL,
  `max_mentees` int DEFAULT NULL,
  `active_mentees` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Mentor_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

--Mentee Table
CREATE TABLE `Mentee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `communication_type` varchar(50) NOT NULL,
  `pref_ethinicity` varchar(50) DEFAULT NULL,
  `pref_timestart` time DEFAULT NULL,
  `pref_timeend` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Mentee_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

--Skills Type Table
CREATE TABLE `SkillType` (
  `id` int NOT NULL AUTO_INCREMENT,
  `topic_name` text NOT NULL,
  `topic_category` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

--Skills Set Table to add mentor and mentee skill set
--E for Experts (Mentors) and A for Acquiring (Mentees) skills
CREATE TABLE `SkillSet` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `skill_id` int NOT NULL,
  `interest` enum('E','A') DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `skill_id` (`skill_id`),
  CONSTRAINT `SkillSet_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
  CONSTRAINT `SkillSet_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `SkillType` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

--Mentorship Table to get the mentee-mentor relationship
CREATE TABLE `Mentorship` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mentor_id` int NOT NULL,
  `mentee_id` int NOT NULL,
  `skill_id` int NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `m_status` enum('A','C','N') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mentor_id` (`mentor_id`),
  KEY `mentee_id` (`mentee_id`),
  KEY `skill_id` (`skill_id`),
  CONSTRAINT `Mentorship_ibfk_1` FOREIGN KEY (`mentor_id`) REFERENCES `User` (`id`),
  CONSTRAINT `Mentorship_ibfk_2` FOREIGN KEY (`mentee_id`) REFERENCES `User` (`id`),
  CONSTRAINT `Mentorship_ibfk_3` FOREIGN KEY (`skill_id`) REFERENCES `SkillType` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci