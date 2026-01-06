import pandas as pd
import datetime as dtime
import random as rd
import data_manager as dm
import time
import sys


df_zone = pd.read_csv("zp_zones.csv", sep=";", dtype=str)
codes_list = df_zone['Codes'].tolist()
df_user_worker = dm.load_user_work_profil()

# Mostrar os detalhes de um pedido específico, incluindo informações do pedido e itens associados.
def showDetailsOrder(order_details, order_items_df, products_df):
    """
    Mostrar os detalhes de um pedido específico, incluindo informações do pedido e itens associados.
    Mostra apenas os itens cujo status é diferente de 'canceled'.
    """
    # Detalhes do pedido
    row = order_details.iloc[0]
    
    numero_pedido = row['order_id']
    nome_cliente = row['name']
    contacto = row['contact']
    morada = row['address']
    codigo_postal = f"{row['ZP1']}-{row['ZP2']}"
    estado_pedido = row['order_status']
    
    print("\n")
    print("─" * 70)
    print("📋 DETALHES DO PEDIDO".center(70))
    print("─" * 70)
    print()
    print(f"  🔢 Número do Pedido:    {numero_pedido}")
    print(f"  👤 Cliente:             {nome_cliente}")
    print(f"  📱 Contacto:            {contacto}")
    print(f"  🏠 Morada:              {morada}")
    print(f"  📮 Código Postal:       {codigo_postal}")
    print(f"  📊 Estado do Pedido:    {estado_pedido}")
    print()

    # Filtrar itens não cancelados
    order_items_df = order_items_df[order_items_df['status'] != 'canceled']

    # Merge com produtos para ter o nome
    merged_items = order_items_df.merge(
        products_df[["product_id", "name_product"]],
        on='product_id',
        how='left'
    )

    print("─" * 70)
    print("📦 ITENS DO PEDIDO".center(80))
    print("─" * 70)
    print()
    
    if merged_items.empty:
        print("  ⚠️  Nenhum item encontrado (todos os itens podem estar cancelados)")
        print()
    else:
        for _, item in merged_items.iterrows():
            product_name = item['name_product'] if pd.notna(item['name_product']) else f"Produto ID: {item['product_id']} (Nome não encontrado)"
            print(f"  📦 {product_name}")
            print(f"     └─ Quantidade: {item['quantity_ordered']} | Preço Unit.: {item['price_unit']}€ | Subtotal: {item['subtotal']}€")
        
        total = merged_items['subtotal'].sum()
        print()
        print("─" * 70)
        print(f"  💰 TOTAL DO PEDIDO: {total}€".ljust(69))
        print("─" * 70)
        print()
    
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
    
    row = order_details.iloc[0]
    # Extrair os valores necessários
    
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
    valid_reason = False
    while not valid_reason:
        cancellation_reason = input("Insira o motivo da rejeição da encomenda: ")
        if cancellation_reason:
            valid_reason = True
        elif len(cancellation_reason) < 5:
            print("❌ O motivo naõ é válido. Ingresse um motivo mais detalhado.")
        else:
            print("❌ O motivo da rejeição não pode estar vazio.")



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
    zone = df_zones.loc[df_zones['Codes'] == ZP1, 'Zone'].iloc[0]
    estafetas = df_user_workers[df_user_workers['dutyArea'] == zone]['id_worker'].tolist()
    estafeta = rd.choice(estafetas)
    
    return estafeta, zone

# Bloqueii de 10s
def bloquear_sistema_10s():
    print("\n" + "═" * 70)
    print("🔒 ACESSO NEGADO - BLOQUEIO DE SEGURANÇA")
    print("═" * 70)
    print("❌ Tentativa de acesso não autorizado detectada!")
    print("⏳ Sistema bloqueado por 10 segundos")
    print("═" * 70 + "\n")

    for i in range(10, 0, -1):  # Countdown de 10 até 1 (mais natural)
        # Limpa a linha anterior (efeito dinâmico)
        print(f"\r⏳ Aguardando {i} segundos... ", end="", flush=True)
        time.sleep(1)
    
    print("\r" + " "*70, end="", flush=True)  # Limpa linha anterior
    print("\n" + "═" * 70)
    print("✅ BLOQUEIO TERMINADO")
    print("🔄 Voltando ao Menu Principal...")
    print("═" * 70 + "\n")
    time.sleep(0.5)