#Yeidman

import pandas as pd
import datetime as dtime
from data_manager import load_orders, save_orders, load_products, save_products, load_order_events, save_order_events, load_order_items, save_order_items
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
        print("===Validação de Encomendas===")
        print("6. Rejeitar encomenda")
        print("7. Validar automaticamente a encomenda")
        print("8. Voltar ao menu anterior")
        choice = input("Selecione uma opção: ")
        
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
            validOption = True
        else:
            print("\nOpção inválida. Por favor, tente novamente.\n")
    return choice
     
MenuInitial = True

while MenuInitial:

    option = initOrderManagementMenu()
    orders_df = load_orders()
    order_it = load_order_items()
    products_df = load_products()
    order_events_df = load_order_events()

    #Diccionario dos nomes dos produto por chave = product_id
    products_name = dict(zip(products_df['product_id'], products_df['name_product']))


    if option == '1':
        
        insideMenu = True
        while insideMenu:
            pending_orders = orders_df[orders_df['order_status'] == 'pending']
            if pending_orders.empty:
                print("======================================")
                print("== Não existem pedidos pendentes ===")
                print("======================================")
                insideMenu = False
                continue
            else:
                pending_id = pending_orders['order_id'].tolist()
                ut.showOrderStatus(pending_orders)

                print("Insira o ID do pedido para ver detalhes ou editar")
                print("Ou insira 'voltar' para regressar ao menu anterior")

                userInput = input("ID do pedido (ou 'voltar'): ")
                userInput = userInput.strip().upper()

                if userInput.strip().lower() == 'voltar':
                    insideMenu = False
                    continue
                

                elif userInput in pending_id:            

                    insideMenu = False

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

                            elif editChoice == '6':

                                if isSupervisor:
                                    orders_df, order_it, products_df, order_events_df = ut.reject_order(userInput, orders_df, order_it, products_df, order_events_df, Manager, save_orders, save_order_items, save_products, save_order_events)
                                    editMenu = False
                                else:
                                    print("Apenas O Supervisor Senior podem rejeitar encomendas.")
                                    editMenu = False

                            elif editChoice == '7':
                                # Validar automaticamente a encomenda
                                if isSupervisor:
                                    order_to_validate = orders_df[orders_df['order_id'] == userInput]
                                    is_valid, reason = ut.addressValidation(order_to_validate)
                                    if is_valid:
                                        print("\n======================================")
                                        print("===Morada válida===")
                                        print("======================================\n")
                                        
                                        is_valid, reason = ut.recipientValidation(order_to_validate)
                                        if is_valid:
                                            print("=======================================")
                                            print("===Dados do destinatário válidos===")
                                            print("=======================================\n")

                                            missing_products = ut.stockValidation(order_items_filtered, products_df)

                                            if not missing_products:
                                                print("======================================")
                                                print("===Stock da Enocmenda válidos===")
                                                print("======================================\n")
                                                
                                                orders_df.loc[orders_df['order_id'] == userInput, 'order_status'] = 'validated'
                                                order_it.loc[order_it['order_id'] == userInput, 'status'] = 'shipped'
                                                save_orders(orders_df)
                                                save_order_items(order_it)
                                                print("Encomenda validada automaticamente com sucesso.\n")

                                                #Registrar evento
                                                new_event = {
                                                    'event_id': 'EV' + dtime.datetime.now().strftime("%Y%m%d%H%M%S"),
                                                    'order_id': userInput,
                                                    'event_type': 'auto_validate_order',
                                                    'timestamp': dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                    'login': Manager,
                                                    'details': "Encomenda validada automaticamente pelo sistema."
                                                }
                                                order_events_df = pd.concat([order_events_df, pd.DataFrame([new_event])], ignore_index=True)
                                                save_order_events(order_events_df)
                                                editMenu = False
                                            else:
                                                qty_prod = order_it[order_it['order_id'] == userInput].shape[0]
                                                print("Encomenda inválida.")
                                                print(f"Produtos não disponíveis:\n"
                                                          + "".join(f"SKU: {sku} " + "Produto: " + products_name[sku] + "\n" for sku in missing_products)
                                                        )
                                                if qty_prod == len(missing_products):
                                                    print("A encomenda deve ser cancelada. Todos os productos estão indisponíveis.")
                                                    orders_df, order_it, products_df, order_events_df = ut.reject_order(userInput, orders_df, order_it, products_df, order_events_df, Manager, save_orders, save_order_items, save_products, save_order_events)
                                                    print("Encomenda rejeitada com sucesso.")

                                                else:
                                                    OpenMenu = True
                                                    while OpenMenu:
                                                    
                                                        print("Deseja preparar a encomenda parcialmente? (s/n)")
                                                        option_validation = input().strip().lower()
                                                        if option_validation in ['s', 'n']:
                                                            OpenMenu = False
                                                            if option_validation == 's':
                                                                OpenMenu = False 
                                                                editMenu = False 
                                                                insideMenu = False
                                                                #Registo de status da encoemenda
                                                                orders_df.loc[orders_df['order_id'] == userInput, "order_status"] = "partially shipped"
                                                                save_orders(orders_df)
                                                                # Registo por defeito do estatus do envío dos artigos
                                                                order_it.loc[order_it['order_id'] == userInput, "status"] = "shipped"
                                                                save_order_items(order_it)

                                                                print("======================================")
                                                                print("===Encomenda preparada parcialmente===")
                                                                print("======================================")                                                                    

                                                                for sku in missing_products:
                                                                    # Atulizamos o status dos artigos no disponíveis na encomenda
                                                                    order_it.loc[(order_it["order_id"] == userInput) & (order_it["product_id"] == sku), "status"] = "canceled"

                                                                    #Quantidade de artigos no disponíveis encomendadas
                                                                    quantity_ordered = order_it.loc[(order_it["order_id"] == userInput) & (order_it["product_id"] == sku), "quantity_ordered"].iloc[0]
                                                                    order_it.loc[(order_it["order_id"] == userInput) & (order_it["product_id"] == sku), "quantity_returned"] = quantity_ordered

                                                                    # Retorno dessa quantidade ao stock ####IMPORTANTE#### ####A DEFINIR####
                                                                    products_df.loc[products_df["product_id"] == sku, "quantity_stock"] += quantity_ordered
                                                                    save_products(products_df)
                                                                    save_order_items(order_it)
                                                                        
                                                                                                                                            
                                                                #Registo de Evento:
                                                                new_event = {
                                                                        'event_id': 'EV' + dtime.datetime.now().strftime("%Y%m%d%H%M%S"),
                                                                        'order_id': userInput,
                                                                        'event_type': 'auto_validate_order',
                                                                        'timestamp': dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                                        'login': Manager,
                                                                        'details': "Encomenda preparada parcialmente com sucesso."
                                                                    }

                                                                order_events_df = pd.concat([order_events_df, pd.DataFrame([new_event])], ignore_index=True)
                                                                save_order_events(order_events_df)
                                                        else:
                                                            print("Opção inválida. Tente novamente.")
                                                    
                                        else:
                                            print(f"Dados do destinatário inválidos. Motivo: {reason}")
                                            print("Voltando ao menu de edição...")                            
                                            save_order_items(order_it)
                                    else:
                                        print(f"Morada inválida. Motivo: {reason}")
                                        OpenMenu = True
                                        while OpenMenu:
                                            option_validation = input("Deseja editar a morada do destinatário? (s/n): ").strip().lower()
                                            if option_validation in ['s', 'n']:
                                                OpenMenu = False
                                                if option_validation == 's':
                                                    new_address = input("Insira a nova morada do destinatário: ")
                                                    zip1, zip2 = input("Insira o novo código postal (formato: 4750-123): ").split("-")
                                                    zip1 = zip1.strip()
                                                    zip2 = zip2.strip()
                                                    
                                                    orders_df.loc[orders_df['order_id'] == userInput, 'address'] = new_address
                                                    orders_df.loc[orders_df['order_id'] == userInput, 'ZP1'] = zip1
                                                    orders_df.loc[orders_df['order_id'] == userInput, 'ZP2'] = zip2
                                                    save_orders(orders_df)
                                                    print("Morada atualizada com sucesso.")                        
                                                    update_order = orders_df[orders_df['order_id'] == userInput]
                                                    ut.showDetailsDestinatario(update_order)

                                                    #Registrar evento
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
                                                    print("Voltando ao menu de edição...")
                                                elif option_validation == 'n':
                                                    print("Voltando ao menu de edição...")
                                            else:
                                                print("Opção inválida. Tente novamente.")                                            
                                    
                                else:
                                    print("Apenas O Supervisor Senior podem rejeitar encomendas.")
                                    print("Voltando ao menu de edição...")
                        
                            elif editChoice == '8':
                                editMenu = False
                                print("A regressar ao menu de pedidos pendentes...")
                else:
                    print("Pedido não encontrado.")
        
    elif option == '6':
        MenuInitial = False
        print("A regressar ao menu principal...")
        #Return

    elif option == '2':
        validated_orders = orders_df[orders_df['order_status'].isin(['validated', 'partially shipped'])].reset_index(drop=True)
        print("\n======================================")
        print("=== Encomendas Validadas ===")
        print("======================================")

        if validated_orders.empty:
            print("\nNão existem encomendas validadas ou parcialmente enviadas.\n")
        else:
            i = 0
            total_orders = len(validated_orders)
            print("\n======================================")
            print(f"=== Total de encomendas validadas: {total_orders}===")
            print("======================================")


            while i < total_orders:
                order = validated_orders.iloc[i]

                print("\n======================================")
                print(f"ID: {order['order_id']} | Estado: {order['order_status']}")
                print(f"Destinatário: {order['name']} | Contacto: {order['contact']}")
                print(f"Morada: {order['address']}")
                print(f"Código Postal: {order['ZP1']}-{order['ZP2']}")
                print("======================================")


                if i < total_orders - 1:
                    # Ainda há próximas encomendas
                    while True:
                        print("Escolha uma das seguintes opções")
                        print("1. Seguinte encomenda")
                        print("2. Sair")
                        resp = input("Opção: ").strip().lower()
                        if resp == '1':
                            i += 1      # passa ao próximo pedido
                            break
                        elif resp == '2':
                            print("A regressar ao menu inicial...")
                            i = total_orders   # força saída do while
                            break
                        else:
                            print("Opção inválida. Escreva '1' para ver a seguiente encomenda\n ou '2' para sair.")
                else:
                    # Última encomenda
                    input("Última encomenda. Prima ENTER para voltar ao menu inicial.")
                    i = total_orders

    elif option == '3':
        canceled_orders = orders_df[orders_df['order_status'] == 'canceled'].reset_index(drop=True)
        