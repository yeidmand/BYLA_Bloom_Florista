import os
import time
import pandas as pd

from mod_complaint import process_smart_complaint
from mod_order_gestao import ModOrderGestao
from mod_delivery import main_delivery
from mod_product import menu_produtos
from mod_client import welcome_client


FILE_CLIENTS = "login_client.csv"
FILE_STAFF = "user_work_profil.csv"


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def verify_login_csv(user_role_choice):
    print(f"\n🔐 A verificar credenciais para: {user_role_choice.upper()}...")

    user_id = input("👤 ID: ").strip()
    password = input("🔑 Password: ").strip()

    try:
        # --- 1.(CLIENT) ---
        if user_role_choice == 'client':
            if not os.path.exists(FILE_CLIENTS):
                print(f"❌ Erro: Ficheiro {FILE_CLIENTS} não existe.")
                time.sleep(2)
                return None

            df = pd.read_csv(FILE_CLIENTS, sep=';', dtype=str)

            match = df[
                (df['id_client'].str.strip() == user_id) &
                (df['password'].str.strip() == password)
            ]

            if not match.empty:
                name = match.iloc[0]['name']
                real_id = match.iloc[0]['id_client']
                print(f"✅ Sucesso! Bem-vindo, {name}")
                time.sleep(1)
                return {"id": real_id, "name": name}

            print("❌ Login Falhou (ID ou Password incorretos).")
            time.sleep(1)
            return None

        # --- 2. (STAFF) ---
        elif user_role_choice in ['estafeta', 'manager']:
            if not os.path.exists(FILE_STAFF):
                print(f"❌ Erro: Ficheiro {FILE_STAFF} não existe.")
                time.sleep(2)
                return None

            df = pd.read_csv(FILE_STAFF, sep=';', dtype=str)

            match = df[
                (df['id_worker'].str.strip() == user_id) &
                (df['password'].str.strip() == password)
            ]

            if match.empty:
                print("❌ Login Falhou (ID ou Password incorretos).")
                time.sleep(1)
                return None

            duty_area = match.iloc[0]['dutyArea'].lower().strip()
            print(duty_area)

            # --- VALIDATIONS---
            if user_role_choice == 'manager':
                if "gestor" in duty_area:
                    # Verificação do gestor especifico
                    if "encomenda" in duty_area:
                        print("✅ Login Gestor de Encomendas Aceite!")
                        time.sleep(1)
                        return {"id": user_id, "módulo": "Encomendas"}

                    elif "produto" in duty_area:
                        print(f"✅ Login Gestor de Productos Aceite! ({duty_area})")
                        time.sleep(1)
                        return {"id": user_id, "módulo": "Produtos"}

                    elif "reclamações" in duty_area:
                        print(f"✅ Login Gestor de Reclamações Aceite! ({duty_area})")
                        time.sleep(1)
                        return {"id": user_id, "módulo": "Reclamações"}

                    else:
                        print(f"❌ Erro: O ID '{user_id}' é de Gestor desconhecido.")
                        time.sleep(2)
                        return None
                else:
                    print(f"❌ Erro: O ID '{user_id}' não é de Gestor.")
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

        # caso role não reconhecido
        print("❌ Tipo de utilizador inválido.")
        time.sleep(1)
        return None

    except Exception as e:
        print(f"❌ Erro de Sistema (CSV): {e}")
        time.sleep(2)
        return None

def mock_portal(portal_name, user_info):
    Valid = True
    while Valid:
        clear()
        print(f"✨ PORTAL: {portal_name} ✨")

        if portal_name == "ÁREA CLIENTE":
            print(f"👤 Cliente: {user_info['name']} | ID: {user_info['id']}")

        print("=" * 40)
        print("1. Entrar (Simulação)")
        print("0. Sair (Logout)")
        print("=" * 40)

        op = input("Opção: ").strip()

        if op == '0':
            Valid = False
            return op
        elif op == '1':
            print("... A trabalhar ...")
            time.sleep(1)
            Valid = False
            return op
        else:
            print("❌ Opção inválida! Escolha 0 ou 1.")
            time.sleep(1)

# INICIO DO PROGRAMA
def main():
    while True:
        clear()
        print("=== BYLA BLOOM FLORISTA ===")
        print("1. Cliente")
        print("2. Staff")
        print("0. Sair")

        op = input("Opção: ").strip()

        if op == '0':
            break

        # --- CLIENTE ---
        elif op == '1':
            print("\n1. Login\n2. Registar")
            sub = input(">> ").strip()

            if sub == '1':
                user = verify_login_csv('client')

                if user:
                    while True:
                        clear()
                        print(f"👋 Olá, {user['name']}!")
                        print("=" * 30)
                        print("1. Ir para Loja (Client Portal)")
                        print("2. Fazer Reclamação (Complaint)")
                        print("0. Logout")
                        print("=" * 30)

                        action = input("👉 Opção: ").strip()

                        if action == '1':
                            mock_portal("LOJA / CLIENT PORTAL", user)
                            welcome_client(user['id'])  # PORTAL CLIENTE

                        elif action == '2':
                            print("\n📝 A abrir Livro de Reclamações...")
                            time.sleep(1)
                            try:
                                process_smart_complaint(user['id']) # Portal Reclamações
                            except Exception as e:
                                print(f"❌ Error system: {e}")
                            print("\n" + "=" * 40)
                            input("👉 Pressione ENTER para voltar ao menu...")

                        elif action == '0':
                            break

                        else:
                            print("❌ Opção inválida! Escolha 0, 1 ou 2.")
                            time.sleep(1)

                    # portal final do cliente
                    op_in = mock_portal("ÁREA CLIENTE", user)
                    if op_in == '0':
                        pass
                    elif op_in == '1':
                        print("....Função PORTAL CLIENTE....") #PORTAL CLIENTE ***
                        time.sleep(1)

            elif sub == '2':
                print("...ABRIR PORTAL CLIENTE PARA NOVO REGISTO...")
                welcome_client("") # PORTAL CLINTE ***
                time.sleep(1)
            else:
                print("❌ Opção inválida! Escolha 1 ou 2.")
                time.sleep(1)

        # --- STAFF ---
        elif op == '2':
            print("\n1. Estafeta\n2. Gestor")
            sub = input(">> ").strip()

            # ESTAFETA
            if sub == '1':
                user = verify_login_csv('estafeta')
                if user:
                    op_in = mock_portal("PORTAL ESTAFETA", user)
                    if op_in == '1':
                        print("....Função PORTAL ESTAFETA....") 
                        main_delivery(user['id']) # PORTAL ESTAFETA
                        time.sleep(1)

            # GESTORES
            elif sub == '2':
                user = verify_login_csv('manager')
                if user:
                    op_in = mock_portal("PORTAL GESTOR", user)
                    if op_in == '1':
                        if user['módulo'] == 'Encomendas':
                            print("....Função PORTAL GESTOR DE ENCOMENDAS....")
                            ModOrderGestao(user['id']) # PORTAL GESTOR ENCOMENDA
                            time.sleep(1)
                        elif user['módulo'] == 'Produtos':
                            print("....Função PORTAL GESTOR DE PRODUTOS....")
                            menu_produtos() # PORTAL GESTOR PRODUTO
                            time.sleep(1)

            else:
                print("❌ Opção inválida! Escolha 1 ou 2.")
                time.sleep(1)

        else:
            print("❌ Opção inválida! Escolha 0, 1 ou 2.")
            time.sleep(1)


if __name__ == "__main__":
    main()