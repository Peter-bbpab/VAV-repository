import json
import os
import csv
import shutil
from datetime import date

DATA_FILE = "lanchonete_dados.json"

products = []
orders = []


def load_data():
    global products, orders

    if not os.path.exists(DATA_FILE):
        products = []
        orders = []
        return

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        products = data.get("products", [])
        orders = data.get("orders", [])


def save_data():
    data = {
        "products": products,
        "orders": orders
    }

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def register_product():
    code = input("Código do produto: ")

    if find_product_by_code(code) is not None:
        print("Já existe um produto com este código.")
        return

    name = input("Nome do produto: ")
    price = float(input("Preço do produto: "))
    stock = int(input("Quantidade em estoque: "))

    product = {
        "code": code,
        "name": name,
        "price": price,
        "stock": stock
    }

    products.append(product)
    save_data()

    print("Produto cadastrado com sucesso!")


def list_products():
    if len(products) == 0:
        print("Nenhum produto cadastrado.")
        return

    print("\n--- Produtos cadastrados ---")
    for product in products:
        print(f"Código: {product['code']}")
        print(f"Nome: {product['name']}")
        print(f"Preço: R$ {product['price']:.2f}")
        print(f"Estoque: {product['stock']}")
        print("-" * 30)


def find_product_by_code(code):
    for product in products:
        if product["code"] == code:
            return product
    return None


def make_order():
    if len(products) == 0:
        print("Nenhum produto cadastrado.")
        return

    customer_name = input("Nome do cliente: ")

    list_products()

    code = input("Digite o código do produto: ")
    product = find_product_by_code(code)

    if product is None:
        print("Produto não encontrado.")
        return

    quantity = int(input("Quantidade desejada: "))

    if quantity <= 0:
        print("Quantidade inválida.")
        return

    if quantity > product["stock"]:
        print("Estoque insuficiente.")
        return

    total = quantity * product["price"]
    product["stock"] -= quantity

    order = {
        "customer_name": customer_name,
        "product_code": product["code"],
        "product_name": product["name"],
        "quantity": quantity,
        "total": total,
        "date": date.today().isoformat()
    }

    orders.append(order)
    save_data()

    print("Pedido realizado com sucesso!")
    print(f"Total: R$ {total:.2f}")


def list_orders():
    if len(orders) == 0:
        print("Nenhum pedido realizado.")
        return

    print("\n--- Pedidos realizados ---")
    for order in orders:
        print(f"Cliente: {order['customer_name']}")
        print(f"Produto: {order['product_name']}")
        print(f"Quantidade: {order['quantity']}")
        print(f"Total: R$ {order['total']:.2f}")
        print(f"Data: {order.get('date', 'Não informada')}")
        print("-" * 30)


def change_price():
    if len(products) == 0:
        print("Nenhum produto cadastrado.")
        return

    list_products()
    product_name = input("Qual o nome do produto que você quer mudar o valor?: ")

    for product in products:
        if product["name"].lower() == product_name.lower():
            new_value = float(input("Digite o novo valor deste produto: "))
            product["price"] = new_value
            save_data()

            print("Valor alterado com sucesso!")
            return

    print("Produto não encontrado.")


def remove_product():
    if len(products) == 0:
        print("Nenhum produto cadastrado.")
        return

    list_products()
    product_code = input("Qual produto deseja excluir: ")

    for product in products:
        if product["code"] == product_code:
            products.remove(product)
            save_data()

            print("Produto removido com sucesso!")
            return

    print("Produto não encontrado.")


def shearch_product():
    if len(products) == 0:
        print("Nenhum produto cadastrado.")
        return

    list_products()

    product_name = input("Qual produto deseja buscar: ")

    for product in products:
        if product["name"].lower() == product_name.lower():
            print(
                "O produto",
                product["name"],
                "existe e ainda possui",
                product["stock"],
                "unidades."
            )
            return

    print("Produto não encontrado.")


def sales_report():
    if len(orders) == 0:
        print("Nenhuma venda realizada.")
        return

    total_vendas = 0

    print("Relatório de vendas")

    for order in orders:
        print(f"Produto: {order['product_name']}")
        print(f"Quantidade vendida: {order['quantity']}")
        print(f"Total: R$ {order['total']:.2f}")
        print(f"Data: {order.get('date', 'Não informada')}")
        print("-" * 30)

        total_vendas += order["total"]

    print(f"Valor total vendido: R$ {total_vendas:.2f}")


def best_selling_product():
    if len(orders) == 0:
        print("Nenhuma venda realizada.")
        return

    sales_by_product = {}

    for order in orders:
        code = order["product_code"]
        name = order["product_name"]
        quantity = order["quantity"]

        if code in sales_by_product:
            sales_by_product[code]["quantity"] += quantity
        else:
            sales_by_product[code] = {
                "name": name,
                "quantity": quantity
            }

    best_code = max(
        sales_by_product,
        key=lambda code: sales_by_product[code]["quantity"]
    )

    best_product = sales_by_product[best_code]

    print("\n--- Produto mais vendido ---")
    print(f"Produto: {best_product['name']}")
    print(f"Quantidade vendida: {best_product['quantity']}")


def daily_total():
    today = date.today().isoformat()
    total = 0

    for order in orders:
        if order.get("date") == today:
            total += order["total"]

    print("\n--- Total vendido hoje ---")
    print(f"Total: R$ {total:.2f}")


def export_csv():
    if len(orders) == 0:
        print("Nenhuma venda realizada.")
        return

    with open(
        "relatorio_vendas.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "Cliente",
            "Código",
            "Produto",
            "Quantidade",
            "Total",
            "Data"
        ])

        for order in orders:
            writer.writerow([
                order["customer_name"],
                order["product_code"],
                order["product_name"],
                order["quantity"],
                order["total"],
                order.get("date", "")
            ])

    print("Relatório exportado com sucesso!")


def backup_json():
    if not os.path.exists(DATA_FILE):
        print("Arquivo JSON não encontrado.")
        return

    backup_file = "lanchonete_dados_backup.json"

    shutil.copy2(DATA_FILE, backup_file)

    print("Backup criado com sucesso!")


def show_menu():
    print("\n=== Sistema para Lanchonete ===")
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("3 - Fazer pedido")
    print("4 - Ver pedidos realizados")
    print("5 - Mudar preço")
    print("6 - Remover produtos")
    print("7 - Pesquisar produto")
    print("8 - Relatório de vendas")
    print("9 - Produto mais vendido")
    print("10 - Total vendido no dia")
    print("11 - Exportar relatório para CSV")
    print("12 - Criar backup do JSON")
    print("13 - Sair")


def main():
    load_data()

    while True:
        show_menu()
        option = input("Escolha uma opção: ")

        if option == "1":
            register_product()
        elif option == "2":
            list_products()
        elif option == "3":
            make_order()
        elif option == "4":
            list_orders()
        elif option == "5":
            change_price()
        elif option == "6":
            remove_product()
        elif option == "7":
            shearch_product()
        elif option == "8":
            sales_report()
        elif option == "9":
            best_selling_product()
        elif option == "10":
            daily_total()
        elif option == "11":
            export_csv()
        elif option == "12":
            backup_json()
        elif option == "13":
            save_data()
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida.")


main()