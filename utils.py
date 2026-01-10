"""
╔═════════════════════════════════════════════════════════════════════════════╗
║                                  UTILS                                      ║
║                                                                             ║
╠═════════════════════════════════════════════════════════════════════════════╣
║ Explicação:                                                                 ║
║                                                                             ║
║ Este ficheiro contém funções utilitárias.                                   ║
║                                                                             ║
║ O seu objetivo principal é centralizar lógica partilha                      ║
║ evitando duplicação de código e facilitando a manutenção e escalabilidade   ║
║ do projeto.                                                                 ║
║                                                                             ║
║ Inclui funções para:                                                        ║
║ - Apresentação detalhada de encomendas e destinatários;                     ║
║ - Validação de dados (destinatário, morada, código postal e stock);         ║
║ - Gestão de stock (retorno de quantidades canceladas);                      ║
║ - Rejeição total de encomendas e registo de eventos;                        ║
║ - Atribuição automática e aleatória de estafetas por zona;                  ║
║ - Mecanismos de bloqueio temporário do sistema por segurança.               ║
║                                                                             ║
║ Como grupo, decidimos disponibilizar este ficheiro desde o início do        ║
║ projeto como um módulo comum, permitindo a criação e reutilização de        ║
║ funções que podem ser chamadas por outros portais ou módulos, garantindo    ║
║ consistência funcional e melhor organização do código.                      ║
╚═════════════════════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import datetime as dtime
import random as rd
import data_manager as dm
import time
import sys


df_zone = pd.read_csv("zp_zones.csv", sep=";", dtype=str)
codes_list = df_zone['Codes'].tolist()
df_user_worker = dm.load_user_work_profil()
products_df = dm.load_products()
order_items = dm.load_order_items()

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
    order_id = row['order_id']
    filtered_items = order_items_df[
        (order_items_df['status'] != 'canceled') & 
        (order_items_df['order_id'] == order_id)
    ]

    # Criar um dicionário para mapear product_id → nome do produto
    product_name_map = dict(zip(products_df['product_id'], products_df['name_product']))

    print("─" * 70)
    print("📦 ITENS DO PEDIDO".center(80))
    print("─" * 70)
    print()
    
    if filtered_items.empty:
        print("  ⚠️  Nenhum item encontrado (todos os itens podem estar cancelados)")
        print()
    else:
        for _, item in filtered_items.iterrows():
            product_name = product_name_map.get(
                item['product_id'], 
                f"Produto ID: {item['product_id']} (Nome não encontrado)"
            )
            print(f"  📦 {product_name}")
            print(f"     └─ Quantidade: {item['quantity_ordered']} | Preço Unit.: {item['price_unit']}€ | Subtotal: {item['subtotal']}€")
        
        total = filtered_items['subtotal'].sum()
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
    """
    
    if isinstance(order_details, pd.Series):
        order_details = pd.DataFrame([order_details])
    
    row = order_details.iloc[0]
    # Extrair os valores necessários
    
    nome = row['name']
    contacto = row['contact']
    morada = row['address']
    zp1 = row['ZP1']
    zp2 = row['ZP2']
    order = row['order_id']
    
    # Formatar código postal com hífen
    codigo_postal = f"{zp1}-{zp2}"

    print("\n")
    print("─" * 70)    
    print(f"📦 PEDIDO: {order}  | 👤 DETALHES DO DESTINATÁRIO".center(70))
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
    # Recebe um Data Frame com os detlahes do pedido
    # Crio novo data frame só com as colunas de interesse
    df_address = order_details[['address', 'ZP1', 'ZP2']]

    # Variaveis pre-definidas
    orderValid = True
    reason = "Válida"
    for _, row in df_address.iterrows():
        # Morada (rua e numero) verifica: vazía ou de dimensão menor que 5
        if row['address'] == "" or pd.isna(row['address']) or len(row['address']) < 5:
            orderValid = False
            reason = "Morada inválida."
            return orderValid, reason
        # Parte 1 do código poastal verifica: vazía, string não numerica, dimensão incorreta, não esta na lista de códigos disponíveis
        if row['ZP1'] == "" or pd.isna(row['ZP1']) or not row['ZP1'].isdigit() or len(row['ZP1']) != 4 or row['ZP1'] not in codes_list:
            reason = "Código Postal de distribuição inválido."
            orderValid = False
            return orderValid, reason
        # Parte 2 código postal verifica: vazía, string não numerica, dimensão incorreta.
        if row['ZP2'] == "" or pd.isna(row['ZP2']) or not row['ZP2'].isdigit() or len(row['ZP2']) != 3:
            reason = "Código Postal (parte 2) inválido."
            orderValid = False
            return orderValid, reason

    return orderValid, reason

