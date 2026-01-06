import pandas as pd
from datetime import datetime
import random
import math
from data_manager import load_orders, save_orders, load_user_work_profil

def stap_time_register():
    now = datetime.now() # obtain the exact moment of action
    format_data = str(now.strftime("%d/%m/%Y %H:%M:%S"))# format time
    return format_data

print(stap_time_register())

# creat data.frame
df = load_user_work_profil()

df1 = load_orders()

# Save the alterations made to the csv
# df.to_excel('db_BYLA_Bloom.xlsx', 'works_delivery', index = False)

print("♾️Portal Estafeta♾️")

# login
attempt_limit = 3
try_login = 0
enter_in_portal = False
close_portal = False

# Phase 0: Start work or close portal
enter_code = 0
sumOrders = 0
orders_to_work = 0

# Phase 1: Accept or Reject orders
end_phase_1 = False
ended_orders = 0
counting = 1

o_id = []
o_status = []
c_name = []
c_contact = []
c_address = []
c_a_number = []
c_zp1 = []
c_zp2 = []
o_reason = []


# Phase 2: Delivery or Not Delivery orders Accept's



def main_menu(): # just to see who it works
    print("🔺 De volta ao Menu Principal 🔺")
    
# main function to limit attempts of choosing codes
# this function is universal for all project
# in Portal Client can be need some changes
# op_dict: dictionary with number of code (key) and what it does (value)
def enter_code_attempt_limit(option_dict, attempt_limit):
    
    try_attempt = 0 # store number of input inserted
    # attempt_limit = 3 # max of input inserted
    continue_work = False # boolean to easy the code
    
    # confirm if enter_code is in dictionary
    while continue_work == False: # boolean to repeat
        try_attempt = try_attempt + 1 # increment number of attempts
        enter_code = int(input("✏️ Introduza uma opção: ")) # input
        if enter_code in option_dict: # if enter_code in dictionary, 
                                      # worker can continue the job
            continue_work = True # stop while, get out of the cycle
            return enter_code
        elif try_attempt < attempt_limit: # if enter_code not in dictionary
            print("Código incorreto.")
            print("Insira um código disponível")
            for code, text in option_dict.items(): # present all dictonary
                print({code}, ":",  {text})
            
        else: # try_attempt = 3, stop the work
            print("🔴 Atingiu o limite de tentativas.")
            print("🕐 Aguarde x segundos.")
            #function = time_waiting
            try_attempt = 0
            
            
# é preciso arranjar uma forma do valor do enter_code sair da função

# Phase: Login in portal delivery

# this while limits the number of attempts to login to the portal
id_worker = 113168


""""
while enter_in_portal == False: # boolean to repeat
    
    try_login = try_login + 1 # increment number of attempts
    id_worker = int(input("🔹 Introduza o seu número Mecanográfico: ")) # input
    pass_worker = input("🔸 Introduza a sua palavra-passe: ")# input
    
    # confirm if Login and Password are correct
    if ((df['id_worker'] == id_worker) & (df['password'] == pass_worker)).any():
        enter_in_portal = True
        orders_to_work = ((df1['id_worker'] == id_worker) & (df1['order_status'] == "assigned")).sum()
        print('Bem-vindo Estafeta', id_worker, "tem", orders_to_work,
              "encomenda(s) para verificar e entregar.")
    elif try_login < attempt_limit: # login or password are incorret
        print("❌ Número Mecanográfico ou Palavra-passe errado!")
    else: # try_login = 3, close the portal
        print("🔒 Atingiu o limite de tentativas.")
        print("📞 Contacte o Gestor")
        close_portal = True
        break
"""
        # main_menu() # return to main menu (all menus)

# print("FIM DA FASE LOGIN")



# PHASE 0: START WORK OR CLOSE PORTAL
print("Escolha uma opção disponível\n",
      "1: Iniciar trabalho\n",
      "0: Terminar seção")

# creat dictionary for gave options to select
dict_ph1 = {1: "Iniciar trabalho",
          0: "Terminar seção"}
# call function with dictionary created
# enter_code_attempt_limit(dict_phase_1) # call function

enter_code = enter_code_attempt_limit(dict_ph1, 3)

if enter_code == 0:
    print("Terminou a seção")
    close_portal = True
    main_menu() # return to main menu (all menus)
    
if enter_code == 1: # apenas para ver no código
    print("")
    
# print("FIM DA FASE 0 - ENTRAR NO PORTAL ESTAFETA")

# PHASE 1: ACCEPT OR REJECT ORDERS
# menu options
print("Escolha uma opção disponível\n",
      "{1}: Aceitar Encomenda\n",
      "{0}: Recusar Encomenda")

# creat dictionary for gave options to select
dict_ph1_assigned_orders = {1: "Aceitar Encomenda",
          0: "Recusar Encomenda"}

