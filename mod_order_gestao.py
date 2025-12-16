#Yeidman

import pandas as pd
import datetime as dtime
from data_manager import load_orders, save_orders, load_products, load_order_events, save_order_events, load_order_items, save_order_items
import utils as ut


#def ModOrderGestao(Manager):
Manager = "SUPm" #ATENCION ELIMNAR AL INTEGRAR
if Manager == "SUPm":
    isSupervisor = True
else:
    isSupervisor = False

def initOrderManagementMenu():
        ValidOption = False

        while ValidOption == False:

            print("\n=== Gestão de Pedidos ===")
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

#Menu Editar Pedidos
def EditOrder():
    validOption = False
    
    while not validOption:
        print("===Editar Pedido===")
        print("1. Editar nome e apelido do destinatário")
        print("2. Editar contacto do destinatário")
        print("3. Editar morada do destinatário")
        print("4. Editar código postal do destinatário")
        print("5. Voltar ao menu anterior")
        choice = input("Selecione uma opção: ")
        validOption = ut.validoption(choice, ['1', '2', '3', '4', '5'])
        if not validOption:
            print("\nOpção inválida. Por favor, tente novamente.\n")
    return choice
     
MenuInitial = True

while MenuInitial:

    option = initOrderManagementMenu()
    orders_df = load_orders()
    order_it = load_order_items()
    products_df = load_products()
    order_events_df = load_order_events()

    if option == '1':
        
        insideMenu = True
        while insideMenu:
            pending_orders = orders_df[orders_df['order_status'] == 'pending']
            ut.showOrderStatus(pending_orders)

            print("Insira o ID do pedido para ver detalhes ou ediar")
            print("Ou inisra 'voltar' para regressar ao menu anterior")

            userInput = input("ID do pedido (ou 'voltar'): ")

            if userInput.strip().lower() == 'voltar':
                insideMenu = False
                continue
            else:
                userInput = userInput.strip().upper()

                order_details = pending_orders[pending_orders['order_id'] == userInput]
                
                order_items_filtered = order_it[order_it['order_id'] == userInput]
                if not order_details.empty:
                    ut.showDetailsOrder(order_details, order_items_filtered, products_df)
                    insideMenu = False

                    editMenu = True
                    while editMenu:
                        editChoice = EditOrder()
                        if editChoice == '1':
                            new_name = input("Insira o novo nome e apelido do destinatário: ")

                            orders_df.loc[orders_df['order_id'] == userInput, 'name'] = new_name
                            save_orders(orders_df)

                            print("Nome e apelido atualizados com sucesso.")                        
                            update_order = orders_df[orders_df['order_id'] == userInput]
                            ut.showDetailsDestinatario(update_order)
                            #Registrar evento
                            # Adicionar nova linha ao DataFrame de eventos
                            new_event = {
                                'event_id': 'EV' + dtime.datetime.now().strftime("%Y%m%d%H%M%S"),
                                'order_id': userInput,
                                'event_type': 'edit_recipient_name',
                                'timestamp': dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'login': Manager,
                                'details': f"Nome do destinatário alterado para: {new_name}"
                            }
                            order_events_df = pd.concat([order_events_df, pd.DataFrame([new_event])], ignore_index=True)
                            save_order_events(order_events_df)
                            print("Deseja continuar a editar este pedido? (s/n)")
                            cont_edit = input().strip().lower()
                            if cont_edit != 's':
                                editMenu = False
                        elif editChoice == '2':
                            new_contact = input("Insira o novo contacto do destinatário: ")

                            orders_df.loc[orders_df['order_id'] == userInput, 'contact'] = new_contact
                            save_orders(orders_df)

                            print("Contacto atualizado com sucesso.")                        
                            update_order = orders_df[orders_df['order_id'] == userInput]
                            ut.showDetailsDestinatario(update_order)
                            #Registrar evento
                            # Adicionar nova linha ao DataFrame de eventos
                            new_event = {
                                'event_id': 'EV' + dtime.datetime.now().strftime("%Y%m%d%H%M%S"),
                                'order_id': userInput,
                                'event_type': 'edit_recipient_contact',
                                'timestamp': dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'login': Manager,
                                'details': f"Contacto do destinatário alterado para: {new_contact}"
                            }
                            order_events_df = pd.concat([order_events_df, pd.DataFrame([new_event])], ignore_index=True)
                            save_order_events(order_events_df)

                            print("Deseja continuar a editar este pedido? (s/n)")
                            cont_edit = input().strip().lower()
                            if cont_edit != 's':
                                editMenu = False

                        elif editChoice == '3':
                            new_address = input("Insira a nova morada do destinatário: ")

                            orders_df.loc[orders_df['order_id'] == userInput, 'address'] = new_address
                            save_orders(orders_df)

                            print("Morada atualizada com sucesso.")                        
                            update_order = orders_df[orders_df['order_id'] == userInput]
                            ut.showDetailsDestinatario(update_order)

                            #Registrar evento
                            # Adicionar nova linha ao DataFrame de eventos
                            new_event = {
                                'event_id': 'EV' + dtime.datetime.now().strftime("%Y%m%d%H%M%S"),
                                'order_id': userInput,
                                'event_type': 'edit_recipient_address',
                                'timestamp': dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'login': Manager,
                                'details': f"Morada do destinatário alterada para: {new_address}"
                            }
                            order_events_df = pd.concat([order_events_df, pd.DataFrame([new_event])], ignore_index=True)
                            save_order_events(order_events_df)

                            print("Deseja continuar a editar este pedido? (s/n)")
                            cont_edit = input().strip().lower()
                            if cont_edit != 's':
                                editMenu = False

                        elif editChoice == '4':
                            new_ZP1 = input("Insira o novo código postal (parte 1) do destinatário: ")
                            new_ZP2 = input("Insira o novo código postal (parte 2) do destinatário: ")

                            orders_df.loc[orders_df['order_id'] == userInput, 'ZP1'] = new_ZP1
                            orders_df.loc[orders_df['order_id'] == userInput, 'ZP2'] = new_ZP2
                            save_orders(orders_df)

                            print("Código postal atualizado com sucesso.")                        
                            update_order = orders_df[orders_df['order_id'] == userInput]
                            ut.showDetailsDestinatario(update_order)

                            #Registrar evento
                            # Adicionar nova linha ao DataFrame de eventos
                            new_event = {
                                'event_id': 'EV' + dtime.datetime.now().strftime("%Y%m%d%H%M%S"),
                                'order_id': userInput,
                                'event_type': 'edit_recipient_postal_code',
                                'timestamp': dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'login': Manager,
                                'details': f"Código postal do destinatário alterado para: {new_ZP1}-{new_ZP2}"
                            }
                            order_events_df = pd.concat([order_events_df, pd.DataFrame([new_event])], ignore_index=True)
                            save_order_events(order_events_df)
                            
                            print("Deseja continuar a editar este pedido? (s/n)")
                            cont_edit = input().strip().lower()
                            if cont_edit != 's':
                                editMenu = False

                        elif editChoice == '5':
                            editMenu = False
                            print("A regressar ao menu de pedidos pendentes...")                           
                else:
                        print("Pedido não encontrado.")
    
    elif option == '6':
        MenuInitial = False
        print("A regressar ao menu principal...")
    else:
        pass