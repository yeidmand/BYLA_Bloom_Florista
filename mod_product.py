#Luís - mod_product.py - Gestão de Produtos Byla Bloom

#Imports
import os
import pandas as pd 

numProdutos = 0

# Funções de Validação e Input
def lerInteiro(mensagem=""):
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("❌ Erro: Insira apenas números inteiros!")

def lerFloat(mensagem=""):
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("❌ Erro: Insira apenas números!")

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
def validarID(numProdutos):
    idEscolhido = lerInteiro()
    while idEscolhido < 1 or idEscolhido > numProdutos:
        print("❌ ID inválido!")
        print("Insira um ID entre 1 e " + str(numProdutos))
        idEscolhido = lerInteiro()
    return idEscolhido


# Funções de Leitura/Escrita CSV


tiposProduto = []       
categoriaProduto = []   
descricaoProduto = []   

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
        "description": descricaoProduto
    }
    df = pd.DataFrame(dados_produtos)
    df.to_csv("products_stock.csv", index=False, sep=";")
    print("✅ Produtos guardados em products_stock.csv!")


def lerProdutosCSV():
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
        i = idsProduto.index(idItem)

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

# Função para decrementar Stock após encomenda (USADO POR: Yeidman (Gestão Encomendas))
def reservarStock(idItem, quantidade):
    try:
        i = idsProduto.index(idItem)

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
        i = idsProduto.index(idItem)

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

            
# Função para listar produtos disponíveis (USADO POR: Beatriz (Portal Cliente)) - retorna DataFrame com produtos que estão ativos e têm stock
def listarProdutosDisponiveis():
    if not os.path.exists("products_stock.csv"):
        print("⚠️ Ficheiro products_stock.csv não foi encontrado!")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv("products_stock.csv", sep=";")

        # Criar listas para produtos disponíveis
        ids_disponiveis = []
        nomes_disponiveis = []
        descricoes_disponiveis = []
        categorias_disponiveis = []
        precos_disponiveis = []
        stocks_disponiveis = []

        numProdutos = len(df)
        for i in range(numProdutos):
            # Verificar se ativo E tem stock
            if str(df["available"][i]) == "true" and df["quantity_stock"][i] > 0:
                ids_disponiveis.append(df["product_id"][i])
                nomes_disponiveis.append(df["name_product"][i])
                descricoes_disponiveis.append(df["description"][i])
                categorias_disponiveis.append(df["category"][i])
                precos_disponiveis.append(df["price_unit"][i])
                stocks_disponiveis.append(df["quantity_stock"][i])

        # Criar DataFrame com produtos disponíveis
        dados_disponiveis = {   
            "product_id": ids_disponiveis,
            "name_product": nomes_disponiveis,
            "description": descricoes_disponiveis,
            "category": categorias_disponiveis,
            "price_unit": precos_disponiveis,
            "quantity_stock": stocks_disponiveis
        }
        df_disponiveis = pd.DataFrame(dados_disponiveis)

        if len(ids_disponiveis) > 0:
            print("\nCatálogo de Produtos Disponíveis 🌻")
            
            for i in range(len(ids_disponiveis)):
                print("\nProduto ID: " + str(ids_disponiveis[i]))
                print("Nome: " + nomes_disponiveis[i])
                print("Descrição: " + descricoes_disponiveis[i])
                print("Categoria: " + categorias_disponiveis[i])
                print("Preço: " + str(precos_disponiveis[i]) + "€")
                print("Stock: " + str(stocks_disponiveis[i]) + " unidades")
                print("\n")
            
            print("Total disponível: " + str(len(ids_disponiveis)) + " produtos")
        else:
            print("⚠️ Nenhum produto disponível no momento!")
        
        return df_disponiveis
        
    except:
        print("❌ Erro ao listar produtos disponíveis!")
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
            if df["product_id"][i] == idItem:

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

    print("Adicionar Novo Produto\n")

    # Gerar ID automático
    novo_id = 1 if not idsProduto else max(idsProduto) + 1
    idsProduto.append(novo_id)
    
    # Recolher dados utilizando funções de validação existentes
    nomeProduto.append(validarNome())
    descricaoProduto.append(validarTexto("Insira a descrição do produto: "))
    categoriaProduto.append(validarTexto("Insira a categoria: "))
    tiposProduto.append(validarTexto("Insira o tipo do produto: "))
    precosProduto.append(verificarPreco())
    stock.append(validarStock())
    disponibilidade.append(verificarDisponibilidade(1))
    
    # Guardar alterações no ficheiro CSV
    guardarProdutosCSV()

    # Confirmação dos dados do produto adicionado
    print("\n Produto adicionado com sucesso! ✅")
    print("\n")
    print("Nome: " + nomeProduto[numProdutos - 1])
    print("Categoria: " + categoriaProduto[numProdutos - 1])
    print("Preço: " + str(precosProduto[numProdutos - 1]) + "€")
    print("Stock: " + str(stock[numProdutos - 1]) + " unidades")
    print("\n")


def alterarProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
    # NOTA: O stock não é alterado aqui para garantir a integridade das opções 6 e 7 (Saídas/Entradas)
    # Permite alterar dados de um produto 
    opcaomenu = -1

    if numProdutos > 0:
        print("Insira o ID/Nº que pretende alterar: ")
        numItemEscolhido = validarID(numProdutos)
        i = numItemEscolhido - 1 # Este Assign serve para não ultrapassar o fim da lista/Array


        # Usar múltiplos prints (mais claro que um print com \n múltiplos) 
        print("\n--- Produto Selecionado ---")
        print("Nome: " + nomeProduto[i])
        print("Descrição: " + descricaoProduto[i])
        print("Categoria: " + categoriaProduto[i])
        print("Preço: " + str(precosProduto[i]) + "€")
        print("Stock: " + str(stock[i]) + " unidades")
        print("Disponibilidade: " + disponibilidade[i])
        print("---------------------------\n")

        while opcaomenu != 0:
            # Menu de opções com vários prints em vez de char13.
            print("\nEscolha, através do número, o que deseja alterar:")
            print("1. Alterar Nome")
            print("2. Alterar Descrição")
            print("3. Alterar Categoria")
            print("4. Alterar Preço")
            print("5. Alterar Disponibilidade")
            print("0. Concluir Alterações")

            # Lê a opção do utilizador.
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
                precosProduto[i] = verificarPreco()
                print("Preço alterado com sucesso!")
            elif opcaomenu == 5:
                disponibilidade[i] = verificarDisponibilidade(1)
                print("Disponibilidade alterada com sucesso!")
            elif opcaomenu == 0:
                print("Alterações Concluídas!")
                # Guardar alterações no ficheiro CSV
                guardarProdutosCSV(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade)
            else:
                print("Opção inválida!")
    else:
        print("O Catálogo está vazio!")

def adicionarStock():
    # Adiciona stock a produto existente 
    
    if numProdutos > 0:
        print("\n📥 ===== Adicionar Stock ===== 📥")
        print("\nInsira o ID do produto para adicionar stock: ")
        idEscolhido = validarID(numProdutos)
        i = idEscolhido - 1

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
        guardarProdutosCSV(idsProduto, nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade)
    else:
        print("❌ Catálogo vazio!")

# Remove um produto do catálogo
def removerProduto():

    if numProdutos > 0:
        print("Insira o ID do produto a remover: ")
        idEscolhido = validarID(numProdutos)
        
        if idEscolhido not in idsProduto: 
            print("❌ ID não encontrado!")
            return numProdutos
         
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
            guardarProdutosCSV()
            print("🗑️  Produto removido com sucesso!")
        else:
            print("Operação cancelada.")
    else:
        print("❌ O Catálogo está vazio!")
    
    return numProdutos


