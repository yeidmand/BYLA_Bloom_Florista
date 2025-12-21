#Luís - Versão refatorada com Pandas e CSV

import pandas as pd
from data_manager import load_products, save_products


def generate_next_product_id(df):
    """Gera o próximo ID de produto disponível"""
    if df.empty:
        return "2001"
    max_id = df["product_id"].astype(int).max()
    return str(max_id + 1)


def adicionarProduto(df):
    """Adiciona um novo produto ao catálogo e guarda no CSV (21/12)."""
    print("Adicionar Novo Produto: \n")
    
    # Recolher dados utilizando funções de validação existentes
    nome = validarNome()
    
    print("Insira a descrição do produto: ")
    descricao = input()
    while len(descricao) == 0:
        print("Erro: Descrição tem que ter mais que 1 carater!")
        descricao = input("Insira a descrição: ")
    
    print("Insira a categoria: ")
    categoria = input()
    while len(categoria) == 0:
        print("Erro: Categoria tem que ter mais que 1 carater!")
        categoria = input("Insira a categoria: ")
    
    preco = verificarPreco()
    stock = validarStock()
    disponibilidade = verificarDisponibilidade(1)
    
    # Criar novo produto
    product_id = generate_next_product_id(df)
    novo_produto = pd.DataFrame([{
        "product_id": product_id,
        "name_product": nome,
        "description": descricao,
        "category": categoria,
        "quantity_stock": stock,
        "price_unit": preco,
        "available": disponibilidade
    }])
    
    df = pd.concat([df, novo_produto], ignore_index=True)
    
    # Guardar no CSV
    save_products(df)
    
    # Confirmação dos dados do produto adicionado
    print("\n Produto adicionado com sucesso! ✅")
    print("\n")
    print("ID: " + product_id)
    print("Nome: " + nome)
    print("Categoria: " + categoria)
    print("Preço: " + str(preco) + "€")
    print("Stock: " + str(stock) + " unidades")
    print("\n")
    
    return df


def alterarProduto(df):
    """Permite alterar dados de um produto (16/12)"""
    # NOTA: O stock não é alterado aqui para garantir a integridade das opções 6 e 7 (Saídas/Entradas)
    opcaomenu = -1

    if len(df) > 0:
        print("Insira o ID do produto que pretende alterar: ")
        product_id = input()

        # Verificar se o ID existe
        if product_id not in df["product_id"].values:
            print("❌ ID de Produto Inválido!")
            return df
        
        # Obter o índice do produto
        idx = df[df["product_id"] == product_id].index[0]
        produto = df.loc[idx]

        # Mostrar produto selecionado
        print("\n--- Produto Selecionado ---")
        print("ID: " + str(produto["product_id"]))
        print("Nome: " + produto["name_product"])
        print("Descrição: " + produto["description"])
        print("Categoria: " + produto["category"])
        print("Preço: " + str(produto["price_unit"]) + "€")
        print("Stock: " + str(produto["quantity_stock"]) + " unidades")
        print("Disponibilidade: " + produto["available"])
        print("---------------------------\n")

        while opcaomenu != 0:
            # Menu de opções
            print("\nEscolha, através do número, o que deseja alterar:")
            print("1. Alterar Nome")
            print("2. Alterar Descrição")
            print("3. Alterar Categoria")
            print("4. Alterar Preço")
            print("5. Alterar Disponibilidade")
            print("0. Concluir Alterações")

            opcaomenu = int(input())

            if opcaomenu == 1:
                df.at[idx, "name_product"] = validarNome()
                print("Nome alterado com sucesso!")
            elif opcaomenu == 2:
                print("Insira a nova Descrição: ")
                novaDescricao = input()
                while len(novaDescricao) == 0:
                    print("Erro: Descrição tem que ter mais que 1 carater!")
                    print("Insira a nova Descrição: ")
                    novaDescricao = input()
                df.at[idx, "description"] = novaDescricao
                print("Descrição alterada com sucesso!")
            elif opcaomenu == 3:
                print("Escreva nova categoria: ")
                novaCategoria = input()
                while len(novaCategoria) == 0:
                    print("Erro: Categoria tem que ter mais que 1 carater!")
                    print("Escreva nova categoria: ")
                    novaCategoria = input()
                df.at[idx, "category"] = novaCategoria
                print("Categoria alterada com sucessso!")
            elif opcaomenu == 4:
                df.at[idx, "price_unit"] = verificarPreco()
                print("Preço alterado com sucessso!")
            elif opcaomenu == 5:
                df.at[idx, "available"] = verificarDisponibilidade(1)
                print("Disponibilidade alterada com sucessso!")
            elif opcaomenu == 0:
                print("Alterações Concluidas!")
                # Guardar alterações no CSV
                save_products(df)
    else:
        print("O Catálogo está vazio!")
    
    return df


