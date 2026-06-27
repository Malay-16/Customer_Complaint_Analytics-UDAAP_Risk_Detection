SELECT 
    State, 
    COUNT(*) as Total_Complaints
FROM complaints
WHERE State IS NOT NULL
GROUP BY State
ORDER BY Total_Complaints DESC;
