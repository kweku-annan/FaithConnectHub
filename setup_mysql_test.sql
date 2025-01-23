-- Preparing a MySQL server for the project

-- Creating Databases
CREATE DATABASE IF NOT EXISTS FaithConnectHub_test_db;

-- Creating a user
CREATE USER IF NOT EXISTS 'FaithConnectHub_test'@'localhost' IDENTIFIED BY 'FaithConnectHub_pwd1';

-- Granting privileges to user
USE FaithConnectHub_dev_db;
GRANT ALL PRIVILEGES ON FaithConnectHub_test_db.* TO 'FaithConnectHub_test'@'localhost';

-- Grant SELECT privilege on performance_schema to FaithConnectHub_dev
GRANT SELECT ON performance_schema.* TO 'FaithConnectHub_test'@'localhost';


-- Apply changes
FLUSH PRIVILEGES;