def filtrarCatalogo(df):
    """Filtra o catálogo por diferentes critérios"""
    opcao = -1
    if len(df) > 0:
        while opcao != 0:
            resultadoFiltro = False
            print("| Filtrar o catálogo: | " + chr(13) + "1 - Por Categoria" + chr(13) + "2 - Por Disponibilidade" + chr(13) + "3 - Por Preço" + chr(13) + "4 - Por Stock" + chr(13) + "0 - Menu Principal")
            opcao = int(input())
            
            if opcao == 1:
                print("Insira a categoria pela qual deseja filtrar: ")
                filtroCategoria = input()
                while len(filtroCategoria) == 0:
                    print("A categoria não pode ser vazia. Tente de novo:")
                    filtroCategoria = input()
                
                filtered = df[df["category"] == filtroCategoria]
                for _, row in filtered.iterrows():
                    print(f"ID: {row['product_id']} | Nome: {row['name_product']} | Categoria: {row['category']}")
                    resultadoFiltro = True
                
                if not resultadoFiltro:
                    print("❌ Não foi encontrado nenhum produto!")
                    
            elif opcao == 2:
                filtroDisponibilidade = verificarDisponibilidade(2)
                filtered = df[df["available"] == filtroDisponibilidade]
                
                for _, row in filtered.iterrows():
                    if row["available"] == "N" and row["quantity_stock"] == 0:
                        print(f"ID: {row['product_id']} | Nome: {row['name_product']} | Disponibilidade: {row['available']} está esgotado!")
                    else:
                        print(f"ID: {row['product_id']} | Nome: {row['name_product']} | Disponibilidade: {row['available']}")
                    resultadoFiltro = True
                
                if not resultadoFiltro:
                    print("❌ Não foi encontrado nenhum produto!")
                    
            elif opcao == 3:
                print("Filtrar Preço:" + chr(13) + "1. Preço igual a: " + chr(13) + "2. Preço acima de: " + chr(13) + "3.  Preço abaixo de: ")
                opcaoPreco = int(input())
                
                if opcaoPreco >= 1 and opcaoPreco <= 3:
                    filtroPreco = verificarPreco()
                    if opcaoPreco == 1:
                        filtered = df[df["price_unit"] == filtroPreco]
                    elif opcaoPreco == 2:
                        filtered = df[df["price_unit"] > filtroPreco]
                    elif opcaoPreco == 3:
                        filtered = df[df["price_unit"] < filtroPreco]
                    
                    for _, row in filtered.iterrows():
                        print(f"ID: {row['product_id']} | Nome: {row['name_product']} | Preço: €{row['price_unit']}")
                        resultadoFiltro = True
                    
                    if not resultadoFiltro:
                        print("❌ Não foi encontrado nenhum produto!")
                else:
                    print("Opção inválida!")
                    
            elif opcao == 4:
                print("Filtrar Stock:" + chr(13) + "1. Stock igual a: " + chr(13) + "2. Stock acima de: " + chr(13) + "3.  Stock abaixo de: ")
                opcaoStock = int(input())
                
                if opcaoStock >= 1 and opcaoStock <= 3:
                    filtroStock = validarStock()
                    if opcaoStock == 1:
                        filtered = df[df["quantity_stock"] == filtroStock]
                    elif opcaoStock == 2:
                        filtered = df[df["quantity_stock"] > filtroStock]
                    elif opcaoStock == 3:
                        filtered = df[df["quantity_stock"] < filtroStock]
                    
                    for _, row in filtered.iterrows():
                        print(f"ID: {row['product_id']} | Nome: {row['name_product']} | Stock: {row['quantity_stock']}")
                        resultadoFiltro = True
                    
                    if not resultadoFiltro:
                        print("❌ Não foi encontrado nenhum produto!")
                else:
                    print("❌ Opção inválida!")
                    
            elif opcao == 0:
                print("Menu Principal")
            else:
                print("❌ Opção introduzida é inválida!")
    else:
        print("Catálogo Vazio. Impossível filtrar!")


