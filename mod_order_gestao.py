"""
╔═════════════════════════════════════════════════════════════════════════════╗
║                    MOD_ORDER_GESTAO                                          ║
║                                                                               ║
║  Melhorias aplicadas:                                                        ║
║  ✓ Estética melhorada (outputs mais agradáveis)                              ║
║  ✓ Cores e formatação (emojis e separadores)                                  ║
║  ✓ Inputs mais personalizados                                                ║
║  ✓ Função centralizada para registar eventos                                 ║
║  ✓ Lógica original mantida intacta                                          ║
║  ✓ Sem try-except (validações simples)                                       ║
║                                                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import datetime as dtime
from data_manager import (
    load_orders, save_orders,
    load_products, save_products,
    load_order_events, save_order_events,
    load_order_items, save_order_items,
    load_user_work_profil
)
import utils as ut
import random as rd


# ════════════════════════════════════════════════════════════════════════════════
# 🎯 SEÇÃO 1: FUNÇÃO CENTRALIZADA PARA REGISTAR EVENTOS
# ════════════════════════════════════════════════════════════════════════════════
# Esta função centraliza o registo de eventos para evitar duplicações de código
# Recebe: order_id, tipo_evento, detalhes, e o gerente que fez a ação
# Devolve: novo evento formatado pronto para guardar

def registar_evento(order_id, tipo_evento, detalhes, manager):
    """
    Registra um evento de forma centralizada.
    
    Parâmetros:
    - order_id: ID da encomenda (ex: "PT01")
    - tipo_evento: tipo de ação (ex: "edit_name", "validate", "reject")
    - detalhes: descrição do que aconteceu
    - manager: ID do gerente que fez a ação
    
    Devolve:
    - Dicionário com evento completo pronto para DataFrame
    """
    
    novo_evento = {
        'event_id': 'EV' + dtime.datetime.now().strftime("%Y%m%d%H%M%S"),
        'order_id': order_id,
        'event_type': tipo_evento,
        'staptime_1': dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'staptime_2': '',
        'login': manager,
        'details': detalhes,
        'latitude': '',
        'longitude': ''
    }
    
    return novo_evento


# ════════════════════════════════════════════════════════════════════════════════
# 🎯 SEÇÃO 2: MENUS COM FORMATAÇÃO MELHORADA
# ════════════════════════════════════════════════════════════════════════════════

def mostrar_linha_decorativa(caractere="═", comprimento=70):
    """
    Mostra uma linha decorativa.
    - caractere: qual símbolo usar ("═", "─", "=", etc)
    - comprimento: quantos caracteres mostrar
    """
    print(caractere * comprimento)


def menu_principal_pedidos():
    """
    Menu principal de gestão de pedidos com formatação melhorada.
    Mostra 6 opções principais para o gerente escolher.
    """
    
    print("\n")
    mostrar_linha_decorativa("═", 70)
    print("📋 GESTÃO DE PEDIDOS - BYLA BLOOM FLORISTA".center(70))
    mostrar_linha_decorativa("═", 70)
    
    opcoes = [
        ("1", "👀 Ver Pedidos Pendentes", "Mostra encomendas que chegaram"),
        ("2", "✅ Ver Pedidos Validados", "Mostra encomendas prontas para entrega"),
        ("3", "❌ Ver Pedidos Cancelados", "Mostra encomendas rejeitadas"),
        ("4", "🚚 Atribuir Estafeta", "Designa entregador para encomenda"),
        ("5", "🗺️  Filtrar por Zona", "Mostra encomendas por região de cobertura"),
        ("6", "🚪 Voltar ao Menu Principal", "Sai deste módulo")
    ]
    
    for num, titulo, descricao in opcoes:
        print(f"\n  {num}. {titulo}")
        print(f"     └─ {descricao}")
    
    print("\n")
    mostrar_linha_decorativa("─", 70)
    
    # Pedir input com validação simples
    while True:
        escolha = input("👉 Seleccione uma opção (1-6): ").strip()
        if escolha in ['1', '2', '3', '4', '5', '6']:
            return escolha
        print("❌ Opção inválida. Digite um número entre 1 e 6.")


def menu_editar_pedido(order_id):
    """
    Menu de edição de um pedido específico.
    Permite editar dados ou validar/rejeitar a encomenda.
    """
    
    print("\n")
    mostrar_linha_decorativa("═", 70)
    print(f"✏️  EDITAR PEDIDO: {order_id}".center(70))
    mostrar_linha_decorativa("═", 70)
    
    print("\n📝 EDITAR DADOS DO DESTINATÁRIO:")
    print("  1. 👤 Nome e apelido")
    print("  2. 📱 Contacto (teléfone)")
    print("  3. 🏠 Morada (rua e número)")
    print("  4. 📮 Código postal")
    print("  5. ↩️  Voltar ao menu anterior")
    
    print("\n✔️  VALIDAÇÃO DA ENCOMENDA:")
    print("  6. 🗑️  Rejeitar encomenda")
    print("  7. ⚡ Validar automaticamente")
    print("  8. ↩️  Voltar ao menu anterior")
    
    print("\n")
    mostrar_linha_decorativa("─", 70)
    
    while True:
        escolha = input("👉 Seleccione uma opção (1-8): ").strip()
        if escolha in ['1', '2', '3', '4', '5', '6', '7', '8']:
            return escolha
        print("❌ Opção inválida. Digite um número entre 1 e 8.")


def menu_filtrar_zona():
    """
    Menu para filtrar encomendas por zona geográfica.
    Mostra as 5 zonas de cobertura + opção de sair.
    """
    
    print("\n")
    mostrar_linha_decorativa("═", 70)
    print("🗺️  FILTRAR ENCOMENDAS POR ZONA".center(70))
    mostrar_linha_decorativa("═", 70)
    
    print("\nEscolha uma zona para ver encomendas:")
    print("  1. 🏙️  Centro")
    print("  2. ⬆️  Norte")
    print("  3. ⬇️  Sul")
    print("  4. ➡️  Este")
    print("  5. ⬅️  Oeste")
    print("  6. 🚫 Fora do limite")
    print("  7. ↩️  Voltar ao menu anterior")
    
    print("\n")
    mostrar_linha_decorativa("─", 70)
    
    while True:
        escolha = input("👉 Seleccione uma opção (1-7): ").strip()
        if escolha in ['1', '2', '3', '4', '5', '6', '7']:
            return escolha
        print("❌ Opção inválida. Digite um número entre 1 e 7.")


# ════════════════════════════════════════════════════════════════════════════════
# 🎯 SEÇÃO 3: FUNÇÕES DE EDIÇÃO DE DADOS COM INPUTS PERSONALIZADOS
# ════════════════════════════════════════════════════════════════════════════════

def editar_nome(orders_df, order_id, manager, order_events_df):
    """
    Edita o nome do destinatário.
    - Pede novo nome
    - Atualiza na base de dados
    - Registra evento
    """
    
    print("\n" + "─" * 70)
    nome_atual = orders_df[orders_df['order_id'] == order_id]['name'].iloc[0]
    print(f"Nome actual: {nome_atual}")
    print("─" * 70)
    
    nome_novo = input("👤 Insira o novo nome completo: ").strip()
    
    if not nome_novo:
        print("❌ Nome não pode estar vazio!")
        return orders_df, order_events_df
    
    # Atualizar na base de dados
    orders_df.loc[orders_df['order_id'] == order_id, 'name'] = nome_novo
    save_orders(orders_df)
    
    # Registar evento usando a função centralizada
    evento = registar_evento(
        order_id,
        "edit_name",
        f"Nome alterado de '{nome_atual}' para '{nome_novo}'",
        manager
    )
    order_events_df = pd.concat([order_events_df, pd.DataFrame([evento])], ignore_index=True)
    save_order_events(order_events_df)
    
    print("✅ Nome actualizado com sucesso!")
    ut.showDetailsDestinatario(orders_df[orders_df['order_id'] == order_id])
    
    return orders_df, order_events_df


def editar_contacto(orders_df, order_id, manager, order_events_df):
    """
    Edita o contacto (teléfone) do destinatário.
    - Pede novo teléfone
    - Atualiza na base de dados
    - Registra evento
    """
    
    print("\n" + "─" * 70)
    contacto_atual = orders_df[orders_df['order_id'] == order_id]['contact'].iloc[0]
    print(f"Contacto actual: {contacto_atual}")
    print("─" * 70)
    
    contacto_novo = input("📱 Insira o novo contacto (ex: 961234567): ").strip()
    
    if not contacto_novo:
        print("❌ Contacto não pode estar vazio!")
        return orders_df, order_events_df
    
    # Atualizar na base de dados
    orders_df.loc[orders_df['order_id'] == order_id, 'contact'] = contacto_novo
    save_orders(orders_df)
    
    # Registar evento
    evento = registar_evento(
        order_id,
        "edit_contact",
        f"Contacto alterado de '{contacto_atual}' para '{contacto_novo}'",
        manager
    )
    order_events_df = pd.concat([order_events_df, pd.DataFrame([evento])], ignore_index=True)
    save_order_events(order_events_df)
    
    print("✅ Contacto actualizado com sucesso!")
    ut.showDetailsDestinatario(orders_df[orders_df['order_id'] == order_id])
    
    return orders_df, order_events_df


def editar_morada(orders_df, order_id, manager, order_events_df):
    """
    Edita a morada do destinatário.
    - Pede nova morada
    - Atualiza na base de dados
    - Registra evento
    """
    
    print("\n" + "─" * 70)
    morada_atual = orders_df[orders_df['order_id'] == order_id]['address'].iloc[0]
    print(f"Morada actual: {morada_atual}")
    print("─" * 70)
    
    morada_nova = input("🏠 Insira a nova morada (ex: Rua Principal, nº 42): ").strip()
    
    if not morada_nova:
        print("❌ Morada não pode estar vazia!")
        return orders_df, order_events_df
    
    # Atualizar na base de dados
    orders_df.loc[orders_df['order_id'] == order_id, 'address'] = morada_nova
    save_orders(orders_df)
    
    # Registar evento
    evento = registar_evento(
        order_id,
        "edit_address",
        f"Morada alterada de '{morada_atual}' para '{morada_nova}'",
        manager
    )
    order_events_df = pd.concat([order_events_df, pd.DataFrame([evento])], ignore_index=True)
    save_order_events(order_events_df)
    
    print("✅ Morada actualizada com sucesso!")
    ut.showDetailsDestinatario(orders_df[orders_df['order_id'] == order_id])
    
    return orders_df, order_events_df


def editar_codigo_postal(orders_df, order_id, manager, order_events_df):
    """
    Edita o código postal do destinatário.
    - Pede novo código postal (parte 1 e 2)
    - Atualiza na base de dados
    - Registra evento
    """
    
    print("\n" + "─" * 70)
    zp1_atual = orders_df[orders_df['order_id'] == order_id]['ZP1'].iloc[0]
    zp2_atual = orders_df[orders_df['order_id'] == order_id]['ZP2'].iloc[0]
    print(f"Código postal actual: {zp1_atual}-{zp2_atual}")
    print("─" * 70)
    
    zp1_novo = input("📮 Código postal (parte 1, ex: 4750): ").strip()
    zp2_novo = input("📮 Código postal (parte 2, ex: 123): ").strip()
    
    if not zp1_novo or not zp2_novo:
        print("❌ Código postal não pode estar vazio!")
        return orders_df, order_events_df
    
    # Atualizar na base de dados
    orders_df.loc[orders_df['order_id'] == order_id, 'ZP1'] = zp1_novo
    orders_df.loc[orders_df['order_id'] == order_id, 'ZP2'] = zp2_novo
    save_orders(orders_df)
    
    # Registar evento
    evento = registar_evento(
        order_id,
        "edit_postal_code",
        f"Código postal alterado de '{zp1_atual}-{zp2_atual}' para '{zp1_novo}-{zp2_novo}'",
        manager
    )
    order_events_df = pd.concat([order_events_df, pd.DataFrame([evento])], ignore_index=True)
    save_order_events(order_events_df)
    
    print("✅ Código postal actualizado com sucesso!")
    ut.showDetailsDestinatario(orders_df[orders_df['order_id'] == order_id])
    
    return orders_df, order_events_df


# ════════════════════════════════════════════════════════════════════════════════
# 🎯 SEÇÃO 4: FUNÇÃO PRINCIPAL DO MÓDULO
# ════════════════════════════════════════════════════════════════════════════════

def ModOrderGestao(Manager):
    """
    Função principal do módulo de gestão de pedidos.
    - Manager: ID do gerente autenticado (ex: "SUPm")
    
    Este módulo permite:
    1. Ver pedidos pendentes, validados, cancelados
    2. Editar dados de pedidos
    3. Validar automaticamente pedidos
    4. Atribuir estafetas
    5. Filtrar por zona
    """
    
    # Verificar se é supervisor (pode rejeitar pedidos)
    isSupervisor = (Manager == "SUPm")
    
    # Carregar dados (CSV convertidos em DataFrames)
    df_zone = pd.read_csv("zp_zones.csv", sep=";", dtype=str)
    df_user_worker = load_user_work_profil()
    orders_df = load_orders()
    order_it = load_order_items()
    products_df = load_products()
    order_events_df = load_order_events()
    
    # Dicionário para conversão rápida: product_id → nome_produto
    products_name = dict(zip(products_df['product_id'], products_df['name_product']))
    
    # Loop principal do módulo
    menu_ativo = True
    
    while menu_ativo:
        
        # Mostrar menu e pedir escolha
        opcao = menu_principal_pedidos()
        
        # ═══════════════════════════════════════════════════════════════
        # OPÇÃO 1: VER PEDIDOS PENDENTES
        # ═══════════════════════════════════════════════════════════════
        
        if opcao == '1':
            
            dentro_menu = True
            
            while dentro_menu:
                
                # Filtrar apenas pedidos com status "pending"
                pedidos_pendentes = orders_df[orders_df['order_status'] == 'pending']
                
                if pedidos_pendentes.empty:
                    print("\n")
                    mostrar_linha_decorativa("═")
                    print("❌ NÃO HÁ PEDIDOS PENDENTES".center(70))
                    mostrar_linha_decorativa("═")
                    print("\nTodos os pedidos já foram processados.\n")
                    dentro_menu = False
                    continue
                
                # Mostrar lista de pedidos pendentes
                print("\n")
                mostrar_linha_decorativa("═")
                print("📋 PEDIDOS PENDENTES".center(70))
                mostrar_linha_decorativa("═")
                
                for _, pedido in pedidos_pendentes.iterrows():
                    print(f"\n  ID: {pedido['order_id']} | Cliente: {pedido['name']}")
                    print(f"  Teléfono: {pedido['contact']} | CP: {pedido['ZP1']}-{pedido['ZP2']}")
                
                print("\n")
                mostrar_linha_decorativa("─")
                
                # Pedir qual pedido ver
                user_input = input("👉 Insira ID do pedido (ou 'voltar'): ").strip().upper()
                
                if user_input.lower() == 'voltar':
                    dentro_menu = False
                    continue
                
                # Verificar se o pedido existe
                if user_input in pedidos_pendentes['order_id'].values:
                    
                    # Carregar detalhes do pedido
                    detalhes_pedido = pedidos_pendentes[pedidos_pendentes['order_id'] == user_input]
                    items_pedido = order_it[order_it['order_id'] == user_input]
                    
                    # Mostrar detalhes completos
                    ut.showDetailsOrder(detalhes_pedido, items_pedido, products_df)
                    
                    dentro_menu = False
                    
                    # Entrar no menu de edição
                    editando = True
                    
                    while editando:
                        
                        edicao_opcao = menu_editar_pedido(user_input)
                        
                        # Opção 1: Editar nome
                        if edicao_opcao == '1':
                            orders_df, order_events_df = editar_nome(
                                orders_df, user_input, Manager, order_events_df
                            )
                        
                        # Opção 2: Editar contacto
                        elif edicao_opcao == '2':
                            orders_df, order_events_df = editar_contacto(
                                orders_df, user_input, Manager, order_events_df
                            )
                        
                        # Opção 3: Editar morada
                        elif edicao_opcao == '3':
                            orders_df, order_events_df = editar_morada(
                                orders_df, user_input, Manager, order_events_df
                            )
                        
                        # Opção 4: Editar código postal
                        elif edicao_opcao == '4':
                            orders_df, order_events_df = editar_codigo_postal(
                                orders_df, user_input, Manager, order_events_df
                            )
                        
                        # Opção 5: Voltar
                        elif edicao_opcao == '5':
                            editando = False
                            print("\n↩️  A voltar ao menu de pedidos pendentes...\n")
                        
                        # Opção 6: Rejeitar (só supervisor)
                        elif edicao_opcao == '6':
                            if isSupervisor:
                                orders_df, order_it, products_df, order_events_df = ut.reject_order(
                                    user_input, orders_df, order_it, products_df,
                                    order_events_df, Manager, save_orders, save_order_items,
                                    save_products, save_order_events
                                )
                                editando = False
                            else:
                                print("\n❌ Apenas o Supervisor pode rejeitar encomendas.\n")
                                editando = False
                        
                        # Opção 7: Validar automaticamente (só supervisor)
                        elif edicao_opcao == '7':
                            if isSupervisor:
                                # Validar morada
                                pedido_validar = orders_df[orders_df['order_id'] == user_input]
                                valida_morada, motivo_morada = ut.addressValidation(pedido_validar)
                                
                                if valida_morada:
                                    
                                    print("\n✅ Morada válida\n")
                                    
                                    # Validar dados do destinatário
                                    valida_destinatario, motivo_dest = ut.recipientValidation(pedido_validar)
                                    
                                    if valida_destinatario:
                                        
                                        print("✅ Dados do destinatário válidos\n")
                                        
                                        # Validar stock
                                        produtos_faltantes = ut.stockValidation(items_pedido, products_df)
                                        
                                        if not produtos_faltantes:
                                            
                                            print("✅ Stock disponível\n")
                                            
                                            # Atualizar status
                                            orders_df.loc[orders_df['order_id'] == user_input, 'order_status'] = 'validated'
                                            order_it.loc[order_it['order_id'] == user_input, 'status'] = 'shipped'
                                            save_orders(orders_df)
                                            save_order_items(order_it)
                                            
                                            # Registar evento
                                            evento = registar_evento(
                                                user_input,
                                                "auto_validate",
                                                "Pedido validado automaticamente pelo sistema",
                                                Manager
                                            )
                                            order_events_df = pd.concat(
                                                [order_events_df, pd.DataFrame([evento])],
                                                ignore_index=True
                                            )
                                            save_order_events(order_events_df)
                                            
                                            print("✅ Encomenda validada com sucesso!\n")
                                            editando = False
                                        
                                        else:
                                            print("❌ Alguns produtos não estão disponíveis\n")
                                            editando = False
                                    
                                    else:
                                        print(f"❌ Dados inválidos: {motivo_dest}\n")
                                        editando = False
                                
                                else:
                                    print(f"❌ Morada inválida: {motivo_morada}\n")
                                    editando = False
                            
                            else:
                                print("\n❌ Apenas o Supervisor pode validar encomendas.\n")
                                editando = False
                        
                        # Opção 8: Voltar
                        elif edicao_opcao == '8':
                            editando = False
                            print("\n↩️  A voltar ao menu de pedidos pendentes...\n")
                        
                        # Pedir confirmação para continuar editando
                        if edicao_opcao in ['1', '2', '3', '4']:
                            continuar = input("\n❓ Deseja continuar editando? (s/n): ").strip().lower()
                            if continuar != 's':
                                editando = False
                
                else:
                    print("\n❌ Pedido não encontrado!\n")
        
        # ═══════════════════════════════════════════════════════════════
        # OPÇÃO 2: VER PEDIDOS VALIDADOS
        # ═══════════════════════════════════════════════════════════════
        
        elif opcao == '2':
            
            pedidos_validados = orders_df[
                orders_df['order_status'].isin(['validated', 'partially shipped'])
            ].reset_index(drop=True)
            
            print("\n")
            mostrar_linha_decorativa("═")
            print("✅ PEDIDOS VALIDADOS".center(70))
            mostrar_linha_decorativa("═")
            
            if pedidos_validados.empty:
                print("\n❌ Não há pedidos validados ou parcialmente enviados.\n")
            
            else:
                print(f"\n📊 Total de pedidos: {len(pedidos_validados)}\n")
                
                i = 0
                total = len(pedidos_validados)
                
                while i < total:
                    
                    pedido = pedidos_validados.iloc[i]
                    
                    print("\n" + "─" * 70)
                    print(f"ID: {pedido['order_id']} | Estado: {pedido['order_status']}")
                    print(f"Cliente: {pedido['name']} | Teléfono: {pedido['contact']}")
                    print(f"Morada: {pedido['address']} | CP: {pedido['ZP1']}-{pedido['ZP2']}")
                    print("─" * 70)
                    
                    if i < total - 1:
                        while True:
                            print("\n1️⃣  Próximo pedido")
                            print("2️⃣  Sair")
                            resp = input("👉 Escolha: ").strip()
                            
                            if resp == '1':
                                i += 1
                                break
                            elif resp == '2':
                                i = total
                                break
                            else:
                                print("❌ Opção inválida")
                    
                    else:
                        input("\n⏬ Último pedido. Prima ENTER para sair...\n")
                        i = total
        
        # ═══════════════════════════════════════════════════════════════
        # OPÇÃO 3: VER PEDIDOS CANCELADOS
        # ═══════════════════════════════════════════════════════════════
        
        elif opcao == '3':
            
            pedidos_cancelados = orders_df[
                orders_df['order_status'] == 'canceled'
            ].reset_index(drop=True)
            
            print("\n")
            mostrar_linha_decorativa("═")
            print("❌ PEDIDOS CANCELADOS".center(70))
            mostrar_linha_decorativa("═")
            
            if pedidos_cancelados.empty:
                print("\n✅ Não há pedidos cancelados.\n")
            
            else:
                print(f"\n📊 Total de pedidos cancelados: {len(pedidos_cancelados)}\n")
                
                i = 0
                total = len(pedidos_cancelados)
                
                while i < total:
                    
                    pedido = pedidos_cancelados.iloc[i]
                    
                    print("\n" + "─" * 70)
                    print(f"ID: {pedido['order_id']} | Motivo: {pedido['order_reason']}")
                    print(f"Cliente: {pedido['name']} | Teléfono: {pedido['contact']}")
                    print(f"Morada: {pedido['address']} | CP: {pedido['ZP1']}-{pedido['ZP2']}")
                    print("─" * 70)
                    
                    if i < total - 1:
                        while True:
                            print("\n1️⃣  Próximo pedido")
                            print("2️⃣  Sair")
                            resp = input("👉 Escolha: ").strip()
                            
                            if resp == '1':
                                i += 1
                                break
                            elif resp == '2':
                                i = total
                                break
                            else:
                                print("❌ Opção inválida")
                    
                    else:
                        input("\n⏬ Último pedido. Prima ENTER para sair...\n")
                        i = total
        
        # ═══════════════════════════════════════════════════════════════
        # OPÇÃO 4: ATRIBUIR ESTAFETA
        # ═══════════════════════════════════════════════════════════════
        
        elif opcao == '4':
            
            pedidos_validados = orders_df[
                orders_df['order_status'].isin(['validated', 'partially shipped'])
            ].reset_index(drop=True)
            
            if pedidos_validados.empty:
                print("\n❌ Não há pedidos validados para atribuir estafeta.\n")
                continue
            
            # Filtrar pedidos SEM estafeta
            pedidos_sem_estafeta = pedidos_validados[
                (pedidos_validados['id_worker'].isna()) |
                (pedidos_validados['id_worker'].astype(str).str.strip() == '') |
                (pedidos_validados['id_worker'].astype(str).str.lower() == 'nan')
            ].reset_index(drop=True)
            
            if pedidos_sem_estafeta.empty:
                print("\n✅ Todos os pedidos já têm estafeta atribuído.\n")
                continue
            
            print("\n")
            mostrar_linha_decorativa("═")
            print(f"🚚 ATRIBUIR ESTAFETA - Total: {len(pedidos_sem_estafeta)}".center(70))
            mostrar_linha_decorativa("═")
            
            i = 0
            total = len(pedidos_sem_estafeta)
            
            while i < total:
                
                pedido = pedidos_sem_estafeta.iloc[i]
                
                print("\n" + "─" * 70)
                ut.showDetailsDestinatario(pedido)
                print("─" * 70)
                
                print("\n1️⃣  Atribuir estafeta automaticamente")
                print("2️⃣  Próximo pedido")
                print("3️⃣  Sair")
                
                resp = input("👉 Escolha: ").strip()
                
                if resp == '1':
                    estafeta, zona = ut.code_zone(int(pedido['ZP1']), df_zone, df_user_worker)
                    orders_df.loc[orders_df['order_id'] == pedido['order_id'], 'id_worker'] = estafeta
                    save_orders(orders_df)
                    
                    evento = registar_evento(
                        pedido['order_id'],
                        "assign_courier",
                        f"Estafeta {estafeta} atribuído (Zona: {zona})",
                        Manager
                    )
                    order_events_df = pd.concat([order_events_df, pd.DataFrame([evento])], ignore_index=True)
                    save_order_events(order_events_df)
                    
                    print(f"\n✅ Estafeta {estafeta} ({zona}) atribuído!\n")
                    i += 1
                
                elif resp == '2':
                    i += 1
                
                elif resp == '3':
                    print("\n↩️  A voltar ao menu principal...\n")
                    i = total
                
                else:
                    print("❌ Opção inválida")
        
        # ═══════════════════════════════════════════════════════════════
        # OPÇÃO 5: FILTRAR POR ZONA
        # ═══════════════════════════════════════════════════════════════
        
        elif opcao == '5':
            
            pedidos_validados = orders_df[
                orders_df['order_status'].isin(['validated', 'partially shipped'])
            ].reset_index(drop=True)
            
            if pedidos_validados.empty:
                print("\n❌ Não há pedidos validados.\n")
                continue
            
            # Filtrar apenas pedidos COM estafeta
            pedidos_com_estafeta = pedidos_validados[
                (pedidos_validados['id_worker'].notna()) &
                (pedidos_validados['id_worker'].astype(str).str.strip() != '') &
                (pedidos_validados['id_worker'].astype(str).str.lower() != 'nan')
            ].reset_index(drop=True)
            
            if pedidos_com_estafeta.empty:
                print("\n❌ Não há pedidos com estafeta atribuído.\n")
                continue
            
            # Mostrar menu de filtro
            opcao_zona = menu_filtrar_zona()
            
            if opcao_zona == '7':
                continue
            
            # Mapa de zonas
            mapa_zonas = {
                '1': ('Center', '🏙️  Centro'),
                '2': ('North', '⬆️  Norte'),
                '3': ('South', '⬇️  Sul'),
                '4': ('East', '➡️  Este'),
                '5': ('West', '⬅️  Oeste'),
                '6': ('Fora do limite', '🚫 Fora do limite')
            }
            
            if opcao_zona in mapa_zonas:
                
                zona_key, zona_emoji = mapa_zonas[opcao_zona]
                
                # Filtrar estafetas da zona
                estafetas_zona = df_user_worker[
                    (~df_user_worker['dutyArea'].str.startswith('Gestor')) &
                    (df_user_worker['dutyArea'] == zona_key)
                ]
                
                # Junctar pedidos com estafetas da zona
                pedidos_zona = pd.merge(
                    pedidos_com_estafeta,
                    estafetas_zona,
                    on='id_worker',
                    how='inner'
                )
                
                print("\n")
                mostrar_linha_decorativa("═")
                print(f"📦 PEDIDOS PARA ENTREGA - {zona_emoji}".center(70))
                mostrar_linha_decorativa("═")
                
                if pedidos_zona.empty:
                    print(f"\n❌ Não há pedidos para a zona {zona_emoji}.\n")
                
                else:
                    print(f"\n✅ Total de pedidos: {len(pedidos_zona)}\n")
                    
                    for _, pedido in pedidos_zona.iterrows():
                        print("─" * 70)
                        ut.showDetailsDestinatario(pedido)
                        print("─" * 70)
                        print()
                    input("Prima ENTER para voltar ao menu...")
            
        # ═══════════════════════════════════════════════════════════════
        # OPÇÃO 6: VOLTAR
        # ═══════════════════════════════════════════════════════════════
        
        elif opcao == '6':
            print("\n👋 Saindo do módulo de gestão de pedidos...\n")
            menu_ativo = False
            return


# ════════════════════════════════════════════════════════════════════════════════
# 🧪 TESTE
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🚀 Módulo de Gestão de Pedidos Carregado")
    print("Chame: ModOrderGestao(manager_id)")
    ModOrderGestao('SUPm')
