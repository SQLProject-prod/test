-- 1. Selecting customers with "@gmail" and adding status
DROP TABLE IF EXISTS tmp_gmail_customers;
CREATE TEMP TABLE tmp_gmail_customers AS
SELECT /* HERE_IS_YOUR_CORE */
FROM sales.customers
WHERE /* HERE_IS_YOUR_CORE */;

----------------------------------------------------------
-- 2. Selection of orders from the last year
DROP TABLE IF EXISTS tmp_orders_last_year;
CREATE TEMP TABLE tmp_orders_last_year AS
SELECT /* HERE_IS_YOUR_CORE */
FROM sales.order_items AS oi
JOIN sales.orders AS o ON oi.order_id = o.order_id
JOIN sales.products AS p ON oi.product_id = p.product_id
JOIN tmp_gmail_customers AS g ON o.customer_id = g.customer_id
WHERE /* HERE_IS_YOUR_CORE */
;

----------------------------------------------------------
-- 3. Calculation of the number of orders and the total amount by customer
DROP TABLE IF EXISTS tmp_customer_summary;
CREATE TEMP TABLE tmp_customer_summary AS
SELECT /* HERE_IS_YOUR_CORE */
FROM /* HERE_IS_YOUR_CORE */
GROUP BY /* HERE_IS_YOUR_CORE */
;

----------------------------------------------------------
-- 4. Selection of products within a certain price range
DROP TABLE IF EXISTS tmp_top_products;
CREATE TEMP TABLE tmp_top_products AS
SELECT /* HERE_IS_YOUR_CORE */
FROM /* HERE_IS_YOUR_CORE */
WHERE /* HERE_IS_YOUR_CORE */
ORDER BY /* HERE_IS_YOUR_CORE */
;

----------------------------------------------------------
-- 5. Final report on clients
SELECT /* HERE_IS_YOUR_CORE */
FROM /* HERE_IS_YOUR_CORE */
WHERE /* HERE_IS_YOUR_CORE */
ORDER BY /* HERE_IS_YOUR_CORE */;

----------------------------------------------------------
-- 6. Final report on goods
SELECT /* HERE_IS_YOUR_CORE */
FROM /* HERE_IS_YOUR_CORE */
WHERE /* HERE_IS_YOUR_CORE */
ORDER BY /* HERE_IS_YOUR_CORE */
