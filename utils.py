import pandas as pd
import datetime as dtime
import random as rd
import data_manager as dm


df_zone = pd.read_csv("zp_zones.csv", sep=";", dtype=str)
codes_list = df_zone['Codes'].tolist()
df_user_worker = dm.load_user_work_profil()

# Mostrar os detalhes de um pedido específico, incluindo informações do pedido e itens associados.
def showDetailsOrder(order_details, order_items_df, products_df):
    """
    Mostrar os detalhes de um pedido específico, incluindo informações do pedido e itens associados.
    Mostra apenas os itens cujo status é diferente de 'canceled'.
    """
    if order_details.empty:
        print("Erro: Detalhes do pedido não encontrados.")
        return

    # Detalhes do pedido
    print("\n=== Detalhes do Pedido ===")
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

    # Filtrar itens não cancelados
    if 'status' in order_items_df.columns:
        order_items_df = order_items_df[order_items_df['status'] != 'canceled']

    # Merge com produtos para ter o nome
    merged_items = order_items_df.merge(
        products_df[["product_id", "name_product"]],
        on='product_id',
        how='left'
    )

    print("=== Itens do Pedido ===")
    if merged_items.empty:
        print("Nenhum item encontrado para este pedido (todos os itens podem estar cancelados).")
    else:
        for _, item in merged_items.iterrows():
            product_name = item['name_product'] if pd.notna(item['name_product']) else f"Produto ID: {item['product_id']} (Nome não encontrado)"
            print(
                f"Produto: {product_name} | "
                f"Quantidade: {item['quantity_ordered']} | "
                f"Preço Unitário: {item['price_unit']}€ | "
                f"Subtotal: {item['subtotal']}€"
            )
        print(f"---------------------------------------------------Total do Pedido: {merged_items['subtotal'].sum()}€\n")
    return

# Mostrar o estado de todos os pedidos
def showOrderStatus(df_orders): # Mostrar o estado de todos os pedidos
    print("\n=== Encomendas ===")
    for _, row in df_orders.iterrows():
        print(f"ID: {row['order_id']} | Estado: {row['order_status']}")
    return

# Mostrar os detalhes do destinatário de um pedido específico
def showDetailsDestinatario(order_details):
    """
    Mostra os detalhes do destinatário de um pedido específico.
    
    Parâmetros:
    - order_details: DataFrame ou Series com os dados da encomenda
    
    Notas:
    - Se receber Series, converte para DataFrame automaticamente
    - Mostra informação de forma formatada e legível
    - Sem erros, apenas validação simples
    """
      
    # Se receber uma Series (uma linha de dados), converter para DataFrame
    # Series: ordem = {name: "João", contact: "961234567", ...}
    if isinstance(order_details, pd.Series):
        order_details = pd.DataFrame([order_details])
    
    # Se DataFrame vazio, não há dados para mostrar
    if order_details.empty:
        print("\n")
        print("─" * 70)
        print("❌ ERRO: Detalhes do pedido não encontrados".center(70))
        print("─" * 70)
        print()
        return
    
    # Garantir que temos a primeira linha (caso tenha múltiplas)
    # iloc[0] = primeira linha (índice 0)
    row = order_details.iloc[0]
    # Extrair os valores necessários
    # row['name'] = acessa a coluna 'name' da linha
    nome = row['name']
    contacto = row['contact']
    morada = row['address']
    zp1 = row['ZP1']
    zp2 = row['ZP2']
    
    # Formatar código postal com hífen
    # Exemplo: "4700" + "103" → "4700-103"
    codigo_postal = f"{zp1}-{zp2}"

    print("\n")
    print("─" * 70)    
    print("👤 DETALHES DO DESTINATÁRIO".center(70))
    print("─" * 70)
    
    # Mostrar cada detalhe com emoji e formatação
    print()
    print(f"  👤 Nome:              {nome}")
    print(f"  📱 Contacto:          {contacto}")
    print(f"  🏠 Morada:            {morada}")
    print(f"  📮 Código Postal:     {codigo_postal}")
    print()
    print("─" * 70)
    print()
    
    return

# Validar o endereço de um pedido específico
def addressValidation(order_details):
    df_address = order_details[['address', 'ZP1', 'ZP2']]
    orderValid = True
    reason = "Válida"
    for _, row in df_address.iterrows():
        if row['address'] == "" or pd.isna(row['address']) or len(row['address']) < 5:
            orderValid = False
            reason = "Morada inválida."
            return orderValid, reason
        if row['ZP1'] == "" or pd.isna(row['ZP1']) or not row['ZP1'].isdigit() or len(row['ZP1']) != 4 or row['ZP1'] not in codes_list:
            reason = "Código Postal de distribuição inválido."
            orderValid = False
            return orderValid, reason
        if row['ZP2'] == "" or pd.isna(row['ZP2']) or not row['ZP2'].isdigit() or len(row['ZP2']) != 3:
            reason = "Código Postal (parte 2) inválido."
            orderValid = False
            return orderValid, reason

    return orderValid, reason

