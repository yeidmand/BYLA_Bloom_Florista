#Luís 

import pandas as pd


def adicionarProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
    # Remove validação do limite - agora as listas crescem automaticamente
    novonumProdutos = numProdutos
    novoNome = validarNome()
    
    print("Insira a descrição do Produto: ")
    novaDescricao = input()
    while len(novaDescricao) == 0:
        print("Erro: Descrição tem que ter mais que 1 carater!")
        print("Insira a descrição do Produto: ")
        novaDescricao = input()
    
    print("Insira a categoria do Produto: ")
    novaCategoria = input()
    while len(novaCategoria) == 0:
        print("Erro: Categoria tem que ter mais que 1 carater!")
        print("Insira a categoria do Produto: ")
        novaCategoria = input()
    
    novoPreco = verificarPreco()
    novoStock = validarStock()
    
    # Se tem stock inicial, fica Disponível (S), senão Indisponível (N).
    # Aplicar o princípio KISS (Keep It Simple).
    if novoStock > 0:
        novaDisponibilidade = "S"
    else:
        novaDisponibilidade = "N"
    
    # Uso .append() em vez de índices para adicionar às listas
    nomeProduto.append(novoNome) 
    descricaoProduto.append(novaDescricao)  
    categoriaProduto.append(novaCategoria)  
    precosProduto.append(novoPreco)  
    stock.append(novoStock)  
    disponibilidade.append(novaDisponibilidade) 
    novonumProdutos = numProdutos + 1
    print("✅ Produto Adicionado com Sucesso!")
    
    return novonumProdutos

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
    opcao = -1
    if numProdutos > 0:
        while opcao != 0:

            # A variável 'resultadoFiltro' é reiniciada dentro do ciclo 'While' para garantir que a cada nova pesquisa começa "limpa"/vazia, evitando falsos positivos de pesquisas anteriores.
            resultadoFiltro = False
            print("| Filtrar o catálogo: | " + chr(13) + "1 - Por Categoria" + chr(13) + "2 - Por Disponibilidade" + chr(13) + "3 - Por Preço" + chr(13) + "4 - Por Stock" + chr(13) + "0 - Menu Principal")
            opcao = int(input())
            if opcao == 1:
                print("Insira a categoria pela qual deseja filtrar: ")
                filtroCategoria = input()

                # 22/11 - Deixava passar, validação feita!
                while len(filtroCategoria) == 0:
                    print("A categoria não pode ser vazia. Tente de novo:")
                    filtroCategoria = input()
                for i in range(0, numProdutos - 1 + 1, 1):
                    if categoriaProduto[i] == filtroCategoria:
                        print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + "|Categoria: " + categoriaProduto[i])
                        resultadoFiltro = True
                if resultadoFiltro == False:
                    print("❌ Não foi encontrado nenhum produto!")
            else:
                if opcao == 2:
                    filtroDisponibilidade = verificarDisponibilidade(2)

                    # 20/11 - Após testes, verifiquei que não mostrava os que têm 0 stock como N - Indispoonível. Seguindo lógica do mundo real, criei validações de forma a que mostrasse tudo que tiver N e/ou stock = 0.
                    for i in range(0, numProdutos - 1 + 1, 1):

                        # 22/11 - Minha lógica estava ao contrário. Nos testes tava a passar coisas erradas que eram mostradas posteriormente no catalogo.
                        if disponibilidade[i] == filtroDisponibilidade:
                            if disponibilidade[i] == "N" and stock[i] == 0:
                                print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Disponibilidade: " + disponibilidade[i] + " está esgotado!")
                            else:
                                print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Disponibilidade: " + disponibilidade[i])
                            resultadoFiltro = True
                    if resultadoFiltro == False:
                        print("❌ Não foi encontrado nenhum produto!")
                else:
                    if opcao == 3:
                        print("Filtrar Preço:" + chr(13) + "1. Preço igual a: " + chr(13) + "2. Preço acima de: " + chr(13) + "3.  Preço abaixo de: ")
                        opcaoPreco = int(input())

                        # 22/11 - Se inserisse valor acima de 3 ele funcionava na mesma. Lógica corrigida.
                        if opcaoPreco >= 1 and opcaoPreco <= 3:
                            filtroPreco = verificarPreco()
                            if opcaoPreco == 1:
                                for i in range(0, numProdutos - 1 + 1, 1):
                                    if precosProduto[i] == filtroPreco:
                                        print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " |Preço  : " + "€" + str(precosProduto[i]))
                                        resultadoFiltro = True
                                if resultadoFiltro == False:
                                    print("❌ Não foi encontrado nenhum produto!")
                            else:
                                if opcaoPreco == 2:
                                    for i in range(0, numProdutos - 1 + 1, 1):
                                        if precosProduto[i] > filtroPreco:
                                            print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Preço  : " + "€" + str(precosProduto[i]))
                                            resultadoFiltro = True
                                    if resultadoFiltro == False:
                                        print("❌ Não foi encontrado nenhum produto!")
                                else:
                                    if opcaoPreco == 3:
                                        for i in range(0, numProdutos - 1 + 1, 1):

                                            # 18/11 - Estava como a opção 1 e por isso não fazia o pretendido.
                                            if precosProduto[i] < filtroPreco:
                                                print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Preço  : " + "€" + str(precosProduto[i]))
                                                resultadoFiltro = True
                                        if resultadoFiltro == False:
                                            print("❌ Não foi encontrado nenhum produto!")
                        else:
                            print("Opção inválida!")
                    else:
                        if opcao == 4:
                            print("Filtrar Stock:" + chr(13) + "1. Stock igual a: " + chr(13) + "2. Stock acima de: " + chr(13) + "3.  Stock abaixo de: ")
                            opcaoStock = int(input())

                            # 22/11 - Se inserisse valor acima de 3 ele funcionava na mesma. Lógica corrigida.
                            if opcaoStock >= 1 and opcaoStock <= 3:
                                filtroStock = validarStock()
                                if opcaoStock == 1:
                                    for i in range(0, numProdutos - 1 + 1, 1):
                                        if stock[i] == filtroStock:
                                            print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Stock: " + str(stock[i]))
                                            resultadoFiltro = True
                                    if resultadoFiltro == False:
                                        print("❌ Não foi encontrado nenhum produto!")
                                else:
                                    if opcaoStock == 2:
                                        for i in range(0, numProdutos - 1 + 1, 1):
                                            if stock[i] > filtroStock:
                                                print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Stock: " + str(stock[i]))
                                                resultadoFiltro = True
                                        if resultadoFiltro == False:
                                            print("❌ Não foi encontrado nenhum produto!")
                                    else:
                                        if opcaoStock == 3:
                                            for i in range(0, numProdutos - 1 + 1, 1):
                                                if stock[i] < filtroStock:
                                                    print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Stock: " + str(stock[i]))
                                                    resultadoFiltro = True
                                            if resultadoFiltro == False:
                                                print("❌ Não foi encontrado nenhum produto!")
                                        else:
                                            print("❌ Nenhum artigo encontrado com essa filtragem!")
                            else:
                                print("❌ Opção inválida!")
                        else:
                            if opcao == 0:
                                print("Menu Principal")
                            else:
                                print("❌ Opção introduzida é inválida!")
    else:
        print("Catálogo Vazio. Impossível filtrar!")

