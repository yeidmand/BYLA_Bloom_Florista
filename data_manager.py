import pandas as pd
import os

FILE_CLIENTS = "login_client.csv"
FILE_STAFF = "user_work_profil.csv"
FILE_PRODUCTS = "products_stock.csv"
FILE_ORDERS = "order_data.csv"
FILE_COMPLAINTS = "complaints.csv"
FILE_ENEVENTS = "order_events.csv"
FILE_ORDERS_ITEMS = "order_items.csv"


def load_products():
    if os.path.exists(FILE_PRODUCTS):
        return pd.read_csv(FILE_PRODUCTS, sep=";", dtype= {
            "product_id": str,
            "name_product": str,
            "stock_quantity": int,
            "price_unit": float,
            "available": bool,
            "category": str,
            "product_type": str,
            "description": str})
    return pd.DataFrame()

def save_products(df):
    df.to_csv(FILE_PRODUCTS, index=False, sep=";")

def load_orders():
    if os.path.exists(FILE_ORDERS):
        df = pd.read_csv(FILE_ORDERS, sep=";", dtype=str)
        return df
    return pd.DataFrame(columns= [
    "order_id",
    "id_client",
    "name",
    "contact",
    "address",
    "ZP1",
    "ZP2",
    "order_status",
    "order_reason",
    "id_worker",
    "duty_area"
])

def save_orders(df):
    df.to_csv(FILE_ORDERS, index=False, sep=";")

def load_complaints():
    if os.path.exists(FILE_COMPLAINTS):
        df = pd.read_csv(FILE_COMPLAINTS, sep=';', dtype=str, encoding='utf-8-sig')
        if "Unnamed: 0" in df.columns:
            df = df.drop(columns=["Unnamed: 0"])
        return df
    
    return pd.DataFrame(columns=[
        "order_id", 
        "client_id", 
        "accused_shipper",
        "reason_type", 
        "priority", 
        "content", 
        "date_created", 
        "status"
    ])

def save_complaints(df):
    df.to_csv(FILE_COMPLAINTS, index=False, sep=';', encoding='utf-8-sig')

def load_order_events():
    if os.path.exists(FILE_ENEVENTS):
        df = pd.read_csv(FILE_ENEVENTS, sep=";")
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['staptime_1'] = pd.to_datetime(df['staptime_1'], errors='coerce')
        df['staptime_2'] = pd.to_datetime(df['staptime_2'], errors='coerce')
        return df
    return pd.DataFrame(
        columns=[
            "event_id",
            "order_id",
            "event_type",
            "staptime_1",
            "staptime_2",
            "login",
            "details",
            "latitude",
            "longitude"
        ]
    )

def save_order_events(df):
    df.to_csv(FILE_ENEVENTS, index=False, sep=";")

def load_order_items():
    if os.path.exists(FILE_ORDERS_ITEMS):
        return pd.read_csv(
            FILE_ORDERS_ITEMS, sep=";", dtype={
                "order_id": str,
                "product_id": str,
                "quantity_ordered": int,
                "price_unit": float,
                "subtotal": float,
                "status": str,
                "quantity_returned": "Int64"
            }
        )
    return pd.DataFrame(
        columns=[
            "order_id", "product_id", "quantity_ordered",
            "price_unit", "subtotal"
        ]
    )

def save_order_items(df):
    df.to_csv(FILE_ORDERS_ITEMS, index=False, sep=";")

def load_user_work_profil():
    if os.path.exists(FILE_STAFF):
        return pd.read_csv(FILE_STAFF, sep=";", dtype=str)
    else:
        return pd.DataFrame(
            columns=[
                "id_worker",
                "password",
                "duty_area",
                "work_hour"
            ]

        )   

def load_zone_codes():
    if os.path.exists("zp_zones.csv"):
        return pd.read_csv("zp_zones.csv", sep=";", dtype=str)
    else:
        return pd.DataFrame(
            columns=[
                "Codes",
                "Zone"
            ]
        )