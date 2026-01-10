#Luís - mod_product.py - Gestão de Produtos Byla Bloom

#Imports
import os
import pandas as pd 

# Funções de Validação e Input
def lerInteiro(mensagem=""):
    while True: 
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("❌ Erro: Insira apenas números!")

def lerFloat(mensagem=""):
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("❌ Erro: Insira apenas números decimais!")            

def validarTexto(mensagem):
    print(mensagem)
    texto = input()
    while len(texto) == 0:
        print("❌ Erro: Campo não pode estar vazio!")
        print(mensagem)
        texto = input()
    return texto

def validarNome():
    nome = ""
    print("Insira nome do Produto: ")
    nome = input()
    while len(nome) == 0:
        print("Erro: Nome tem que ter mais que 1 carater!")
        print("Insira nome do Produto: ")
        nome = input() 
    return nome

def validarStock():
    stock = lerInteiro("Insira a quantidade de produto para stock: ")
    while stock < 0:
        print("Erro: O stock do produto não pode ser negativo! Volte a inserir, por favor!")
        stock = lerInteiro("Insira a quantidade de produto para stock: ")
    return stock

def verificarPreco():
    preco =lerFloat("Insira o Preço: ")
    while preco < 0:
        print("Erro: O Preço do produto não pode ser negativo! Volte a inserir, por favor!")
        preco =lerFloat("Insira o Preço: ")
    return preco

def verificarDisponibilidade(opcaoOperacao):
    
    disponibilidade = ""

    if opcaoOperacao == 1:
        print("Informe se está disponível(S/N): ")
    elif opcaoOperacao == 2:
        print("Disponibilidade desejada (S - Disponível / N - Indisponível): ")
    elif opcaoOperacao == 3:
        print("⚠️ Tem a certeza que deseja remover o produto(S/N)?")
    disponibilidade = input().upper()  
    
    while disponibilidade != "S" and disponibilidade != "N":
        print("Erro: Opção inválida. Insira apenas 'S' ou 'N': ")
        disponibilidade = input().upper()
    
    return disponibilidade

# Função para validar ID do produto
def validarID():
    while True:
        idEscolhido = input("Insira ID do produto: ").strip()
        if idEscolhido.isdigit():
            id_int = int(idEscolhido)  # ✅ Converter para int
            if id_int in idsProduto:   # ✅ Comparar int com int
                return id_int
        
        print("❌ ID inválido!")
        print(f"IDs disponíveis: {idsProduto}")



# Funções de Leitura/Escrita CSV

tiposProduto = []       
categoriaProduto = []   
descricaoProduto = []  
duracoesProduto = []




def guardarProdutosCSV():
    ativo = ["true" if d == "S" else "false" for d in disponibilidade]
    dados_produtos = {
        "product_id": idsProduto,
        "name_product": nomeProduto,
        "quantity_stock": stock,
        "price_unit": precosProduto,
        "available": ativo,
        "category": categoriaProduto,
        "product_type": tiposProduto,
        "description": descricaoProduto,
        "duracaoPadraoMin": duracoesProduto
    }
    df = pd.DataFrame(dados_produtos)
    df.to_csv("products_stock.csv", index=False, sep=";")
    print("✅ Produtos guardados em products_stock.csv!")


def lerProdutosCSV():
    global numProdutos
    if not os.path.exists("products_stock.csv"):
        print("⚠️ Ficheiro products_stock.csv não encontrado.")
        return 0
    try:
        df = pd.read_csv("products_stock.csv", sep=";")
        # Limpa listas
        idsProduto.clear()
        nomeProduto.clear()
        descricaoProduto.clear()
        categoriaProduto.clear()
        precosProduto.clear()
        stock.clear()
        disponibilidade.clear()
        tiposProduto.clear()
        duracoesProduto.clear()
        
        for i in range(len(df)):
            idsProduto.append(int(df["product_id"][i]))
            nomeProduto.append(str(df["name_product"][i]))
            stock.append(int(df["quantity_stock"][i]))
            precosProduto.append(float(df["price_unit"][i]))
            avail = str(df["available"][i]).strip().lower()
            disponibilidade.append("S" if avail == "true" else "N")
            categoriaProduto.append(str(df["category"][i]))
            tiposProduto.append(str(df["product_type"][i]))
            descricaoProduto.append(str(df["description"][i]))
            duracoesProduto.append(int(df["duracaoPadraoMin"][i]) if "duracaoPadraoMin" in df.columns else 0)

        numProdutos = len(nomeProduto)
        print(f"✅ {numProdutos} itens carregados!")
        return numProdutos
    except Exception as e:
        print(f"❌ Erro ao carregar: {e}")
        return 0

