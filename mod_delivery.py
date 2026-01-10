import pandas as pd
import datetime as dtime
import os
import random
import math
import data_manager as dm

def create_event(order_id, event_type, id_worker, details = "", lat = "", 
                 lon = ""):
    # Creat a event
    event_id = "EV" + dtime.datetime.now().strftime("%Y%m%d%H%M%S")
    timestamp = dtime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    event = {
        "event_id": event_id,
        "order_id": order_id,
        "event_type": event_type,
        "staptime_1": timestamp,
        "staptime_2": "",
        "login": id_worker,
        "details": details,
        "latitude": lat,
        "longitude": lon
    }
    
    return event

# Create GPS coordinates
# Point of reference: Universidade do Minho, Campus Gualtar
lat_center = 41.560177
lon_center = -8.397281
meters_moviment = 50000 # distance from the centre to each zone (in metres)
meters_random = 5000 # random dispersion (in metres)

# convert meters to degrees to creat coordinates
def convert_meters_to_degrees(lat_ref, meters_north=0.0, meters_east=0.0):
    lat_moviment = meters_north / 111_000.0
    coslat = math.cos(math.radians(lat_ref))
    lon_moviment = meters_east / (111_000.0 * max(0.0001, abs(coslat)))
    return lat_moviment, lon_moviment

# creat a random point to the coordinates
def random_point(lat, lon, meters_radius = meters_random):
    ang = random.uniform(0, 2 * math.pi)
    r = meters_radius * math.sqrt(random.random())
    meters_north = r * math.cos(ang)
    meters_east = r * math.sin(ang)
    lat_moviment, lon_moviment = convert_meters_to_degrees(lat, meters_north, 
                                                           meters_east)
    return round(lat + lat_moviment, 6), round(lon + lon_moviment, 6)

# generate the coordenates
def generate_coordinates(zone):
    zones = {
        "Center": (0, 0),
        "North": (meters_moviment, 0),
        "South": (-meters_moviment, 0),
        "East": (0, meters_moviment),
        "West": (0, -meters_moviment),
    }
    meters_north, meters_east = zones[zone]
    dlat, dlon = convert_meters_to_degrees(lat_center, meters_north, 
                                           meters_east)
    lat_anchor = lat_center + dlat
    lon_anchor = lon_center + dlon
    return random_point(lat_anchor, lon_anchor)


def show_orders(orders_df, id_worker):
    # Show orders assigned to the worker
    
    orders_assigned = orders_df[orders_df["id_worker"] == id_worker]
    
    if orders_assigned.empty:
        print("\n❌ Não tens encomendas atribuídas")
        return None
    
    print("\n" + "="*70)
    print("📋 AS TUAS ENCOMENDAS ATRIBUÍDAS")
    print("="*70)
    
    for idx, (_, enc) in enumerate(orders_assigned.iterrows(), 1):
        print(f"\n[{idx}] Encomenda: {enc['order_id']}")
        print(f"    Cliente: {enc['name']}")
        print(f"    Contacto: {enc['contact']}")
        print(f"    Morada: {enc['address']}")
        print(f"    Código-Postal: {enc['ZP1']}-{enc['ZP2']}")
        print(f"    Estado: {enc['order_status']}")
        if str(enc.get('order_status', '')).lower() == "recusada":
            print(f"    Motivo: {enc.get('order_reason', '')}")
        if str(enc.get('order_status', '')).lower() == "não entregue":
            print(f"    Motivo: {enc.get('order_reason', '')}")    
        print("    " + "-"*60)
    
    return orders_assigned


def accept_order(orders_df, events_df, order_id, id_worker):
    # Accept order
    
    # Check if the order exists
    if order_id not in orders_df["order_id"].values:
        print(f"\n❌ Encomenda {order_id} no encontrada")
        return orders_df, events_df
    
    print(f"\n✅ Encomenda aceite {order_id}...")
    
    lat = 41.560177
    lon = -8.397281
    print("📍 Latitude:", lat)
    print("📍 Longitude:", lon)
    
    # Update status
    orders_df.loc[orders_df["order_id"] == order_id, "order_status"] = "em distribuição"
    orders_df.loc[orders_df["order_id"] == order_id, "order_reason"] = ""
    
    # Create a event
    event = create_event(
        order_id = order_id,
        event_type = "aceite",
        id_worker = id_worker,
        details = f"Encomenda aceite por {id_worker}",
        lat = lat,
        lon = lon
    )
    
    events_df = pd.concat([events_df, pd.DataFrame([event])], ignore_index=True)
    
    print(f"✅ Encomenda {order_id} aceite!")
    print(f"   Data e Hora: {event['staptime_1']}")
    
    return orders_df, events_df


