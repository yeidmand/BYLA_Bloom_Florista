import os
import time
import pandas as pd
import datetime as dtime

import data_manager as dm
from mod_product import listarProdutosDisponiveis, reservarStock
from utils import order_filters, showDetailsOrder

FILE_CLIENTS = "login_client.csv"


# ----------------- FUNÇÕES AUXILIARES CSV CLIENTES -----------------

def load_clients():
    """Le login_client.csv devolvendo DataFrame (ou vazio)."""
    if not os.path.exists(FILE_CLIENTS):
        # Se não existir, cria estrutura base
        cols = ["id_client", "name", "contact", "password", "address", "ZP1", "ZP2"]
        return pd.DataFrame(columns=cols)
    return pd.read_csv(FILE_CLIENTS, sep=";", dtype=str)


def save_clients(df_clients):
    """Guarda DataFrame em login_client.csv."""
    df_clients.to_csv(FILE_CLIENTS, sep=";", index=False)


def generate_new_client_id(df_clients: pd.DataFrame) -> str:
    """Gera ID cliente automático (CL001, CL002, ...)."""
    if df_clients.empty:
        return "CL001"
    # supõe formato CLxxx
    df_clients = df_clients.copy()
    df_clients["num"] = df_clients["id_client"].str.extract(r"(\d+)", expand=False).astype(int)
    new_num = df_clients["num"].max() + 1
    return f"CL{new_num:03d}"


# ----------------- REGISTO / CRIAÇÃO DE CLIENTE -----------------

def register_new_client() -> str:
    """
    Cria um novo cliente:
    - Pede dados básicos
    - Gera id_client automático
    - Guarda em login_client.csv
    - Devolve id_client criado
    """
    try:
        print("\n" + "═" * 70)
        print("📝 REGISTO DE NOVO CLIENTE".center(70))
        print("═" * 70)

        df_clients = load_clients()

        # Dados básicos
        name = input("👤 Nome: ").strip()
        while len(name) < 3:
            print("❌ Nome inválido (mínimo 3 caracteres).")
            name = input("👤 Nome: ").strip()

        contact = input("📱 Telemóvel (9 dígitos, começa por 9 ou 2): ").strip()
        while (not contact.isdigit()) or len(contact) != 9 or contact[0] not in ("9", "2"):
            print("❌ Telemóvel inválido.")
            contact = input("📱 Telemóvel (9 dígitos, começa por 9 ou 2): ").strip()

        # Password simples (apenas para este projeto)
        password = input("🔑 Password: ").strip()
        while len(password) < 3:
            print("❌ Password muito curta (mínimo 3 caracteres).")
            password = input("🔑 Password: ").strip()

        address = input("🏠 Morada: ").strip()
        while len(address) < 5:
            print("❌ Morada inválida (mínimo 5 caracteres).")
            address = input("🏠 Morada: ").strip()

        zp1 = input("📮 Código Postal (parte 1 - 4 dígitos): ").strip()
        while not (zp1.isdigit() and len(zp1) == 4):
            print("❌ Código postal (parte 1) inválido.")
            zp1 = input("📮 Código Postal (parte 1 - 4 dígitos): ").strip()

        zp2 = input("📮 Código Postal (parte 2 - 3 dígitos): ").strip()
        while not (zp2.isdigit() and len(zp2) == 3):
            print("❌ Código postal (parte 2) inválido.")
            zp2 = input("📮 Código Postal (parte 2 - 3 dígitos): ").strip()

        # Gerar novo ID
        new_id = generate_new_client_id(df_clients)

        # Criar linha
        new_row = {
            "id_client": new_id,
            "name": name,
            "contact": contact,
            "password": password,
            "address": address,
            "ZP1": zp1,
            "ZP2": zp2
        }

        df_clients = pd.concat([df_clients, pd.DataFrame([new_row])], ignore_index=True)
        save_clients(df_clients)

        print("\n✅ Cliente registado com sucesso!")
        print(f"👉 ID Cliente: {new_id}")
        print("\n🎉 Vai ser redirecionado para o Portal do Cliente...")
        time.sleep(2)

        return new_id
    
    except Exception as e:
        print(f"\n❌ Erro no registo: {e}")
        print("   O registo não foi completado.")
        time.sleep(2)
        return None