# Funções de Integração (para outros módulos)

# Função para validar stock disponível de um produto (USADO POR: Yeidman (Gestão Encomendas))
def validarStockDisponivel(idItem, quantidade):
    try:
        i = idsProduto.index(int(idItem))

        if disponibilidade[i] != "S":
            print("⚠️ Produto está Indisponível!")
            return False
        
        if stock[i] < quantidade:
            print("⚠️ Stock insuficiente! Disponível: " + str(stock[i]))
            return False
        
        return True

    except ValueError:
        print("⚠️ Produto não foi encontrado!")
        return False

# Função para decrementar Stock após encomenda 
def reservarStock(idItem, quantidade):
    try:
        i = idsProduto.index(int(idItem))

        if stock[i] < quantidade:
            print("❌ Stock insuficiente!")
            return False
        
        stock_antigo = stock[i]
        stock[i] -= quantidade

        if stock[i] == 0:
            disponibilidade[i] = "N"
            print("⚠️ " + nomeProduto[i] + " esgotou!")
        
        print("✅ Stock reservado: " + str(quantidade) + "x " + nomeProduto[i])
        print("   Anterior: " + str(stock_antigo) + " → Novo: " + str(stock[i]))

        guardarProdutosCSV()
        return True

    except ValueError:
        print("❌ Produto não foi encontrado!")
        return False


def devolverStock(idItem, quantidade):
    if quantidade <= 0:
        print("❌ Quantidade inválida para devolução!")
        return False
    
    try:
        i = idsProduto.index(int(idItem))

        stock_antigo = stock[i]
        stock[i] += quantidade

        if stock[i] > 0:
            disponibilidade[i] = "S"
            print("✅ " + nomeProduto[i] + " voltou a ficar disponível!")
        
        print("✅ Stock devolvido: " + str(quantidade) + "x " + nomeProduto[i])
        print("   Anterior: " + str(stock_antigo) + " → Novo: " + str(stock[i]))

        guardarProdutosCSV()
        return True

    except ValueError:
        print("❌ Produto não foi encontrado!")
        return False

            
# Função para listar produtos disponíveis 
def listarProdutosDisponiveis():
    if not os.path.exists("products_stock.csv"):
        print("⚠️ Ficheiro products_stock.csv não foi encontrado!")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv("products_stock.csv", sep=";")
        
        # ✅ Filtrar produtos disponíveis usando boolean direto
        df_disponiveis = df[
            (df["available"] == True) &  # ✅ Compara com boolean
            (df["quantity_stock"] > 0)
        ].copy()
        
        if len(df_disponiveis) > 0:
            print("\nCatálogo de Produtos Disponíveis 🌻")
            
            for idx, row in df_disponiveis.iterrows():
                print(f"\nProduto ID: {row['product_id']}")
                print(f"Nome: {row['name_product']}")
                print(f"Descrição: {row['description']}")
                print(f"Categoria: {row['category']}")
                print(f"Preço: {row['price_unit']}€")
                print(f"Stock: {row['quantity_stock']} unidades")
                print()
            
            print(f"Total disponível: {len(df_disponiveis)} produtos")
        else:
            print("⚠️ Nenhum produto disponível no momento!")
        
        return df_disponiveis[[
            "product_id",
            "name_product", 
            "description",
            "category",
            "price_unit",
            "quantity_stock"
        ]]
        
    except Exception as e:
        print(f"❌ Erro ao listar produtos disponíveis: {e}")
        return pd.DataFrame()

