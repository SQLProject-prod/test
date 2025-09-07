-- 1. Selecting customers with "@gmail" and adding status
DROP TABLE IF EXISTS tmp_gmail_customers;
CREATE TEMP TABLE tmp_gmail_customers AS
SELECT
    customer_id,
    LEFT(name, STRPOS(name, ' ') - 1) AS first_name,
    RIGHT(name, LENGTH(name) - STRPOS(name, ' ')) AS last_name,
    email,
    'ACTIVE' AS status
FROM sales.customers
WHERE email LIKE '%gmail.com';

----------------------------------------------------------
-- 2. Selection of orders from the last year
DROP TABLE IF EXISTS tmp_orders_last_year;
CREATE TEMP TABLE tmp_orders_last_year AS
SELECT
	g.customer_id,
    g.first_name,
    g.last_name,
	oi.order_id,
	oi.order_item_id,
	oi.quantity,
	p.price
FROM sales.order_items AS oi
JOIN sales.orders AS o ON oi.order_id = o.order_id
JOIN sales.products AS p ON oi.product_id = p.product_id
JOIN tmp_gmail_customers AS g ON o.customer_id = g.customer_id
WHERE order_date BETWEEN CURRENT_DATE - interval '1 year' AND CURRENT_DATE
;

----------------------------------------------------------
-- 3. Calculation of the number of orders and the total amount by customer
DROP TABLE IF EXISTS tmp_customer_summary;
CREATE TEMP TABLE tmp_customer_summary AS
SELECT
	customer_id,
    first_name,
    last_name,
	COUNT(DISTINCT order_id) as total_orders,
	SUM(quantity * price) AS total_spent
FROM tmp_orders_last_year
GROUP BY
    customer_id,
    first_name,
    last_name
;

----------------------------------------------------------
-- 4. Selection of products within a certain price range
DROP TABLE IF EXISTS tmp_top_products;
CREATE TEMP TABLE tmp_top_products AS
SELECT
    product_id,
    product_name,
    category_id,
    price
FROM sales.products
where
	price > 100
ORDER BY price desc
;

----------------------------------------------------------
-- 5. Final report on clients
SELECT
    customer_id,
    first_name,
    last_name,
    total_orders,
    total_spent,
    'HIGH VALUE' AS customer_type
FROM tmp_customer_summary
WHERE total_spent > 500
ORDER BY total_spent DESC;

----------------------------------------------------------
-- 6. Final report on goods
SELECT
    product_name,
    category_id,
    price
FROM tmp_top_products
WHERE price > 500
ORDER BY price DESC;