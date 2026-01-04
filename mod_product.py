#Luís 

import os
import pandas as pd 


# Função para validar stock disponível de um produto (USADO POR: Yeidman (Gestão Encomendas))
def validarStockDisponivel(idItem, quantidade):
    # Verificar se ficheiro existe
    if not os.path.exists("catalogo.csv"):
        print("⚠️ Ficheiro catalogo.csv não foi encontrado!")
        return False
    
    # Tentar ler o ficheiro
    try:
        df = pd.read_csv("catalogo.csv")
        
        # Procurar o produto pelo ID
        produto_encontrado = False
        numProdutos = len(df)
        
        for i in range(0, numProdutos, 1):
            if df["idItem"][i] == idItem:
                produto_encontrado = True
                
                # Verificar se está ativo
                if str(df["ativo"][i]) != "true":
                    print("⚠️ Produto está Indisponível!")
                    return False
                
                # Verificar stock
                if df["stock"][i] >= quantidade:
                    return True
                else:
                    print("⚠️ Stock insuficiente! Disponível: " + str(df["stock"][i]))
                    return False
        
        # Se chegou aqui, produto não existe
        if not produto_encontrado:
            print("⚠️ Produto não foi encontrado!")

        return False
        
    except:
        print("❌ Erro ao ler ficheiro!")
        return False


# Função para decrementar Stock após encomenda (USADO POR: Yeidman (Gestão Encomendas))
def reservarStock(idItem, quantidade):
    # Verificar se ficheiro existe
    if not os.path.exists("catalogo.csv"):
        print("❌ Ficheiro catalogo.csv não foi encontrado!")
        return False
    try:
        # Ler ficheiro atual
        df = pd.read_csv("catalogo.csv")
        # Criar listas para guardar dados
        ids = []
        tipos = []
        nomes = [] 
        descricoes = []
        categorias = []
        precos = []
        stocks = []
        ativos = []

        produto_encontrado = False
        numProdutos = len(df)

        # Copiar todos os dados para listas
        for i in range(0, numProdutos, 1):
            ids.append(df["idItem"][i])
            tipos.append(df["tipo"][i])
            nomes.append(df["nome"][i])
            descricoes.append(df["descricao"][i])
            categorias.append(df["categoria"][i])
            precos.append(df["preco"][i])
            stocks.append(df["stock"][i])
            ativos.append(df["ativo"][i])

            # Se encontrar o produto, modificar stock
            if df["idItem"][i] == idItem:
                produto_encontrado = True

                # Verificar se tem stock suficiente
                if stocks[i] < quantidade:
                    print("❌ Stock insuficiente!")
                    return False
                
                # Decrementar stock
                stock_antigo = stocks[i]
                stocks[i] = stocks[i] - quantidade 

                # Se esgotou, marcar inativo
                if stocks[i] == 0:
                    ativos[i] = "false"    
                    print("⚠️ " + nomes[i] + " esgotou!")   

                print("✅ Stock reservado: " + str(quantidade) + "x " + nomes[i])
                print("   Anterior: " + str(stock_antigo) + " → Novo: " + str(stocks[i]))

        if not produto_encontrado:
            print("❌ Produto não foi encontrado!")
            return False 
        
        # Criar DataFrame novo
        dados_novos = {
            "idItem": ids,
            "tipo": tipos,
            "nome": nomes,
            "descricao": descricoes,
            "categoria": categorias,
            "preco": precos,
            "stock": stocks,
            "ativo": ativos
        }
        
        df_novo = pd.DataFrame(dados_novos)
        df_novo.to_csv("catalogo.csv", index=False)
        
        return True
        
    except:
        print("❌ Erro ao reservar stock!")
        return False