def obterDetalhesProduto(idItem):
    if not os.path.exists("products_stock.csv"):
        print("⚠️ Ficheiro products_stock.csv não foi encontrado!")
        return None
    
    try:
        df = pd.read_csv("products_stock.csv", sep=";")
        numProdutos = len(df)
        
        # Procurar produto pelo ID
        for i in range(numProdutos):
            if str(df["product_id"][i]) == str(idItem):

                detalhes = {
                    "product_id": df["product_id"][i],
                    "product_type": df["product_type"][i],
                    "name_product": df["name_product"][i],
                    "description": df["description"][i],
                    "category": df["category"][i],
                    "price_unit": df["price_unit"][i],
                    "quantity_stock": df["quantity_stock"][i],
                    "available": df["available"][i]
                }
                
                print("\n🌻 ===== Detalhes do Produto ===== 🌻")
                print("\n--- Produto ID: " + str(detalhes["product_id"]) + " ---")
                print("Nome: " + detalhes["name_product"])
                print("Descrição: " + detalhes["description"])
                print("Categoria: " + detalhes["category"])
                print("Preço: " + str(detalhes["price_unit"]) + "€")
                print("Stock: " + str(detalhes["quantity_stock"]) + " unidades")
                
                if str(detalhes["available"]).lower() == "true" and detalhes["quantity_stock"] > 0:                    
                    print("Estado: Disponível ✅")
                elif detalhes["quantity_stock"] == 0:
                    print("Estado: Esgotado ❌")
                else:
                    print("Estado: Indisponível ❌")
                
                print("==========================================\n")
                
                return detalhes
        
        print("⚠️ Produto ID " + str(idItem) + " não foi encontrado!")
        return None
        
    except:
        print("❌ Erro ao obter detalhes do produto!")
        return None

# Funções de Gestão de Produtos 

# Adiciona um novo produto ao catálogo 
def adicionarProduto():

    global numProdutos
    print("Adicionar Novo Produto\n")

    # Gerar ID automático
    novo_id = 1 if not idsProduto else max(idsProduto) + 1
    idsProduto.append(novo_id)
    
    # Recolher dados utilizando funções de validação existentes
    nomeProduto.append(validarNome())
    descricaoProduto.append(validarTexto("Insira a descrição do produto: "))
    categoriaProduto.append(validarTexto("Insira a categoria: "))
    tiposProduto.append("produto")
    duracoesProduto.append(0)
    precosProduto.append(verificarPreco())
    stock.append(validarStock())
    disponibilidade.append(verificarDisponibilidade(1))
    
    # Guardar alterações no ficheiro CSV
    guardarProdutosCSV()
    numProdutos = len(nomeProduto)

    # Confirmação dos dados do produto adicionado
    print("\n Produto adicionado com sucesso! ✅")
    print("\n")
    print("Nome: " + nomeProduto[numProdutos - 1])
    print("Categoria: " + categoriaProduto[numProdutos - 1])
    print("Preço: " + str(precosProduto[numProdutos - 1]) + "€")
    print("Stock: " + str(stock[numProdutos - 1]) + " unidades")
    print("\n")


