# 🌻 BYLA Bloom - Trabalho de Algoritmia

Repositório para o trabalho de grupo da cadeira de **Algoritmia e Programação** (2024/2025).
O objetivo é criar um programa em Python para gerir uma florista, convertendo a lógica que desenvolvemos antes em Flowgorithm.

# 🎯 Visão Geral do Código

Este projeto está desenhado para gerir um portal de acesso tanto para **utilizadores** como para **gestores**. A estrutura geral do código organiza-se da seguinte forma:

## Fluxo da Aplicação

1. **Ponto de entrada (`main`)**  
   - Todo o acesso ao portal começa pelo ficheiro `main.py`.  
   - O `main` é responsável por realizar as **validações de entrada**, verificando a identidade de quem acede.  
   - Dependendo do tipo de utilizador (utilizador comum ou gestor), o `main` redireciona para o portal correspondente.

2. **Portais específicos**  
   - Cada portal (utilizador ou gestor) assume que a validação já foi realizada pelo `main`.  
   - Isto significa que **cada portal não precisa de validar a entrada**, podendo concentrar-se apenas na sua funcionalidade específica.  
   - É fundamental importar as funções necessárias do gestor de base de dados para garantir a consistência e atualização automática dos dados.

## 📌 Gestão de Base de Dados 📌 ⚠️

- Vamos trabalhar com **ficheiros CSV** como base de dados.  
- O ficheiro `data_manager.py` contém funções para **ler, guardar e atualizar ficheiros CSV** de forma eficiente.  
- Cada portal deve importar apenas as funções que necessita para a sua operação.  
- Qualquer modificação nos dados deve ser refletida automaticamente no CSV, garantindo que a informação esteja sempre atualizada para qualquer novo acesso ao portal.

## 💻 Requisitos Técnicos

- É **imprescindível trabalhar com 🐼 `pandas` e 📈 `DataFrames`** para manipular os dados de forma eficiente.  
- O objetivo é criar um código **funcional e otimizado**, aproveitando ao máximo as capacidades do Python e do `pandas`.

## 🤝 Boas Práticas

- Evitar duplicação de código entre portais; centralizar a gestão de dados em `data_manager.py`.  
- Manter o fluxo de validação apenas em `main`.  
- Garantir que todas as modificações são corretamente escritas no CSV, para manter a integridade da base de dados.


## 👥 O Nosso Grupo

* **Gestão de Produtos:** Luís Gonçalves
* **Gestão de Encomendas:** Yeidman
* **Gestão de Clientes:** Beatriz
* **Distribuição:** André Silva
* **Reclamações e Avaliações, e `main`:** Tong Nguyen

---

## 🚧 Estado dos Módulos

### 1. Gestão de Produtos (`mod_product.py`)  
Este módulo `mod_product.py` implementa o sistema de **gestão de produtos** da florista BYLA Bloom, onde o gestor adiciona, altera, remove produtos, gere stock e consulta estatísticas do catálogo.

- Gere o catálogo completo de produtos em `products_stock.csv` com persistência automática.
- Permite operações CRUD (criar, ler, atualizar, remover) com validações robustas.
- Expõe **5 funções públicas de integração** para módulos de encomendas e portal cliente.
- Menu interativo (`menu_produtos()`) chamado a partir de `main.py`.

## Funções de validação e input

- `lerInteiro(mensagem)`: Captura input inteiro com proteção contra `ValueError`, loop até input válido.
- `lerFloat(mensagem)`: Captura input decimal (preços) com proteção contra `ValueError`.
- `validarTexto(mensagem)`: Valida que texto não está vazio, pede re-inserção se necessário.
- `validarNome()`: Valida nome do produto (≥ 1 caracter), bloqueia campos vazios.
- `validarStock()`: Valida quantidade de stock (≥ 0), impede valores negativos.
- `verificarPreco()`: Valida preço unitário (≥ 0), bloqueia preços negativos.
- `verificarDisponibilidade(opcaoOperacao)`: Valida input S/N para disponibilidade, reutilizável em adicionar/alterar/remover.
- `validarID()`: Valida que ID existe em `idsProduto`, mostra IDs disponíveis se inválido.

