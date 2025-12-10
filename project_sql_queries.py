# Query 1: Count approaches per asteroid
QUERY_1 = """
SELECT 
    a.name,
    COUNT(*) as approach_count
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
GROUP BY a.id, a.name
ORDER BY approach_count DESC
LIMIT 50
"""

# Query 2: Average velocity per asteroid
QUERY_2 = """
SELECT 
    a.name,
    ROUND(AVG(c.relative_velocity_kmph), 2) as avg_velocity
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
GROUP BY a.id, a.name
ORDER BY avg_velocity DESC
LIMIT 50
"""

# Query 3: Top 10 fastest asteroids
QUERY_3 = """
SELECT 
    a.name,
    MAX(c.relative_velocity_kmph) as max_velocity
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
GROUP BY a.id, a.name
ORDER BY max_velocity DESC
LIMIT 10
"""

# Query 4: Hazardous asteroids with >3 approaches
QUERY_4 = """
SELECT 
    a.name,
    a.is_potentially_hazardous_asteroid as hazardous,
    COUNT(*) as approach_count
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
WHERE a.is_potentially_hazardous_asteroid = 1
GROUP BY a.id, a.name
HAVING COUNT(*) > 3
ORDER BY approach_count DESC
"""

# Query 5: Month with most approaches
QUERY_5 = """
SELECT 
    strftime('%Y-%m', close_approach_date) as month,
    COUNT(*) as approach_count
FROM close_approach
GROUP BY strftime('%Y-%m', close_approach_date)
ORDER BY approach_count DESC
"""

# Query 6: Fastest ever approach
QUERY_6 = """
SELECT 
    a.name,
    c.close_approach_date,
    c.relative_velocity_kmph as velocity
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
ORDER BY c.relative_velocity_kmph DESC
LIMIT 1
"""

# Query 7: Sort by max diameter
QUERY_7 = """
SELECT 
    name,
    estimated_diameter_max_km as max_diameter,
    is_potentially_hazardous_asteroid as hazardous
FROM asteroids
ORDER BY estimated_diameter_max_km DESC
LIMIT 50
"""

# Query 8: Approaches getting closer over time
QUERY_8 = """
SELECT 
    a.name,
    c.close_approach_date,
    c.miss_distance_km
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
WHERE a.id IN (
    SELECT neo_reference_id
    FROM close_approach
    GROUP BY neo_reference_id
    HAVING COUNT(*) > 1
)
ORDER BY a.name, c.close_approach_date
LIMIT 100
"""

# Query 9: Closest approach per asteroid
QUERY_9 = """
SELECT 
    a.name,
    c.close_approach_date,
    MIN(c.miss_distance_km) as closest_distance
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
GROUP BY a.id, a.name
ORDER BY closest_distance ASC
LIMIT 50
"""

# Query 10: High velocity (>50,000 km/h)
QUERY_10 = """
SELECT 
    a.name,
    c.relative_velocity_kmph as velocity,
    c.close_approach_date
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
WHERE c.relative_velocity_kmph > 50000
ORDER BY c.relative_velocity_kmph DESC
LIMIT 100
"""

# Query 11: Monthly approach count
QUERY_11 = """
SELECT 
    strftime('%Y-%m', close_approach_date) as month,
    COUNT(*) as count
FROM close_approach
GROUP BY strftime('%Y-%m', close_approach_date)
ORDER BY month
"""

# Query 12: Highest brightness (lowest magnitude)
QUERY_12 = """
SELECT 
    name,
    absolute_magnitude_h as magnitude,
    estimated_diameter_max_km as size
FROM asteroids
ORDER BY absolute_magnitude_h ASC
LIMIT 10
"""

# Query 13: Hazardous vs non-hazardous count
QUERY_13 = """
SELECT 
    CASE 
        WHEN is_potentially_hazardous_asteroid = 1 THEN 'Hazardous'
        ELSE 'Non-Hazardous'
    END as category,
    COUNT(*) as count
FROM asteroids
GROUP BY is_potentially_hazardous_asteroid
"""

# Query 14: Closer than Moon (<1 LD)
QUERY_14 = """
SELECT 
    a.name,
    c.close_approach_date,
    c.miss_distance_lunar as lunar_distance
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
WHERE c.miss_distance_lunar < 1
ORDER BY c.miss_distance_lunar ASC
LIMIT 50
"""

