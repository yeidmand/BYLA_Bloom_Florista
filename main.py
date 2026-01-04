import os
import sys

try:
    import mod_client
except ImportError:
    print("❌ Critical Error: Missing file 'mod_client.py'")
    mod_client = None

try:
    import mod_delivery
except ImportError:
    print("❌ Critical Error: Missing file 'mod_delivery.py'")
    mod_delivery = None

try:
    import mod_order_gestao
except ImportError:
    print("❌ Critical Error: Missing file 'mod_order_gestao.py'")
    mod_order_gestao = None


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
                print("\n⚠️ Cannot run: 'mod_client.py' is missing.")
                input("Enter to return...")
                continue

            print("\n" + "-"*30)
            print("❓ Are you already registered?")
            print("   y: Yes (Login)")
            print("   n: No (Register)")
            is_reg = input("👉 Select (y/n): ").lower().strip()

            # --- A. (NEW USER) ---
            if is_reg == 'n':
                print("\n[System] Opening Registration...")
                
                # CHECK 1:  'run_client_portal' is existed?
                if hasattr(mod_client, 'run_client_portal'):
                    try:
                        mod_client.run_client_portal("")
                    except Exception as e:
                        print(f"❌ Runtime Error in mod_client: {e}")
                else:
                    print("⚠️ Error: Function 'run_client_portal' NOT FOUND in mod_client.py")
                
                print("[System] Portal closed.") 
                input("Press Enter...")

            # --- B. (LOGIN) ---
            elif is_reg == 'y':
                print("\n🔐 --- SECURE LOGIN ---")
                
                # CHECK 2:  'execute_login' is existed ?
                if hasattr(mod_client, 'execute_login'):
                    try:
                        user_session = mod_client.execute_login()
                    except Exception as e:
                        print(f"❌ Runtime Error in Login: {e}")
                        user_session = None
                else:
                    print("⚠️ Error: Function 'execute_login' NOT FOUND in mod_client.py")
                    user_session = None

                # Process the LOGIN results
                if user_session and user_session.get('role') == 'client':
                    client_id = user_session['id']
                    print(f"\n✅ Welcome back, {user_session.get('name', 'Client')}!")
                    
                    # CHECK 3: Gọi lại Portal với ID
                    if hasattr(mod_client, 'run_client_portal'):
                        try:
                            mod_client.run_client_portal(client_id)
                        except Exception as e:
                            print(f"❌ Runtime Error inside Client Menu: {e}")
                    else:
                        print("⚠️ Error: Function 'run_client_portal' missing.")
                    
                    input("Press Enter to return...")
                elif user_session:
                    print("\n❌ Access Denied: This account is not a Client.")
                    input("Press Enter...")
                else:
                    print("\n❌ Login failed or cancelled.")
                    input("Press Enter...")

        # =================================================================
        # 2. STAFF AREA
        # =================================================================
        elif choice == '2':
            if not mod_client:
                print("\n⚠️ Cannot login: 'mod_client.py' is missing.")
                input("Enter to return...")
                continue

            print("\n🔐 --- STAFF LOGIN ---")
            
            # CHECK Login
            if hasattr(mod_client, 'execute_login'):
                user_session = mod_client.execute_login()
            else:
                print("⚠️ Error: Function 'execute_login' NOT FOUND.")
                user_session = None
            
            if user_session:
                user_id = user_session['id']
                user_role = user_session['role']
                
                print(f"\n✅ Access Granted: {user_role.upper()}")
                
                # --- SHIPPER (ESTAFETA) ---
                if user_role == 'estafeta':
                    if mod_delivery and hasattr(mod_delivery, 'main_delivery'):
                        try:
                            mod_delivery.main_delivery(user_id)
                        except Exception as e:
                            print(f"❌ Error inside Shipper Module: {e}")
                    else:
                        print("⚠️ Error: Function 'main_delivery' missing in mod_delivery.py")

                # --- MANAGER  ---
                elif user_role == 'manager':
                    
                    if mod_order_gestao and hasattr(mod_order_gestao, 'ModOrderGestao'):
                        try:
                            mod_order_gestao.ModOrderGestao(user_id)
                        except Exception as e:
                            print(f"❌ Error inside Manager Module: {e}")
                    else:
                        print("⚠️ Error: Function 'ModOrderGestao' missing in mod_order_gestao.py")
                
                else:
                    print(f"❌ Role '{user_role}' is not supported yet.")
                
                input("Press Enter to return...")

            else:
                print("\n❌ Login failed!")
                input("Press Enter...")

        # =================================================================
        # INVALID
        # =================================================================
        else:
            print("\n❌ Invalid selection.")
            input("Press Enter...")

if __name__ == "__main__":
    main()