def verificarEncomenda():
    
    # Processa encomenda de produto 
    # Melhorias de apresentação e validações.
    
    if numProdutos > 0:
        # Usar múltiplos prints (mais claro que um print com \n múltiplos)
        print("\n📋 ===== Catálogo para Encomenda ===== 📋")
        
        for i in range(0, numProdutos, 1):
            print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Preço: " + str(precosProduto[i]) + "€" + " | Stock: " + str(stock[i]))
        
        print("\nQual o nº do item/ID que deseja encomendar: ")
        numItemEscolhido = lerInteiro()
        
        while numItemEscolhido < 1 or numItemEscolhido > numProdutos:
            print("❌ ID/Nº Artigo Inválido!")
            numItemEscolhido = lerInteiro("Insira ID válido: ")
        
        i = numItemEscolhido - 1
        
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
                    guardarProdutosCSV(idsProduto, nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade)
                else:
                    print("\n❌ Stock insuficiente!")
                    print("Stock disponível: " + str(stock[i]) + " unidades")
                    print("Quantidade solicitada: " + str(encomenda) + " unidades")
    else:
        print("❌ Catálogo vazio. Não existe stock!")

# Funções de Consulta e Listagem


def filtrarCatalogo():
    
    # Filtra produtos por múltiplos critérios (categoria, disponibilidade, preço, stock) usando Pandas
    
    if len(nomeProduto) == 0:
        print("❌ Catálogo Vazio. Impossível filtrar!")
        return
    
    try:
        df = pd.read_csv("products_stock.csv", sep=";")
    except:
        print("❌ Erro ao ler ficheiro!")
        return 
    
    opcao = -1
    
    if numProdutos > 0:
        # While para manter menu ativo até escolher 0
        while opcao != 0:
            # Reset a cada pesquisa (evitar resultados errados)
            resultadoFiltro = False
            
            print("\n🔍 ===== Filtrar o Catálogo ===== 🔍")
            print("1 - Por Categoria")
            print("2 - Por Disponibilidade")
            print("3 - Por Preço")
            print("4 - Por Stock")
            print("0 - Menu Principal")
            opcao = lerInteiro("Escolha: ")
            
            # OPÇÃO 1: Filtrar por Categoria
            if opcao == 1:
                filtroCategoria = validarTexto("Insira a categoria pela qual deseja filtrar: ")
                df_filtro = df[df["category"].str.contains(filtroCategoria, case=False, na=False)]
                
                for i in range(0, numProdutos, 1):
                    if categoriaProduto[i] == filtroCategoria:
                        print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Categoria: " + categoriaProduto[i])
                        resultadoFiltro = True
                
                if len(df_filtro) == 0:
                    print("❌ Não foi encontrado nenhum produto!")
                else:
                    print(df_filtro[["product_id", "name_product", "category"]].to_string(index=False))
            
            # OPÇÃO 2: Filtrar por Disponibilidade
            elif opcao == 2:
                filtroDisponibilidade = verificarDisponibilidade(2)
                df_filtro = df[df["available"].astype(str).str.lower() == ("true" if filtroDisponibilidade == "S" else "false")]
                
                for i in range(0, numProdutos, 1):
                    if disponibilidade[i] == filtroDisponibilidade:
                        if disponibilidade[i] == "N" and stock[i] == 0:
                            print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Disponibilidade: " + disponibilidade[i] + " - está esgotado!")
                        else:
                            print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Disponibilidade: " + disponibilidade[i])
                        
                        resultadoFiltro = True

                if len(df_filtro) == 0:
                    print("❌ Não foi encontrado nenhum produto!")
                else:
                    print(df_filtro[["product_id", "name_product", "available"]].to_string(index=False))
            
            # OPÇÃO 3: Filtrar por Preço
            elif opcao == 3:
                print("Filtrar Preço:")
                print("1. Preço igual a")
                print("2. Preço acima de")
                print("3. Preço abaixo de")
                opcaoPreco = lerInteiro()
               
                if opcaoPreco in [1,2,3]:
                    filtroPreco = verificarPreco()
                    if opcaoPreco == 1:
                        df_filtro = df[df["price_unit"] == filtroPreco]
                    elif opcaoPreco == 2:
                        df_filtro = df[df["price_unit"] > filtroPreco]
                    else:
                        df_filtro = df[df["price_unit"] < filtroPreco]
                    
                    if len(df_filtro) == 0:
                        print("❌ Não foi encontrado nenhum produto!")
                    else:
                        print(df_filtro[["product_id", "name_product", "price_unit"]].to_string(index=False))
            
            # OPÇÃO 4: Filtrar por Stock
            elif opcao == 4:
                print("Filtrar Stock:")
                print("1. Stock igual a")
                print("2. Stock acima de")
                print("3. Stock abaixo de")
                opcaoStock = lerInteiro()

                if opcaoStock in [1, 2, 3]:
                    filtroStock = validarStock()  
                    if opcaoStock == 1:
                        df_filtro = df[df["quantity_stock"] == filtroStock]
                    elif opcaoStock == 2:
                        df_filtro = df[df["quantity_stock"] > filtroStock]
                    else:
                        df_filtro = df[df["quantity_stock"] < filtroStock]

                    if len(df_filtro) == 0:
                        print("❌ Não foi encontrado nenhum produto!")
                    else:
                        print(df_filtro[["product_id", "name_product", "quantity_stock"]].to_string(index=False))
            else:
                if opcao != 0:
                    print("❌ Opção inválida! Escolha uma opção entre 0 e 4.")

    

