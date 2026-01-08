import pandas as pd
import data_manager as dm
from datetime import datetime
from utils import order_filters

def mod_client(client_id):
    clients_df = pd.read_csv('login_client.csv', sep=';', dtype=str)
    
    if pd.isna(client_id) or str(client_id).strip() == '':
        register_new_client(clients_df)
    else:
        welcome_client(client_id, clients_df)

def register_new_client(clients_df):
    print("Registar novo cliente:")
    name = input("Nome: ")
    contact = input("Contacto: ")
    password = input("Password: ")
    address = input("Morada: ")
    zp1 = input("ZP1: ")
    zp2 = input("ZP2: ")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    new_id = f"CL{timestamp}"
    new_row = {
        'id_client': new_id, 'name': name, 'contact': contact,
        'password': password, 'address': address, 'ZP1': zp1, 'ZP2': zp2
    }
    
    clients_df = pd.concat([clients_df, pd.DataFrame([new_row])], ignore_index=True)
    clients_df.to_csv('login_client.csv', index=False, sep=',')
    print(f"Cliente {new_id} registado!")

def welcome_client(client_id, clients_df):
    client = clients_df[clients_df['id_client'] == client_id].iloc[0]
    print(f"Bem-vindo {client['name']}!")
    print("1. Fazer encomenda")
    print("2. Ver encomendas")
    
    op = input("Opção: ")
    if op == '1':
        fazer_encomenda(client_id, client)
    elif op == '2':
        ver_encomendas(client_id)

def fazer_encomenda(client_id, client):
    products_df = dm.load_products()
    print("Produtos disponíveis:")
    for _, p in products_df[products_df['available']].iterrows():
        print(f"{p['product_id']} - {p['name_product']} (stock: {p['quantity_stock']})")
    
    items = []
    while True:
        pid = input("ID produto (Enter para parar): ")
        if not pid:
            break
        qty = int(input("Qtd (max stock): "))
        items.append({'product_id': pid, 'quantity_ordered': qty, 'price_unit': products_df[products_df['product_id']==pid]['price_unit'].iloc[0]})
    
    print("AVISO: encomenda não cancelável!")
    if input("Confirmar? (s/n): ") == 's':
        orders_df = dm.load_orders()
        oid = f"PT{len(orders_df)+1:02d}"
        new_order = pd.DataFrame([{
            'order_id': oid, 'id_client': client_id, 'name': client['name'],
            'contact': client['contact'], 'address': client['address'],
            'ZP1': client['ZP1'], 'ZP2': client['ZP2'], 'order_status': 'pending',
            'order_reason': '', 'id_worker': '', 'dutyarea': ''
        }])
        orders_df = pd.concat([orders_df, new_order])
        dm.save_orders(orders_df)
        
        items_df = dm.load_order_items()
        for item in items:
            item['order_id'] = oid
            item['subtotal'] = item['quantityordered'] * item['priceunit']
            item['status'] = 'pending'
            item['quantity_returned'] = 0
            items_df = pd.concat([items_df, pd.DataFrame([item])])
        dm.save_order_items(items_df)
        
        print(f"Encomenda {oid} criada!")

def ver_encomendas(client_id):
    orders_df = dm.load_orders()
    client_orders = orders_df[orders_df['id_client'] == client_id]
    
    if client_orders.empty:
        print("Ainda não fez pedidos.")
        return
    
    print("Seus pedidos:")
    for _, o in client_orders.iterrows():
        print(o['order_id'], o['order_status'])
    
    if input("Filtrar por status? (s/n): ") == 's':
        order_filters(client_id, orders_df, dm.load_products())

mod_client("CL001")