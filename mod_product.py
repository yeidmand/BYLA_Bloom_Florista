#Luís 

import pandas as pd


def adicionarProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
    
    #Adiciona um novo produto ao catálogo (21/12).
    # Melhorias de apresentação similares a alterarProduto.
    
    # Usar múltiplos prints (mais claro que um print com \n múltiplos)
    print("Adicionar Novo Produto\n")
    
    # Recolher dados utilizando funções de validação existentes
    nomeProduto.append(validarNome())
    
    print("Insira a descrição do produto: ")
    descricao = input()
    while len(descricao) == 0:
        print("Erro: Descrição tem que ter mais que 1 carater!")
        descricao = input("Insira a descrição: ")
    descricaoProduto.append(descricao)
    
    print("Insira a categoria: ")
    categoria = input()
    while len(categoria) == 0:
        print("Erro: Categoria tem que ter mais que 1 carater!")
        categoria = input("Insira a categoria: ")
    categoriaProduto.append(categoria)
    
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
    
    return numProdutos

def alterarProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
    # NOTA: O stock não é alterado aqui para garantir a integridade das opções 6 e 7 (Saídas/Entradas)
    # Pemite alterar dados de um produto (16/12)
    opcaomenu = -1

    if numProdutos > 0:
        print("Insira o ID/Nº que pretende alterar: ")
        numItemEscolhido = int(input())

        while numItemEscolhido < 1 or numItemEscolhido > numProdutos:
            print("❌ ID/Nº Artigo Inválido!")
            print("Insira um ID entre 1 e " + str(numProdutos))
            numItemEscolhido = int(input())

        # Este Assign serve para não ultrapassar o fim da lista/Array
        i = numItemEscolhido - 1

        # Usar múltiplos prints (mais claro que um print com \n múltiplos) (16/12)
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

            opcaomenu = int(input()) # Lê a opção do utilizador.

            if opcaomenu == 1:
                nomeProduto[i] = validarNome()
                print("Nome alterado com sucesso!")
            else:
                if opcaomenu == 2:
                    print("Insira a nova Descrição: ")
                    novaDescricao = input()
                    # Nova validação para descrição não vazia
                    while len(novaDescricao) == 0:
                        print("Erro: Descrição tem que ter mais que 1 carater!")
                        print("Insira a nova Descrição: ")
                        novaDescricao = input()
                    descricaoProduto[i] = novaDescricao
                    print("Descrição alterada com sucesso!")
                else:
                    if opcaomenu == 3:
                        print("Escreva nova categoria: ")
                        novaCategoria = input()
                        # Validação para categoria não vazia
                        while len(novaCategoria) == 0:
                            print("Erro: Categoria tem que ter mais que 1 carater!")
                            print("Escreva nova categoria: ")
                            novaCategoria = input()
                        categoriaProduto[i] = novaCategoria
                        print("Categoria alterada com sucessso!")
                    else:
                        if opcaomenu == 4:
                            precosProduto[i] = verificarPreco()
                            print("Preço alterado com sucessso!")
                        else:
                            if opcaomenu == 5:
                                disponibilidade[i] = verificarDisponibilidade(1)
                                print("Disponibilidade alterada com sucessso!")
                            else:
                                if opcaomenu == 0:
                                    print("Alterações Concluidas!")
    else:
        print("O Catálogo está vazio!")

