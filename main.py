import os
import sys
import time

# ---DATABASE TEST
VALID_IDS = {
    "client":   ["101", "102", "103"],      
    "estafeta": ["E01", "worker1"],          
    "manager":  ["SUPm", "admin", "M01"]     
}

def clear():
    """Limpar o ecrã"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mock_portal(name):
    while True:
        clear()
        print(f"✨ BEM-VINDO AO PORTAL: {name.upper()} ✨")
        print("="*40)
        print("1. Simular Trabalho")
        print("0. Sair e Voltar ao Menu Principal")
        print("="*40)
        op = input("Opção: ")
        if op == '0':
            print(f"👋 A sair do {name}...")
            time.sleep(1)
            break 
        elif op == '1':
            print("🔨 A trabalhar... (Simulação)")
            input("Enter para continuar...")

# --- LOGIC CHECK ID  ---
def verify_credentials(role_required):
    """
    Kiểm tra ID dựa trên danh sách VALID_IDS ở trên.
    """
    print(f"\n🔐 A verificar credenciais para: {role_required.upper()}...")
    
    
    user_id = input("👤 ID Utilizador: ").strip()
    

    password = input("🔑 Palavra-passe: ").strip()

    # --- LOGIC CHECK DATABASE ---

    allowed_list = VALID_IDS.get(role_required, [])
    
    if user_id in allowed_list:
        print("✅ Credenciais Válidas!")
        time.sleep(1)
        return user_id
    else:
        print(f"❌ Erro: O ID '{user_id}' não é válido ou não tem permissão de {role_required}.")
        print(f"   (Dica para teste: Tente usar {allowed_list})")
        time.sleep(2)
        return None

# --- 4. MAIN FLOW ---
def main():
    while True:
        clear()
        print("="*60)
        print("🌸  BYLA BLOOM FLORISTA - MAIN SYSTEM  🌸")
        print("="*60)
        print("1. Área Cliente (Customer)")
        print("2. Área Staff (Estafeta / Gestor)")
        print("0. Sair")
        print("-" * 60)
        
        choice = input("👉 Selecione Opção: ").strip()
        
        if choice == '0':
            print("\n👋 Adeus!")
            break

        # --- CLIENT ---
        elif choice == '1':
        
            print("\n" + "-"*30)
            print("❓ Já tem registo?")
            print("   y: Sim (Login)")
            print("   n: Não (Novo Registo)")
            is_reg = input("👉 (y/n): ").lower().strip()

            if is_reg == 'n':
                mock_portal("Cliente (Novo)")
            elif is_reg == 'y':
                client_id = verify_credentials("client") # Check list ["101", "102"]
                if client_id:
                    mock_portal(f"Cliente {client_id}")

        # --- STAFF ---
        elif choice == '2':
            print("\n🔐 --- STAFF ACCESS ---")
            print("1. Estafeta (Courier)")
            print("2. Gestor (Manager)")
            print("0. Voltar")
            staff_choice = input("👉 Selecione Cargo: ")

            if staff_choice == '1':
                worker_id = verify_credentials("estafeta") # Check list ["E01"]
                if worker_id:
                    mock_portal(f"Estafeta {worker_id}")

            elif staff_choice == '2':
                manager_id = verify_credentials("manager") # Check list ["SUPm"]
                if manager_id:
                    # Manager Menu
                    while True:
                        clear()
                        print(f"📊 GESTOR: {manager_id}")
                        print("1. Orders")
                        print("2. Products")
                        print("0. Logout")
                        op = input("Opção: ")
                        if op == '1': mock_portal("Orders")
                        elif op == '2': mock_portal("Products")
                        elif op == '0': break

            elif staff_choice == '0':
                continue
        else:
            print("Opção inválida.")
            time.sleep(1)

if __name__ == "__main__":
    main()