## Persistência de dados (CSV)

- `guardarProdutosCSV()`: Converte listas globais (`idsProduto`, `nomeProduto`, `stock`, etc.) para DataFrame Pandas e guarda em `products_stock.csv` com separador `;`. Converte `disponibilidade` S/N → `true`/`false`.
- `lerProdutosCSV()`: Carrega `products_stock.csv`, popula listas globais, converte `available` (`true`/`false` → S/N). Se ficheiro não existe, retorna `0` para criar produtos padrão.

## Gestão de produtos (CRUD)

- `adicionarProduto()`: 
  - Gera ID automático (`max(idsProduto) + 1` ou `1` se vazio).
  - Recolhe nome, descrição, categoria, preço, stock, disponibilidade com funções de validação.
  - Adiciona às listas globais (`idsProduto.append()`, etc.).
  - Chama `guardarProdutosCSV()` para persistir.
  - Confirma adição com exibição de dados.

- `alterarProduto()`:
  - Lista catálogo, pede ID com `validarID()`.
  - Mostra dados atuais do produto selecionado.
  - Menu secundário (1-Nome, 2-Descrição, 3-Categoria, 4-Tipo, 5-Preço, 6-Disponibilidade).
  - Atualiza lista específica (`nomeProduto[i] = ...`), persiste com `guardarProdutosCSV()`.
  - Loop até utilizador escolher "Concluir Alterações".

- `removerProduto()`:
  - Pede ID, mostra dados do produto a remover.
  - Confirmação S/N com `verificarDisponibilidade(3)`.
  - **Soft-delete:** Altera `disponibilidade[i] = "N"` (não remove das listas).
  - Persiste com `guardarProdutosCSV()`.

- `adicionarStock()`:
  - Pede ID e quantidade a adicionar (> 0).
  - Atualiza `stock[i] += quantidade`.
  - Se `stock` anterior era `0` e `disponibilidade` era "N", reativa produto (`disponibilidade[i] = "S"`).
  - Mostra stock anterior/novo, persiste alterações.

## Consulta e filtros

- `listarCatalogo()`: 
  - Lista todos os produtos com índice sequencial + ID real.
  - Mostra nome, descrição, categoria, tipo, preço, stock, estado (Disponível ✅ / Indisponível ❌).
  - Exibe total de produtos no final.

- `filtrarCatalogo()`:
  - Menu com 4 opções de filtro (Categoria, Disponibilidade, Preço, Stock).
  - **Categoria:** Filtra por `str.contains()` (case-insensitive), mostra `product_id`, nome, categoria, preço.
  - **Disponibilidade:** Filtra por `available == "true"/"false"`, mostra stock.
  - **Preço:** 3 sub-opções (igual, acima, abaixo), valida com `verificarPreco()`.
  - **Stock:** 3 sub-opções (igual, acima, abaixo), valida com `validarStock()`.
  - Usa Pandas para filtros (`df[df["price_unit"] > preco]`), blindagem de tipos com `pd.to_numeric()`.

- `verificarEstatisticas()`:
  - **Resumo Geral:** Total produtos, disponíveis, esgotados, valor total em stock (`sum(stock[i] * preço[i])`).
  - **TOP 5 Categorias:** Usa `value_counts().head(5)` para contar produtos/categoria.
  - **Preço Médio/Categoria:** Usa `groupby("category")["price_unit"].mean()`.

## Integração com outros módulos

- `validarStockDisponivel(idItem, quantidade)`:
  - Verifica se produto existe (`idItem in idsProduto`).
  - Verifica se está disponível (`disponibilidade[i] == "S"`).
  - Verifica se `stock[i] >= quantidade`.
  - **Usado por:** `mod_order_gestao.py` antes de aceitar encomenda.
  - Retorna `True`/`False`, imprime mensagens de erro.

- `reservarStock(idItem, quantidade)`:
  - Decrementa stock (`stock[i] -= quantidade`).
  - Se `stock[i] == 0`, marca como indisponível (`disponibilidade[i] = "N"`).
  - Mostra stock anterior → novo, persiste com `guardarProdutosCSV()`.
  - **Usado por:** `mod_order_gestao.py` após validação de encomenda.
  - Retorna `True`/`False`.

