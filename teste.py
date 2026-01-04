# -*- coding: utf-8 -*-
"""
EXEMPLO DE TESTES DO SISTEMA DE LOGIN
Este arquivo demonstra como usar as funções de autenticação
"""

from data_manager_updated import authenticate_user, load_all_clients_for_login, load_all_staff_for_login

def test_login_system():
    """Testa o sistema de login com dados reais dos CSVs"""
    
    print("=" * 60)
    print("TESTE DO SISTEMA DE AUTENTICAÇÃO")
    print("=" * 60)
    
    # Exibir clientes disponíveis
    print("\n📋 CLIENTES DISPONÍVEIS PARA LOGIN:")
    print("-" * 60)
    df_clients = load_all_clients_for_login()
    if not df_clients.empty:
        for idx, row in df_clients.iterrows():
            print(f"  • Nome: {row['name']}")
            print(f"    ID (Telemóvel): {row['id']}")
            print(f"    Senha: {row['pass']}")
            print()
    
    # Exibir staff disponível
    print("📋 GESTORES E ESTAFETAS DISPONÍVEIS PARA LOGIN:")
    print("-" * 60)
    df_staff = load_all_staff_for_login()
    if not df_staff.empty:
        for idx, row in df_staff.iterrows():
            print(f"  • ID: {row['id']}")
            print(f"    Tipo: {row['role'].replace('_', ' ').title()}")
            print(f"    Área: {row['duty_area']}")
            print(f"    Senha: {row['pass']}")
            print()
    
    # Testes de login
    print("\n" + "=" * 60)
    print("TESTANDO LOGINS")
    print("=" * 60)
    
    # Teste 1: Cliente com sucesso
    print("\n✅ Teste 1: Login de Cliente (SUCESSO ESPERADO)")
    print("-" * 60)
    user_id = "961219231"  # Telemóvel do Joao Pereira
    password = "client1"
    result = authenticate_user(user_id, password)
    if result:
        print(f"✓ Login bem-sucedido!")
        print(f"  Tipo: {result['type']}")
        print(f"  Nome: {result['name']}")
        print(f"  Role: {result['role']}")
        print(f"  → Direcionado para: PORTAL DE CLIENTE")
    else:
        print(f"✗ Falha no login")
    
    # Teste 2: Cliente com senha errada
    print("\n❌ Teste 2: Login de Cliente")