def alterarProduto():
    global numProdutos

    if numProdutos == 0: 
        print("❌ O Catálogo está vazio!") 
        return
    
    listarCatalogo()
    print("Insira o ID/Nº que pretende alterar: ")
    idEscolhido = validarID()
    i = idsProduto.index(idEscolhido) 

    print("\n--- Produto Selecionado ---")
    print("Nome: " + nomeProduto[i])
    print("Descrição: " + descricaoProduto[i])
    print("Categoria: " + categoriaProduto[i])
    print("Tipo: " + tiposProduto[i])  
    print("Preço: " + str(precosProduto[i]) + "€")
    print("Stock: " + str(stock[i]) + " unidades")
    print("Disponibilidade: " + disponibilidade[i])
    print("---------------------------\n")

    opcaomenu = -1

    while opcaomenu != 0:
        print("\nEscolha, através do número, o que deseja alterar:")
        print("1. Alterar Nome")
        print("2. Alterar Descrição")
        print("3. Alterar Categoria")
        print("4. Alterar Tipo")
        print("5. Alterar Preço")
        print("6. Alterar Disponibilidade")
        print("0. Concluir Alterações")

        opcaomenu = lerInteiro()  

        if opcaomenu == 1:
                nomeProduto[i] = validarNome()
                print("Nome alterado com sucesso!")
        elif opcaomenu == 2:
                descricaoProduto[i] = validarTexto("Insira a nova Descrição: ")
                print("Descrição alterada com sucesso!")
        elif opcaomenu == 3:
                categoriaProduto[i] = validarTexto("Escreva nova categoria: ")
                print("Categoria alterada com sucesso!")
        elif opcaomenu == 4:
                tiposProduto[i] = "produto" 
                print("⚠️ O tipo de produto é fixo: 'produto'.") # nao trabalhamos com serviços
        elif opcaomenu == 5:
                precosProduto[i] = verificarPreco()
                print("Preço alterado com sucesso!")
        elif opcaomenu == 6:
                disponibilidade[i] = verificarDisponibilidade(1)
                print("Disponibilidade alterada com sucesso!")
        elif opcaomenu == 0:
                print("Alterações Concluídas!")
                # Guardar alterações no ficheiro CSV
                guardarProdutosCSV()
                return
        else:
                print("Opção inválida!")

def adicionarStock():
    # Adiciona stock a produto existente 
    
    if numProdutos > 0:
        print("\n📥 ===== Adicionar Stock ===== 📥")
        print("\nInsira o ID do produto para adicionar stock: ")
        idEscolhido = validarID()
        i = idsProduto.index(idEscolhido)

        # Usar múltiplos prints (mais claro que um print com \n múltiplos)
        print("\n--- Produto Selecionado ---")
        print("Nome: " + nomeProduto[i])
        print("Stock atual: " + str(stock[i]) + " unidades")
        print("---------------------------")
        
        quantidade = lerInteiro("Quantidade a adicionar: ")
        
        while quantidade <= 0:
            print("Erro: Quantidade tem que ser superior a 0!")
            quantidade = lerInteiro("Quantidade a adicionar: ")
        
        stockAntigo = stock[i]
        stock[i] = stock[i] + quantidade
        
        print("\n✅ Stock atualizado com sucesso!")
        print("Stock anterior: " + str(stockAntigo) + " unidades")
        print("Quantidade adicionada: " + str(quantidade) + " unidades")
        print("Novo stock: " + str(stock[i]) + " unidades")
        
        # Atualizar disponibilidade se estava esgotado
        if stockAntigo == 0 and disponibilidade[i] == "N":
            disponibilidade[i] = "S"
            print("✅ Produto voltou a ficar disponível!")

        # Guardar alterações no ficheiro CSV
        guardarProdutosCSV()
    else:
        print("❌ Catálogo vazio!")

# Remove um produto do catálogo
def removerProduto():

    global numProdutos
    if numProdutos > 0:
        print("Insira o ID do produto a remover: ")
        idEscolhido = validarID()   
        i = idsProduto.index(idEscolhido)

        print("--- Produto a Remover ---")
        print("ID: " + str(idEscolhido))
        print("Nome: " + nomeProduto[i])
        print("Descrição: " + descricaoProduto[i])
        print("Categoria: " + categoriaProduto[i])
        print("Preço: " + str(precosProduto[i]) + "€")
        print("Stock: " + str(stock[i]) + " unidades")
        print("-------------------------\n")
        
        confirmacao = verificarDisponibilidade(3)
        
        if confirmacao == "S": 
            disponibilidade[i] = "N" 
            numProdutos = len(nomeProduto)
            guardarProdutosCSV()
            print("🗑️  Produto removido com sucesso!")
        else:
            print("Operação cancelada.")
    else:
        print("❌ O Catálogo está vazio!")