# Query 15: Within 0.05 AU
QUERY_15 = """
SELECT 
    a.name,
    c.close_approach_date,
    c.astronomical as AU_distance
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
WHERE c.astronomical < 0.05
ORDER BY c.astronomical ASC
LIMIT 50
"""

# BONUS QUERIES 

CUSTOM_1 = """
-- Year-over-year trends
SELECT 
    strftime('%Y', close_approach_date) as year,
    COUNT(*) as total_approaches
FROM close_approach
GROUP BY strftime('%Y', close_approach_date)
ORDER BY year
"""


CUSTOM_2 = """
-- Average miss distance by month
SELECT 
    strftime('%m', close_approach_date) as month_num,
    CASE strftime('%m', close_approach_date)
        WHEN '01' THEN 'January' WHEN '02' THEN 'February'
        WHEN '03' THEN 'March' WHEN '04' THEN 'April'
        WHEN '05' THEN 'May' WHEN '06' THEN 'June'
        WHEN '07' THEN 'July' WHEN '08' THEN 'August'
        WHEN '09' THEN 'September' WHEN '10' THEN 'October'
        WHEN '11' THEN 'November' WHEN '12' THEN 'December'
    END as month_name,
    ROUND(AVG(miss_distance_lunar), 2) as avg_distance_LD
FROM close_approach
GROUP BY strftime('%m', close_approach_date)
ORDER BY month_num
"""

CUSTOM_3 = """
-- Asteroids with multiple close calls
SELECT 
    a.name,
    COUNT(*) as close_calls,
    MIN(c.miss_distance_lunar) as closest_LD,
    MAX(c.relative_velocity_kmph) as max_velocity
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
WHERE c.miss_distance_lunar < 5
GROUP BY a.id, a.name
HAVING COUNT(*) > 1
ORDER BY close_calls DESC
LIMIT 20
"""
# Risk Score Analysis
CUSTOM_RISK = """
SELECT 
    a.name,
    ROUND(a.estimated_diameter_max_km * c.relative_velocity_kmph / 
          CASE WHEN c.miss_distance_lunar > 0 THEN c.miss_distance_lunar ELSE 1 END, 2) as risk_score,
    c.close_approach_date
FROM asteroids a
JOIN close_approach c ON a.id = c.neo_reference_id
WHERE a.is_potentially_hazardous_asteroid = 1
ORDER BY risk_score DESC
LIMIT 20
"""
# Size Categories
CUSTOM_SIZE = """
SELECT 
    CASE 
        WHEN estimated_diameter_max_km < 0.1 THEN 'Tiny (<0.1km)'
        WHEN estimated_diameter_max_km < 0.5 THEN 'Small (0.1-0.5km)'
        WHEN estimated_diameter_max_km < 1.0 THEN 'Medium (0.5-1km)'
        ELSE 'Large (>1km)'
    END as size_category,
    COUNT(*) as count
FROM asteroids
GROUP BY size_category
ORDER BY count DESC
"""

# Dictionary for easy access
QUERIES = {
    "1. Approach Count Per Asteroid": QUERY_1,
    "2. Average Velocity Per Asteroid": QUERY_2,
    "3. Top 10 Fastest Asteroids": QUERY_3,
    "4. Hazardous with >3 Approaches": QUERY_4,
    "5. Month with Most Approaches": QUERY_5,
    "6. Fastest Ever Approach": QUERY_6,
    "7. Sorted by Max Diameter": QUERY_7,
    "8. Approaches Getting Closer": QUERY_8,
    "9. Closest Approach Per Asteroid": QUERY_9,
    "10. High Velocity (>50k km/h)": QUERY_10,
    "11. Monthly Approach Count": QUERY_11,
    "12. Highest Brightness": QUERY_12,
    "13. Hazardous vs Non-Hazardous": QUERY_13,
    "14. Closer Than Moon (<1 LD)": QUERY_14,
    "15. Within 0.05 AU": QUERY_15,
    "BONUS: Year-over-Year Trends": CUSTOM_1,
    "BONUS: Avg Distance by Month": CUSTOM_2,
    "BONUS: Multiple Close Calls": CUSTOM_3,
    "BONUS: Risk Score Analysis": CUSTOM_RISK,
    "BONUS: Size Categories": CUSTOM_SIZE,
}