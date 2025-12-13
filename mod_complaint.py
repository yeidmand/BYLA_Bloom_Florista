#Tong

import pandas as pd
import data_manager
from datetime import datetime

def process_smart_complaint(current_client_id):
    print("\n" + "="*45)
    print("📢 SMART COMPLAINT REGISTRATION SYSTEM")
    print("="*45)


    df_orders = data_manager.load_orders()
    df_complaints = data_manager.load_complaints()

    
    order_id = input("👉 Enter Order ID: ").strip()
    order_pedido = df_orders[df_orders['order_id'] == order_id]

    
    if order_pedido.empty:
        print(f"❌ Error: Order ID '{order_id}' not found.")
        return

    
    if order_pedido.iloc[0]['id_client'] != current_client_id:
        print("❌ Error: You cannot report another person's order.")
        return

    
    history = df_complaints[df_complaints['order_id'] == order_id]
    if not history.empty:
        print(f"⚠️ Notice: You already have {len(history)} active complaint(s) for this order.")
        confirm = input("Submit another one? (y/n): ").lower()
        if confirm != 'y': return

    
    current_status = order_pedido.iloc[0]['status']

    shipper_id_from_order = order_pedido.iloc[0]['id_worker']


    if pd.isna(shipper_id_from_order) or shipper_id_from_order == "":
        accused_shipper = "Unknown"
    else:
        accused_shipper = shipper_id_from_order


    
    print("\n🔻 Please select a reason:")
    print("   1. Late Delivery (Not Received yet)") 
    print("   2. Damaged Product")
    print("   3. Wrong Item Delivered")
    print("   4. Rude Shipper")
    print("   5. Other")
    
    choice = input("👉 Select (1-5): ")

    reason_type = "Other"
    priority = "Normal"


    if choice == "1":
        reason_type = "Late Delivery"
        
        if current_status == "Pending":
            priority = "High" 
        else:
            priority = "Normal"
            
    elif choice == "2":
        reason_type = "Damaged Product"
        priority = "URGENT"
        
    elif choice == "3":
        reason_type = "Wrong Item"
        priority = "High"
        
    elif choice == "4":
        reason_type = "Shipper Issue"
        priority = "Medium"
        
    elif choice == "5": 
        reason_type = "Other Reason"
        priority = "Low"

    
    detail = input(f"👉 Please provide details for '{reason_type}': ")


    new_complaint = {
        "order_id": order_id,
        "client_id": current_client_id,
        "accused_shipper": accused_shipper,
        "reason_type": reason_type,
        "priority": priority,
        "content": detail,
        "date_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Open"
    }

    df_complaints = pd.concat([df_complaints, pd.DataFrame([new_complaint])], ignore_index=True)
    data_manager.save_complaints(df_complaints)

    print("\n" + "-"*45)
    print("✅ COMPLAINT RECORDED!")
    print(f"🔖 Priority Level: [{priority}]")
    print(f"🕒 Timestamp: {new_complaint['date_created']}")
    print("-" * 45)