# Validar os dados do destinatário de um pedido específico
def recipientValidation(order_details):
    df_recipient = order_details[['name', 'contact']]
    recipientValid = True
    reason = "Válido"
    for _, row in df_recipient.iterrows():
        if row['name'] == "" or pd.isna(row['name']) or len(row['name']) < 3:
            recipientValid = False
            reason = "Nome do destinatário inválido."
            return recipientValid, reason
        if row['contact'] == "" or pd.isna(row['contact']) or len(row['contact']) < 9 or not row['contact'].isdigit() or row['contact'][0] not in ("9","2"):
            reason = "Contacto do destinatário inválido."
            recipientValid = False
            return recipientValid, reason
        
    return recipientValid, reason

# Validar o stock dos produtos de um pedido específico
def stockValidation(order_items_df, products_df):
    merged_items = order_items_df.merge(
        products_df[["product_id", "available"]],
        on='product_id',
        how='left'
    )
    # Listas para armazenar produtos em falta e com stock insuficiente
    missing_products = []
    
    for _, item in merged_items.iterrows():
        if item['available'] == "N":
            missing_products.append(item['product_id'])
                
    return missing_products

# return Stock, funçao que recebe um df de order_it e adiciona os items cancelados a products_df
def return_stock (order_items_df_canceled, products_df):
   
    for _, item in order_items_df_canceled.iterrows():
        pid = item["product_id"]
        ordered = int(item["quantity_ordered"])
        
        products_df.loc[products_df["product_id"] == pid, "quantity_stock"] += ordered
        
    return products_df

#Função de rejeitar encomenda
def reject_order(order_id, orders_df, order_it, products_df, order_events_df, manager, save_orders, save_order_items, save_products, save_order_events):
    # Perguntar motivo
    cancellation_reason = input("Insira o motivo da rejeição da encomenda: ")

    # Atualizar encomenda
    orders_df.loc[orders_df['order_id'] == order_id, 'order_reason'] = cancellation_reason
    orders_df.loc[orders_df['order_id'] == order_id, 'order_status'] = 'canceled'
    save_orders(orders_df)

    # Atualizar artigos
    order_it.loc[order_it['order_id'] == order_id, 'status'] = 'canceled'
    order_it.loc[order_it['order_id'] == order_id, 'quantity_returned'] = order_it["quantity_ordered"]
    save_order_items(order_it)

    # Devolver stock
    order_canceled = order_it.loc[order_it['order_id'] == order_id, ["product_id", "quantity_ordered"]]
    products_df = return_stock(order_canceled, products_df)  # função que já tens em utils
    save_products(products_df)

    print("Encomenda rejeitada com sucesso.")

    # Registar evento
    new_event = {
        'event_id': 'EV' + dtime.datetime.now().strftime("%Y%m%d%H%M%S"),
        'order_id': order_id,
        'event_type': 'reject_order',
        'timestamp': dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'login': manager,
        'details': "Encomenda rejeitada pelo gestor."
    }
    order_events_df = pd.concat([order_events_df, pd.DataFrame([new_event])], ignore_index=True)
    save_order_events(order_events_df)

    return orders_df, order_it, products_df, order_events_df

# Zona do código postal e estafeta random
def code_zone(ZP1, df_zones, df_user_workers):
    """
    Atribuir estafeta baseado no código postal (ZP1)
    """
    # Converter ZP1 para string e remover espaços
    ZP1_str = str(ZP1).strip()
    
    # Converter Codes para string também (garantir)
    if df_zones['Codes'].dtype != 'object':
        df_zones['Codes'] = df_zones['Codes'].astype(str)
    
    # Procurar o código postal
    if ZP1_str in df_zones['Codes'].values:
        zone = df_zones.loc[df_zones['Codes'] == ZP1_str, 'Zone'].iloc[0]
        estafetas = df_user_workers[df_user_workers['dutyArea'] == zone]['id_worker'].tolist()
        
        if estafetas:
            estafeta = rd.choice(estafetas)
        else:
            estafeta = '1001'
    else:
        estafeta = '1001'
        zone = "Fora do limite"
    
    return estafeta, zone