# ----------------- CRIAÇÃO E GESTÃO DE ENCOMENDAS -----------------

def generate_new_order_id(orders_df: pd.DataFrame) -> str:
    """Gera ID de encomenda automática (PT01, PT02, ...)."""
    if orders_df.empty:
        return "PT01"
    orders_df = orders_df.copy()
    orders_df["num"] = orders_df["order_id"].str.extract(r"(\d+)", expand=False).astype(int)
    new_num = orders_df["num"].max() + 1
    return f"PT{new_num:02d}"


def create_new_order(id_client: str):
    """
    Criar nova encomenda:
    - Carrega cliente de login_client.csv
    - Cria linha em order_data.csv com status 'pending'
    - Permite escolher produtos E RESERVA STOCK (máx stock disponível)
    - Só mostra produtos available=True E quantity_stock > 0
    - Se stock=0 após reserva → available=False
    - Regista evento inicial em order_events.csv
    """
    try:
        clients_df = load_clients()
        client_row = clients_df[clients_df["id_client"] == id_client]

        if client_row.empty:
            print("❌ Cliente não encontrado.")
            time.sleep(1)
            return

        client_row = client_row.iloc[0]
        name = client_row["name"]
        contact = client_row["contact"]
        address = client_row["address"]
        zp1 = client_row["ZP1"]
        zp2 = client_row["ZP2"]

        # Carregar encomendas existentes
        orders_df = dm.load_orders()
        order_items_df = dm.load_order_items()
        order_events_df = dm.load_order_events()

        # CARREGAR E MOSTRAR SÓ PRODUTOS DISPONÍVEIS (available=True E stock>0)
        products_df = dm.load_products()
        
        # CORREÇÃO: Converter coluna 'available' para boolean e garantir tipos corretos
        if 'available' in products_df.columns:
            products_df['available'] = products_df['available'].astype(str).str.lower().isin(['true', '1', 'yes'])
        
        if 'quantity_stock' in products_df.columns:
            products_df['quantity_stock'] = pd.to_numeric(products_df['quantity_stock'], errors='coerce').fillna(0).astype(int)
        
        # CRÍTICO: Converter product_id para int para comparação
        if 'product_id' in products_df.columns:
            products_df['product_id'] = pd.to_numeric(products_df['product_id'], errors='coerce').fillna(0).astype(int)
        
        produtos_disp = products_df[
            (products_df["available"] == True) & 
            (products_df["quantity_stock"] > 0)
        ].copy()

        # Gerar novo ID de encomenda
        new_order_id = generate_new_order_id(orders_df)

        # Criar linha de encomenda
        new_order = {
            "order_id": new_order_id,
            "id_client": id_client,
            "name": name,
            "contact": contact,
            "address": address,
            "ZP1": zp1,
            "ZP2": zp2,
            "order_status": "pending",
            "order_reason": "",
            "id_worker": "",
            "duty_zone": ""
        }

        orders_df = pd.concat([orders_df, pd.DataFrame([new_order])], ignore_index=True)

        print("\n" + "─" * 70)
        print("🛒 NOVA ENCOMENDA".center(70))
        print("─" * 70)
        print(f"📦 Número do Pedido: {new_order_id}")
        print(f"👤 Cliente: {name}")
        print(f"🏠 Morada: {address} ({zp1}-{zp2})\n")

        # MOSTRAR PRODUTOS DISPONÍVEIS
        if produtos_disp.empty:
            print("⚠️ Não há produtos disponíveis (stock=0 ou available=False).")
            print("\n⚠️ Encomenda não pode ser criada sem produtos.")
            print("   A encomenda não será guardada.")
            time.sleep(2)
            return  # ❌ NÃO guardar encomenda vazia

        print("📋 Produtos disponíveis (available=True, stock>0):")
        for _, prod in produtos_disp.iterrows():
            # CORREÇÃO: Garantir conversão segura de tipos
            prod_id = int(prod['product_id']) if pd.notna(prod['product_id']) else 0
            prod_name = str(prod['name_product']) if pd.notna(prod['name_product']) else "N/A"
            prod_price = float(prod['price_unit']) if pd.notna(prod['price_unit']) else 0.0
            prod_stock = int(prod['quantity_stock']) if pd.notna(prod['quantity_stock']) else 0
            
            print(f"  ID:{prod_id:2} | {prod_name:<15} | Preço: {prod_price:6.2f}€ | Stock: {prod_stock:3}")

        # Variável para controlar se adicionou pelo menos 1 produto
        items_added = False

        # Escolher produtos (loop até sair)
        while True:
            pid_input = input("\nID Produto (ENTER para terminar): ").strip()
            
            # ✅ CORREÇÃO BUG #4: Verificar se input está vazio ANTES de validar
            if pid_input == "":
                break

            if not pid_input.isdigit():
                print("❌ ID inválido.")
                continue

            pid = int(pid_input)
            
            prod_row = produtos_disp[produtos_disp["product_id"] == pid]
            
            if prod_row.empty:
                print(f"❌ Produto não disponível (stock=0 ou available=False).")
                continue

            prod_row = prod_row.iloc[0]
            stock_disp = int(prod_row["quantity_stock"])
            
            qty_input = input(f"Quantidade (máx {stock_disp}): ").strip()
            if not qty_input.isdigit() or int(qty_input) <= 0:
                print("❌ Quantidade inválida.")
                continue

            qty = int(qty_input)
            if qty > stock_disp:
                print(f"❌ Stock insuficiente! Máximo: {stock_disp}")
                continue

            price = float(prod_row["price_unit"])
            subtotal = price * qty

            # **RESERVAR STOCK** usando mod_product.reservarStock (já importado no topo)
            if reservarStock(pid, qty):
                # SÓ se reserva OK → adicionar item
                new_item = {
                    "order_id": new_order_id,
                    "product_id": pid,
                    "quantity_ordered": qty,
                    "price_unit": price,
                    "subtotal": subtotal,
                    "status": "ordered",
                    "quantity_returned": 0
                }
                order_items_df = pd.concat([order_items_df, pd.DataFrame([new_item])], ignore_index=True)
                print(f"✅ Reservado: {qty} x {prod_row['name_product']} ({subtotal:.2f}€)")
                items_added = True  # ✅ Marcamos que adicionou pelo menos 1 produto
                
                # Atualizar lista de produtos disponíveis para refletir novo stock
                products_df = dm.load_products()
                if 'available' in products_df.columns:
                    products_df['available'] = products_df['available'].astype(str).str.lower().isin(['true', '1', 'yes'])
                if 'quantity_stock' in products_df.columns:
                    products_df['quantity_stock'] = pd.to_numeric(products_df['quantity_stock'], errors='coerce').fillna(0).astype(int)
                # CRÍTICO: Converter product_id para int
                if 'product_id' in products_df.columns:
                    products_df['product_id'] = pd.to_numeric(products_df['product_id'], errors='coerce').fillna(0).astype(int)
                produtos_disp = products_df[
                    (products_df["available"] == True) & 
                    (products_df["quantity_stock"] > 0)
                ].copy()
            else:
                print("❌ Erro ao reservar stock.")
                continue

        # ✅ VALIDAÇÃO: Só guardar encomenda se tiver pelo menos 1 produto
        if not items_added:
            print("\n⚠️ Nenhum produto adicionado!")
            print("   A encomenda não será criada.")
            time.sleep(2)
            return

        # Guardar encomenda e itens
        dm.save_orders(orders_df)
        dm.save_order_items(order_items_df)

        # Registar evento inicial
        event_id = "EV" + dtime.datetime.now().strftime("%Y%m%d%H%M%S")
        timestamp = dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_event = {
            "event_id": event_id,
            "order_id": new_order_id,
            "event_type": "created",
            "timestamp": timestamp,
            "login": id_client,
            "details": "Pedido criado pelo cliente."
        }
        order_events_df = pd.concat([order_events_df, pd.DataFrame([new_event])], ignore_index=True)
        dm.save_order_events(order_events_df)

        print("\n✅ Encomenda criada com sucesso!")
        print(f"🔢 Número do Pedido: {new_order_id}")
        time.sleep(1.5)
        
    except Exception as e:
        print(f"\n❌ Erro ao criar encomenda: {e}")
        time.sleep(2)