def filtrarCatalogo(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
    
    # Filtra produtos por múltiplos critérios (categoria, disponibilidade, preço, stock) (21/12).
    
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
            opcao = int(input("Escolha: "))
            
            # OPÇÃO 1: Filtrar por Categoria
            if opcao == 1:
                print("Insira a categoria pela qual deseja filtrar: ")
                filtroCategoria = input()
                
                while len(filtroCategoria) == 0:
                    print("A categoria não pode ser vazia. Tente de novo: ")
                    filtroCategoria = input()
                
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
                opcaoPreco = int(input())
                
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
                opcaoStock = int(input())
                
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
            
            # OPÇÃO 0: Voltar
            elif opcao == 0:
                print("↩️ Menu Principal")
            
            else:
                print("❌ Opção introduzida inválida!")
    else:
        print("❌ Catálogo Vazio. Impossível filtrar!")

    

def listarCatalogo(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
     #Lista todos os produtos do catálogo (21/12).

    if numProdutos > 0:
        print("\n🌻 ===== Catálogo de Produtos ===== 🌻")
        
        # Usar múltiplos prints (mais claro que um print com \n múltiplos)  
        #  # Percorrer todos os produtos
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


def adicionarStock(nomeProduto, stock, disponibilidade, numProdutos):
    
    # Nome mais descritivo (melhor prática) (21/12).
    # Adiciona stock a produto existente (21/12).
    
    if numProdutos > 0:
        print("\n📥 ===== Adicionar Stock ===== 📥")
        print("\nInsira o ID do produto para adicionar stock: ")
        idEscolhido = int(input())
        
        while idEscolhido < 1 or idEscolhido > numProdutos:
            print("❌ ID inválido!")
            print("Insira um ID entre 1 e " + str(numProdutos))
            idEscolhido = int(input())
        
        i = idEscolhido - 1
        
        # Usar múltiplos prints (mais claro que um print com \n múltiplos)
        print("\n--- Produto Selecionado ---")
        print("Nome: " + nomeProduto[i])
        print("Stock atual: " + str(stock[i]) + " unidades")
        print("---------------------------")
        
        print("\nQuantidade a adicionar: ")
        quantidade = int(input())
        
        while quantidade <= 0:
            print("Erro: Quantidade tem que ser superior a 0!")
            quantidade = int(input("Quantidade a adicionar: "))
        
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
    else:
        print("❌ Catálogo vazio!")

def removerProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):

    # Remove um produto do catálogo (20/12).
    # Estrutura baseada em alterarProduto (reutilização de validação)

    if numProdutos > 0:
        print("Insira o ID do produto a remover: ")
        idEscolhido = int(input())
        
        # Validação de ID (similar a alterarProduto)
        while idEscolhido < 1 or idEscolhido > numProdutos:
            print("❌ ID inválido!")
            print("Insira um ID entre 1 e " + str(numProdutos))
            idEscolhido = int(input())
        
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
        else:
            print("Operação cancelada.")
    else:
        print("❌ O Catálogo está vazio!")
    
    return numProdutos


def validarNome():
    nome = ""

    # 21/11 - Adicionada maior robustez após ter questionado o professor.
    # 21/11 - Utilizar o len (da documentação oficial) para ler o tamanho do texto e não aceitar vazio.
    print("Insira nome do Produto: ")
    nome = input()
    while len(nome) == 0:
        print("Erro: Nome tem que ter mais que 1 carater!")
        print("Insira nome do Produto: ")
        nome = input()
    
    return nome

def validarStock():
    # Função para validar Stock inserido (evitar negativos)
    print("Insira a quantidade de produto para stock: ")
    stock = int(input())

    # Condição utilizada para evitar stock negativo
    while stock < 0:
        print("Erro: O stock do produto não pode ser negativo! Volte a inserir, por favor!")
        stock = int(input())
    
    return stock

def verificarDisponibilidade(opcaoOperacao):
    # Função que muda a pergunta consoante o parametro (1, 2, 3)
    # Variável inicializada vazia
    disponibilidade = ""

    # Utilizada para definir estado em Adicionar e Alterar produto
    if opcaoOperacao == 1:
        print("Informe se está disponível(S/N): ")
    else:

        # Utilizada para questionar qual o estado que pretende filtrar
        if opcaoOperacao == 2:
            print("Disponibilidade desejada (S - Disponível / N - Indisponível): ")
        else:

            # Validação de segurança para remover produto
            if opcaoOperacao == 3:
                print("⚠️ Tem a certeza que deseja remover o produto(S/N)?")
    disponibilidade = input()
    while disponibilidade != "S" and disponibilidade != "N":
        print("Erro: Opção inválida. Insira apenas 'S' ou 'N': ")
        disponibilidade = input()
    
    return disponibilidade

def verificarEncomenda(stock, disponibilidade, numProdutos, nomeProduto, precosProduto):
    
    # Processa encomenda de produto (21/12).
    # Melhorias de apresentação e validações.
    
    if numProdutos > 0:
        # Usar múltiplos prints (mais claro que um print com \n múltiplos)
        print("\n📋 ===== Catálogo para Encomenda ===== 📋")
        
        for i in range(0, numProdutos, 1):
            print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Preço: " + str(precosProduto[i]) + "€" + " | Stock: " + str(stock[i]))
        
        print("\nQual o nº do item/ID que deseja encomendar: ")
        numItemEscolhido = int(input())
        
        while numItemEscolhido < 1 or numItemEscolhido > numProdutos:
            print("❌ ID/Nº Artigo Inválido!")
            numItemEscolhido = int(input("Insira ID válido: "))
        
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
                encomenda = int(input())
                
                while encomenda <= 0:
                    print("Erro: Quantidade tem que ser superior a 0!")
                    print("Insira a quantidade a encomendar: ")
                    encomenda = int(input())
                
                if encomenda <= stock[i]:
                    stock[i] = stock[i] - encomenda
                    print("\n✅ Encomenda realizada com sucesso!")
                    print("Quantidade encomendada: " + str(encomenda) + " unidades")
                    print("Stock restante: " + str(stock[i]) + " unidades")
                    
                    # Atualizar disponibilidade se esgotou
                    if stock[i] == 0:
                        disponibilidade[i] = "N"
                        print("⚠️ Produto esgotou! Marcado como indisponível.")
                else:
                    print("\n❌ Stock insuficiente!")
                    print("Stock disponível: " + str(stock[i]) + " unidades")
                    print("Quantidade solicitada: " + str(encomenda) + " unidades")
    else:
        print("❌ Catálogo vazio. Não existe stock!")

def verificarEstatisticas(precosProduto, categoriaProduto, stock, disponibilidade, numProdutos):
    
    #Mostra estatísticas do catálogo (21/12).
    
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

def verificarPreco():
    # 7/11 - Função para validar preço inserido
    print("Insira o Preço: ")
    preco = float(input())
    while preco < 0:
        print("Erro: O Preço do produto não pode ser negativo! Volte a inserir, por favor!")
        preco = float(input())
    
    return preco

# Main
# Arrays para armazenar produtos, os seus detalhes e preço
# Mudei de arrays fixos para listas dinâmicas para não ter limite de 10 produtos (13/12)
stock = [] 
nomeProduto = [] 
descricaoProduto = []
categoriaProduto = []
disponibilidade = []
precosProduto = []

# Controla a execução do menu principal
opcaoMenu = -1

# Inicializa a opção com valor inválido (-1) para garantir a entrada no ciclo do menu
# Contador de Produtos
numProdutos = 3

# Dados iniciais para testes - 3 produtos pré-definidos
# Uso .append() para adicionar às listas vazias (13/12)

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


# Atualiza contador após adicionar os 3 produtos iniciais
numProdutos = 3


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
    
    opcaoMenu = int(input("Escolha uma opção: "))
    
    # Lógica para Adicionar Produto aqui
    if opcaoMenu == 1:
        # Chama função para criar o registo do item
        numProdutos = adicionarProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
    else:
        if opcaoMenu == 2:
            # Chama função para alterar dados pré-definidos ou inseridos
            alterarProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
        else:
            if opcaoMenu == 3:
                # Chama função para apagar registo
                numProdutos = removerProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
            else:
                if opcaoMenu == 4:
                    # Função para mostrar todos os dados em formato catálogo
                    listarCatalogo(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
                else:
                    if opcaoMenu == 5:
                        # Função para mostrar todos os dados de uma filtragem requisitada
                        filtrarCatalogo(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos)
                    else:
                        if opcaoMenu == 6:
                            # Função que simula a saída de stock
                            verificarEncomenda(stock, disponibilidade, numProdutos, nomeProduto, precosProduto)
                        else:
                            if opcaoMenu == 7:
                                # Função que simula a entrada de stock
                                adicionarStock(nomeProduto, stock, disponibilidade, numProdutos)
                            else:
                                if opcaoMenu == 8:
                                    # Funcionalidade extra da parte 2 enunciado
                                    verificarEstatisticas(precosProduto, categoriaProduto, stock, disponibilidade, numProdutos)
                                else:
                                    if opcaoMenu == 0:
                                        print("👋 A sair da aplicação...")
                                    else:
                                        print("Opção inválida. Insira um número de 0 a 8 e tente novamente.")