def decline_orders(orders_df, events_df, order_id, id_worker):
    # Decline orders
    
    # Check if the order exists
    if order_id not in orders_df["order_id"].values:
        print(f"\n❌ Encomenda {order_id} não encontrada")
        return orders_df, events_df
    
    # Insert reason
    print(f"\n❌ Encomenda recusada {order_id}...")
    reason = input("📝 Motivo da recusa: ").strip()
    
    # 
    num = 1
    while reason == "":
        print("⚠️  Motivo obrigatório!")
        num = num + 1
        reason = input("📝 Motivo da recusa: ").strip()
        if num == 3 and reason == "":
            reason = "Motivo não referido"
            print("    Não referiu o motivo da recusa\n",
                  "   Motivo referido como", "'" + reason + "'")
    
    # Update status
    orders_df.loc[orders_df["order_id"] == order_id, "order_status"] = "recusada"
    orders_df.loc[orders_df["order_id"] == order_id, "order_reason"] = reason
    
    lat = 41.560177
    lon = -8.397281
    
    # Create event
    event = create_event(
        order_id = order_id,
        event_type = "recusada",
        id_worker = id_worker,
        details = f"Recusada por {id_worker}. Motivo: {reason}",
        lat = lat,
        lon = lon
    )
    
    events_df = pd.concat([events_df, pd.DataFrame([event])], ignore_index=True)

    print(f"❌ Encomenda {order_id} recusada!")
    print(f"   Motivo: {reason}")
    print("📍 Latitude:", lat)
    print("📍 Longitude:", lon)
    
    return orders_df, events_df


def delivery_orders(orders_df, events_df, order_id, id_worker):
    # Delivery orders
    
    # Check if the order exists
    if order_id not in orders_df["order_id"].values:
        print(f"\n❌ Encomenda {order_id} não encontrada")
        return orders_df, events_df
    
    # Check if status order is accepted
    status = orders_df[orders_df["order_id"] == order_id]["order_status"].iloc[0]
    if status != "em distribuição":
        print(f"\n❌ Encomenda não foi aceitada (Estado: {status})")
        return orders_df, events_df
    
    working_zone = orders_df[orders_df["id_worker"] == id_worker]["duty_zone"].iloc[0]
    lat, lon = generate_coordinates(working_zone)
    
    client = input("👤 Nome de quem recebeu: ").strip()
    
    # Update status
    orders_df.loc[orders_df["order_id"] == order_id, "order_status"] = "entregue"
    
    # Create event
    event = create_event(
        order_id = order_id,
        event_type = "entregue",
        id_worker = id_worker,
        details = f"Entregue a: {client}",
        lat = lat,
        lon = lon
    )
    
    events_df = pd.concat([events_df, pd.DataFrame([event])], ignore_index=True)
    
    print(f"\n✅ Encomenda {order_id} entregue!")
    print(f"   Recibida por: {client}")
    print(f"   Localização: ({lat}, {lon})")
    
    return orders_df, events_df


def decline_delivery(orders_df, events_df, order_id, id_worker):
    # Decline delivery
    
    # Check if the order exists
    if order_id not in orders_df["order_id"].values:
        print(f"\n❌ Encomenda {order_id} não encontrada")
        return orders_df, events_df
    
    # Check if status order is accepted
    status = orders_df[orders_df["order_id"] == order_id]["order_status"].iloc[0]
    if status != "em distribuição":
        print(f"\n❌ Encomenda não foi aceite (Estado: {status})")
        return orders_df, events_df
    
    # Types of reason to not delivery
    print(f"\n❌ Encomenda não entregue {order_id}")
    print("\nMotivos de não entregar:")
    print("1. Morada errada")
    print("2. Cliente indisponível")
    print("3. Portaria fechada")
    print("4. Problemas de acesso")
    print("5. Cliente recusa aceitar encomenda")
    print("6. Outro")
    
    type_select = input("\nSelecionar um tipo (1-6): ").strip()
    
    dict_reasons = {
        "1": "Morada errada",
        "2": "Cliente Indisponivel",
        "3": "Portaria fechada",
        "4": "Problema de acesso",
        "5": "Cliente recusa aceitar encomenda",
        "6": "Outro"
    }
    
    reason = dict_reasons.get(type_select, "outro")
    description = input("📝 Descrição: ").strip()
    
    working_zone = orders_df[orders_df["id_worker"] == id_worker]["duty_zone"].iloc[0]
    lat, lon = generate_coordinates(working_zone)
    
    # Update status
    orders_df.loc[orders_df["order_id"] == order_id, "order_status"] = "não entregue"
    orders_df.loc[orders_df["order_id"] == order_id, "order_reason"] = f"{reason}: {description}"
    
    # Create event
    event = create_event(
        order_id = order_id,
        event_type = "não entregue",
        id_worker = id_worker,
        details = f"Não entregue: {reason} - {description}",
        lat = lat,
        lon = lon
    )
    
    events_df = pd.concat([events_df, pd.DataFrame([event])], ignore_index=True)
    
    print("\n❌ Encomenda não entregue!")
    print(f"   Tipo: {reason}")
    print(f"   Descrição: {description}")
    
    return orders_df, events_df

