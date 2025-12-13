def optionVerify(option, options_list):
    """
    Verifies if the given option is in the list of valid options.

    Parameters:
    option (str): The option to verify.
    options_list (list): The list of valid options.

    Returns:
    bool: True if the option is valid, False otherwise.
    """
    return option in options_list

def showDetailsOrder(order_details, order_it, products_df):
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

    marged_items = order_it.merge(products_df[["product_id","name_product"]], on='product_id', how='left')
    print("\n=== Itens do Pedido ===")
    for _, item in marged_items.iterrows():
        print(f"Produto: {item['name_product']} | Quantidade: {item['quantity']}")
    return