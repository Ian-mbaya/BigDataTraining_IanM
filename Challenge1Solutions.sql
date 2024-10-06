# QUESTION 1
use challenge1;
SELECT a.customer_id, SUM(b.price) AS TOTAL_SALES
FROM sales AS a
JOIN menu AS b ON a.product_id = b.product_id
GROUP BY a.customer_id;

# QUESTION 2
USE challenge1;
SELECT customer_id, COUNT(DISTINCT order_date) AS Days
FROM SALES
GROUP BY customer_id;

# QUESTION 3
USE challenge1;
select customer_id,  order_date, product_name
from sales as a join menu as b
order by customer_id, order_date;

# QUESTION 3
USE challenge1;
WITH first_productCTE AS (
	SELECT a.customer_id, b.product_name,
    row_number() over (partition by customer_id order by customer_id) row_a
    FROM sales as a
    join menu as b on a.product_id = b.product_id
    )
    SELECT *
    FROM first_productCTE
    where row_a = 1;
    
# QUESTION 4
USE challenge1;
SELECT ANY_VALUE(b.product_name) AS Product, COUNT(a.product_id) as Total 
from sales as a join 
menu as b on a.product_id = b.product_id
group by a.product_id
order by  Total desc
LIMIT 1;

# QUESTION 5
USE challenge1;

WITH most_popularCTE AS (
    SELECT 
        a.customer_id, 
        b.product_id, 
        COUNT(b.product_id) AS Total_Orders, 
        DENSE_RANK() OVER (PARTITION BY a.customer_id ORDER BY COUNT(a.product_id) DESC) AS rank1
    FROM menu AS b
    JOIN sales AS a ON b.product_id = a.product_id
    GROUP BY a.customer_id, a.product_id, b.product_name
)

SELECT * FROM most_popularCTE 
WHERE rank1 = 1;

# QUESTION 6
USE challenge1;
WITH members_joined AS
(
SELECT c.customer_id, a.product_id,
ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY a.order_date) as row_num
from members as c
join sales as a on c.customer_id = a.customer_id and 
a.order_date > c.join_date
)
select customer_id, product_name from members_joined as d join menu as b 
on d.product_id = b.product_id
WHERE row_num = 1
order by customer_id;

# QUESTION 7
USE challenge1;
WITH members_joined AS
(
SELECT c.customer_id, a.product_id,
ROW_NUMBER() OVER (PARTITION BY c.customer_id ORDER BY a.order_date DESC) as row_num
from members as c
join sales as a on c.customer_id = a.customer_id and 
a.order_date < c.join_date
)
select customer_id, product_name from members_joined as d join menu as b 
on d.product_id = b.product_id
WHERE row_num = 1
order by customer_id;

# QUESTION 8
USE challenge1;

SELECT a.customer_id, COUNT(a.product_id) as total_items,
sum(b.price) AS total_sales
from sales as a join members as c on a.customer_id = c.customer_id and
a.order_date < c.join_date join menu as b
ON a.product_id = b.product_id
group by a.customer_id
order by a.customer_id;

# QUESTION 9
with points_table as (
select customer_id, 
case when sales.product_id = 1 then 20 * menu.price
     when sales.product_id in (2 , 3) then 10  * menu.price
     end as points
from sales join 
menu on sales.product_id = menu.product_id)
select pt.customer_id, 
sum(points) as totalpoints
from points_table as pt
group by pt.customer_id;

# QUESTION 10
WITH join_week AS (
  SELECT 
    sales.customer_id,
    sales.order_date,
    CASE 
      -- Check if the order falls within the first week after joining
      WHEN sales.order_date BETWEEN members.join_date AND DATE_ADD(members.join_date, INTERVAL 7 DAY)
      THEN 2 -- Apply 2x multiplier for the first week
      ELSE 1 -- Regular points multiplier otherwise
    END AS multiplier
  FROM sales
  JOIN members
    ON sales.customer_id = members.customer_id
  WHERE sales.order_date <= '2024-01-31' 
),
points_table AS (
  SELECT 
    sales.customer_id,
    sales.order_date,
    -- Multiply the points based on product and the first week multiplier
    CASE 
      WHEN sales.product_id = 1 THEN 20 * menu.price * jw.multiplier   -- Sushi: 20 points
      ELSE 10 * menu.price * jw.multiplier  
    END AS points
  FROM sales
  JOIN menu
    ON sales.product_id = menu.product_id
  JOIN join_week jw
    ON sales.customer_id = jw.customer_id 
    AND sales.order_date = jw.order_date 
),
final_points AS (
  SELECT 
    pt.customer_id, 
    SUM(points) AS total_points
  FROM points_table as pt
  GROUP by pt.customer_id
)

SELECT fp.customer_id, fp.total_points
FROM final_points as fp
WHERE fp.customer_id IN ('A', 'B');