def devolverStock(idItem, quantidade):
    # Validar quantidade positiva
    if quantidade <= 0:
        print("❌ Quantidade inválida para devolução! Deve ser maior que 0.")
        return False  
    
    # Verificar se ficheiro existe
    if not os.path.exists("catalogo.csv"):
        print("❌ Ficheiro catalogo.csv não foi encontrado!")
        return False 
     
    try:
        # Ler ficheiro atual
        df = pd.read_csv("catalogo.csv")

        # Criar listas para guardar dados
        ids = []
        tipos = []
        nomes = [] 
        descricoes = []
        categorias = []
        precos = []
        stocks = []
        ativos = []

        produto_encontrado = False
        numProdutos = len(df)

            # Copiar todos os dados para listas
        for i in range(0, numProdutos, 1):
            ids.append(df["idItem"][i])
            tipos.append(df["tipo"][i])
            nomes.append(df["nome"][i])
            descricoes.append(df["descricao"][i])
            categorias.append(df["categoria"][i])
            precos.append(df["preco"][i])
            stocks.append(df["stock"][i])
            ativos.append(df["ativo"][i])

            # Se encontrar o produto, modificar stock  
            if df["idItem"][i] == idItem:
                produto_encontrado = True

                # Incrementar stock
                stock_antigo = stocks[i]
                stocks[i] = stocks[i] + quantidade 

                # Se estava esgotado, passar a disponível
                if stocks[i] > 0:
                    ativos[i] = "true"    
                    print("✅ " + nomes[i] + " voltou a ficar disponível!")   

                print("✅ Stock devolvido: " + str(quantidade) + "x " + nomes[i])
                print("   Anterior: " + str(stock_antigo) + " → Novo: " + str(stocks[i]))

        if not produto_encontrado:
            print("❌ Produto não foi encontrado!")
            return False
        # Criar DataFrame novo  
        dados_novos = {
            "idItem": ids,
            "tipo": tipos,
            "nome": nomes,
            "descricao": descricoes,
            "categoria": categorias,
            "preco": precos,
            "stock": stocks,
            "ativo": ativos
        }
        df_novo = pd.DataFrame(dados_novos)
        df_novo.to_csv("catalogo.csv", index=False)
        return True
    except:
        print("❌ Erro ao devolver stock!")
        return False
            
# Função para listar produtos disponíveis (USADO POR: Beatriz (Portal Cliente)) - retorna DataFrame com produtos que estão ativos e têm stock
def listarProdutosDisponiveis():
    # Verificar se ficheiro existe
    if not os.path.exists("catalogo.csv"):
        print("⚠️ Ficheiro catalogo.csv não foi encontrado!")
        return pd.DataFrame()
    
    try:
        # Ler ficheiro atual
        df = pd.read_csv("catalogo.csv")

        # Criar listas para produtos disponíveis
        ids_disponiveis = []
        nomes_disponiveis = []
        descricoes_disponiveis = []
        categorias_disponiveis = []
        precos_disponiveis = []
        stocks_disponiveis = []

        numProdutos = len(df)
        for i in range(0, numProdutos, 1):
            # Verificar se ativo E tem stock
            if str(df["ativo"][i]) == "true" and df["stock"][i] > 0:
                ids_disponiveis.append(df["idItem"][i])
                nomes_disponiveis.append(df["nome"][i])
                descricoes_disponiveis.append(df["descricao"][i])
                categorias_disponiveis.append(df["categoria"][i])
                precos_disponiveis.append(df["preco"][i])
                stocks_disponiveis.append(df["stock"][i])

        # Criar DataFrame com produtos disponíveis
        dados_disponiveis = {   
            "idItem": ids_disponiveis,
            "nome": nomes_disponiveis,
            "descricao": descricoes_disponiveis,
            "categoria": categorias_disponiveis,
            "preco": precos_disponiveis,
            "stock": stocks_disponiveis
        }
        df_disponiveis = pd.DataFrame(dados_disponiveis)

        if len(ids_disponiveis) > 0:
            print("\nCatálogo de Produtos Disponíveis 🌻")
            
            for i in range(0, len(ids_disponiveis), 1):
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
    # Verificar se ficheiro existe  
    if not os.path.exists("catalogo.csv"):
        print("⚠️ Ficheiro catalogo.csv não foi encontrado!")
        return None
    
    try:
        # Ler ficheiro atual
        df = pd.read_csv("catalogo.csv")
        numProdutos = len(df)
        
        # Procurar produto pelo ID
        for i in range(0, numProdutos, 1):
            if df["idItem"][i] == idItem:

                detalhes = {
                    "idItem": df["idItem"][i],
                    "tipo": df["tipo"][i],
                    "nome": df["nome"][i],
                    "descricao": df["descricao"][i],
                    "categoria": df["categoria"][i],
                    "preco": df["preco"][i],
                    "stock": df["stock"][i],
                    "ativo": df["ativo"][i]
                }
                
                print("\n🌻 ===== Detalhes do Produto ===== 🌻")
                print("\n--- Produto ID: " + str(detalhes["idItem"]) + " ---")
                print("Nome: " + detalhes["nome"])
                print("Descrição: " + detalhes["descricao"])
                print("Categoria: " + detalhes["categoria"])
                print("Preço: " + str(detalhes["preco"]) + "€")
                print("Stock: " + str(detalhes["stock"]) + " unidades")
                
                if str(detalhes["ativo"]).lower() == "true" and detalhes["stock"] > 0:
                    print("Estado: Disponível ✅")
                elif detalhes["stock"] == 0:
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