- `devolverStock(idItem, quantidade)`:
  - Incrementa stock (`stock[i] += quantidade`).
  - Se `stock[i] > 0`, reativa produto (`disponibilidade[i] = "S"`).
  - **Usado por:** `mod_order_gestao.py` em cancelamentos/rejeições.
  - Retorna `True`/`False`.

- `listarProdutosDisponiveis()`:
  - Carrega `products_stock.csv`, filtra `available == True` e `quantity_stock > 0`.
  - Exibe catálogo formatado (ID, nome, descrição, categoria, preço, stock).
  - **Usado por:** `mod_client.py` no portal cliente.
  - Retorna DataFrame com 6 colunas (`product_id`, `name_product`, `description`, `category`, `price_unit`, `quantity_stock`).

- `obterDetalhesProduto(idItem)`:
  - Carrega produto específico de CSV por `product_id`.
  - Retorna dicionário com 8 campos (`product_id`, `product_type`, `name_product`, etc.).
  - Exibe formatação visual com emojis (Estado: Disponível ✅ / Esgotado ❌ / Indisponível ❌).
  - **Usado por:** Todos os módulos para exibir detalhes de produto.

## Menu interativo

- `menu_produtos()`:
  - Menu principal com 8 opções + sair (0).
  - Valida input com `lerInteiro()`.
  - Opções: 1-Adicionar, 2-Alterar, 3-Remover, 4-Listar, 5-Filtrar, 6-Fazer Encomenda (simulação), 7-Adicionar Stock, 8-Estatísticas, 0-Voltar.
  - Ao sair (0), chama `guardarProdutosCSV()` e faz `return` para `main.py`.
  - Loop até utilizador escolher sair.

- `verificarEncomenda()`:
  - **Simulação de encomenda** (para testes internos, não usada em produção).
  - Lista produtos, pede ID e quantidade, valida stock, decrementa e persiste.

## Dados padrão

Se `products_stock.csv` não existir ao iniciar (`numProdutos == 0`), cria **3 produtos padrão**:
1. **Girassol** (ID: 1, Categoria: Flor, Preço: 5.0€, Stock: 10)
2. **Rosa** (ID: 2, Categoria: Flor, Preço: 7.0€, Stock: 20)
3. **Orquídea** (ID: 3, Categoria: Planta, Preço: 27.5€, Stock: 1)
---

### 2. Gestão de Encomendas (`mod_order_gestao.py`) - 

Este módulo `mod_order_gestao.py` implementa o sistema de **gestão de encomendas** para gestores (Sénior/Júnior), onde validam pedidos, editam dados, atribuem estafetas e filtram por zona.

- Gere encomendas em `orders.csv`, itens em `order_items.csv`, eventos em `order_events.csv`.
- Distingue permissões entre Gestor Sénior (validar/rejeitar) e Gestor Júnior (só visualizar/editar).
- Integra com `mod_product.py` para validação/devolução de stock.
- Regista todas as ações em `order_events.csv` para auditoria completa.

## Tipos de utilizadores

- **Gestor Sénior (Manager = "SUPm"):** Permissões completas, incluindo validação automática e rejeição de encomendas.
- **Gestor Júnior:** Permissões restritas, não pode validar ou rejeitar. Tentativas repetidas bloqueiam acesso temporariamente.

## Funções de registo de eventos

- `registar_evento(order_id, tipo_evento, detalhes, manager)`:
  - Cria dicionário com `event_id` (formato `EV_YYYYMMDDHHMMSS`), `order_id`, `event_type`, `login` (manager), `details`.
  - Adiciona timestamps (`staptime_1`, `staptime_2`), latitude/longitude vazios.
  - **Usado por:** Todas as operações de edição, validação, rejeição, atribuição.
  - Retorna dicionário pronto para `pd.concat()` em `order_events.csv`.

## Funções de menu

