import pandas as pd
import utils as ut

# DataFrame de pedidos
orders_df = pd.DataFrame([
    {"order_id": "PT01", "product_id": 2001, "quantity_ordered": 10, "price_unit": "3,00", "subtotal": "30,00"},
    {"order_id": "PT01", "product_id": 2002, "quantity_ordered": 5, "price_unit": "5,00", "subtotal": "25,00"}
])

# DataFrame de productos
products_df = pd.DataFrame([
    {"product_id": 2001, "name_product": "Flores variadas", "quantity_stock": 250, "price_unit": "3,00"},
    {"product_id": 2002, "name_product": "Rosas", "quantity_stock": 500, "price_unit": "5,00"},
    {"product_id": 2003, "name_product": "Lirios", "quantity_stock": 150, "price_unit": "12,00"},
    {"product_id": 2004, "name_product": "Tuplipas", "quantity_stock": 175, "price_unit": "15,00"},
    {"product_id": 2005, "name_product": "Margaridas", "quantity_stock": 200, "price_unit": "8,00"}
])

# Hacer un merge para obtener el nombre del producto
merged_df = pd.merge(orders_df, products_df[["product_id", "name_product"]], on="product_id", how="left")
print(merged_df)

# Mostrar de manera más legible
for _, row in merged_df.iterrows():
        print(f"  Producto: {row['name_product']}  |  Cantidad: {row['quantity_ordered']}")