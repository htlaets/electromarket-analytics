-- 1. Revenue by category

SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;


-- 2. Profit by category

SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS revenue,
    ROUND(SUM(oi.quantity * p.cost), 2) AS total_cost,
    ROUND(
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) - SUM(oi.quantity * p.cost),
        2
    ) AS profit
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY profit DESC;


-- 3. Top 10 customers by revenue

SELECT
    c.customer_id,
    c.full_name,
    c.city,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.full_name, c.city
ORDER BY total_revenue DESC
LIMIT 10;


-- 4. Orders by status

SELECT
    status,
    COUNT(*) AS orders_count
FROM orders
GROUP BY status
ORDER BY orders_count DESC;


-- 5. Revenue by acquisition channel

SELECT
    c.acquisition_channel,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY c.acquisition_channel
ORDER BY revenue DESC;


-- 6. Repeat purchase rate

WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(order_id) AS orders_count
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT
    ROUND(
        SUM(CASE WHEN orders_count >= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS repeat_purchase_rate_percent
FROM customer_orders;


-- 7. Cancellation rate by acquisition channel

SELECT
    c.acquisition_channel,
    COUNT(o.order_id) AS total_orders,
    SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(
        SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(o.order_id),
        2
    ) AS cancellation_rate_percent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.acquisition_channel
ORDER BY cancellation_rate_percent DESC;


-- 8. Conversion rate by traffic source

SELECT
    traffic_source,
    COUNT(session_id) AS sessions,
    SUM(made_purchase) AS purchases,
    ROUND(SUM(made_purchase) * 100.0 / COUNT(session_id), 2) AS conversion_rate_percent
FROM sessions
GROUP BY traffic_source
ORDER BY conversion_rate_percent DESC;