def listarCatalogo(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
    print("| Catálogo Atualizado | ")

    # Também posso fazer ao contrário, se for maior que -1 o que está no falso passa a verdade. Questionar professor.
    if numProdutos > -1:

        # até numProdutos -1 para percorremos os índices de 0 até ao último item adicionado, que está na posição numProdutos - 1
        for i in range(0, numProdutos - 1 + 1, 1):

            # Indice do array começa no 0, logo, usamos i + 1 para lista começar numerada em 1. NomeProduto[i] para aceder ao nome guardado no array na posição i
            # 
            # 25/10 - Coloquei "ID" por agora no i+1 para aparecer no output
            print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Descrição: " + descricaoProduto[i] + " | Categoria: " + categoriaProduto[i] + " | Preço: " + str(precosProduto[i]) + "€" + " | Stock: " + str(stock[i]) + " | Disponível: " + disponibilidade[i])
    else:
        print("Catálogo Vazio")

def novoStock(nomeProduto, stock, disponibilidade, numProdutos):
    if numProdutos > 0:
        print("Qual o ID do produto que deseja adicionar Stock: ")
        numItemEscolhido = int(input())

        # Utilização de um ciclo 'While' em vez de um 'IF'.
        # Isto impede que o programa termine se o utilizador errar o ID, obrigando-o a inserir um ID válido para continuar.
        while numItemEscolhido < 1 or numItemEscolhido > numProdutos:
            print("ID/Nº Artigo Inválido!")
            print("Insira um ID entre 1 e " + str(numProdutos))
            numItemEscolhido = int(input())
        i = numItemEscolhido - 1
        print("Está a alterar o stock do Produto: " + "Produto: " + nomeProduto[i] + " | Stock Atual: " + str(stock[i]))
        quantidadeInserida = validarStock()
        if quantidadeInserida > 0:
            stock[i] = stock[i] + quantidadeInserida
            if stock[i] > 0:
                disponibilidade[i] = "S"
            print("✅ Stock adicionado com sucesso!" + "Stock Atualizado: " + str(stock[i]))
        else:
            print("Stock inserido tem que ser superior a 0!")
    else:
        print("Catálogo Vazio. Não existe stock!")

def removerProduto(nomeProduto, descricaoProduto, categoriaProduto, precosProduto, stock, disponibilidade, numProdutos):
    novonumProdutos = numProdutos

    # Variável inicializada vazia
    confirmacao = ""
    if numProdutos > 0:
        print("Qual o nº do item que deseja remover?")
        numItemEscolhido = int(input())
        while numItemEscolhido < 1 or numItemEscolhido > numProdutos:
            print("❌ ID/Nº Artigo Inválido!")
            print("Insira um ID entre 1 e " + str(numProdutos))
            numItemEscolhido = int(input())

        # Vai fazer com que o item seja o primeiro do indice/primeiro ID
        decrementarIndice = numItemEscolhido - 1

        # Validação de segurança em caso de erro ao inserir o ID do artigo.
        confirmacao = verificarDisponibilidade(3)
        if confirmacao == "S":

            # Quando um item é apagado, forma-se um "buraco" no índice correspondente.
            # Para preencher esse espaço, o ciclo move os itens à direita do buraco uma posição à esquerda. (+1)
            # Vai apenas até numProdutos - 2 porque o último elemento (-1) é copiado para a penúltima posição, e não precisamos de ler para além do fim da lista.
            for i in range(decrementarIndice, numProdutos - 2 + 1, 1):
                nomeProduto[i] = nomeProduto[i + 1]
                descricaoProduto[i] = descricaoProduto[i + 1]
                categoriaProduto[i] = categoriaProduto[i + 1]
                precosProduto[i] = precosProduto[i + 1]
                stock[i] = stock[i + 1]
                disponibilidade[i] = disponibilidade[i + 1]
            novonumProdutos = numProdutos - 1
            print("🗑️ Item removido com sucesso!")
        else:
            print("Item não removido. Ação cancelada!")
    else:
        print("O Catálogo está vazio!")
    
    return novonumProdutos

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
    encomenda = 0
    if numProdutos > 0:
        print("| Catálogo !")
        for i in range(0, numProdutos - 1 + 1, 1):
            print("ID: " + str(i + 1) + " | Nome: " + nomeProduto[i] + " | Preço: " + str(precosProduto[i]) + "€" + " | Stock: " + str(stock[i]))
        print("Qual o nº do item/ID que deseja encomendar: ")
        numItemEscolhido = int(input())
        while numItemEscolhido < 1 or numItemEscolhido > numProdutos:
            print("ID/Nº Artigo Inválido!")
            numItemEscolhido = int(input())
        i = numItemEscolhido - 1
        if stock[i] == 0:
            print("❌ Sem stock!" + chr(13) + "Produto indisponível de momento!")
        else:
            print("Insira a quantidade a encomendar: ")
            encomenda = int(input())
            while encomenda <= 0:
                print("Quantidade tem que ser superior a 0!")
                print("Insira a quantidade a encomendar: ")
                encomenda = int(input())
            if encomenda <= stock[i]:
                stock[i] = stock[i] - encomenda
                print("✅ Produto encomendado!")

                # Isto previne que produtos esgotados apareçam como disponíveis.
                if stock[i] == 0:
                    disponibilidade[i] = "N"
                    print("⚠️ Produto selecionado esgotou!")
            else:
                print("❌ Produto Indisponivel/Sem Stock suficiente!")
    else:
        print("Catálogo Vazio. Não existe stock!")

def verificarEstatisticas(precosProduto, categoriaProduto, stock, disponibilidade, numProdutos):
    # 21/11 - Funcionalidade da parte 2 do enunciado aplicada de forma parcial.
    disponivel = 0
    esgotado = 0
    total = 0
    if numProdutos > 0:

        # Ao invés de percorrer a lista uma vez para contar os "Ativos", outra para os "Esgotados" e mais uma para o "Valor", usei um único ciclo.
        for i in range(0, numProdutos - 1 + 1, 1):
            if disponibilidade[i] == "S":
                disponivel = disponivel + 1
            if stock[i] == 0 or disponibilidade[i] == "N":
                esgotado = esgotado + 1
            total = total + stock[i] * precosProduto[i]
        print("Total de Itens: " + str(numProdutos))
        print("Produtos Disponíveis: " + str(disponivel))
        print("Produtos Esgotados: " + str(esgotado))
        print("Valor em Stock: " + str(total) + "€")
    else:
        print("Catálogo Vazio. Não é possível fornecer estatísticas")

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
                                novoStock(nomeProduto, stock, disponibilidade, numProdutos)
                            else:
                                if opcaoMenu == 8:
                                    # Funcionalidade extra da parte 2 enunciado
                                    verificarEstatisticas(precosProduto, categoriaProduto, stock, disponibilidade, numProdutos)
                                else:
                                    if opcaoMenu == 0:
                                        print("👋 A sair da aplicação...")
                                    else:
                                        print("Opção inválida. Insira um número de 0 a 8 e tente novamente.")