- `menu_principal_pedidos()`: Menu com 6 opções (Ver Pendentes, Validados, Cancelados, Atribuir Estafeta, Filtrar Zona, Voltar). Valida input 1-6, loop até escolha válida.
- `menu_editar_pedido(order_id)`: Menu secundário com 8 opções (editar nome/contacto/morada/CP, validar, rejeitar, voltar). Retorna escolha 1-8.
- `menu_filtrar_zona()`: Menu com 7 opções (Centro, Norte, Sul, Este, Oeste, Fora do limite, Voltar). Retorna escolha 1-7.

## Funções de edição de encomendas

- `editar_nome(orders_df, order_id, manager, order_events_df)`:
  - Mostra nome atual, pede novo nome (validação não vazio).
  - Atualiza `orders_df.loc[..., "name"]`, persiste com `save_orders()`.
  - Regista evento `"edit_name"` com detalhes "Nome alterado de X para Y".
  - **Usado por:** Menu edição pedidos pendentes.
  - Retorna `orders_df`, `order_events_df` atualizados.

- `editar_contacto(orders_df, order_id, manager, order_events_df)`:
  - Mostra contacto atual, pede novo (ex: "961234567").
  - Atualiza `contact`, regista evento `"edit_contact"`.
  - Retorna DataFrames atualizados.

- `editar_morada(orders_df, order_id, manager, order_events_df)`:
  - Mostra morada atual, pede nova (ex: "Rua Principal, nº 42").
  - Atualiza `address`, regista evento `"edit_address"`.
  - Retorna DataFrames atualizados.

- `editar_codigo_postal(orders_df, order_id, manager, order_events_df)`:
  - Mostra CP atual (ZP1-ZP2), pede novo em 2 partes (ex: "4750" + "123").
  - Atualiza `ZP1`, `ZP2`, regista evento `"edit_postal_code"`.
  - Retorna DataFrames atualizados.

## Validação e rejeição

- **Validação automática (opção 7, só Sénior):**
  - Chama `ut.address_validation(pedido)` para verificar morada.
  - Chama `ut.recipient_validation(pedido)` para verificar dados destinatário.
  - Chama `ut.stock_validation(items_pedido, products_df)` para verificar stock disponível.
  - Se tudo válido: `order_status → "validated"`, `status → "shipped"` nos itens, regista evento `"auto_validate"`.
  - Se falhar: Mostra motivo específico (morada/destinatário/stock inválidos).

- **Rejeição (opção 6, só Sénior):**
  - Chama `ut.reject_order()` que atualiza `order_status → "canceled"`, `status → "canceled"` nos itens.
  - Devolve stock automaticamente com `mod_product.devolverStock()`.
  - Regista evento com motivo da rejeição.

## Atribuição de estafeta

- **Atribuir estafeta (opção 4):**
  - Filtra pedidos `validated` ou `partially_shipped` **sem** estafeta (`id_worker` vazio/NaN).
  - Para cada pedido: Chama `ut.code_zone(ZP1, df_zone, df_user_worker)` que determina zona pelo código postal.
  - Atribui estafeta disponível daquela zona automaticamente.
  - Atualiza `orders_df.loc[..., "id_worker"]`, regista evento `"assign_courier"` com zona.
  - **Usado por:** Gestor após validação de encomendas.

## Filtragem por zona

- **Filtrar por zona (opção 5):**
  - Menu com 7 zonas (Centro, Norte, Sul, Este, Oeste, Fora do limite, Voltar).
  - Filtra `user_work_profil.csv` para estafetas da zona (`duty_area.startswith("Gestor_")` == False).
  - Junta (`pd.merge`) pedidos validados com estafetas da zona.
  - Mostra lista formatada com `ut.show_details_destinatario()`.

## Visualização de encomendas

- **Ver Pendentes (opção 1):**
  - Filtra `order_status == "pending"`.
  - Lista pedidos, utilizador escolhe ID para ver detalhes com `ut.show_details_order()`.
  - Entra em loop de edição (menu_editar_pedido).

- **Ver Validados (opção 2):**
  - Filtra `order_status.isin(["validated", "partially_shipped"])`.
  - Navegação pedido-a-pedido (1-Próximo, 2-Sair).

