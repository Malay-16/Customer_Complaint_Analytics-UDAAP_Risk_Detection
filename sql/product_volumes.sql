SELECT 
    Product, 
    COUNT(*) as Total_Complaints
FROM complaints
GROUP BY Product
ORDER BY Total_Complaints DESC;