def verificarEncomenda():
    
    # Processa encomenda de produto 
    # Melhorias de apresentação e validações.
    
    if numProdutos > 0:
        print("\n📋 ===== Catálogo para Encomenda ===== 📋")
        
        # ✅ Mostra IDs reais
        for i in range(numProdutos):
            print(f"ID: {idsProduto[i]} | Nome: {nomeProduto[i]} | Preço: {precosProduto[i]}€ | Stock: {stock[i]}")
        
        print("\nInsira o ID do produto que deseja encomendar: ")
        idEscolhido = validarID()  
        i = idsProduto.index(idEscolhido)  
        
        # Mostrar produto selecionado
        print("\n--- Produto Selecionado ---")
        print("Nome: " + nomeProduto[i])
        print("Preço: " + str(precosProduto[i]) + "€")
        print("Stock disponível: " + str(stock[i]) + " unidades")
        print("---------------------------")
        
        if stock[i] == 0:
            print("\n❌ Sem stock!")
            print("Produto indisponível de momento!")
        else:
            if disponibilidade[i] == "N":
                print("\n⚠️ Produto marcado como indisponível!")
                print("Não é possível encomendar neste momento.")
            else:
                print("\nInsira a quantidade a encomendar: ")
                encomenda = lerInteiro()

                while encomenda <= 0:
                    print("Erro: Quantidade tem que ser superior a 0!")
                    print("Insira a quantidade a encomendar: ")
                    encomenda = lerInteiro()

                if encomenda <= stock[i]:
                    stock[i] = stock[i] - encomenda
                    print("\n✅ Encomenda realizada com sucesso!")
                    print("Quantidade encomendada: " + str(encomenda) + " unidades")
                    print("Stock restante: " + str(stock[i]) + " unidades")
                    
                    # Atualizar disponibilidade se esgotou
                    if stock[i] == 0:
                        disponibilidade[i] = "N"
                        print("⚠️ Produto esgotou! Marcado como indisponível.")

                    # Guardar alterações no ficheiro CSV
                    guardarProdutosCSV()
                else:
                    print("\n❌ Stock insuficiente!")
                    print("Stock disponível: " + str(stock[i]) + " unidades")
                    print("Quantidade solicitada: " + str(encomenda) + " unidades")
    else:
        print("❌ Catálogo vazio. Não existe stock!")

# Funções de Consulta e Listagem