def listarCatalogo(df):
    """Lista todos os produtos do catálogo"""
    print("| Catálogo Atualizado | ")
    
    if len(df) > 0:
        for _, row in df.iterrows():
            print(f"ID: {row['product_id']} | Nome: {row['name_product']} | Descrição: {row['description']} | Categoria: {row['category']} | Preço: {row['price_unit']}€ | Stock: {row['quantity_stock']} | Disponível: {row['available']}")
    else:
        print("Catálogo Vazio")


def novoStock(df):
    """Adiciona stock a um produto existente"""
    if len(df) > 0:
        print("Qual o ID do produto que deseja adicionar Stock: ")
        product_id = input()
        
        # Verificar se o ID existe
        if product_id not in df["product_id"].values:
            print("ID/Nº Artigo Inválido!")
            return df
        
        idx = df[df["product_id"] == product_id].index[0]
        produto = df.loc[idx]
        
        print(f"Está a alterar o stock do Produto: {produto['name_product']} | Stock Atual: {produto['quantity_stock']}")
        quantidadeInserida = validarStock()
        
        if quantidadeInserida > 0:
            df.at[idx, "quantity_stock"] = produto["quantity_stock"] + quantidadeInserida
            if df.at[idx, "quantity_stock"] > 0:
                df.at[idx, "available"] = "S"
            
            # Guardar no CSV
            save_products(df)
            
            print(f"✅ Stock adicionado com sucesso! Stock Atualizado: {df.at[idx, 'quantity_stock']}")
        else:
            print("Stock inserido tem que ser superior a 0!")
    else:
        print("Catálogo Vazio. Não existe stock!")
    
    return df


def removerProduto(df):
    """Remove um produto do catálogo (20/12)."""
    if len(df) > 0:
        print("Insira o ID do produto a remover: ")
        product_id = input()
        
        # Verificar se o ID existe
        if product_id not in df["product_id"].values:
            print("❌ ID inválido!")
            return df
        
        idx = df[df["product_id"] == product_id].index[0]
        produto = df.loc[idx]
        
        # Mostrar produto a remover
        print("\n⚠️  Vai remover o seguinte produto:")
        print("--- Produto a Remover ---")
        print(f"ID: {produto['product_id']}")
        print(f"Nome: {produto['name_product']}")
        print(f"Descrição: {produto['description']}")
        print(f"Categoria: {produto['category']}")
        print(f"Preço: {produto['price_unit']}€")
        print(f"Stock: {produto['quantity_stock']} unidades")
        print("-------------------------\n")
        
        # Pedir confirmação
        print("Tem a certeza que deseja remover? (S/N): ")
        confirmacao = input()
        
        if confirmacao.upper() == "S":
            # Remover produto do DataFrame
            df = df.drop(idx).reset_index(drop=True)
            
            # Guardar no CSV
            save_products(df)
            
            print("🗑️  Produto removido com sucesso!")
        else:
            print("Operação cancelada.")
    else:
        print("❌ O Catálogo está vazio!")
    
    return df


def validarNome():
    """Valida e retorna o nome do produto"""
    print("Insira nome do Produto: ")
    nome = input()
    while len(nome) == 0:
        print("Erro: Nome tem que ter mais que 1 carater!")
        print("Insira nome do Produto: ")
        nome = input()
    return nome


def validarStock():
    """Função para validar Stock inserido (evitar negativos)"""
    print("Insira a quantidade de produto para stock: ")
    stock = int(input())
    while stock < 0:
        print("Erro: O stock do produto não pode ser negativo! Volte a inserir, por favor!")
        stock = int(input())
    return stock


def verificarDisponibilidade(opcaoOperacao):
    """Função que muda a pergunta consoante o parametro (1, 2, 3)"""
    disponibilidade = ""
    
    if opcaoOperacao == 1:
        print("Informe se está disponível(S/N): ")
    elif opcaoOperacao == 2:
        print("Disponibilidade desejada (S - Disponível / N - Indisponível): ")
    elif opcaoOperacao == 3:
        print("⚠️ Tem a certeza que deseja remover o produto(S/N)?")
    
    disponibilidade = input()
    while disponibilidade != "S" and disponibilidade != "N":
        print("Erro: Opção inválida. Insira apenas 'S' ou 'N': ")
        disponibilidade = input()
    
    return disponibilidade