- **Ver Cancelados (opção 3):**
  - Filtra `order_status == "canceled"`.
  - Mostra motivo (`order_reason`), navegação pedido-a-pedido.

## Função principal

- `ModOrderGestao(Manager)`:
  - Verifica se `Manager == "SUPm"` para permissões.
  - Carrega DataFrames: `load_orders()`, `load_order_items()`, `load_products()`, `load_order_events()`, `load_user_work_profil()`.
  - Loop principal com `menu_principal_pedidos()`, redireciona para opções específicas.
  - **Chamado por:** `main.py` após login de gestor.

---

### 3. Portal Cliente (`mod_client.py`) - 

Este módulo `mod_client.py` implementa o **portal de cliente** onde utilizadores se registam, criam encomendas, consultam pedidos e fazem avaliações do serviço.

- Gere registo e persistência de clientes em `login_client.csv`.
- Permite criar encomendas, escolher produtos, atualizar stock e eventos.
- Integra com `mod_product.py` para validar/reservar stock.
- Expõe menu interativo (`welcome_client()`) chamado de `main.py`.

## Gestão de clientes

- `load_clients()`: Carrega `login_client.csv`, cria DataFrame vazio com colunas base se não existir (`id_client`, `name`, `contact`, `password`, `address`, `ZP1`, `ZP2`).
- `save_clients(df_clients)`: Guarda DataFrame em `login_client.csv` com separador `;`.
- `generate_new_client_id(df_clients)`: Gera ID sequencial formato `CL001`, `CL002`, assume padrão `CLxxx`. Encontra maior ID existente, incrementa.
- `register_new_client()`:
  - Recolhe nome, contacto, password, morada, CP (ZP1, ZP2).
  - Valida inputs não vazios (loops até válido).
  - Gera ID com `generate_new_client_id()`, adiciona a `df_clients`.
  - Persiste com `save_clients()`, retorna `id_client` criado.
  - **Usado por:** `welcome_client()` se cliente novo.

## Criação de encomendas

- `generate_new_order_id(orders_df)`: Cria ID sequencial formato `PT01`, `PT02`, extrai número de `PTxx`, incrementa.
- `create_new_order(id_client)`:
  - Carrega dados cliente de `login_client.csv`, valida existência.
  - Cria registo em `orders` com `order_status="pending"`, `id_worker` vazio, dados cliente (nome, contacto, morada, CP).
  - Lista produtos disponíveis com `dm.load_products()` (filtro `available == True`, `quantity_stock > 0`).
  - Loop de seleção: Pede `product_id` e quantidade, valida stock.
  - Adiciona itens a `order_items` com `status="processing"`.
  - Atualiza stock com `mod_product.reservarStock()`, marca `available=False` se esgotou.
  - Persiste `orders` com `dm.save_orders()`, `order_items` com `dm.save_order_items()`.
  - Regista evento `"created"` em `order_events.csv` com timestamp.
  - **Usado por:** Portal cliente após login.

## Consulta de encomendas

- `list_my_orders(id_client)`:
  - Carrega `orders`, filtra por `id_client`.
  - Delega em `order_filters()` (em `utils.py`) para menu de filtros (Todas, Pendentes, Validadas, Entregues, Canceladas).
  - **Usado por:** Portal cliente opção "Ver Minhas Encomendas".

- `show_order_details_client(id_client)`:
  - Filtra encomendas do cliente, lista `order_id` e estados.
  - Pede `order_id` específico, valida pertença ao cliente.
  - Carrega itens com `load_order_items()`, produtos com `load_products()`.
  - Chama `showDetailsOrder()` (de `utils.py`) para exibir detalhes completos (destinatário, produtos, quantidades, preços).
  - **Usado por:** Portal cliente opção "Ver Detalhes de Pedido".

## Avaliações

- `rate_delivered_order(id_client)`:
  - Filtra encomendas com `order_status == "entregue"` do cliente.
  - Lista pedidos entregues, pede `order_id` a avaliar.
  - Recolhe rating (1 a 5, validação numérica) e comentário opcional.
  - Verifica existência de `avaliacoes.csv`, cria se não existir.
  - Adiciona registo: `order_id`, `id_client`, `rating`, `comment`, `timestamp`.
  - Persiste avaliação, confirma submissão.
  - **Usado por:** Portal cliente após entrega.

