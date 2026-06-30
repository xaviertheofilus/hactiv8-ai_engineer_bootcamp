
-- ASSIGNMENT 3
-- TASK 1
SELECT
    o.order_id,
    c.company_name,
    e.first_name || ' ' || e.last_name AS employee_name,
    o.order_date
FROM orders o
INNER JOIN customers c
    ON o.customer_id = c.customer_id
INNER JOIN employees e
    ON o.employee_id = e.employee_id
ORDER BY o.order_date DESC
LIMIT 20;


--1.2
SELECT
    c.customer_id,
    c.company_name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;


--1.3
-- cust yg belum pernah order ada 2 orang yaitu PARIS dan FISSA

-- 2.1
SELECT
    c.company_name,
    c.country,
    ROUND(
        SUM(od.unit_price * od.quantity * (1 - od.discount))::numeric,
        2
    ) AS total_revenue    
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_details od
    ON o.order_id = od.order_id
GROUP BY c.company_name, c.country
ORDER BY total_revenue DESC;

--2.2
SELECT
    c.company_name,
    c.country,
    ROUND(SUM(od.unit_price * od.quantity * (1 - od.discount))::numeric, 2) AS total_revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN order_details od
    ON o.order_id = od.order_id
WHERE c.country IN ('USA', 'Germany')
GROUP BY c.company_name, c.country
HAVING SUM(od.unit_price * od.quantity * (1 - od.discount)) > 10000
ORDER BY total_revenue DESC;


--2.3
WITH customer_revenue AS (
    SELECT
        c.customer_id,
        c.country,
        SUM(od.unit_price * od.quantity * (1 - od.discount))::numeric AS total_revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_details od
        ON o.order_id = od.order_id
    GROUP BY c.customer_id, c.country
)
SELECT
    country,
    ROUND(AVG(total_revenue), 2) AS avg_revenue
FROM customer_revenue
GROUP BY country
ORDER BY avg_revenue DESC
LIMIT 10;

-----------
WITH base AS (
    SELECT
        company_name,
        country,
        round(sum(unit_price * quantity * (1 - discount)):: NUMERIC, 2) AS revenue
    FROM customers a 
    JOIN orders b USING (customer_id)
    JOIN order_details c USING (order_id)
    GROUP BY 1, 2
    ORDER BY revenue DESC
)
SELECT
    a.country, avg(revenue) AS rerata_revenue,
    COUNT(a.company_name) as jumlah_pelanggan
FROM base a 
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10


--task 3
SELECT
    p.product_name,
    p.unit_price,
    c.category_name
FROM products p
LEFT JOIN categories c
    ON p.category_id = c.category_id
WHERE p.unit_price >
    (SELECT AVG(unit_price) FROM products)
ORDER BY p.unit_price DESC;


--task3.2
SELECT
    product_id,
    SUM(quantity) AS total_quantity
FROM order_details
GROUP BY product_id
HAVING SUM(quantity) >
    (
        SELECT AVG(total_qty)
        FROM (
            SELECT SUM(quantity) AS total_qty
            FROM order_details
            GROUP BY product_id
        ) 
    );



-- 3.3
SELECT
    p.product_name,
    t.total_quantity
FROM (
    SELECT
        product_id,
        SUM(quantity) AS total_quantity
    FROM order_details
    GROUP BY product_id
    HAVING SUM(quantity) >
        (
            SELECT AVG(total_qty)
            FROM (
                SELECT SUM(quantity) AS total_qty
                FROM order_details
                GROUP BY product_id
            ) 
        )
) t
JOIN products p
    ON t.product_id = p.product_id;



--4.1
SELECT
    s.company_name,
    COUNT(p.product_id) AS total_products
FROM suppliers s
JOIN products p
    ON s.supplier_id = p.supplier_id
GROUP BY s.company_name
HAVING COUNT(p.product_id) > 2;


--4.2
SELECT DISTINCT
    s.company_name,
    c.category_name
FROM suppliers s
JOIN products p
    ON s.supplier_id = p.supplier_id
JOIN categories c
    ON p.category_id = c.category_id
WHERE s.supplier_id IN (
    SELECT supplier_id
    FROM products
    GROUP BY supplier_id
    HAVING COUNT(product_id) > 2
)
ORDER BY s.company_name, c.category_name;


-- Task 4.3
SELECT
    s.company_name,
    ROUND(AVG(p.unit_price)::numeric, 2) AS avg_product_price
FROM suppliers s
JOIN products p
    ON s.supplier_id = p.supplier_id
GROUP BY s.company_name
ORDER BY avg_product_price DESC
LIMIT 1;

SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY company_name ORDER BY rerata DESC) AS rn 
    FROM(
        SELECT company_name, p.product_name, AVG(p.unit_price) as rerata from suppliers s 
        JOIN products p USING (supplier_id)
        GROUP BY 1, 2
        ORDER BY 1 ASC, 3 DESC) a 
    ) a
WHERE rn = 1


-- 5
SELECT
    p.product_name,
    c.category_name,
    ROUND(
        SUM(od.unit_price * od.quantity * (1 - od.discount))::numeric,
        2
    ) AS total_revenue
FROM order_details od
JOIN products p
    ON od.product_id = p.product_id
JOIN categories c
    ON p.category_id = c.category_id
JOIN orders o
    ON od.order_id = o.order_id
GROUP BY
    p.product_name,
    c.category_name
ORDER BY total_revenue DESC
LIMIT 5;