def statistic_events(orders, estafeta_id):
    # 
    
    # Filtrar eventos del estafeta
    my_orders = orders[orders["id_worker"] == estafeta_id]
    
    if my_orders.empty:
        print("\n❌ Sem eventos efetuados")
        return
    print("Impossível calcular estatísticas devido à falta de TRABALHO!")
    accept = len(my_orders[my_orders["order_status"] == "em distribuição"])
    declined = len(my_orders[my_orders["order_status"] == "recusada"])
    if accept == 0:
        delivery = len(my_orders[my_orders["order_status"] == "entregue"])
        not_delivery = len(my_orders[my_orders["order_status"] == "não entregue"])
        accept = delivery + not_delivery
        if accept == 0:
            print("Impossível calcular estatísticas devido à falta de TRABALHO!")
            return
        else:
            order_total = len(my_orders["order_id"])
            sucsses_rate = (delivery / accept * 100) if order_total > 0 else 0
            # Mostrar
            print("\n" + "="*70)
            print("📊 MIS MÉTRICAS")
            print("="*70)
            print(f"\n📦 ENCOMENDAS:")
            print(f"   • Aceites:   {accept}")
            print(f"   • Recusadas:  {declined}")
            print(f"   • Entregues:  {delivery}")
            print(f"   • Não Entregues:    {not_delivery}")
            print(f"\n✅ Taxa de Sucesso: {sucsses_rate:.1f}%")
            print(f"   Total de Encomendas: {order_total}")
            print("\n" + "="*70)
    else:
        accept = accept + delivery + not_delivery
        order_total = len(my_orders["order_id"])
        sucsses_rate = (delivery / accept * 100) if order_total > 0 else 0
        # Mostrar
        print("\n" + "="*70)
        print("📊 MIS MÉTRICAS")
        print("="*70)
        print(f"\n📦 ENCOMENDAS:")
        print(f"   • Aceites:   {accept}")
        print(f"   • Recusadas:  {declined}")
        print(f"   • Entregues:  {delivery}")
        print(f"   • Não Entregues:    {not_delivery}")
        print(f"\n✅ Taxa de Sucesso: {sucsses_rate:.1f}%")
        print(f"   Total de Encomendas: {order_total}")
        print("\n" + "="*70)
    
    
    
    

# MAIN MENU PORTAL ESTAFETA

def main_delivery(id_worker):
    # Main Portal Estafeta
    
    print("\n" + "="*70)
    print("♾️ PORTAL ESTAFETA - BYLA BLOOM")
    print("="*70)
    print(f"Bem-Vindo: {id_worker}")
    
    open_portal = True
    
    while open_portal:
        
        # load data
        orders = dm.load_orders()
        events = dm.load_order_events()
        
        
        print("\n" + "="*70)
        print("MENU PRINCIPAL")
        print("="*70)
        print("1. Ver as minhas encomendas")
        print("2. Aceitar encomenda")
        print("3. Recusar encomenda")
        print("4. Registar encomenda entregue")
        print("5. Registar encomenda não entregue")
        print("6. Ver as minhas estatística")
        print("0. Sair")
        print("="*70)
        
        option = input("\n✏️ Selecione uma opção: ").strip()
        
        # OPTION 1: View Orders
        if option == "1":
            my_orders = show_orders(orders, id_worker)
            input("\nPrima ENTER para continuar...")
        
        # OPTION 2: Accpet
        elif option == "2":
            my_orders = show_orders(orders, id_worker)
            if my_orders is not None:
                order_id = input("\n✏️ ID da encomenda aceite: ").strip().upper()
                orders, events = accept_order(
                    orders, events, order_id, id_worker
                )
                dm.save_orders(orders)
                dm.save_order_events(events)
            input("\nPrima ENTER para continuar...")
        
        # OPTION 3: Declined
        elif option == "3":
            my_orders = show_orders(orders, id_worker)
            if my_orders is not None:
                order_id = input("\n✏️ ID da encomenda recusada: ").strip().upper()
                orders, events = decline_orders(
                    orders, events, order_id, id_worker)
                dm.save_orders(orders)
                dm.save_order_events(events)
            input("\nPrima ENTER para continuar...")
        
        # OPTION 4: Delivery
        elif option == "4":
            my_orders = show_orders(orders, id_worker)
            if my_orders is not None:
                order_id = input("\n✏️ ID da encomenda entregue: ").strip().upper()
                orders, events = delivery_orders(
                    orders, events, order_id, id_worker
                )
                dm.save_orders(orders)
                dm.save_order_events(events)
            input("\nPrima ENTER para continuar...")
        
        # OPTION 5: Not Delivery
        elif option == "5":
            my_orders = show_orders(orders, id_worker)
            if my_orders is not None:
                order_id = input("\n✏️ ID da encomenda não entregue: ").strip().upper()
                orders, events = decline_delivery(
                    orders, events, order_id, id_worker
                )
                dm.save_orders(orders)
                dm.save_order_events(events)
            input("\nPrima ENTER para continuar...")
        
        # OPTION 6: STATISTIC
        elif option == "6":
            statistic_events(orders, id_worker)
            input("\nPrima ENTER para continuar...")
            print("Ainda sem função atualizada")
        
        # OPTION 0: Log out
        elif option == "0":
            print("\n👋 Até Amanhã!")
            open_portal = False
        
        else:
            print("\n❌ Opção inválida")
            input("Prima ENTER para continuar...")
