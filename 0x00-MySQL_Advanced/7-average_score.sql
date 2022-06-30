-- computes and store the average score for a student
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser
(user_id INT)
BEGIN
    SELECT AVG(score) FROM corrections WHERE `user_id` = user_id;
    UPDATE users SET average_score = (SELECT AVG(score) FROM corrections WHERE `user_id` = user_id)
    WHERE `id` = user_id;
END$$
DELIMITER ;$$
