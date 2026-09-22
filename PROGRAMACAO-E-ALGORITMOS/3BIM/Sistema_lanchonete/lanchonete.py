"""
    nome: Daniel Boaventura e Pablo
    data: Setembro/2026
    projeto: Lanchonete
"""

import json
import os

products = []
orders = []

def load_data():
    if os.path.exists("lanchonete_dados.json"):
        with open("lanchonete_dados.json", "r") as arquivo:
            dados = json.load(arquivo)
            products.extend(dados.get("products", []))
            orders.extend(dados.get("orders", []))



def save_data():
    with open("lanchonete_dados.json", "w") as arquivo:
        dados = {
             "products": products,
             "orders": orders
        }
        json.dump(dados, arquivo, indent=4)


load_data()



def register_product():
    code = input("Digite o codigo do produto: ")
    name = input("Digite o nome do produto: ")
    price = float(input("Digite o preço do produto: "))
    stock = int(input("Digite a quantidade do estoque: "))

    new_product = {
    "code": code,
    "name": name,
    "price": price,
    "stock": stock
}
    products.append(new_product)
    save_data()



def list_products():
    print("--- PRODUTOS CADASTRADOS ---")

    for product in products:
        print(
            f"Codigo: {product['code']} | "
            f"Nome: {product['name']} | "
            f"Preco: R$ {product['price']:.2f} | "
            f"Estoque: {product['stock']}"
        )

def make_order():
    customer_name = input("Qual o nome do cliente: ")
    code = input("Qual o codigo do produto: ")
    product_found = None

    for product in products:
     if product["code"] == code:
        product_found = product
        break
     
    if product_found is None:
        print("Produto não encontrado.")
        return
    
    quantity = int(input("Digite a quantidade: "))
    
    if quantity > product_found["stock"]:
        print("Estoque insuficiente.")

        return
    
    total = quantity * product_found["price"]
    product_found["stock"] -= quantity

    order = {
        "customer_name": customer_name,
        "product_code": product_found["code"],"product_name": product_found["name"],
"quantity": quantity,
"total": total
}
    

    "product_code": product_found["code"],
"product_name": product_found["name"],
"quantity": quantity,
"total": total
}


