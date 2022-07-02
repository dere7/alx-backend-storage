-- creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student.

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser
(u_id INT)
BEGIN
    UPDATE users SET average_score = (SELECT SUM(score * weight) / SUM(weight) FROM corrections, projects WHERE project_id = id AND user_id = u_id)
    WHERE `id` = u_id;
END$$
DELIMITER ;
