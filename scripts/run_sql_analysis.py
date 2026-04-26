import sqlite3
import pandas as pd


conn = sqlite3.connect("data/database/electromarket.db")


queries = {
    "Revenue by category": """
        SELECT
            p.category,
            ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status = 'completed'
        GROUP BY p.category
        ORDER BY revenue DESC;
    """,

    "Orders by status": """
        SELECT
            status,
            COUNT(*) AS orders_count
        FROM orders
        GROUP BY status
        ORDER BY orders_count DESC;
    """,

    "Revenue by acquisition channel": """
        SELECT
            c.acquisition_channel,
            ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS revenue
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status = 'completed'
        GROUP BY c.acquisition_channel
        ORDER BY revenue DESC;
    """
}


for title, query in queries.items():
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

    df = pd.read_sql_query(query, conn)
    print(df)


conn.close()