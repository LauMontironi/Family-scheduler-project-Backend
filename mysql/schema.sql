CREATE SCHEMA IF NOT EXISTS `family_schedule` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `family_schedule`;

-- USERS
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- FAMILIES
CREATE TABLE IF NOT EXISTS families (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- FAMILY MEMBERS
CREATE TABLE IF NOT EXISTS family_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT NOT NULL,
    user_id INT NOT NULL,
    role ENUM('admin', 'parent') NOT NULL DEFAULT 'parent',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_family_user (family_id, user_id),
    CONSTRAINT fk_fm_family FOREIGN KEY (family_id) REFERENCES families (id) ON DELETE CASCADE,
    CONSTRAINT fk_fm_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- CHILDREN
CREATE TABLE IF NOT EXISTS children (
    id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    birthdate DATE NULL,
    notes TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_children_family FOREIGN KEY (family_id) REFERENCES families (id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- EVENTS
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    family_id INT NOT NULL,
    child_id INT NULL,
    created_by INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    type ENUM(
        'activity',
        'medical',
        'birthday',
        'reminder',
        'school',
        'other'
    ) NOT NULL DEFAULT 'other',
    start_at DATETIME NOT NULL,
    end_at DATETIME NULL,
    location VARCHAR(255) NULL,
    notes TEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_events_family_start (family_id, start_at),
    INDEX idx_events_child_start (child_id, start_at),
    CONSTRAINT fk_events_family FOREIGN KEY (family_id) REFERENCES families (id) ON DELETE CASCADE,
    CONSTRAINT fk_events_child FOREIGN KEY (child_id) REFERENCES children (id) ON DELETE SET NULL,
    CONSTRAINT fk_events_user FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE RESTRICT
) ENGINE = InnoDB;

-- Ajuste columna password_hash -> password
ALTER TABLE users
CHANGE COLUMN password_hash password VARCHAR(255) NOT NULL;

-- Campos extra
ALTER TABLE family_members
ADD COLUMN relationship_label VARCHAR(50) NULL,
ADD COLUMN avatar_url VARCHAR(500) NULL;