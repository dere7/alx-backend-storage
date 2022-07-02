-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers
()
BEGIN
    DECLARE u_id, finished INT;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET finished = 1;
    OPEN cur;
    REPEAT FETCH cur INTO u_id;
        UPDATE users SET average_score = (SELECT SUM(score * weight) / SUM(weight) FROM corrections, projects WHERE project_id = id AND user_id = u_id)
        WHERE `id` = u_id;
    UNTIL finished = 1 END REPEAT;
    CLOSE cur;
END$$
DELIMITER ;