def lerInteiro(mensagem=""):
    
    # Lê inteiro com proteção contra crashes - inserir texto em vez de número Inteiro 
    while True:
        try:
            valor = int(input(mensagem))
            return valor
        except ValueError:
            print("❌ Erro: Insira apenas números inteiros!")


def lerFloat(mensagem=""):
    
    # Lê float com proteção contra crashes - inserir texto em vez de número 
    while True:
        try:
            valor = float(input(mensagem))
            return valor
        except ValueError:
            print("❌ Erro: Insira apenas números!")


# Função para validar texto não vazio (descrição, categoria, etc.)
def validarTexto(mensagem):
    print(mensagem)
    texto = input()
    while len(texto) == 0:
        print("❌ Erro: Campo não pode estar vazio!")
        print(mensagem)
        texto = input()
    return texto

# Função para validar ID do produto
def validarID(numProdutos):
    idEscolhido = lerInteiro()
    while idEscolhido < 1 or idEscolhido > numProdutos:
        print("❌ ID inválido!")
        print("Insira um ID entre 1 e " + str(numProdutos))
        idEscolhido = lerInteiro()
    return idEscolhido

# Função para guardar produtos no ficheiro CSV
def guardarProdutosCSV(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade):
    # Criar IDs automáticos: 1, 2, 3, ... conforme número de produtos - (Faltava isto na parte do Flowgorithm)
    ids = list(range(1, len(nomeProduto) + 1))
    
    # Converter disponibilidade S/N para true/false (conforme enunciado)
    ativo = []
    # Percorre cada elemento e converte: S -> "true", N -> "false"
    for i in disponibilidade:
        if i == "S":
            ativo.append("true")
        else:
            ativo.append("false")
    
    # Criar dicionário com estrutura do catalogo.csv (Seguindo o enunciado) - Preparar dados dos produtos para estrutura CSV
    dados_produtos = {
        "idItem": ids,
        "tipo": ["produto"] * len(nomeProduto),
        "nome": nomeProduto,
        "descricao": descricaoProduto,
        "categoria": categoriaProduto,
        "preco": precosProduto,
        "stock": stock,
        "ativo": ativo
    }
    
    # Criar DataFrame do Pandas (Seguindo o enunciado)
    df = pd.DataFrame(dados_produtos)
    
    # Guardar em CSV
    df.to_csv("catalogo.csv", index=False)
    print("✅ Produtos guardados em catalogo.csv!")

    # Função para ler produtos do ficheiro CSV
def lerProdutosCSV(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade):
    # Verificar se ficheiro existe antes de tentar ler
    if not os.path.exists("catalogo.csv"):
        print("⚠️ Ficheiro catalogo.csv não foi encontrado.")
        print("📝 A iniciar com produtos padrão (primeira execução).")
        return 0
    
    try:
        df = pd.read_csv("catalogo.csv")
        
        # Carregar dados para as listas
        for i in range(len(df)):
            nomeProduto.append(df["nome"][i])
            descricaoProduto.append(df["descricao"][i])
            categoriaProduto.append(df["categoria"][i])
            precosProduto.append(df["preco"][i])
            stock.append(df["stock"][i])
            
            # Converter ativo true/false para S/N
            ativo_str = str(df["ativo"][i]).lower()
            if ativo_str == "true":
                disponibilidade.append("S")
            else:
                disponibilidade.append("N")
        
        numProdutos = len(nomeProduto)
        print(f"✅ {numProdutos} produtos carregados do ficheiro catalogo.csv!")
        return numProdutos
    # Seguindo o exemplo do professor para capturar erros
    except:
        print("❌ Erro ao carregar catálogo!")
        print("📝 A iniciar com produtos padrão.")
        return 0