# Validar os dados do destinatário de um pedido específico
def recipientValidation(order_details):
    # Recebe um Data Frame com os dados da encoemnda
    # Crio novo data frame só com as colunas de interesse
    df_recipient = order_details[['name', 'contact']]

    # Variaves pre-definidas
    recipientValid = True
    reason = "Válido"

    for _, row in df_recipient.iterrows():
        # Nome, verifico: vazío oyu dimensão incorreta
        if row['name'] == "" or pd.isna(row['name']) or len(row['name']) < 3:
            recipientValid = False
            reason = "Nome do destinatário inválido."
            return recipientValid, reason
        # Número de telemóvel, verifica: vazío, dimensão incorreta, ou que não comece por 9 ou 2.
        if row['contact'] == "" or pd.isna(row['contact']) or len(row['contact']) < 9 or not row['contact'].isdigit() or row['contact'][0] not in ("9","2"):
            reason = "Contacto do destinatário inválido."
            recipientValid = False
            return recipientValid, reason
        
    return recipientValid, reason

# Validar o stock dos produtos de um pedido específico
def stockValidation(order_items_df, products_df):
    # Recbe o Data Frame com os artigos encomendados dum pedido em específico
    # Recebe o Data Frame dos Produtos (products_stock.csv)
    # Crio novo Data Frame com fazendo 'intersecçao' om o product_id e adicionado o coluna 'avaliabe' à esquerda 
    merged_items = order_items_df.merge(
        products_df[["product_id","quantity_stock", "available"]],
        on='product_id',
        how='left'
    )
    # Listas para armazenar produtos não disponíveis na encomenda
    missing_products = []
    
    for _, item in merged_items.iterrows():
        # False equivale a indisponível. Se for False agrega a lista
        if item['available'] == False and item["quantity_stock"] != 0:
            missing_products.append(item['product_id'])
                
    return missing_products

# Retornar quantidades canceladas ao 'armazem' (ao stock)
def return_stock (order_items_df_canceled, products_df):
   # Recebe um Data Frame dos produtos cancelados associados a uma encomenda em específico
   # Recebe o Data Frame dos produtos
   # Itero por linha, onde item é uma Serie
    for _, item in order_items_df_canceled.iterrows():
        # Crio variaves a utilizar
        pid = item["product_id"]
        # Codigo modular, portanto, quero garantizar que o valor que vou gardar é um inteiro pra não dar erro
        ordered = int(item["quantity_ordered"])
        # Iterativamente retorno a quantidade encomendada dos produtos cancelados a quantidade em stock
        products_df.loc[products_df["product_id"] == pid, "quantity_stock"] += ordered
        
    return products_df

