import pandas as pd

def showDetailsOrder(order_details, order_items_df, products_df):
    """
    Muestra los detalles de un solo pedido, incluyendo la lista de productos
    con sus nombres (en lugar de IDs).

    Parameters:
    order_details (DataFrame): DataFrame de una sola fila con los datos del pedido.
    order_items_df (DataFrame): DataFrame con los artículos filtrados para ese pedido.
    products_df (DataFrame): DataFrame completo con la información de los productos.
    """
    if order_details.empty:
        print("Erro: Detalhes do pedido não encontrados.")
        return

    # Parte de los detalles del pedido
    print("=== Detalhes do Pedido ===")
    details = {"Numero do Pedido": order_details.iloc[0]['order_id'],
                "Nome do Cliente": order_details.iloc[0]['name'],
                "Contacto": order_details.iloc[0]['contact'],
                "Morada": order_details.iloc[0]['address'],
                "Codigo Postal": f"{order_details.iloc[0]['ZP1']}-{order_details.iloc[0]['ZP2']}",
                "Estado do Pedido": order_details.iloc[0]['order_status'],
                }
    for key, value in details.items():
        print(f"{key}: {value}")

    # Parte de los artículos - Realizar el merge para obtener el nombre del producto
    merged_items = order_items_df.merge(
        products_df[["product_id", "name_product"]],
        on='product_id',
        how='left'
    )

    print("\n=== Itens do Pedido ===")
    if merged_items.empty:
        print("Nenhum item encontrado para este pedido.")
    else:
        # Iterar sobre los artículos y mostrarlos con el nombre del producto
        for _, item in merged_items.iterrows():
            product_name = item['name_product'] if pd.notna(item['name_product']) else f"Produto ID: {item['product_id']} (Nome não encontrado)"
            print(f"Produto: {product_name} | Quantidade: {item['quantity_ordered']} | Preço Unitário: {item['price_unit']} | Subtotal: {item['subtotal']}")

def showOrderStatus(df_orders):
    print("\n=== Encomendas ===")
    for _, row in df_orders.iterrows():
        print(f"ID: {row['order_id']} | Estado: {row['order_status']}")
    return

def validoption(choice, valid_options):
    return choice in valid_options

def showDetailsDestinatario(order_details):
    if order_details.empty:
        print("Erro: Detalhes do pedido não encontrados.")
        return

    print("\n=== Detalhes do Destinatário ===")
    details = {"Nome do Destinatário": order_details.iloc[0]['name'],
                "Contacto": order_details.iloc[0]['contact'],
                "Morada": order_details.iloc[0]['address'],
                "Codigo Postal": f"{order_details.iloc[0]['ZP1']}-{order_details.iloc[0]['ZP2']}",
                }
    for key, value in details.items():
        print(f"{key}: {value}")