def filtrarCatalogo():
    """Filtros combinados usando 100% Pandas"""
    
    if numProdutos == 0:
        print("❌ Catálogo vazio!")
        return
    
    try:
        df = pd.read_csv("products_stock.csv", sep=";")
    except:
        print("❌ Erro ao ler CSV!")
        return

    # Blindagem de tipos
    df["price_unit"] = pd.to_numeric(df["price_unit"], errors="coerce")
    df["quantity_stock"] = pd.to_numeric(df["quantity_stock"], errors="coerce")
    df["category"] = df["category"].astype(str).str.strip()

    df = df.dropna(subset=["price_unit", "quantity_stock"])

    opcao = -1
    
    while opcao != 0:
        print("\n🔍 ===== Filtros Combinados ===== 🔍")
        print("1 - Categoria | 2 - Disponibilidade | 3 - Preço | 4 - Stock | 0 - Sair")
        opcao = lerInteiro("Escolha: ")
        
        if opcao == 1:
            cat = validarTexto("Categoria: ").strip()
            resultado = df[df["category"].str.contains(cat, case=False, na=False)]
            
            if resultado.empty:
                print("❌ Nenhum produto encontrado!")
            else:
                print("\n✅ Resultados:")
                print(resultado[["product_id", "name_product", "category", "price_unit"]].to_string(index=False))
        
        elif opcao == 2:
            disp = verificarDisponibilidade(2)
            ativo_val = "true" if disp == "S" else "false"
            resultado = df[df["available"].astype(str).str.lower() == ativo_val]
            
            if resultado.empty:
                print("❌ Nenhum produto encontrado!")
            else:
                print("\n✅ Resultados:")
                print(resultado[["product_id", "name_product", "available", "quantity_stock"]].to_string(index=False))
        
        elif opcao == 3:
            print("1-Igual | 2-Acima | 3-Abaixo")
            op = lerInteiro()
            
            if op in [1, 2, 3]:
                preco = verificarPreco()
                
                if op == 1:
                    resultado = df[df["price_unit"] == preco]
                elif op == 2:
                    resultado = df[df["price_unit"] > preco]
                else:
                    resultado = df[df["price_unit"] < preco]
                
                if resultado.empty:
                    print("❌ Nenhum encontrado!")
                else:
                    print("\n✅ Resultados:")
                    print(resultado[["product_id", "name_product", "price_unit"]].to_string(index=False))
        
        elif opcao == 4:
            print("1-Igual | 2-Acima | 3-Abaixo")
            op = lerInteiro()
            
            if op in [1, 2, 3]:
                stk = validarStock()
                
                if op == 1:
                    resultado = df[df["quantity_stock"] == stk]
                elif op == 2:
                    resultado = df[df["quantity_stock"] > stk]
                else:
                    resultado = df[df["quantity_stock"] < stk]
                
                if resultado.empty:
                    print("❌ Nenhum produto encontrado!")
                else:
                    print("\n✅ Resultados:")
                    print(resultado[["product_id", "name_product", "quantity_stock"]].to_string(index=False))
        
        elif opcao != 0:
            print("❌ Opção inválida!")

    

def listarCatalogo():
     # Lista todos os produtos do catálogo

    if numProdutos > 0:
        print("\n🌻 ===== Catálogo de Produtos ===== 🌻")

        for i in range(numProdutos):
            print(f"\n--- Produto #{i + 1} (ID Real: {idsProduto[i]}) ---")
            print("Nome: " + nomeProduto[i])
            print("Descrição: " + descricaoProduto[i])
            print("Categoria: " + categoriaProduto[i])
            print("Tipo: " + tiposProduto[i])   
            print("Preço: " + str(precosProduto[i]) + "€")
            print("Stock: " + str(stock[i]) + " unidades")
            

            if disponibilidade[i] == "S":
                print("Estado: Disponível ✅")
            else:
                print("Estado: Indisponível ❌") 

        print("\nTotal de produtos: " + str(numProdutos))
        print("\n")
    else:
        print("❌ O Catálogo está vazio! ❌")

# Função para mostrar estatísticas do catálogo
def verificarEstatisticas():
    print("\n📈 ===== Estatísticas do Catálogo ===== 📈")
    
    # Resumo Geral (usa listas globais)
    if numProdutos > 0:
        disponivel = sum(1 for i in range(numProdutos) if disponibilidade[i] == "S" and stock[i] > 0)
        esgotado = sum(1 for i in range(numProdutos) if stock[i] == 0 or disponibilidade[i] == "N")
        valor_total = sum(stock[i] * precosProduto[i] for i in range(numProdutos))
        
        print(f"\nResumo Geral")
        print(f"Total de Produtos: {numProdutos}")
        print(f"Disponíveis: {disponivel}")
        print(f"Esgotados: {esgotado}")
        print(f"Valor em Stock: {valor_total}€\n")
    
    print("🏆 TOP 5 Categorias")
    
    if not os.path.exists("products_stock.csv"):
        print("⚠️ Ficheiro não encontrado!")
        return
    
    try:
        df = pd.read_csv("products_stock.csv", sep=";")
        
        if df.empty:
            print("⚠️ Não há produtos no catálogo!")
            return
        # Limpar e padronizar categorias
        df["category"] = df["category"].astype(str).str.strip().str.title()
        
        # Converter preço para número
        df["price_unit"] = pd.to_numeric(df["price_unit"], errors="coerce")
        
        # Remover linhas sem categoria ou preço válido
        df = df.dropna(subset=["category", "price_unit"])
        
        if df.empty:
            print("⚠️ Não há dados válidos para estatísticas!")
            return
        
        # TOP 5 categorias
        top5 = df["category"].value_counts().head(5)
        for i, (cat, qtd) in enumerate(top5.items(), 1):
            print(f"{i}. {cat}: {qtd} produto(s)")
        
        # Preço médio por categoria
        print("\n💰 Preço Médio por Categoria:")
        preco_medio = df.groupby("category")["price_unit"].mean().round(2)
        
        if preco_medio.empty:
            print("⚠️ Não foi possível calcular preços médios!")
            return
        
        for categoria, preco in preco_medio.items():
            print(f"{categoria}: {preco}€")
    
    except Exception as e:
        print(f"❌ Erro ao calcular estatísticas: {e}")