def list_my_orders(id_client: str):
    """Usa util.order_filters para listar encomendas do cliente por estado."""
    try:
        orders_df = dm.load_orders()
        order_filters(id_client, orders_df)  # função do utils.py
    except Exception as e:
        print(f"\n❌ Erro ao listar encomendas: {e}")
        time.sleep(2)


def show_order_details_client(id_client: str):
    """Mostrar detalhes de um pedido específico do cliente."""
    try:
        orders_df = dm.load_orders()
        order_items_df = dm.load_order_items()
        products_df = dm.load_products()

        my_orders = orders_df[orders_df["id_client"] == id_client]
        if my_orders.empty:
            print("\n⚠️ Ainda não tem encomendas.")
            time.sleep(1)
            return

        print("\nSeus pedidos:")
        for _, row in my_orders.iterrows():
            print(f"- {row['order_id']} | Estado: {row['order_status']}")

        oid_input = input("\nDigite o ID do pedido para ver detalhes (ex: PT12 ou apenas 12): ").strip()
        
        # ✅ CORREÇÃO BUG #7: Converter input para uppercase DEPOIS de converter
        # Se for número, converter para PTxx
        if oid_input.isdigit():
            num = int(oid_input)
            oid = f"PT{num:02d}"
            print(f"   ℹ️  Convertido '{oid_input}' → '{oid}'")
        else:
            # Garantir uppercase
            oid = oid_input.upper()
            # Se não começar com PT, adicionar
            if not oid.startswith("PT") and oid.replace("PT", "").isdigit():
                oid = "PT" + oid
        
        # Verificar se existe
        order_sel = my_orders[my_orders["order_id"] == oid]
        if order_sel.empty:
            print(f"\n❌ Pedido '{oid}' não foi encontrado!")
            print(f"   📋 Seus pedidos disponíveis:")
            for _, row in my_orders.iterrows():
                print(f"      • {row['order_id']}")
            time.sleep(2)
            return

        items_sel = order_items_df[order_items_df["order_id"] == oid]
        showDetailsOrder(order_sel, items_sel, products_df)
        
    except Exception as e:
        print(f"\n❌ Erro ao mostrar detalhes: {e}")
        time.sleep(2)


