SELECT `date`, COUNT(request) as request_counts
FROM logs
GROUP BY `date`
ORDER BY request_counts DESC
LIMIT 10;