## Portal interativo

- `welcome_client(id_client)`:
  - Se `id_client` vazio, chama `register_new_client()` e carrega nome para saudação.
  - Menu com 5 opções: 1-Nova Encomenda, 2-Ver Encomendas, 3-Detalhes Pedido, 4-Avaliar Encomenda, 0-Sair.
  - Encaminha opções para `create_new_order()`, `list_my_orders()`, `show_order_details_client()`, `rate_delivered_order()`.
  - Loop até utilizador escolher sair (0).
  - **Chamado por:** `main.py` após login de cliente.

---

### 4. Portal Estafeta (`mod_delivery.py`) - 

Este módulo `mod_delivery.py` implementa o **portal de estafeta** onde trabalhadores aceitam/recusam encomendas, registam entregas e consultam estatísticas.

- Gere encomendas atribuídas ao estafeta (`id_worker`).
- Gera coordenadas GPS aleatórias por zona para simular entregas.
- Regista eventos de aceitação/recusa/entrega em `order_events.csv`.
- Calcula estatísticas de desempenho (taxa de sucesso).

**Referência de localização:** Universidade do Minho, Campus Gualtar (Lat: `41.560177`, Lon: `-8.397281`)

## Funções de geração de coordenadas

- `convert_meters_to_degrees(lat_ref, meters_north=0.0, meters_east=0.0)`:
  - Converte metros em graus de latitude/longitude.
  - Aproximação: 1º latitude ≈ 111.000m, longitude ajustada por `cos(latitude)`.
  - **Usado por:** `random_point()`, `generate_coordinates()`.
  - Retorna `(lat_moviment, lon_moviment)`.

- `random_point(lat, lon, meters_radius=5000)`:
  - Gera coordenada aleatória dentro de raio (metros) ao redor de ponto base.
  - Escolhe ângulo (`0` a `2π`) e distância aleatórios uniformemente.
  - Converte para graus com `convert_meters_to_degrees()`, soma a lat/lon base.
  - **Usado por:** `generate_coordinates()` para dispersão.
  - Retorna `(latitude, longitude)` arredondados a 6 decimais.

- `generate_coordinates(zone)`:
  - Gera coordenada em zona específica ("Center", "North", "South", "East", "West").
  - Define deslocamentos (±50km) por zona a partir de `(lat_center, lon_center)`.
  - Cria ponto âncora (centro da zona), adiciona dispersão aleatória (±5km) com `random_point()`.
  - **Usado por:** `delivery_orders()`, `decline_delivery()` para registar localização.
  - Retorna `(latitude, longitude)`.

## Funções de gestão de encomendas

- `show_orders(orders_df, id_worker)`:
  - Filtra encomendas com `id_worker == id_worker` atribuído.
  - Mostra listagem formatada: `order_id`, cliente, contacto, morada, CP, estado, motivo.
  - **Usado por:** Portal estafeta ao iniciar sessão.
  - Retorna DataFrame filtrado ou `None` se vazio.

- `accept_order(orders_df, events_df, order_id, id_worker)`:
  - Valida existência de `order_id`.
  - Atualiza `order_status → "em distribuição"` (ou similar).
  - Cria evento com `create_event()`: tipo `"aceite"`, timestamp, coordenadas (0,0).
  - Adiciona a `events_df` com `pd.concat()`.
  - **Usado por:** Estafeta ao aceitar encomenda.
  - Retorna `orders_df`, `events_df` atualizados.

- `decline_orders(orders_df, events_df, order_id, id_worker)`:
  - Pede motivo da recusa (input obrigatório).
  - Atualiza `order_status → "recusada"`, `order_reason` com motivo.
  - Cria evento tipo `"recusada"` com coordenadas fixas.
  - **Usado por:** Estafeta ao recusar encomenda atribuída.
  - Retorna `orders_df`, `events_df` atualizados.