# ----------------- AVALIAÇÕES / FEEDBACK -----------------

def rate_delivered_order(id_client: str):
    """
    Avaliar serviço:
    - Permite avaliar encomendas com estado 'entregue' ou 'aceite'
    - Grava em avaliacoes.csv (rating 1–5, comentário opcional)
    """
    try:
        orders_df = dm.load_orders()
        # ✅ CORREÇÃO: Aceitar múltiplos estados como "entregue"
        delivered = orders_df[
            (orders_df["id_client"] == id_client) &
            (orders_df["order_status"].isin(["entregue", "aceite", "concluída", "completed"]))
        ]

        if delivered.empty:
            print("\n⚠️ Não tem encomendas concluídas para avaliar.")
            print("   Estados aceites: entregue, aceite, concluída")
            time.sleep(2)
            return

        print("\nEncomendas concluídas/entregues:")
        for _, row in delivered.iterrows():
            print(f"- {row['order_id']} | Estado: {row['order_status']} | Morada: {row['address']}")

        oid = input("\nID do pedido a avaliar (ex: PT01): ").strip().upper()
        
        # ✅ Aceitar número e converter
        if oid.isdigit():
            oid = f"PT{int(oid):02d}"
            print(f"   (Convertido para: {oid})")
        
        if oid not in delivered["order_id"].tolist():
            print(f"❌ Pedido '{oid}' não encontrado ou não está concluído.")
            time.sleep(1)
            return

        nota = input("⭐ Rating (1-5): ").strip()
        while nota not in ["1", "2", "3", "4", "5"]:
            print("❌ Rating inválido.")
            nota = input("⭐ Rating (1-5): ").strip()

        comentario = input("📝 Comentário (opcional, ENTER para saltar): ").strip()

        # Guardar em avaliacoes.csv
        file_rate = "avaliacoes.csv"
        if os.path.exists(file_rate):
            df_rate = pd.read_csv(file_rate, sep=";", dtype=str)
        else:
            df_rate = pd.DataFrame(columns=[
                "order_id", "id_client", "rating", "comment", "timestamp"
            ])

        new_row = {
            "order_id": oid,
            "id_client": id_client,
            "rating": nota,
            "comment": comentario,
            "timestamp": dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        df_rate = pd.concat([df_rate, pd.DataFrame([new_row])], ignore_index=True)
        df_rate.to_csv(file_rate, sep=";", index=False)

        print("\n✅ Obrigado pela sua avaliação!")
        time.sleep(1.5)
        
    except Exception as e:
        print(f"\n❌ Erro ao registar avaliação: {e}")
        time.sleep(2)


# ----------------- PORTAL CLIENTE  -----------------

def welcome_client(id_client: str):
    """
    Função chamada pelo main.py.
    - Se id_client == "" → criar novo cliente e depois abrir portal
    - Se id_client != "" → assume que já foi verificado em main.py
    """
    try:
        if id_client == "":
            id_client = register_new_client()
            
            if not id_client:  # Se registo falhou
                return

        # Carregar nome para saudação
        df_clients = load_clients()
        row = df_clients[df_clients["id_client"] == id_client]
        
        if row.empty:
            print("❌ Erro: Cliente não encontrado no sistema.")
            time.sleep(1.5)
            return
        
        name = row.iloc[0]["name"]

        open_portal = True
        while open_portal:
            os.system("cls" if os.name == "nt" else "clear")
            print("═" * 70)
            print("🌸 PORTAL CLIENTE – BYLA BLOOM 🌸".center(70))
            print("═" * 70)
            print(f"👤 {name} (ID: {id_client})")
            print("─" * 70)
            print("1. Fazer nova encomenda")
            print("2. Ver minhas encomendas (filtros)")
            print("3. Ver detalhes de um pedido")
            print("4. Avaliar encomenda entregue")
            print("0. Sair")
            print("─" * 70)

            op = input("Opção: ").strip()

            if op == "1":
                create_new_order(id_client)
                input("\nENTER para continuar...")
            elif op == "2":
                list_my_orders(id_client)
                input("\nENTER para continuar...")
            elif op == "3":
                show_order_details_client(id_client)
                input("\nENTER para continuar...")
            elif op == "4":
                rate_delivered_order(id_client)
                input("\nENTER para continuar...")
            elif op == "0":
                print("\n👋 Até breve!")
                time.sleep(1)
                open_portal = False
            else:
                print("❌ Opção inválida.")
                time.sleep(1)
                
    except Exception as e:
        print(f"\n❌ Erro no portal do cliente: {e}")
        time.sleep(2)


if __name__ == "__main__":
    welcome_client("")