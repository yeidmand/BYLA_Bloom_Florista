import pandas as pd
import os 

FILE_CLIENTS = "login_client.csv"
FILE_STAFF = "user_work_profil.csv"
FILE_PRODUCTS = "products_stock.csv"
FILE_ORDERS = "order_data.csv"
FILE_COMPLAINTS = "complaints.csv"
FILE_ENEVENTS = "order_events.csv"
FILE_ORDERS_ITEMS = "order_items.csv"

def load_all_users_for_login():
    all_users = []

    if os.path.exists(FILE_CLIENTS):
        try:
            df=pd.read_csv(FILE_CLIENTS, sep=';', dtype=str)
            for _, row in df.iterrows():
                all_users.append({
                    "id": str(row["contact"]),
                    "pass": str(row["password"]),
                    "role": "client",
                    "name": str(row["name"])
                })
        except Exception as e:
            print(f"Error read clients: {e}")

    if os.path.exists(FILE_STAFF):
        try:
            df = pd.read_csv(FILE_STAFF, sep=';', dtype=str)
            for _, row in df.iterrows():
                user_role = "estafeta"
                if "Gestor" in str(row["dutyArea"]):
                    user_role = "manager"
                
                all_users.append({
                    "id": str(row["login"]),
                    "pass": str(row["password"]),
                    "role": user_role,
                    "name": str(row["login"])
                })
        except Exception as e:
            print(f"⚠ Lỗi đọc Staff: {e}")

    return pd.DataFrame(all_users)


def load_products():
    if os.path.exists(FILE_PRODUCTS):
        return pd.read_csv(FILE_PRODUCTS, sep=';', dtype=str)
    return pd.DataFrame()

def save_products(df):
    df.to_csv(FILE_PRODUCTS, index=False, sep=';')

def load_orders():
    if os.path.exists(FILE_ORDERS):
        return pd.read_csv(FILE_ORDERS, sep=';')
    return pd.DataFrame(columns= [
    "order_id",
    "id_client",
    "name",
    "contact",
    "address",
    "ZP1",
    "ZP2",
    "order_status",
    "tracking_number",
    "id_worker"
])

def save_orders(df):
    df.to_csv(FILE_ORDERS, index=False, sep=';')

def load_complaints():
    if os.path.exists(FILE_COMPLAINTS):
        return pd.read_csv(FILE_COMPLAINTS, sep=';')
    return pd.DataFrame(columns=["order_id", "content"])

def save_complaints(df):
    df.to_csv(FILE_COMPLAINTS, index=False, sep=';')

def load_order_events():
    if os.path.exists(FILE_ENEVENTS):
        return pd.read_csv(FILE_ENEVENTS, sep=';')
    return pd.DataFrame(columns=[
        "event_id",
        "order_id",
        "order_status",
        "timestamp",
        "login",
        "reason"
    ])
def save_order_events(df):
    df.to_csv(FILE_ENEVENTS, index=False, sep=';')

def load_order_items():
    if os.path.exists(FILE_ORDERS_ITEMS):
        return pd.read_csv(FILE_ORDERS_ITEMS, sep=';')
    return pd.DataFrame(columns=[
        "order_id",
        "product_id",
        "quantity_ordered",
        "price_unit",
        "subtotal"
    ])
def save_order_items(df):
    df.to_csv(FILE_ORDERS_ITEMS, index=False, sep=';')
    