- `delivery_orders(orders_df, events_df, order_id, id_worker)`:
  - Verifica estado `"em distribuição"`.
  - Gera coordenadas da zona de trabalho com `generate_coordinates()`.
  - Pede nome do recebedor (input).
  - Atualiza `order_status → "entregue"`.
  - Cria evento tipo `"entregue"` com detalhes (recebedor) e coordenadas GPS.
  - **Usado por:** Estafeta ao confirmar entrega.
  - Retorna `orders_df`, `events_df` atualizados.

- `decline_delivery(orders_df, events_df, order_id, id_worker)`:
  - Permite recusa apenas se estado `"em distribuição"`.
  - Menu com motivos predefinidos (Cliente ausente, Morada errada, Recusa receber, Outros).
  - Pede descrição adicional (input livre).
  - Gera coordenadas da zona com `generate_coordinates()`.
  - Atualiza `order_status → "não entregue"`, `order_reason` com motivo.
  - Cria evento tipo `"não entregue"` com coordenadas.
  - **Usado por:** Estafeta em tentativa de entrega falhada.
  - Retorna `orders_df`, `events_df` atualizados.

## Estatísticas

- `statistic_events(orders, estafeta_id)`:
  - Filtra encomendas atribuídas a `estafeta_id`.
  - Conta por estado: aceites, recusadas, entregues, não entregues.
  - Calcula taxa de sucesso: `(entregues / (aceites + não_entregues)) × 100`.
  - Mostra resumo formatado com total de encomendas e percentagem.
  - **Usado por:** Portal estafeta opção "Ver Estatísticas".

## Portal interativo

- `main_delivery(id_worker)`:
  - Carrega `orders`, `events`, `user_work_profil`.
  - Mostra encomendas atribuídas com `show_orders()`.
  - Menu com opções: 1-Aceitar, 2-Recusar, 3-Entregar, 4-Recusar Entrega, 5-Estatísticas, 0-Sair.
  - Redireciona para funções específicas conforme escolha.
  - Persiste alterações com `save_orders()`, `save_order_events()`.
  - **Chamado por:** `main.py` após login de estafeta.

---

### 5. Reclamações (`mod_complaint.py`) 

Este módulo `mod_complaint.py` implementa o sistema de **reclamações** para clientes insatisfeitos, permitindo registar queixas sobre encomendas com priorização automática.

- Valida que reclamação pertence ao cliente atual e ao seu pedido.
- Atribui prioridades automáticas baseadas no tipo de problema e estado da encomenda.
- Persiste reclamações em `complaints.csv` através de `data_manager`.

## Registo de reclamação

- `process_smart_complaint(current_client_id)`:
  - Carrega `orders` com `data_manager.load_orders()`, `complaints` com `data_manager.load_complaints()`.
  - Pede `order_id`, valida existência e pertença ao `current_client_id` (bloqueia reclamações de outros clientes).
  - Verifica histórico: Se já existe reclamação no mesmo pedido, pede confirmação para continuar.
  - Extrai `id_worker` (shipper) do pedido para `accused_shipper` (ou "Unknown" se vazio).
  - **Usado por:** Portal cliente após problemas com encomenda.

## Seleção de motivos e priorização

- **Motivos pré-definidos com prioridades automáticas:**
  1. **Late Delivery:** `High` se `order_status == "Pending"`, senão `Normal`.
  2. **Damaged Product:** `URGENT` (sempre).
  3. **Wrong Item:** `High` (sempre).
  4. **Rude Shipper:** `Medium` (sempre).
  5. **Other:** `Low` (sempre).
  
- Utilizador escolhe motivo (1-5), sistema atribui prioridade automaticamente.
- Pede descrição detalhada (input livre, `content`).

## Persistência

- Cria registo com campos: `order_id`, `client_id`, `accused_shipper`, `reason_type`, `priority`, `content`, `date_created` (timestamp), `status="Open"`.
- Adiciona a `df_complaints` com `pd.concat()`.
- Guarda com `data_manager.save_complaints(df_complaints)`.
- Confirma registo com exibição da prioridade atribuída e timestamp.
- **Usado por:** Portal cliente opção "Fazer Reclamação".

---