def listarCatalogo(idsProduto, nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
     # Lista todos os produtos do catálogo

    if numProdutos > 0:
        print("\n🌻 ===== Catálogo de Produtos ===== 🌻")
        
        # Usar múltiplos prints (mais claro que um print com \n múltiplos)  
        # Percorrer todos os produtos
        for i in range(0, numProdutos, 1):
            print("\n--- Produto " + str(i + 1) + " ---")
            print("ID: " + str(idsProduto[i]))
            print("Nome: " + nomeProduto[i])
            print("Descrição: " + descricaoProduto[i])
            print("Categoria: " + categoriaProduto[i])
            print("Preço: " + str(precosProduto[i]) + "€")
            print("Stock: " + str(stock[i]) + " unidades")
            
            # Mostrar estado de disponibilidade
            if disponibilidade[i] == "S":
                print("Estado: Disponível ✅")
            else:
                print("Estado: Indisponível ❌")
            print("\n")
        
        print("\nTotal de produtos: " + str(numProdutos))
        print("\n")
    else:
        print("❌ O Catálogo está vazio! ❌")

# Função para mostrar estatísticas do catálogo
def verificarEstatisticas(precosProduto, categoriaProduto, stock, disponibilidade, numProdutos):
    
    if numProdutos > 0:
        disponivel = 0
        esgotado = 0
        total = 0
        
        # Calcular estatísticas num único ciclo
        for i in range(0, numProdutos, 1):
            if disponibilidade[i] == "S" and stock[i] > 0:
                disponivel = disponivel + 1
            else:
                if stock[i] == 0 or disponibilidade[i] == "N":
                    esgotado = esgotado + 1
            
            total = total + stock[i] * precosProduto[i]
        
        # Usar múltiplos prints (mais claro que um print com \n múltiplos)
        print("\n📈 ===== Estatísticas do Catálogo ===== 📈")
        print("\nResumo Geral")
        print("Total de Produtos registados: " + str(numProdutos))
        print("Produtos Disponíveis: " + str(disponivel))
        print("Produtos Esgotados/Indisponíveis: " + str(esgotado))
        print("\nValor em Stock")
        print("Valor Total: " + str(total) + "€")
    print("\n")
    
    print("\n TOP 5 Categorias ")
    
    # Ler CSV para ter acesso aos dados completos
    if os.path.exists("products_stock.csv"):
            try:
                df = pd.read_csv("products_stock.csv", sep=";")
                
                listaCategorias = []
                listaQuantidades = []
                
                # Contar produtos por categoria
                for i in range(len(df)):
                    categoriaAtual = df['categoria'][i]
                    
                    categoriaExiste = False
                    posicao = -1
                    
                    for j in range(len(listaCategorias)):
                        if listaCategorias[j] == categoriaAtual:
                            categoriaExiste = True
                            posicao = j
                            break
                    
                    if categoriaExiste:
                        listaQuantidades[posicao] = listaQuantidades[posicao] + 1
                    else:
                        listaCategorias.append(categoriaAtual)
                        listaQuantidades.append(1)
                
                # Ordenar listas
                for i in range(len(listaQuantidades)):
                    for j in range(i + 1, len(listaQuantidades)):
                        if listaQuantidades[j] > listaQuantidades[i]:
                            tempQtd = listaQuantidades[i]
                            listaQuantidades[i] = listaQuantidades[j]
                            listaQuantidades[j] = tempQtd
                            
                            tempCat = listaCategorias[i]
                            listaCategorias[i] = listaCategorias[j]
                            listaCategorias[j] = tempCat
                
                # Mostrar TOP 5
                limite = 5
                if len(listaCategorias) < 5:
                    limite = len(listaCategorias)
                
                for i in range(limite):
                    print(str(i + 1) + ". " + listaCategorias[i] + ": " + str(listaQuantidades[i]) + " produto(s)")
                
                
                # ADICIONAR: PREÇO MÉDIO POR CATEGORIA (enunciado exige!)
                print("\nPreço Médio por Categoria")
                
                for i in range(len(listaCategorias)):
                    categoria = listaCategorias[i]
                    
                    somaPrecos = 0
                    contador = 0
                    
                    for j in range(len(df)):
                        if df['categoria'][j] == categoria:
                            somaPrecos = somaPrecos + df['preco'][j]
                            contador = contador + 1
                    
                    precoMedio = somaPrecos / contador
                    print(categoria + ": " + str(round(precoMedio, 2)) + "€")
                
            except:
                print("❌ Erro ao calcular estatísticas avançadas!")
        
            print("\n")
    else:
        print("❌ Catálogo vazio. Não é possível fornecer estatísticas.")

# MENU PRINCIPAL

# Listas para armazenar os dados dos produtos
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
    
    # Produto 2: Rosa
    idsProduto.append(2)
    nomeProduto.append("Rosa")
    descricaoProduto.append("Flor Vermelha")
    categoriaProduto.append("Flor")
    precosProduto.append(7.0)
    stock.append(20)
    disponibilidade.append("S")
    tiposProduto.append("Flor")
    
    # Produto 3: Orquídea
    idsProduto.append(3)
    nomeProduto.append("Orquídea")
    descricaoProduto.append("Flor Roxa")
    categoriaProduto.append("Planta")
    precosProduto.append(27.5)
    stock.append(1)
    disponibilidade.append("S")
    tiposProduto.append("Planta")
    
    numProdutos = 3
    print("✅ 3 produtos padrão criados.")

# Controla a execução do menu principal
opcaoMenu = -1

# Mantém o programa a correr até o utilizador escolher 0
while opcaoMenu != 0:
    # Menu Gestor
    # posso utilizar /n para nova linha num unico print 
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
    
    opcaoMenu = lerInteiro("Escolha uma opção: ")
    
    if opcaoMenu == 1:
        # Chama função para criar o registo do item
        numProdutos = adicionarProduto()
    elif opcaoMenu == 2:
        # Chama função para alterar dados pré-definidos ou inseridos
        alterarProduto()
    elif opcaoMenu == 3:
        # Chama função para apagar registo
        numProdutos = removerProduto(idsProduto, nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 4:
        # Função para mostrar todos os dados em formato catálogo
        listarCatalogo(idsProduto, nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 5:
        # Função para mostrar todos os dados de uma filtragem requisitada
        filtrarCatalogo()
    elif opcaoMenu == 6:
        # Função que simula a saída de stock
        verificarEncomenda(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 7:
        # Função que simula a entrada de stock
        adicionarStock(idsProduto, nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 8:
        # Funcionalidade extra da parte 2 enunciado
        verificarEstatisticas(precosProduto, categoriaProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 0:
        # Antes de sair, guardar produtos no ficheiro CSV!
        guardarProdutosCSV()
        print("👋 A sair da aplicação...")
    else:
        print("Opção inválida. Insira um número de 0 a 8 e tente novamente.")
