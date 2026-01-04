import os
import sys

import mod_client           # Login & Client Portal
import mod_delivery         # Courier Portal
import mod_order_gestao     # Order Management
import mod_product          # Product Management

def clear():
    """Clear terminal screen"""
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
            print("\n👋 Goodbye!")
            break

        # =================================================================
        # 1. CLIENT AREA (CUSTOMER)
        # =================================================================
        elif choice == '1':
            print("\n" + "-"*30)
            print("❓ Are you already registered?")
            print("   y: Yes (Login)")
            print("   n: No (New Customer)")
            is_reg = input("👉 Select (y/n): ").lower().strip()

            # --- CASE A: NOT REGISTERED -> Call with empty ID "" ---
            if is_reg == 'n':
                print("\n[System] Opening Client Portal (New User)...")
                # "Not registered -> call customer function with empty id_client"
                mod_client.run_client_portal("") 
                
                print("[System] Portal closed.") 
                input("Press Enter...")

            # --- CASE B: REGISTERED -> Verify Pass -> Call with ID ---
            elif is_reg == 'y':
                print("\n🔐 --- CLIENT LOGIN ---")
                
                # "Registered -> verify password & phone -> get id_client"
                # (Def execute_login of mod_client do the checking pass/phone)
                user_session = mod_client.execute_login()

                if user_session and user_session.get('role') == 'client':
                    client_id = user_session['id']
                    print(f"\n✅ Welcome back, {user_session.get('name', 'Client')}!")
                    
                    # "Call customer function" (with ID)
                    mod_client.run_client_portal(client_id)
                    
                    print("[System] Portal closed.")
                    input("Press Enter...")
                else:
                    print("\n❌ Login failed or Account is not a Client.")
                    input("Press Enter...")

        # =================================================================
        # 2. STAFF AREA (SHIPPER / MANAGER)
        # =================================================================
        elif choice == '2':
            print("\n🔐 --- STAFF LOGIN ---")
            
            # 1. Call Login to take Role
            user_session = mod_client.execute_login()
            
            if user_session:
                user_id = user_session['id']
                user_role = user_session['role']
                
                print(f"\n✅ Access Granted: {user_role.upper()}")

                # --- SHIPPER (COURIER) ---
                if user_role == 'estafeta':
                    # "Call courier function (for now just print...)"
                    
                    print(f"🚀 Launching Courier Portal for ID: {user_id}")
                    mod_delivery.main_delivery(user_id)

                # --- MANAGER ---
                elif user_role == 'manager':
                    # "Check which manager -> call correct portal"
        
                    while True:
                        print("\n📊 --- MANAGER DASHBOARD ---")
                        print("1. Order Management (Gestão de Pedidos)")
                        print("2. Product Management (Gestão de Produtos)")
                        print("0. Log out")
                        m_choice = input("👉 Select: ")

                        if m_choice == '1':
                            mod_order_gestao.ModOrderGestao(user_id)
                        elif m_choice == '2':
                            mod_product.main_product()
                        elif m_choice == '0':
                            break
                        else:
                            print("❌ Invalid option.")
                
                else:
                    print(f"❌ Unknown Role: {user_role}")
                
                input("Press Enter to return...")

            else:
                print("\n❌ Login failed.")
                input("Press Enter...")

        else:
            print("\n❌ Invalid selection.")
            input("Press Enter...")

if __name__ == "__main__":
    main()