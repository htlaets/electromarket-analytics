import os
import sqlite3
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker


np.random.seed(42)
fake = Faker("ru_RU")
Faker.seed(42)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_DIR = os.path.join(BASE_DIR, "data", "database")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)


def random_date(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    random_days = np.random.randint(0, delta.days + 1)
    return start + timedelta(days=int(random_days))


def generate_customers(n=5000):
    cities = [
        "Москва", "Санкт-Петербург", "Казань", "Екатеринбург",
        "Новосибирск", "Нижний Новгород", "Самара", "Краснодар",
        "Ростов-на-Дону", "Воронеж"
    ]

    channels = ["SEO", "Paid Ads", "Social Media", "Referral", "Email"]

    customers = []

    for i in range(1, n + 1):
        gender = np.random.choice(["Male", "Female"], p=[0.48, 0.52])

        customers.append({
            "customer_id": f"C{i:05d}",
            "full_name": fake.name_male() if gender == "Male" else fake.name_female(),
            "gender": gender,
            "age": int(np.random.randint(18, 65)),
            "city": np.random.choice(cities),
            "registration_date": random_date("2023-01-01", "2025-12-31").date(),
            "acquisition_channel": np.random.choice(
                channels,
                p=[0.25, 0.30, 0.20, 0.15, 0.10]
            )
        })

    return pd.DataFrame(customers)


def generate_products(n=1000):
    categories = {
        "Smartphones": (15000, 150000),
        "Laptops": (30000, 250000),
        "Headphones": (2000, 40000),
        "TV": (20000, 180000),
        "Gaming": (5000, 120000),
        "Accessories": (500, 15000),
        "Smart Home": (2000, 60000)
    }

    brands = ["Samsung", "Apple", "Xiaomi", "Huawei", "Sony", "Lenovo", "Asus", "LG", "Acer", "Logitech"]

    products = []

    for i in range(1, n + 1):
        category = np.random.choice(list(categories.keys()))
        min_price, max_price = categories[category]
        price = round(float(np.random.uniform(min_price, max_price)), 2)
        cost = round(price * float(np.random.uniform(0.55, 0.80)), 2)

        products.append({
            "product_id": f"P{i:05d}",
            "product_name": f"{np.random.choice(brands)} {category} Model {i}",
            "category": category,
            "brand": np.random.choice(brands),
            "price": price,
            "cost": cost
        })

    return pd.DataFrame(products)


def generate_orders(customers, n=25000):
    statuses = ["completed", "cancelled", "returned"]
    payment_methods = ["Card", "Cash", "Installment", "Online Wallet"]
    delivery_types = ["Courier", "Pickup Point", "Post"]

    orders = []

    customer_ids = customers["customer_id"].tolist()
    registration_dates = dict(zip(customers["customer_id"], customers["registration_date"]))

    for i in range(1, n + 1):
        customer_id = np.random.choice(customer_ids)
        reg_date = pd.to_datetime(registration_dates[customer_id])

        order_date = random_date(
            reg_date.strftime("%Y-%m-%d"),
            "2026-03-31"
        ).date()

        orders.append({
            "order_id": f"O{i:06d}",
            "customer_id": customer_id,
            "order_date": order_date,
            "status": np.random.choice(statuses, p=[0.82, 0.11, 0.07]),
            "payment_method": np.random.choice(payment_methods),
            "delivery_type": np.random.choice(delivery_types)
        })

    return pd.DataFrame(orders)


def generate_order_items(orders, products):
    order_items = []
    product_ids = products["product_id"].tolist()
    product_prices = dict(zip(products["product_id"], products["price"]))

    item_id = 1

    for order_id in orders["order_id"]:
        items_count = np.random.randint(1, 5)

        selected_products = np.random.choice(product_ids, size=items_count, replace=False)

        for product_id in selected_products:
            price = product_prices[product_id]
            discount = np.random.choice([0, 0.05, 0.10, 0.15, 0.20], p=[0.50, 0.20, 0.15, 0.10, 0.05])

            order_items.append({
                "order_item_id": f"OI{item_id:07d}",
                "order_id": order_id,
                "product_id": product_id,
                "quantity": int(np.random.choice([1, 1, 1, 2, 3])),
                "unit_price": price,
                "discount": discount
            })

            item_id += 1

    return pd.DataFrame(order_items)


def generate_sessions(customers, n=60000):
    devices = ["Desktop", "Mobile", "Tablet"]
    traffic_sources = ["Organic", "Paid Ads", "Social", "Referral", "Email", "Direct"]

    sessions = []

    customer_ids = customers["customer_id"].tolist()
    registration_dates = dict(zip(customers["customer_id"], customers["registration_date"]))

    for i in range(1, n + 1):
        customer_id = np.random.choice(customer_ids)
        reg_date = pd.to_datetime(registration_dates[customer_id])

        added_to_cart = np.random.choice([0, 1], p=[0.65, 0.35])

        if added_to_cart == 1:
            made_purchase = np.random.choice([0, 1], p=[0.45, 0.55])
        else:
            made_purchase = np.random.choice([0, 1], p=[0.95, 0.05])

        sessions.append({
            "session_id": f"S{i:07d}",
            "customer_id": customer_id,
            "session_date": random_date(
                reg_date.strftime("%Y-%m-%d"),
                "2026-03-31"
            ).date(),
            "device": np.random.choice(devices, p=[0.35, 0.55, 0.10]),
            "traffic_source": np.random.choice(traffic_sources),
            "pages_viewed": int(np.random.randint(1, 25)),
            "session_duration_min": round(float(np.random.uniform(1, 40)), 2),
            "added_to_cart": int(added_to_cart),
            "made_purchase": int(made_purchase)
        })

    return pd.DataFrame(sessions)


def generate_reviews(orders, order_items, n=10000):
    completed_orders = orders[orders["status"] == "completed"]["order_id"].tolist()
    order_to_products = order_items.groupby("order_id")["product_id"].apply(list).to_dict()

    reviews = []

    selected_orders = np.random.choice(completed_orders, size=min(n, len(completed_orders)), replace=False)

    for i, order_id in enumerate(selected_orders, start=1):
        products_in_order = order_to_products.get(order_id, [])
        if not products_in_order:
            continue

        reviews.append({
            "review_id": f"R{i:06d}",
            "customer_id": orders.loc[orders["order_id"] == order_id, "customer_id"].values[0],
            "product_id": np.random.choice(products_in_order),
            "order_id": order_id,
            "rating": int(np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.08, 0.17, 0.35, 0.35])),
            "review_date": random_date("2023-01-01", "2026-03-31").date()
        })

    return pd.DataFrame(reviews)


def save_to_csv(dataframes):
    for name, df in dataframes.items():
        path = os.path.join(RAW_DIR, f"{name}.csv")
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"Saved: {path}")


def save_to_sqlite(dataframes):
    db_path = os.path.join(DB_DIR, "electromarket.db")

    conn = sqlite3.connect(db_path)

    for name, df in dataframes.items():
        df.to_sql(name, conn, if_exists="replace", index=False)
        print(f"Table created: {name}")

    conn.close()
    print(f"SQLite database created: {db_path}")


def main():
    print("Generating customers...")
    customers = generate_customers()

    print("Generating products...")
    products = generate_products()

    print("Generating orders...")
    orders = generate_orders(customers)

    print("Generating order items...")
    order_items = generate_order_items(orders, products)

    print("Generating sessions...")
    sessions = generate_sessions(customers)

    print("Generating reviews...")
    reviews = generate_reviews(orders, order_items)

    dataframes = {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
        "sessions": sessions,
        "reviews": reviews
    }

    save_to_csv(dataframes)
    save_to_sqlite(dataframes)

    print("Done!")


if __name__ == "__main__":
    main()