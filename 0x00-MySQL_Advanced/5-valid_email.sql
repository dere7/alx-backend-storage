-- reset valid_email if it is changed
DELIMITER $$
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email NOT LIKE NEW.email THEN
        SET NEW.valid_email = 0; 
    END IF;
END$$

DELIMITER ;$$
