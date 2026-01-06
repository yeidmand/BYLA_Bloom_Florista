import os
import time
import pandas as pd
import mod_complaint
from mod_order_gestao import ModOrderGestao
from mod_delivery import main_delivery



FILE_CLIENTS = "login_client.csv"
FILE_STAFF = "user_work_profil.csv"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# =============================================================================
# CHECK DATABASE 
# =============================================================================
def verify_login_csv(user_role_choice):

    print(f"\n🔐 A verificar credenciais para: {user_role_choice.upper()}...")
    
    user_id = input("👤 ID: ").strip()
    password = input("🔑 Password: ").strip()

    try:
        # --- 1.(CLIENT) ---
        if user_role_choice == 'client':
            if not os.path.exists(FILE_CLIENTS):
                print(f"❌ Erro: Ficheiro {FILE_CLIENTS} não existe.")
                return None
            
            
            df = pd.read_csv(FILE_CLIENTS, sep=';', dtype=str)
            
            
            match = df[ (df['contact'].str.strip() == user_id) & (df['password'].str.strip() == password) ] #Verificamos o contacto e a password
            
            if not match.empty:
                name = match.iloc[0]['name']
                real_id = match.iloc[0]['id_client']
                
                print(f"✅ Sucesso! Bem-vindo, {name}")
                time.sleep(1)
                
                return {"id": real_id, "name": name}

        # --- 2.  (STAFF) ---
        elif user_role_choice in ['estafeta', 'manager']:
            if not os.path.exists(FILE_STAFF):
                print(f"❌ Erro: Ficheiro {FILE_STAFF} não existe.")
                return None

        
            df = pd.read_csv(FILE_STAFF, sep=';', dtype=str)
            
    
            match = df[ (df['id_worker'].str.strip() == user_id) & (df['password'].str.strip() == password) ]
            
            if not match.empty:
        
                duty_area = match.iloc[0]['dutyArea'].lower().strip()
                print(duty_area)
                # --- VALIDATIONS---
            
                if user_role_choice == 'manager':
                    if "gestor" in duty_area:
                        # Verificação do gestor especifico
                        if "encomenda" in duty_area:
                            print(f"✅ Login Gestor de Encomendas Aceite!")
                            time.sleep(1)
                            return {"id": user_id, "módulo": "Encomendas"}
                        elif "produto" in duty_area:
                            print(f"✅ Login Gestor de Productos Aceite! ({duty_area})")
                            time.sleep(1)
                            return {"id": user_id, "módulo": "Produtos"}
                        elif "estafeta" in duty_area:
                            print(f"✅ Login Gestor de Estafeta Aceite! ({duty_area})")
                            time.sleep(1)
                            return {"id": user_id, "módulo": "Estafeta"}
                        elif "reclamações" in duty_area:
                            print(f"✅ Login Gestor de Reclamações Aceite! ({duty_area})")
                            time.sleep(1)
                            return {"id": user_id, "módulo": "Reclamações"}
                        else:
                            print(f"❌ Erro: O ID '{user_id}' é de Gestor desconhecido.")
                            time.sleep(2)
                            return None                       
                    else:
                        print(f"❌ Erro: O ID '{user_id}' é de Estafeta, não de Gestor.")
                        time.sleep(2)
                        return None
                
                
                if user_role_choice == 'estafeta':
                    if "gestor" not in duty_area: 
                        print(f"✅ Login Estafeta Aceite! (Zona: {duty_area})")
                        time.sleep(1)
                        return {"id": user_id}
                    else:
                        print(f"❌ Erro: O ID '{user_id}' é de Gestor, não de Estafeta.")
                        time.sleep(2)
                        return None

        print("❌ Login Falhou (ID ou Password incorretos).")
        time.sleep(1)
        return None

    except Exception as e:
        print(f"❌ Erro de Sistema (CSV): {e}")
        return None

