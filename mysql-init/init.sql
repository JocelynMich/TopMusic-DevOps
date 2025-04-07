CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user'
);
INSERT INTO users (username, password, role)
VALUES ('admin', '$2b$12$f9i3yvciu2Upwnqmc4bkjOSGNqsglJwI6hfpatOvp8mTUDpgi0NzO', 'admin')