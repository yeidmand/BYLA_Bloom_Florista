#Yeidman

import pandas as pd
import datetime as dtime
from data_manager import load_orders, save_orders, load_products, load_order_events, save_order_events, load_order_items, save_order_items
import utils as ut


#def ModOrderGestao(Manager):
#if Manager == "SUPm":
    #isSupervisor = True
#else:
    #isSupervisor = False

def initOrderManagementMenu():
        ValidOption = False

        while ValidOption == False:

            print("=== Gestão de Pedidos ===")
            print("1. Ver Pedidos Pendentes")
            print("2. Ver Pedidos Validados")
            print("3. Ver pedidos cancelados")
            print("4. Atribuir estafeta")
            print("5. Filtrar pedidos")
            print("6. Voltar ao menu principal")
            choice = input("Selecione uma opção: ")
            if choice in ['1', '2', '3', '4', '5', '6']:
                ValidOption = True
            else:
                print("Opção inválida. Por favor, tente novamente.")    


        return choice

MenuInitial = True

while MenuInitial:

    option = initOrderManagementMenu()
    orders_df = load_orders()
    order_it = load_order_items()
    products_df = load_products()
    order_events_df = load_order_events()

    if option == '1':
        pending_orders = orders_df[orders_df['order_status'] == 'pending']
        print(pending_orders[['order_id', 'order_status']])
        print("\n")
        print("Insira o ID do pedido para ver detalhes ou ediar")
        print("Ou inisra 'voltar' para regressar ao menu anterior")
        userInput = input("ID do pedido (ou 'voltar'): ")
        if userInput.strip().lower() == 'voltar':
            continue
        else:
            userInput = userInput.strip().upper()
            order_details = pending_orders[pending_orders['order_id'] == userInput]
            if not order_details.empty:
                print(order_details)
                details = {
                    "Numero do Pedido": order_details.iloc[0]['order_id'],
                    "Nome do Cliente": order_details.iloc[0]['name'],
                    "Contacto": order_details.iloc[0]['contact'],
                    "Morada": order_details.iloc[0]['address'],
                    "Codigo Postal": f"{order_details.iloc[0]['ZP1']}-{order_details.iloc[0]['ZP2']}",
                    "Estado do Pedido": order_details.iloc[0]['order_status'],
                }
                for key, value in details.items():
                    print(f"{key}: {value}")
                else:
                    print("Pedido não encontrado.")
    else:
        pass