WITH member_info AS (
    SELECT 
        m.member_id,
        m.gender,
        DATE_PART('year', AGE(CURRENT_DATE, m.birth_date))::int AS age
    FROM fitness.members m
),

trainer_revenue AS (
    SELECT 
        w.trainer_id,
        mi.gender,
        mi.age,
        SUM(s.price) AS total_revenue
    FROM fitness.workouts w
    JOIN member_info mi ON w.member_id = mi.member_id
    JOIN fitness.subscriptions s ON w.member_id = s.member_id AND w.workout_date BETWEEN s.start_date AND s.end_date
    GROUP BY w.trainer_id, mi.gender, mi.age
),
    
agg_revenue AS (
    SELECT 
        tr.trainer_id,
        t.name AS trainer_name,
        SUM(total_revenue) AS total_earned,
        SUM(CASE WHEN gender = 'Female' THEN total_revenue ELSE 0 END) AS earned_from_females,
        SUM(CASE WHEN gender = 'Male' THEN total_revenue ELSE 0 END) AS earned_from_males
    FROM trainer_revenue tr
    JOIN fitness.trainers t ON tr.trainer_id = t.trainer_id
    GROUP BY tr.trainer_id, t.name
),

age_profit AS (
    SELECT trainer_id,
           STRING_AGG(age::text, ', ') AS ages,
           MAX(total_age_revenue) AS revenue_from_best_age
    FROM (
        SELECT 
            trainer_id,
            age,
            SUM(total_revenue) AS total_age_revenue,
            RANK() OVER (PARTITION BY trainer_id ORDER BY SUM(total_revenue) DESC) AS rnk
        FROM trainer_revenue
        GROUP BY trainer_id, age
        ORDER BY trainer_id, age
    ) ranked
    WHERE rnk = 1
    GROUP BY trainer_id
)

SELECT 
    ar.trainer_name,
    ar.total_earned,
    ar.earned_from_females,
    ar.earned_from_males,
    ap.ages AS best_ages,
    ap.revenue_from_best_age
FROM agg_revenue ar
JOIN age_profit ap ON ar.trainer_id = ap.trainer_id
ORDER BY ar.total_earned DESC;