# =============================================================================
# SIMULATION PORTAL (avoid crashing)
# =============================================================================
def mock_portal(portal_name, user_info):

    while True:
        clear()
        print(f"✨ PORTAL: {portal_name} ✨")
        if portal_name == "ÁREA CLIENTE": #Isto SÒ Mostrar no se for Cliente
            print(f"👤 Cliente: {user_info['name']} | ID: {user_info['id']}")
        
        print("="*40)
        print("1. Entrar (Simulação)")
        print("0. Sair (Logout)")
        print("="*40)
        op = input("Opção: ")

        if op == '0': break
        if op == '1': 
            op = input("Opção: ").strip()
        
        if op == '0': 
            return op
        elif op == '1':
            print("... A trabalhar ...")
            time.sleep(1)
            return op
        else:
            print("❌ Opção inválida! Escolha 0 ou 1.")

# =============================================================================
# MAIN
# =============================================================================
def main():
    while True:
        clear()
        print("=== BYLA BLOOM FLORISTA ===")
        print("1. Cliente")
        print("2. Staff")
        print("0. Sair")
        op = input("Opção: ")

        if op == '0': break

        # --- CLIENTE ---
        elif op == '1':
            print("\n1. Login\n2. Registar")
            sub = input(">> ")

            if sub == '1':
                user = verify_login_csv('client')

                if user: 
                    while True:
                        clear()
                        print(f"👋 Olá, {user['name']}!")
                        print("="*30)
                        print("1. Ir para Loja (Client Portal)")
                        print("2. Fazer Reclamação (Complaint)")
                        print("0. Logout")
                        print("="*30)

                        action = input("👉 Opção: ")

                        if action == '1':
                            mock_portal("LOJA / CLIENT PORTAL", user)
                        
                        elif action == '2':
                            print("\n📝 A abrir Livro de Reclamações...")
                            time.sleep(1)

                            try:
                                mod_complaint.process_smart_complaint(user['id'])
                            except Exception as e:
                                print(f"❌ Error system: {e}")

                            
                            print("\n" + "="*40)
                            input("👉 Pressione ENTER para voltar ao menu...") 
                            
                            
                        elif action == '0':
                            break

                if user: 
                    op_in = mock_portal("ÁREA CLIENTE", user)
                    if op_in == '0': 
                        break
                    elif op_in == '1':
                        print("....Função PORTAL CLIENTE....") #MODIFICAR UMA VEZ EXISTA A FUNÇÂO PORTAL CLIENTE ex. mod_cliente(user['id'])
                        time.sleep(1)
                        break
                else:
                    break


            elif sub == '2':
                print("...ABRIR PORTAL CLIENTE PARA NOVO REGISTO...") #MODIFICAR UMA VEZ EXISTA A FUNÇÂO PORTAL CLIENTE ex. mod_cliente("")
                time.sleep(1)
                break


        # --- STAFF ---
        elif op == '2':
            print("\n1. Estafeta\n2. Gestor")
            sub = input(">> ")

            if sub == '1':
                user = verify_login_csv('estafeta')
                if user: mock_portal("PORTAL ESTAFETA", user)

                if user: 
                    op_in = mock_portal("PORTAL ESTAFETA", user)
                    if op_in == '0': 
                        break
                    elif op_in == '1':
                        print("....Função PORTAL ESTAFETA....") #ESTAFETA
                        main_delivery(user['id'])
                        time.sleep(1)
                        break
                else:   
                    break

            elif sub == '2':
                user = verify_login_csv('manager')
                if user: 
                    op_in = mock_portal("PORTAL GESTOR", user)
                    if op_in == '0': 
                        break
                    elif op_in == '1':
                        if user['módulo'] == 'Encomendas':
                            print("....Função PORTAL GESTOR DE ENCOMENDAS....")
                            ModOrderGestao(user['id'])                             # GESTOR DE ENCOMENDAS
                            time.sleep(1)
                            break
                        elif user['módulo'] == 'Produtos':
                            print("....Função PORTAL GESTOR DE PRODUTOS....") # MODIFICAR UMA VEZ EXISTA ex. mod_product()
                            time.sleep(1)
                            break
                        elif user['módulo'] == 'Estafeta':
                            print("....Função PORTAL GESTOR DE ESTAFETA....")
                            main_delivery(user['id'])
                            time.sleep(1)
                            break
                        elif user['módulo'] == 'Reclamações':
                            print("....Função PORTAL GESTOR DE RECLAMAÇÕES....") # MODIFICAR UMA VEZ EXISTA ex. mod_reclamacoes()
                else:
                    break
        else:
            print("❌ Opção inválida! Escolha 0, 1 ou 2.")


if __name__ == "__main__":
    main()