def verificarEncomenda(df):
    """Simula uma encomenda/saída de stock"""
    if len(df) > 0:
        print("| Catálogo !")
        for _, row in df.iterrows():
            print(f"ID: {row['product_id']} | Nome: {row['name_product']} | Preço: {row['price_unit']}€ | Stock: {row['quantity_stock']}")
        
        print("Qual o ID do produto que deseja encomendar: ")
        product_id = input()
        
        if product_id not in df["product_id"].values:
            print("ID/Nº Artigo Inválido!")
            return df
        
        idx = df[df["product_id"] == product_id].index[0]
        produto = df.loc[idx]
        
        if produto["quantity_stock"] == 0:
            print("❌ Sem stock!" + chr(13) + "Produto indisponível de momento!")
        else:
            print("Insira a quantidade a encomendar: ")
            encomenda = int(input())
            while encomenda <= 0:
                print("Quantidade tem que ser superior a 0!")
                print("Insira a quantidade a encomendar: ")
                encomenda = int(input())
            
            if encomenda <= produto["quantity_stock"]:
                df.at[idx, "quantity_stock"] = produto["quantity_stock"] - encomenda
                
                # Guardar no CSV
                save_products(df)
                
                print("✅ Produto encomendado!")
                
                # Previne que produtos esgotados apareçam como disponíveis
                if df.at[idx, "quantity_stock"] == 0:
                    df.at[idx, "available"] = "N"
                    save_products(df)
                    print("⚠️ Produto selecionado esgotou!")
            else:
                print("❌ Produto Indisponivel/Sem Stock suficiente!")
    else:
        print("Catálogo Vazio. Não existe stock!")
    
    return df


def verificarEstatisticas(df):
    """Mostra estatísticas do catálogo"""
    if len(df) > 0:
        disponivel = len(df[df["available"] == "S"])
        esgotado = len(df[(df["quantity_stock"] == 0) | (df["available"] == "N")])
        total = (df["quantity_stock"] * df["price_unit"]).sum()
        
        print(f"Total de Itens: {len(df)}")
        print(f"Produtos Disponíveis: {disponivel}")
        print(f"Produtos Esgotados: {esgotado}")
        print(f"Valor em Stock: {total}€")
    else:
        print("Catálogo Vazio. Não é possível fornecer estatísticas")


def verificarPreco():
    """Função para validar preço inserido"""
    print("Insira o Preço: ")
    preco = float(input())
    while preco < 0:
        print("Erro: O Preço do produto não pode ser negativo! Volte a inserir, por favor!")
        preco = float(input())
    return preco


# Main (se executado diretamente)
if __name__ == "__main__":
    # Carregar produtos do CSV
    df_produtos = load_products()
    
    # Controla a execução do menu principal
    opcaoMenu = -1
    
    # Mantém o programa a correr até o utilizador escolher 0
    while opcaoMenu != 0:
        # Menu Gestor
        print("🌻 ===== Portal Gestor Florista ===== 🌻")
        print("1. Adicionar Produto ➕")
        print("2. Alterar Produto 📝")
        print("3. Remover Produto ❌")
        print("4. Listar Catálogo 📋")
        print("5. Filtrar Catálogo 🔍")
        print("6. Fazer Encomenda 📤")
        print("7. Adicionar Stock 📥")
        print("8. Ver estatisticas 📈")
        print("0. Sair 👋")
        print()
        
        opcaoMenu = int(input("Escolha uma opção: "))
        
        if opcaoMenu == 1:
            df_produtos = adicionarProduto(df_produtos)
        elif opcaoMenu == 2:
            df_produtos = alterarProduto(df_produtos)
        elif opcaoMenu == 3:
            df_produtos = removerProduto(df_produtos)
        elif opcaoMenu == 4:
            listarCatalogo(df_produtos)
        elif opcaoMenu == 5:
            filtrarCatalogo(df_produtos)
        elif opcaoMenu == 6:
            df_produtos = verificarEncomenda(df_produtos)
        elif opcaoMenu == 7:
            df_produtos = novoStock(df_produtos)
        elif opcaoMenu == 8:
            verificarEstatisticas(df_produtos)
        elif opcaoMenu == 0:
            print("👋 A sair da aplicação...")
        else:
            print("Opção inválida. Insira um número de 0 a 8 e tente novamente.")
