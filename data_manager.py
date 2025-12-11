import pandas as pd
import os 

FILE_CLIENTS = "login_client.csv"
FILE_STAFF = "works_delivery.csv"
FILE_PRODUCTS = "products_stock.csv"
FILE_ORDERS = "orders.csv"
FILE_COMPLAINTS = "complaints.csv"

def load_all_users_for_login():
    all_users = []

    if os.path.exists(FILE_CLIENTS):
        try:
            df=pd.read_csv(FILE_CLIENTS, sep=';', dtype=str)
            for _, row in df.iterrows():
                all_users.append({
                    "id": str(row["Contact"]),
                    "pass": str(row["Password"]),
                    "role": "client",
                    "name": str(row["Name"])
                })
        except Exception as e:
            print(f"Error read clients: {e}")

    if os.path.exists(FILE_STAFF):
        try:
            df = pd.read_csv(FILE_STAFF, sep=';', dtype=str)
            for _, row in df.iterrows():
                user_role = "estafeta"
                if "Gestor" in str(row["Zone"]):
                    user_role = "manager"
                
                all_users.append({
                    "id": str(row["Login"]),
                    "pass": str(row["Password"]),
                    "role": user_role,
                    "name": str(row["Login"])
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
    return pd.DataFrame(columns=["order_id", "client_id", "product_id", "status", "shipper_id"])

def save_orders(df):
    df.to_csv(FILE_ORDERS, index=False, sep=';')

def load_complaints():
    if os.path.exists(FILE_COMPLAINTS):
        return pd.read_csv(FILE_COMPLAINTS, sep=';')
    return pd.DataFrame(columns=["order_id", "content"])

def save_complaints(df):
    df.to_csv(FILE_COMPLAINTS, index=False, sep=';')
