import os
import sys

# --- IMPORT MODULES (Defensive Import) ---
try:
    import mod_client           # Login & Client Portal
except ImportError:
    mod_client = None

try:
    import mod_delivery         # Estafeta Module
except ImportError:
    mod_delivery = None

try:
    import mod_order_gestao     # Order Management Module
except ImportError:
    mod_order_gestao = None

try:
    import mod_product          # Product Module
except ImportError:
    mod_product = None


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        clear()
        print("="*60)
        print("🌸  BYLA BLOOM FLORISTA - MAIN SYSTEM  🌸")
        print("="*60)
        print("1. Client Area (Customer)")
        print("2. Staff Area (Shipper/Manager)")
        print("0. Exit")
        print("-" * 60)
        
        choice = input("👉 Select Option: ").strip()
        
        # =================================================================
        # 0. EXIT
        # =================================================================
        if choice == '0':
            print("\n👋 Goodbye! See you next time.")
            break

        # =================================================================
        # 1. CLIENT AREA
        # =================================================================
        elif choice == '1':
            if not mod_client:
                print("\n⚠️ Error: 'mod_client.py' is missing.")
                input("Enter to return...")
                continue

            print("\n" + "-"*30)
            print("❓ Are you already registered?")
            print("   y: Yes (Login)")
            print("   n: No (Register)")
            is_reg = input("👉 Select (y/n): ").lower().strip()

            # --- A. NEW USER (REGISTER) ---
            if is_reg == 'n':
                print("\n[System] Opening Registration (Param: Empty)...")
                if hasattr(mod_client, 'run_client_portal'):
                    try:
                        # Logic: Pass empty string "" for new users
                        mod_client.run_client_portal("") 
                    except Exception as e:
                        print(f"❌ Error in mod_client: {e}")
                
                print("[System] Portal closed.") 
                input("Press Enter...")

            # --- B. REGISTERED USER (LOGIN) ---
            elif is_reg == 'y':
                print("\n🔐 --- SECURE LOGIN ---")
                if hasattr(mod_client, 'execute_login'):
                    user_session = mod_client.execute_login() # Returns dict
                else:
                    user_session = None

                # LOGIN SUCCESS -> CLIENT ROLE
                if user_session and user_session.get('role') == 'client':
                    client_id = user_session['id']
                    print(f"\n✅ Welcome back, {user_session.get('name', 'Client')}!")
                    
                    # Logic: Pass client_id for registered users
                    if hasattr(mod_client, 'run_client_portal'):
                        mod_client.run_client_portal(client_id)
                    
                    
                    print("[System] Portal closed.")
                    input("Press Enter to return...")
                elif user_session:
                    print("\n❌ Access Denied: This account is not a Client.")
                    input("Press Enter...")
                else:
                    print("\n❌ Login failed.")
                    input("Press Enter...")

        # =================================================================
        # 2. STAFF AREA
        # =================================================================
        elif choice == '2':
            if not mod_client:
                print("\n⚠️ Error: Login module missing.")
                input("Enter to return...")
                continue

            print("\n🔐 --- STAFF LOGIN ---")
            user_session = mod_client.execute_login()
            
            if user_session:
                user_id = user_session['id']
                user_role = user_session['role']
                
                print(f"\n✅ Access Granted: {user_role.upper()}")
                
                # --- A. SHIPPER (ESTAFETA) ---
                if user_role == 'estafeta':
                    # Logic: Receives id_worker
                    if mod_delivery and hasattr(mod_delivery, 'main_delivery'):
                        mod_delivery.main_delivery(user_id)
                    else:
                        print("⚠️ Error: mod_delivery or function missing.")

                # --- B. MANAGER (GESTAO) ---
                elif user_role == 'manager':
                    while True:
                        print("\n--- MANAGER MENU ---")
                        print("1. Order Management (Gestão de Pedidos)")
                        print("2. Product Management (Gestão de Produtos)")
                        print("0. Back")
                        m_choice = input("👉 Select: ")

                        if m_choice == '1':
                            # Logic: Receives id_worker
                            if mod_order_gestao and hasattr(mod_order_gestao, 'ModOrderGestao'):
                                mod_order_gestao.ModOrderGestao(user_id)
                            else:
                                print("⚠️ Error: Order module missing.")

                        elif m_choice == '2':
                            # Logic: NO PARAMETERS for Product
                            if mod_product and hasattr(mod_product, 'main_product'):
                                mod_product.main_product() 
                            else:
                                print("⚠️ Error: Product module missing.")
                        
                        elif m_choice == '0':
                            break
                
                else:
                    print(f"❌ Role '{user_role}' not supported.")
                
                input("Press Enter to return...")
            else:
                print("\n❌ Login failed.")
                input("Press Enter...")

        else:
            print("\n❌ Invalid selection.")
            input("Press Enter...")

if __name__ == "__main__":
    main()