SELECT 
    Company,
    COUNT(*) as Total_Complaints,
    SUM(CASE WHEN "Consumer disputed?" = 'Yes' THEN 1 ELSE 0 END) as Total_Disputes
FROM complaints
GROUP BY Company
ORDER BY Total_Complaints DESC;
