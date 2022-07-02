-- adds a new correction for a student
DELIMITER $$
CREATE PROCEDURE AddBonus
(user_id INT, project_name VARCHAR(255), score INT)
BEGIN
    IF (SELECT id FROM projects WHERE name LIKE project_name) IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
    END IF;
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, (SELECT id FROM projects WHERE name LIKE project_name), score);
END$$
DELIMITER ;
