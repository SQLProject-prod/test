-- 1. Створення тимчасової таблиці з новими зарплатами
CREATE TEMP TABLE tmp_salary_review AS
SELECT
    e.id AS employee_id,
    e.department_id,
    e.salary AS old_salary,
    CASE
        WHEN e.salary > dept.avg_salary THEN ROUND(e.salary * 0.95, 2)
        ELSE ROUND(e.salary * 1.10, 2)
    END AS new_salary
FROM data_editing.employees e
JOIN (
    SELECT department_id, AVG(salary) AS avg_salary
    FROM data_editing.employees
    GROUP BY department_id
) dept ON e.department_id = dept.department_id;

-- 2. Вставка нових змін у salary_changes
INSERT INTO data_editing.salary_changes (employee_id, new_salary, change_date)
SELECT t.employee_id, t.new_salary, CURRENT_DATE
FROM tmp_salary_review t
LEFT JOIN data_editing.salary_changes s
    ON t.employee_id = s.employee_id AND t.new_salary = s.new_salary
WHERE s.employee_id IS NULL;

-- 3. Оновлення зарплат у employees
UPDATE data_editing.employees e
SET salary = t.new_salary
FROM tmp_salary_review t
WHERE e.id = t.employee_id;

-- 4. Створення нового департаменту
INSERT INTO data_editing.departments (name, manager)
VALUES ('Digital Banking', 'James Anderson');

-- 5. Прийом на роботу нових співробітників
INSERT INTO data_editing.employees (first_name, last_name, department_id, salary, hire_date)
VALUES
('Emily', 'Johnson', (SELECT id FROM data_editing.departments WHERE name='Digital Banking'), 1500, CURRENT_DATE),
('Michael', 'Brown', (SELECT id FROM data_editing.departments WHERE name='Digital Banking'), 1600, CURRENT_DATE),
('Sarah', 'Davis', (SELECT id FROM data_editing.departments WHERE name='Digital Banking'), 1550, CURRENT_DATE);

-- 6. Фіксація зарплат нових співробітників у salary_changes
INSERT INTO data_editing.salary_changes (employee_id, new_salary, change_date)
SELECT id, salary, CURRENT_DATE
FROM data_editing.employees
WHERE department_id = (SELECT id FROM data_editing.departments WHERE name='Digital Banking');

-- 7. Звіт по новому департаменту
SELECT
    d.name AS department_name,
    COUNT(e.id) AS num_employees,
    ROUND(AVG(e.salary), 2) AS avg_salary
FROM data_editing.employees e
JOIN data_editing.departments d ON e.department_id = d.id
WHERE d.name = 'Digital Banking'
GROUP BY d.name;

-- 8. Прибирання тимчасових таблиць
DROP TABLE tmp_salary_review;
