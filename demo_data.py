import pandas as pd
import numpy as np

def generate_demo_dataset() -> pd.DataFrame:
    """
    Generates a realistic multi-period business dataset containing intentional business patterns:
    1. Revenue decline in South region due to Product A stock shortage.
    2. Electronics category revenue growth.
    3. March outlier anomaly.
    """
    np.random.seed(42)

    # Dates spanning 12 months (Jan 2025 to Dec 2025)
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    n_rows = 240

    sample_dates = np.random.choice(dates, size=n_rows)
    sample_dates.sort()
    sample_ts = pd.to_datetime(sample_dates)

    regions = ["North", "South", "East", "West"]
    region_weights = [0.3, 0.3, 0.2, 0.2]
    sampled_regions = np.random.choice(regions, size=n_rows, p=region_weights)

    products_map = {
        "Product A": "Electronics",
        "Product B": "Electronics",
        "Product C": "Office Supplies",
        "Product D": "Furniture"
    }

    products = list(products_map.keys())
    sampled_products = np.random.choice(products, size=n_rows)
    sampled_categories = [products_map[p] for p in sampled_products]

    customer_ids = [f"CUST-{np.random.randint(1000, 9999)}" for _ in range(n_rows)]

    unit_prices = {
        "Product A": 450.0,
        "Product B": 300.0,
        "Product C": 45.0,
        "Product D": 120.0
    }

    unit_costs = {
        "Product A": 280.0,
        "Product B": 180.0,
        "Product C": 20.0,
        "Product D": 70.0
    }

    quantities = []
    revenues = []
    costs = []
    profits = []
    inventories = []

    for i in range(n_rows):
        dt = sample_ts[i]
        reg = sampled_regions[i]
        prod = sampled_products[i]
        
        base_qty = np.random.randint(5, 25)
        
        # Pattern 1: Inventory bottleneck & sales decline in South region in H2 (after July 1)
        if reg == "South" and dt > pd.Timestamp("2025-07-01"):
            if prod == "Product A":
                base_qty = max(1, int(base_qty * 0.45))  # 55% drop in Product A qty
                inv = np.random.randint(3, 12)  # Low inventory
            else:
                base_qty = int(base_qty * 0.8)
                inv = np.random.randint(15, 35)
        else:
            inv = np.random.randint(40, 100)

        # Pattern 2: Electronics growth in Q4
        if products_map[prod] == "Electronics" and dt > pd.Timestamp("2025-10-01") and reg != "South":
            base_qty = int(base_qty * 1.35)

        price = unit_prices[prod]
        cost_unit = unit_costs[prod]

        rev = round(base_qty * price, 2)
        cst = round(base_qty * cost_unit, 2)
        prf = round(rev - cst, 2)

        # Pattern 3: Inject single anomaly in March
        if i == 50:
            rev = 15.0  # Unusually low sales transaction anomaly
            prf = -200.0

        quantities.append(base_qty)
        revenues.append(rev)
        costs.append(cst)
        profits.append(prf)
        inventories.append(inv)

    df = pd.DataFrame({
        "Order_Date": [d.strftime("%Y-%m-%d") for d in sample_ts],
        "Region": sampled_regions,
        "Product": sampled_products,
        "Category": sampled_categories,
        "Customer_ID": customer_ids,
        "Quantity": quantities,
        "Revenue": revenues,
        "Cost": costs,
        "Profit": profits,
        "Inventory_Level": inventories
    })

    return df