# run all orders
for i in range(0, len(df1)):
    # confirm if the assigned to worker
    if df1.iloc[i,13] == id_worker and df1.iloc[i,7] == "assigned":
        o_id = df1.iloc[i, 0]
        c_name = df1.iloc[i,2]
        c_contact = df1.iloc[i,3]
        c_address = df1.iloc[i,4]
        c_zp1 = df1.iloc[i,5]
        c_zp2 = df1.iloc[i,6]
        o_status = df1.iloc[i,7]
        o_reason = df1.iloc[i,8]
        # print data of order
        print("📦 Encomenda:", o_id,"\n🧑‍💼 Name:", c_name,"\n📞 Contacto:", c_contact, 
              "\n🚩 Morada:", c_address,"\n📍 Código-Postal:", c_zp1, "-", c_zp2)
        
        enter_code = enter_code_attempt_limit(dict_ph1_assigned_orders, 3)
        
        # order accpet
        if enter_code == 1:
            df1.iloc[i,7] = "on_truck" # change status order
            df1.iloc[i,9] = stap_time_register() # register date and hour
        
        # order declined
        if enter_code == 0:
            df1.iloc[i,7] = "denied" # change status order
            # write the reason of denied
            write_reason = input("Encomenda recusada, inserir o motivo: ")
            df1.iloc[i,8] = write_reason
            df1.iloc[i,9] = stap_time_register()
            while write_reason == "" and counting < 3: # can't be empti
                counting = counting + 1
                print("⚠️ Erro: sem motivo definido")
                write_reason = input("Insira o motivo: ")
                df1.iloc[i,8] = write_reason # update the input
                if write_reason == "" and counting == 3:
                    # update the input automatically
                    df1.iloc[i,8] = "Sem motivo referido"
        
        
# print("FIM DA 1ªFASE - ACEITAR OU RECUSAR ENCOMENDAS")


# PHASE 2: DELIVERY OR NOT DELIVERY ORDERS
# menu options
print("Escolha uma opção disponível\n",
      "{1}: Entregar Encomenda\n",
      "{0}: Não entregar Encomenda")

# creat dictionary for gave options to select
dict_ph2_delivery_orders = {1: "Entregar Encomenda",
          0: "Não entregar Encomenda"}

# ALL GPS CODE WAS DEVELOPED by COPILOT
# Point of reference: Universidade do Minho, Campos Gualtar
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
    lat_moviment, lon_moviment = convert_meters_to_degrees(lat, meters_north, meters_east)
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
    norte_m, leste_m = zones[zone]
    dlat, dlon = convert_meters_to_degrees(lat_center, norte_m, leste_m)
    lat_anchor = lat_center + dlat
    lon_anchor = lon_center + dlon
    return random_point(lat_anchor, lon_anchor)

# run all orders
for i in range(0, len(df1)):
    # confirm if the orders is on_truck
    if df1.iloc[i,13] == id_worker and df1.iloc[i,7] == "on_truck":
        o_id = df1.iloc[i, 0]
        c_name = df1.iloc[i,2]
        c_contact = df1.iloc[i,3]
        c_address = df1.iloc[i,4]
        c_zp1 = df1.iloc[i,5]
        c_zp2 = df1.iloc[i,6]
        o_status = df1.iloc[i,7]
        o_reason = df1.iloc[i,8]
        # print data of order
        print("📦 Encomenda:", o_id,"\n🧑‍💼 Name:", c_name,"\n📞 Contacto:", c_contact, 
              "\n🚩 Morada:", c_address,"\n📍 Código-Postal:", c_zp1, "-", c_zp2)
        
        enter_code = enter_code_attempt_limit(dict_ph2_delivery_orders, 3)
        
        # creat coordinates and store
        # respective zone
        working_zone = df.loc[df['id_worker'] == id_worker, 'duty_area'].iloc[0]
        lat_store, lon_store = generate_coordinates(working_zone)
        df1.iloc[0,11] = lat_store
        df1.iloc[0,12] = lon_store
        
        
        # order delivery
        if enter_code == 1:
            df1.iloc[i,7] = "delivery" # change status order
            df1.iloc[i,10] = stap_time_register() # register date and hour
        
        # order not delivery
        if enter_code == 0:
            df1.iloc[i,7] = "not delivery" # change status order
            # write the reason of denied
            write_reason = input("Encomenda não entregue, inserir o motivo: ")
            df1.iloc[i,8] = write_reason
            df1.iloc[i,10] = stap_time_register()
            while write_reason == "" and counting < 3: # can't be empti
                counting = counting + 1
                print("⚠️ Erro: sem motivo definido")
                write_reason = input("Insira o motivo: ")
                df1.iloc[i,8] = write_reason # update the input
                if write_reason == "" and counting == 3:
                    # update the input automatically
                    df1.iloc[i,8] = "Sem motivo referido"

df1.to_csv('orders_data.csv', sep = ";", index = False)

print("FIM DA 2ªFASE - ENTREGAR OU NÂO ENTREGAR ENCOMENDAS")


# df1.to_csv('orders_data.csv', sep = ";", index = False)

print("Fim.")


    

# Save the alterations made to the csv
# df.to_csv('login_estafetas.csv', index = False)