#LISTAS GLOBAIS - Inicializadas ao importar módulo
idsProduto = []
stock = [] 
nomeProduto = [] 
descricaoProduto = []
categoriaProduto = []
disponibilidade = []
precosProduto = []

# Tentar carregar produtos do ficheiro CSV (persistência de dados)
numProdutos = lerProdutosCSV()

# Se não existir ficheiro ou erro ao ler, criar produtos predefinidos
if numProdutos == 0:
    print("📦 A criar produtos predefinidos...")
    
    # Produto 1: Girassol
    idsProduto.append(1)
    nomeProduto.append("Girassol")
    descricaoProduto.append("Flor Amarela")
    categoriaProduto.append("Flor")
    precosProduto.append(5.0)
    stock.append(10)
    disponibilidade.append("S")
    tiposProduto.append("Flor")
    duracoesProduto.append(0)
    
    # Produto 2: Rosa
    idsProduto.append(2)
    nomeProduto.append("Rosa")
    descricaoProduto.append("Flor Vermelha")
    categoriaProduto.append("Flor")
    precosProduto.append(7.0)
    stock.append(20)
    disponibilidade.append("S")
    tiposProduto.append("Flor")
    duracoesProduto.append(0)
    
    # Produto 3: Orquídea
    idsProduto.append(3)
    nomeProduto.append("Orquídea")
    descricaoProduto.append("Flor Roxa")
    categoriaProduto.append("Planta")
    precosProduto.append(27.5)
    stock.append(1)
    disponibilidade.append("S")
    tiposProduto.append("Planta")
    duracoesProduto.append(0)
    
    numProdutos = 3
    print("✅ 3 produtos padrão criados.")


# Função do Menu Principal para o main.py=
def menu_produtos():
    opcaoMenu = -1
    
    while opcaoMenu != 0:
        print("🌻 ===== Portal Gestor Florista ===== 🌻")
        print("1. Adicionar Produto ➕")
        print("2. Alterar Produto 📝")
        print("3. Remover Produto ❌")
        print("4. Listar Catálogo 📋")
        print("5. Filtrar Catálogo 🔍")
        print("6. Fazer Encomenda 📤")
        print("7. Adicionar Stock 📥")
        print("8. Ver estatisticas 📈")
        print("0. Voltar ao Menu Principal 👋")
        print()
        
        opcaoMenu = lerInteiro("Escolha uma opção: ")
        
        if opcaoMenu == 1:
            adicionarProduto()
        elif opcaoMenu == 2:
            alterarProduto()
        elif opcaoMenu == 3:
            removerProduto()
        elif opcaoMenu == 4:
            listarCatalogo()
        elif opcaoMenu == 5:
            filtrarCatalogo()
        elif opcaoMenu == 6:
            verificarEncomenda()
        elif opcaoMenu == 7:
            adicionarStock()
        elif opcaoMenu == 8:
            verificarEstatisticas()
        elif opcaoMenu == 0:
            guardarProdutosCSV()
            print("👋 A voltar ao menu principal...")
            return  # ✅ Volta para main.py
        else:
            print("Opção inválida. Insira um número de 0 a 8 e tente novamente.")

if __name__ == "__main__":
    menu_produtos()
