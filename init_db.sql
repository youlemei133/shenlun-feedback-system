-- 申论判官反馈系统数据库初始化脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS shenlun_feedback CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE shenlun_feedback;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nickname VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    score VARCHAR(10) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_phone (phone),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 题目表
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    material TEXT NOT NULL,
    requirement TEXT NOT NULL,
    score INT DEFAULT 15,
    status VARCHAR(20) DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 答案表
CREATE TABLE IF NOT EXISTS answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    version VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_question_id (question_id),
    INDEX idx_version (version),
    UNIQUE KEY unique_question_version (question_id, version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 反馈表
CREATE TABLE IF NOT EXISTS feedbacks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    prefer VARCHAR(10) NOT NULL,
    reasons JSON,
    other_reason TEXT,
    willing_to_train VARCHAR(20),
    ip_address VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_question_id (question_id),
    INDEX idx_prefer (prefer),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入示例数据（可选）
-- INSERT INTO questions (title, material, requirement, score, status) VALUES
-- ('2024 年湖南省考 - 乡村振兴', '给定资料 1：...', '(1) 全面、准确、有条理；(2) 不超过 200 字。', 15, 'active');
