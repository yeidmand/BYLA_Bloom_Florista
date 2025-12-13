import pandas as pd 
import os

FILE_CLIENTS = "login_client.csv"
FILE_STAFF = "works_delivery.csv"
FILE_PRODUCTS = "products_stock.csv"
FILE_ORDERS = "orders.csv"
FILE_COMPLAINTS = "complaints.csv"

def create_data_final():
    print("Checking data system....")

    if not os.path.exists(FILE_CLIENTS):
        data_clients = {
            "Name": ["Joao Pereira", "Maria Fernandes"],
            "Contact": ["961219231", "930153233"],
            "Password": ["client1", "client2"],
            "Address": ["Travessia Amelia Rodrigues", "Rua Antonio Fonseca"],
            "ZP1": ["152", "743"],
            "ZP2": ["4700", "4720"],
            "Orders": ["103", "336"]
        }

        pd.DataFrame(data_clients).to_csv(FILE_CLIENTS, index=False, sep=";")
        print(f"Newly created: {FILE_CLIENTS}")
    else: 
        print(f"Already exist: {FILE_CLIENTS} (keep)")

    if not os.path.exists(FILE_STAFF):
        data_staff = {
            "Login": ["109609", "113168"],
            "Password": ["Yeidman", "Andre"],
            "Zone": ["Gestor", "Center"],
            "Work_Hour": ["all_day", "week_morning"]
        }
        pd.DataFrame(data_staff).to_csv(FILE_STAFF, index=False, sep=';')
        print(f"Newly created: {FILE_STAFF}")
    else:
        print(f"Already exist: {FILE_STAFF} (keep)")

    if not os.path.exists(FILE_PRODUCTS):
        data_products = {
            "Id": [2001, 2002, 2003, 2004, 2005],
            "Product": ["Flores variadas", "Rosas", "Lirios", "Tuplipas", "Margaridas"],
            "Quantity in stock": [250, 500, 150, 175, 200],
            "Unite price": ["3,00", "5,00", "12,00", "15,00", "8,00"]
        }
        pd.DataFrame(data_products).to_csv(FILE_PRODUCTS, index=False, sep=';')
        print(f"Newly created: {FILE_PRODUCTS}")
    else:
        print(f"Already exist: {FILE_PRODUCTS} (keep)")

    if not os.path.exists(FILE_ORDERS):
        cols = ["order_id", "client_id", "product_id", "status", "shipper_id"]
        pd.DataFrame(columns=cols).to_csv(FILE_ORDERS, index=False, sep=';')
        print(f"Newly created: {FILE_ORDERS}")
    else:
        print(f"Already exist: {FILE_ORDERS} (keep)")


    if not os.path.exists(FILE_COMPLAINTS):
        columns_complaints = [
            "order_id", 
            "client_id", 
            "accused_shipper",
            "reason_type", 
            "priority", 
            "content", 
            "date_created", 
            "status"
        ]
        
        df_complaints = pd.DataFrame(columns=columns_complaints)
        
        df_complaints.to_csv(FILE_COMPLAINTS, index=False, sep=';', encoding='utf-8-sig')
        print("New file complaints csv has been created.")
    else:
        print("Exited. Skip")

if __name__ == "__main__":
    create_data_final()

