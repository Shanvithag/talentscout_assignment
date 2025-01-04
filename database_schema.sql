CREATE DATABASE IF NOT EXISTS talentscout;

USE talentscout;

CREATE TABLE candidates 
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    experience INT,
    position VARCHAR(255),
    location VARCHAR(255),
    tech_stack TEXT,
    answers TEXT
);
