import os
import time
import pandas as pd
import mod_complaint


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
            
            
            match = df[ (df['id_client'].str.strip() == user_id) & (df['password'].str.strip() == password) ]
            
            if not match.empty:
                
                name = match.iloc[0]['name']
                print(f"✅ Sucesso! Bem-vindo, {name}")
                time.sleep(1)
                return {"id": user_id, "name": name}

        # --- 2.  (STAFF) ---
        elif user_role_choice in ['estafeta', 'manager']:
            if not os.path.exists(FILE_STAFF):
                print(f"❌ Erro: Ficheiro {FILE_STAFF} não existe.")
                return None

        
            df = pd.read_csv(FILE_STAFF, sep=';', dtype=str)
            
    
            match = df[ (df['id_worker'].str.strip() == user_id) & (df['password'].str.strip() == password) ]
            
            if not match.empty:
        
                duty_area = match.iloc[0]['dutyArea'].strip()
                
                # --- VALIDATIONS---
            
                if user_role_choice == 'manager':
                    if "Gestor" in duty_area: 
                        print(f"✅ Login Gestor Aceite! ({duty_area})")
                        time.sleep(1)
                        return {"id": user_id, "name": f"Gestor {user_id}"}
                    else:
                        print(f"❌ Erro: O ID '{user_id}' é de Estafeta, não de Gestor.")
                        time.sleep(2)
                        return None
                
                
                if user_role_choice == 'estafeta':
                    if "Gestor" not in duty_area: 
                        print(f"✅ Login Estafeta Aceite! (Zona: {duty_area})")
                        time.sleep(1)
                        return {"id": user_id, "name": f"Estafeta {user_id}"}
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
        print(f"👤 User: {user_info['name']} | ID: {user_info['id']}")
        print("="*40)
        print("1. Entrar (Simulação)")
        print("0. Sair (Logout)")
        print("="*40)
        op = input("Opção: ")

        if op == '0': break
        if op == '1': 
            print("... A trabalhar ...")
            time.sleep(1)

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
                            mod_complaint.process_smart_complaint(user['id']) 
                            
                        elif action == '0':
                            break

            elif sub == '2':
                mock_portal("NOVO REGISTO", {"id": "NEW", "name": "Visitante"})

        # --- STAFF ---
        elif op == '2':
            print("\n1. Estafeta\n2. Gestor")
            sub = input(">> ")

            if sub == '1':
                user = verify_login_csv('estafeta')
                if user: mock_portal("PORTAL ESTAFETA", user)

            elif sub == '2':
                user = verify_login_csv('manager')
                if user: mock_portal("PORTAL GESTOR", user)

if __name__ == "__main__":
    main()