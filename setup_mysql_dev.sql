-- Preparing a MySQL server for the project

-- Creating Databases
CREATE DATABASE IF NOT EXISTS FaithConnectHub_dev_db;

-- Creating a user
CREATE USER IF NOT EXISTS 'FaithConnectHub_dev'@'localhost' IDENTIFIED BY 'FaithConnectHub_pwd';

-- Granting privileges to user
USE FaithConnectHub_dev_db;
GRANT ALL PRIVILEGES ON FaithConnectHub_dev_db.* TO 'FaithConnectHub_dev'@'localhost';

-- Grant SELECT privilege on performance_schema to FaithConnectHub_dev
GRANT SELECT ON performance_schema.* TO 'FaithConnectHub_dev'@'localhost';


-- Apply changes
FLUSH PRIVILEGES;
