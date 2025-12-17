# 🌻 BYLA Bloom - Trabalho de Algoritmia

Repositório para o trabalho de grupo da cadeira de **Algoritmia e Programação** (2024/2025).
O objetivo é criar um programa em Python para gerir uma florista, convertendo a lógica que desenvolvemos antes em Flowgorithm.

# Visão Geral do Código

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

## Gestão de Base de Dados

- Vamos trabalhar com **ficheiros CSV** como base de dados.  
- O ficheiro `data_manager.py` contém funções para **ler, guardar e atualizar ficheiros CSV** de forma eficiente.  
- Cada portal deve importar apenas as funções que necessita para a sua operação.  
- Qualquer modificação nos dados deve ser refletida automaticamente no CSV, garantindo que a informação esteja sempre atualizada para qualquer novo acesso ao portal.

## Requisitos Técnicos

- É **imprescindível trabalhar com `pandas` e `DataFrames`** para manipular os dados de forma eficiente.  
- O objetivo é criar um código **funcional e otimizado**, aproveitando ao máximo as capacidades do Python e do `pandas`.

## Boas Práticas

- Evitar duplicação de código entre portais; centralizar a gestão de dados em `data_manager.py`.  
- Manter o fluxo de validação apenas em `main`.  
- Garantir que todas as modificações são corretamente escritas no CSV, para manter a integridade da base de dados.


## 👥 O Nosso Grupo

* **Gestão de Produtos:** Luís Gonçalves
* **Gestão de Encomendas:** Yeidman
* **Gestão de Clientes:** Beatriz
* **Distribuição:** André Silva

---

## 🚧 Estado dos Módulos

### 1. Gestão de Produtos (`mod_product.py`)

Nesta fase inicial (V1), este módulo já replica a lógica do fluxograma original. Ainda não utiliza ficheiros (CSV) nem Pandas, mantendo os dados em listas/arrays na memória durante a execução.

**O que já funciona:**
* ✅ **Catálogo:** Listagem completa de flores e plantas.
* ✅ **Gestão:** Adicionar novos produtos e remover antigos (com reordenação de listas).
* ✅ **Stock:** Entrada de stock e verificação de produtos esgotados.
* ✅ **Validações:** Impede preços negativos e nomes vazios.
* ✅ **Estatísticas:** Cálculo do valor total em armazém.

**Próximos passos:**
* Implementar persistência de dados (CSV).
* Integração com Pandas (Parte II).

---

### 2. Gestão de Encomendas (`mod_delivery.py`)
*(Em desenvolvimento...)*

---

### 3. Gestão de Clientes (`mod_client.py`)
*(Em desenvolvimento...)*

---

### 4. Distribuição (`mod_delivery.py`)
*(Em desenvolvimento...)*

---