# Adiciona um novo produto ao catálogo 
def adicionarProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
        
    # Usar múltiplos prints (mais claro que um print com \n múltiplos)
    print("Adicionar Novo Produto\n")
    
    # Recolher dados utilizando funções de validação existentes
    nomeProduto.append(validarNome())
    descricaoProduto.append(validarTexto("Insira a descrição do produto: "))
    categoriaProduto.append(validarTexto("Insira a categoria: "))
    precosProduto.append(verificarPreco())
    stock.append(validarStock())
    disponibilidade.append(verificarDisponibilidade(1))
    
    numProdutos = numProdutos + 1
    
    # Confirmação dos dados do produto adicionado
    print("\n Produto adicionado com sucesso! ✅")
    print("\n")
    print("Nome: " + nomeProduto[numProdutos - 1])
    print("Categoria: " + categoriaProduto[numProdutos - 1])
    print("Preço: " + str(precosProduto[numProdutos - 1]) + "€")
    print("Stock: " + str(stock[numProdutos - 1]) + " unidades")
    print("\n")

    # Guardar alterações no ficheiro CSV
    guardarProdutosCSV(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade)

    return numProdutos

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


def filtrarCatalogo(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
    
    # Filtra produtos por múltiplos critérios (categoria, disponibilidade, preço, stock) 
    
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
                
                for i in range(0, numProdutos, 1):

                    if categoriaProduto[i] == filtroCategoria:
                        print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Categoria: " + categoriaProduto[i])
                        resultadoFiltro = True
                
                if resultadoFiltro == False:
                    print("❌ Não foi encontrado nenhum produto!")
            
            # OPÇÃO 2: Filtrar por Disponibilidade
            elif opcao == 2:
                filtroDisponibilidade = verificarDisponibilidade(2)
                
                for i in range(0, numProdutos, 1):
                    if disponibilidade[i] == filtroDisponibilidade:
                        # Caso especial: produto marcado como N E com stock 0 (esgotado)
                        if disponibilidade[i] == "N" and stock[i] == 0:
                            print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Disponibilidade: " + disponibilidade[i] + " - está esgotado!")
                        else:
                            print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Disponibilidade: " + disponibilidade[i])
                        
                        # Se encontrou pelo menos 1, então:
                        resultadoFiltro = True

                # Se não encontrou nenhum:
                if resultadoFiltro == False:
                    print("❌ Não foi encontrado nenhum produto!")
            
            # OPÇÃO 3: Filtrar por Preço
            elif opcao == 3:
                print("Filtrar Preço:")
                print("1. Preço igual a")
                print("2. Preço acima de")
                print("3. Preço abaixo de")
                opcaoPreco = lerInteiro()
               
                if opcaoPreco >= 1 and opcaoPreco <= 3:
                    filtroPreco = verificarPreco()
                    
                    if opcaoPreco == 1:
                        for i in range(0, numProdutos, 1):
                            if precosProduto[i] == filtroPreco:
                                print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Preço: " + str(precosProduto[i]) + "€")
                                resultadoFiltro = True
                        
                        if resultadoFiltro == False:
                            print("❌ Não foi encontrado nenhum produto!")
                    
                    elif opcaoPreco == 2:
                        for i in range(0, numProdutos, 1):
                            if precosProduto[i] > filtroPreco:
                                print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Preço: " + str(precosProduto[i]) + "€")
                                resultadoFiltro = True
                        
                        if resultadoFiltro == False:
                            print("❌ Não foi encontrado nenhum produto!")
                    
                    elif opcaoPreco == 3:
                        for i in range(0, numProdutos, 1):
                            if precosProduto[i] < filtroPreco:
                                print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Preço: " + str(precosProduto[i]) + "€")
                                resultadoFiltro = True
                        
                        if resultadoFiltro == False:
                            print("❌ Não foi encontrado nenhum produto!")
                else:
                    print("❌ Opção inválida!")
            
            # OPÇÃO 4: Filtrar por Stock
            elif opcao == 4:
                print("Filtrar Stock:")
                print("1. Stock igual a")
                print("2. Stock acima de")
                print("3. Stock abaixo de")
                opcaoStock = lerInteiro()
                
                if opcaoStock >= 1 and opcaoStock <= 3:
                    filtroStock = validarStock()
                    
                    if opcaoStock == 1:
                        for i in range(0, numProdutos, 1):
                            if stock[i] == filtroStock:
                                print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Stock: " + str(stock[i]))
                                resultadoFiltro = True
                        
                        if resultadoFiltro == False:
                            print("❌ Não foi encontrado nenhum produto!")
                    
                    elif opcaoStock == 2:
                        for i in range(0, numProdutos, 1):
                            if stock[i] > filtroStock:
                                print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Stock: " + str(stock[i]))
                                resultadoFiltro = True
                        
                        if resultadoFiltro == False:
                            print("❌ Não foi encontrado nenhum produto!")
                    
                    elif opcaoStock == 3:
                        for i in range(0, numProdutos, 1):
                            if stock[i] < filtroStock:
                                print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Stock: " + str(stock[i]))
                                resultadoFiltro = True
                        
                        if resultadoFiltro == False:
                            print("❌ Não foi encontrado nenhum produto!")
                else:
                    print("❌ Opção inválida!")
            
            # OPÇÃO 0 = Voltar
            elif opcao == 0:
                print("↩️ Menu Principal")
            
            else:
                print("❌ Opção introduzida inválida!")
    else:
        print("❌ Catálogo Vazio. Impossível filtrar!")

    

def listarCatalogo(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
     # Lista todos os produtos do catálogo

    if numProdutos > 0:
        print("\n🌻 ===== Catálogo de Produtos ===== 🌻")
        
        # Usar múltiplos prints (mais claro que um print com \n múltiplos)  
        # Percorrer todos os produtos
        for i in range(0, numProdutos, 1):
            print("\n--- Produto " + str(i + 1) + " ---")
            print("ID: " + str(i + 1))
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
        print("==================================\n")
    else:
        print("❌ O Catálogo está vazio! ❌")


def adicionarStock(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
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
        guardarProdutosCSV(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade)
    else:
        print("❌ Catálogo vazio!")

# Remove um produto do catálogo
def removerProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):

    if numProdutos > 0:
        print("Insira o ID do produto a remover: ")
        idEscolhido = validarID(numProdutos)
        i = idEscolhido - 1

        # Usar múltiplos prints (mais claro que um print com \n múltiplos)
        print("\n⚠️  Vai remover o seguinte produto:")
        print("--- Produto a Remover ---")
        print("ID: " + str(idEscolhido))
        print("Nome: " + nomeProduto[i])
        print("Descrição: " + descricaoProduto[i])
        print("Categoria: " + categoriaProduto[i])
        print("Preço: " + str(precosProduto[i]) + "€")
        print("Stock: " + str(stock[i]) + " unidades")
        print("-------------------------\n")
        
        # Pedir confirmação
        print("Tem a certeza que deseja remover? (S/N): ")
        confirmacao = input()
        
        if confirmacao.upper() == "S":
            # Remover de todas as listas usando .pop()
            nomeProduto.pop(i)
            descricaoProduto.pop(i)
            categoriaProduto.pop(i)
            precosProduto.pop(i)
            stock.pop(i)
            disponibilidade.pop(i)
            
            print("🗑️  Produto removido com sucesso!")
            numProdutos = numProdutos - 1

            # Guardar alterações no ficheiro CSV
            guardarProdutosCSV(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade)
        else:
            print("Operação cancelada.")
    else:
        print("❌ O Catálogo está vazio!")
    
    return numProdutos


# Função que valida se o nome do produto não é vazio
def validarNome():
    nome = ""
    print("Insira nome do Produto: ")
    nome = input()
    while len(nome) == 0:
        print("Erro: Nome tem que ter mais que 1 carater!")
        print("Insira nome do Produto: ")
        nome = input() 
    return nome


# Função para validar stock (evitar negativos) 
def validarStock():
    print("Insira a quantidade de produto para stock: ")
    stock = lerInteiro()
    while stock < 0:
        print("Erro: O stock do produto não pode ser negativo! Volte a inserir, por favor!")
        stock = lerInteiro()
    return stock


# Função que muda a pergunta consoante o parâmetro (1, 2, 3)
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

def verificarEncomenda(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
    
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
                    guardarProdutosCSV(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade)
                else:
                    print("\n❌ Stock insuficiente!")
                    print("Stock disponível: " + str(stock[i]) + " unidades")
                    print("Quantidade solicitada: " + str(encomenda) + " unidades")
    else:
        print("❌ Catálogo vazio. Não existe stock!")

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
        print("\n--- Resumo Geral ---")
        print("Total de Produtos registados: " + str(numProdutos))
        print("Produtos Disponíveis: " + str(disponivel))
        print("Produtos Esgotados/Indisponíveis: " + str(esgotado))
        print("\n--- Valor em Stock ---")
        print("Valor Total: " + str(total) + "€")
        print("========================================\n")
    else:
        print("❌ Catálogo vazio. Não é possível fornecer estatísticas.")

# Função para validar preço (evitar negativos) 
def verificarPreco():
    print("Insira o Preço: ")
    preco =lerFloat()
    while preco < 0:
        print("Erro: O Preço do produto não pode ser negativo! Volte a inserir, por favor!")
        preco =lerFloat()
    return preco

# Main
# Arrays para armazenar produtos, os seus detalhes e preço
# Mudei de arrays fixos para listas dinâmicas para não ter limite de 10 produtos
stock = [] 
nomeProduto = [] 
descricaoProduto = []
categoriaProduto = []
disponibilidade = []
precosProduto = []

# Tentar carregar produtos do ficheiro CSV (persistência de dados)
numProdutos = lerProdutosCSV(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade)

# Se não existir ficheiro ou erro ao ler, criar produtos predefinidos
if numProdutos == 0:
    print("📦 A criar produtos predefinidos...")
    
    # Produto 1: Girassol
    nomeProduto.append("Girassol")
    descricaoProduto.append("Flor Amarela")
    categoriaProduto.append("Flor")
    precosProduto.append(5.0)
    stock.append(10)
    disponibilidade.append("S")
    
    # Produto 2: Rosa
    nomeProduto.append("Rosa")
    descricaoProduto.append("Flor Vermelha")
    categoriaProduto.append("Flor")
    precosProduto.append(7.0)
    stock.append(20)
    disponibilidade.append("S")
    
    # Produto 3: Orquídea
    nomeProduto.append("Orquídea")
    descricaoProduto.append("Flor Roxa")
    categoriaProduto.append("Planta")
    precosProduto.append(27.5)
    stock.append(1)
    disponibilidade.append("S")
    
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
        numProdutos = adicionarProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 2:
        # Chama função para alterar dados pré-definidos ou inseridos
        alterarProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 3:
        # Chama função para apagar registo
        numProdutos = removerProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 4:
        # Função para mostrar todos os dados em formato catálogo
        listarCatalogo(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 5:
        # Função para mostrar todos os dados de uma filtragem requisitada
        filtrarCatalogo(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 6:
        # Função que simula a saída de stock
        verificarEncomenda(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 7:
        # Função que simula a entrada de stock
        adicionarStock(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 8:
        # Funcionalidade extra da parte 2 enunciado
        verificarEstatisticas(precosProduto, categoriaProduto, stock, disponibilidade, numProdutos)
    elif opcaoMenu == 0:
        # Antes de sair, guardar produtos no ficheiro CSV!
        guardarProdutosCSV(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade)
        print("👋 A sair da aplicação...")
    else:
        print("Opção inválida. Insira um número de 0 a 8 e tente novamente.")