#Função de rejeitar encomenda total
def reject_order(order_id, orders_df, order_it, products_df, order_events_df, manager, save_orders, save_order_items, save_products, save_order_events):
    
    valid_reason = False
    while not valid_reason:
        # Motivo de rejeição
        cancellation_reason = input("Insira o motivo da rejeição da encomenda: ")
        # Se o motivo não estiver vazío
        if cancellation_reason:
            valid_reason = True
        # Se o motivo tiver uma dimensão não permitida.
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

    # Devolver ao stock
    order_canceled = order_it.loc[order_it['order_id'] == order_id, ["product_id", "quantity_ordered"]]
    products_df = return_stock(order_canceled, products_df)  # função que já tenho
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
    Atribuir estafeta baseado no código postal (ZP1, parte 1)
    """
    # Recebe o código postal ZP1
    # Recebe o Data Frame com cos ZP1's e as Zonas
    # Recebe o Data Frame com os dados dos estafetas
    # Como Garantimos na base de dados que para cada código postal apenas existe uma zona associada, podemos fazer a selecção na Serie com o iloc[0] 
    zone = df_zones.loc[df_zones['Codes'] == ZP1, 'Zone'].iloc[0]
    # Crio uma lista com os id dos estafetas daquela Zona
    # Aplico outra forma (experimento): Data Frame filtrado - Selcciono coluna (Agora temos una Serie) - Transformo em lista
    estafetas = df_user_workers[df_user_workers['dutyArea'] == zone]['id_worker'].tolist()
    # De maneira 'aleatoria' utilizo a funcção random choice para escolher algum elemento da lista
    estafeta = rd.choice(estafetas)
    
    return estafeta, zone

# Bloqueii de 10s
def bloquear_sistema_10s():
    # Mensagem de Bloqueio
    print("\n" + "═" * 70)
    print("🔒 ACESSO NEGADO - BLOQUEIO DE SEGURANÇA")
    print("═" * 70)
    print("❌ Tentativa de acesso não autorizado detectada!")
    print("⏳ Sistema bloqueado por 10 segundos")
    print("═" * 70 + "\n")

    for i in range(10, 0, -1):  
        # Limpa a linha anterior (efeito dinâmico)
        # \r sobreescreve na mesma linha, para dar o efeito de conteo regressivo
        # end edita la parte final del print en este caso deixa de ser por deifeito \n para "", ou seja evitamo o salto de linha
        # flush = TRUE permite que o texto mude iterativamente
        print(f"\r⏳ Aguardando {i} segundos... ", end="", flush=True)
        # Antes de passar a seguinte iteração espera 1 seg.
        time.sleep(1)
    
    # Depois da ultima iteração 'limpamos' do terminal com espaços
    print("\r" + " "*70, end="")
    print("\n" + "═" * 70)
    print("✅ BLOQUEIO TERMINADO")
    print("🔄 Voltando ao Menu Principal...")
    print("═" * 70 + "\n")
    time.sleep(0.5)

#---------------------------------------------------#
# Função para filtrar encomendas do cliente por status
def order_filters(id_client, orders_df, produtos=products_df):
    
    # Recebe o id de cliente 
    # o Data Frame de todas as encomendas
    #  E os productos (paramentro não obligatorio)
    # Criamos um Data Frame das encomdas feitas pelo cliente   
    orders_client = orders_df[orders_df['id_client'] == id_client]

    # Se o Data Frame estiver vazio, então não há encomendas feitas por este cliente
    if orders_client.empty:
        print("\nNão há encomendas para este cliente.")
        return

    # Inicio de Menu de Filtros por Status
    MenuOrderFilter = True
    while MenuOrderFilter:
        print("\n" + "═" * 70)
        print("Filtrar Minhas Encomendas por status".center(70))
        print("═" * 70)
        print()
        print("Escolha uma das seguintes opções: ")
        print("1. Pendentes")
        print("2. Validadas")
        print("3. Parcialmente Validadas")
        print("4. Canceladas")
        print("5. Em distribuição")
        print("6. Entregue")
        print("7. Recusada")
        print("8. Não Entregue")
        print("9. Voltar")
        print()
        print("─" * 70)
        
        opcao = input("Opção: ")
        if opcao not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            print("Opção inválida. Tente novamente.")
            continue

        if opcao == "9":
            MenuOrderFilter = False
            break
        else:
            # Status diponíveis
            # Com validação de saida, em alguns casos o index 0 representa o valor atribuido nos outros modulos e index 1 o valor da saida(pt).
            status_map = {
                "1": ["pending", "pendente"],
                "2": "validada", 
                "3": ['partially shipped', "parcialmente validada"],
                "4": ["canceled", "cancelada"],
                "5": "em distribuição",
                "6": "entregue",
                "7": "recusada",
                "8": "não entregue"
            }

            # Accedemos ao status associado à opção escolhida
            status = status_map[opcao]
            
            # Verificar se o status é uma lista
            if isinstance(status, list):
                # Filtramos o Data Frame para obter as encomedas do cliente que tenham este status
                encomendas = orders_client[orders_client['order_status'] == status[0]].reset_index(drop=True)

                if encomendas.empty:
                    print(f"\nNão há encomendas '{status[1]}' para este cliente.")
                else:
                    # Otra forma de iterar Data Frame
                    for i in range(len(encomendas)):
                        
                        # Linha como Data Frame
                        encomenda_df = encomendas.iloc[[i]]
                        # Unica linha (Serie) accedo ao valor do order_id
                        order_id = encomendas.iloc[i]['order_id']
                        # Filtro para obter um Data Frame com os artigos da encomenda
                        artigos_df = order_items[order_items['order_id'] == order_id]
                        # Mostrar detalhes da encomenda, com função ja criada
                        showDetailsOrder(encomenda_df, artigos_df, produtos)
                    print("\nVoltando...")
            else:
                encomendas = orders_client[orders_client['order_status'] == status].reset_index(drop=True)
                if encomendas.empty:
                    print(f"\nNão há encomendas '{status}' para este cliente.")
                else:
                    for i in range(len(encomendas)):

                        encomenda_df = encomendas.iloc[[i]]
                        
                        order_id = encomendas.iloc[i]['order_id']
                        artigos_df = order_items[order_items['order_id'] == order_id]
                        showDetailsOrder(encomenda_df, artigos_df, produtos)
                    print("\nVoltando...")