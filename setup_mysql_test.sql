SET @db_name := 'hbnb_test_db';
SET @user_name := 'hbnb_test';
SET @user_pass := 'hbnb_test_pwd';

PREPARE stmt FROM '
    CREATE DATABASE IF NOT EXISTS ?;
    CREATE USER IF NOT EXISTS ?@localhost IDENTIFIED BY ?;
    GRANT ALL PRIVILEGES ON `hbnb_test_db`.* TO ?@localhost;
    GRANT SELECT ON `performance_schema`.* TO ?@localhost;
    FLUSH PRIVILEGES;
';

EXECUTE stmt USING @db_name, @user_name, @user_pass, @user_name, @user_name;

DEALLOCATE PREPARE stmt;
