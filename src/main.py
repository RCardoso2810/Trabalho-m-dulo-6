# ══════════════════════════════════════════════════════════════
#  main.py
#  Menu terminal — menu principal + sub-menus por modulo
# ══════════════════════════════════════════════════════════════

from cliente import (
    criar_cliente, ler_cliente_por_id, listar_todos_clientes,
    atualizar_cliente, remover_cliente, CAMPOS_EDITAVEIS_CLIENTE,
)
from jogo import (
    criar_jogo, ler_jogo_por_id, listar_todos_jogos,
    atualizar_jogo, remover_jogo, CAMPOS_EDITAVEIS_JOGO,
)
from transacao import (
    criar_transacao, ler_transacao_por_id, listar_todas_transacoes,
    listar_transacoes_por_cliente, atualizar_transacao, remover_transacao,
    CAMPOS_EDITAVEIS_TRANSACAO,
)
from casino import (
    criar_casino, ler_casino_por_id, listar_todos_casinos,
    atualizar_casino, remover_casino, adicionar_item_sala,
    remover_item_sala, listar_sala, CAMPOS_EDITAVEIS_CASINO,
)


# ══════════════════════════════════════════════════════════════
#  SUB-MENU CLIENTES
# ══════════════════════════════════════════════════════════════

def menu_clientes():
    while True:
        print("\n--- CLIENTES ---")
        print("1 - Criar cliente")
        print("2 - Listar clientes")
        print("3 - Consultar cliente")
        print("4 - Atualizar cliente")
        print("5 - Remover cliente")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome          = input("Nome: ")
            data_nasc     = input("Data nascimento (DD/MM/AAAA): ")
            genero        = input("Genero (M/F/OUTRO): ")
            nacionalidade = input("Nacionalidade: ")
            contacto      = input("Contacto (telefone / email): ")
            saldo         = input("Saldo inicial (EUR): ")
            nivel         = input("Nivel (BRONZE/PRATA/OURO/PLATINA/VIP): ")
            estado        = input("Estado (ATIVO/INATIVO): ")
            code, obj = criar_cliente(nome, data_nasc, genero, nacionalidade,
                                      contacto, saldo, nivel, estado)
            if code == 201:
                print(f"[{code}] Cliente criado com sucesso.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "2":
            code, obj = listar_todos_clientes()
            if code == 200:
                print(f"[{code}] {len(obj)} cliente(s) encontrado(s).")
                for c in obj:
                    print(c)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "3":
            id_c = input("ID do cliente: ")
            code, obj = ler_cliente_por_id(id_c)
            if code == 200:
                print(f"[{code}] Cliente encontrado.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "4":
            id_c  = input("ID do cliente: ")
            print(f"Campos editaveis: {' | '.join(CAMPOS_EDITAVEIS_CLIENTE)}")
            campo = input("Campo a editar: ")
            valor = input("Novo valor: ")
            code, obj = atualizar_cliente(id_c, campo, valor)
            if code == 200:
                print(f"[{code}] Cliente actualizado com sucesso.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "5":
            id_c = input("ID do cliente: ")
            code, obj = remover_cliente(id_c)
            if code == 200:
                print(f"[{code}] {obj}")
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "0":
            break
        else:
            print("[400] Opcao invalida.")


# ══════════════════════════════════════════════════════════════
#  SUB-MENU JOGOS
# ══════════════════════════════════════════════════════════════

def menu_jogos():
    while True:
        print("\n--- JOGOS ---")
        print("1 - Criar jogo")
        print("2 - Listar jogos")
        print("3 - Consultar jogo")
        print("4 - Atualizar jogo")
        print("5 - Remover jogo")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome      = input("Nome do jogo: ")
            custo_min = input("Custo minimo (EUR): ")
            saldo_j   = input("Saldo da banca (EUR): ")
            retorno   = input("Retorno (ex: 35 ou -0.5): ")
            nivel_ac  = input("Nivel acesso (BRONZE/PRATA/OURO/PLATINA/VIP): ")
            estado    = input("Estado (ATIVO/INATIVO): ")
            dealer    = input("Tem dealer? (SIM/NAO): ")
            tabuleiro = input("Tem tabuleiro? (SIM/NAO): ")
            pecas     = input("Tem pecas? (SIM/NAO): ")
            cartas    = input("Tem cartas? (SIM/NAO): ")
            dados     = input("Tem dados? (SIM/NAO): ")
            maquina   = input("E uma maquina/slot? (SIM/NAO): ")
            code, obj = criar_jogo(nome, custo_min, saldo_j, retorno, nivel_ac, estado,
                                   dealer, tabuleiro, pecas, cartas, dados, maquina)
            if code == 201:
                print(f"[{code}] Jogo criado com sucesso.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "2":
            code, obj = listar_todos_jogos()
            if code == 200:
                print(f"[{code}] {len(obj)} jogo(s) encontrado(s).")
                for j in obj:
                    print(j)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "3":
            id_j = input("ID do jogo: ")
            code, obj = ler_jogo_por_id(id_j)
            if code == 200:
                print(f"[{code}] Jogo encontrado.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "4":
            id_j  = input("ID do jogo: ")
            print(f"Campos editaveis: {' | '.join(CAMPOS_EDITAVEIS_JOGO)}")
            campo = input("Campo a editar: ")
            valor = input("Novo valor: ")
            code, obj = atualizar_jogo(id_j, campo, valor)
            if code == 200:
                print(f"[{code}] Jogo actualizado com sucesso.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "5":
            id_j = input("ID do jogo: ")
            code, obj = remover_jogo(id_j)
            if code == 200:
                print(f"[{code}] {obj}")
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "0":
            break
        else:
            print("[400] Opcao invalida.")


# ══════════════════════════════════════════════════════════════
#  SUB-MENU TRANSACOES
# ══════════════════════════════════════════════════════════════

def menu_transacoes():
    while True:
        print("\n--- TRANSACOES ---")
        print("1 - Criar transacao")
        print("2 - Listar transacoes")
        print("3 - Consultar transacao")
        print("4 - Listar transacoes por cliente")
        print("5 - Atualizar transacao")
        print("6 - Remover transacao")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            id_cli   = input("ID do cliente (ex: CLI0001): ")
            tipo     = input("Tipo (ENTRADA/SAIDA): ")
            tipo_mov = input("Tipo de movimento (ENTRADA/SAIDA): ")
            montante = input("Montante (EUR): ")
            metodo   = input("Metodo de pagamento (DINHEIRO/CARTAO/TRANSFERENCIA/CRYPTO): ")
            estado   = input("Estado (PENDENTE/CONCLUIDA/CANCELADA): ")
            code, obj = criar_transacao(id_cli, tipo, tipo_mov, montante, metodo, estado)
            if code == 201:
                print(f"[{code}] Transacao criada com sucesso.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "2":
            code, obj = listar_todas_transacoes()
            if code == 200:
                print(f"[{code}] {len(obj)} transacao(oes) encontrada(s).")
                for t in obj:
                    print(t)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "3":
            id_t = input("ID da transacao (ex: TRN00001): ")
            code, obj = ler_transacao_por_id(id_t)
            if code == 200:
                print(f"[{code}] Transacao encontrada.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "4":
            id_cli = input("ID do cliente (ex: CLI0001): ")
            code, obj = listar_transacoes_por_cliente(id_cli)
            if code == 200:
                print(f"[{code}] {len(obj)} transacao(oes) encontrada(s).")
                for t in obj:
                    print(t)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "5":
            id_t  = input("ID da transacao: ")
            print(f"Campos editaveis: {' | '.join(CAMPOS_EDITAVEIS_TRANSACAO)}")
            campo = input("Campo a editar: ")
            valor = input("Novo valor: ")
            code, obj = atualizar_transacao(id_t, campo, valor)
            if code == 200:
                print(f"[{code}] Transacao actualizada com sucesso.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "6":
            id_t = input("ID da transacao: ")
            code, obj = remover_transacao(id_t)
            if code == 200:
                print(f"[{code}] {obj}")
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "0":
            break
        else:
            print("[400] Opcao invalida.")


# ══════════════════════════════════════════════════════════════
#  SUB-MENU CASINOS
# ══════════════════════════════════════════════════════════════

def menu_casinos():
    while True:
        print("\n--- CASINOS ---")
        print("1 - Criar casino")
        print("2 - Listar casinos")
        print("3 - Consultar casino")
        print("4 - Atualizar casino")
        print("5 - Remover casino")
        print("6 - Adicionar item a sala (jogo/funcionario/cliente)")
        print("7 - Remover item de sala (jogo/funcionario/cliente)")
        print("8 - Listar sala (jogos/funcionarios/clientes)")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome  = input("Nome do casino: ")
            loc   = input("Localizacao: ")
            taxa  = input("Taxa/imposto (%): ")
            moeda = input("Moeda (EUR/USD/GBP/CHF/JPY): ")
            cap   = input("Capacidade maxima: ")
            code, obj = criar_casino(nome, loc, taxa, moeda, cap)
            if code == 201:
                print(f"[{code}] Casino criado com sucesso.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "2":
            code, obj = listar_todos_casinos()
            if code == 200:
                print(f"[{code}] {len(obj)} casino(s) encontrado(s).")
                for c in obj:
                    print(c)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "3":
            id_cas = input("ID do casino (ex: CAS0001): ")
            code, obj = ler_casino_por_id(id_cas)
            if code == 200:
                print(f"[{code}] Casino encontrado.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "4":
            id_cas = input("ID do casino: ")
            print(f"Campos editaveis: {' | '.join(CAMPOS_EDITAVEIS_CASINO)}")
            campo  = input("Campo a editar: ")
            valor  = input("Novo valor: ")
            code, obj = atualizar_casino(id_cas, campo, valor)
            if code == 200:
                print(f"[{code}] Casino actualizado com sucesso.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "5":
            id_cas = input("ID do casino: ")
            code, obj = remover_casino(id_cas)
            if code == 200:
                print(f"[{code}] {obj}")
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "6":
            id_cas  = input("ID do casino: ")
            tipo    = input("Tipo (jogos/funcionarios/clientes): ")
            item_id = input("ID do item a adicionar: ")
            code, obj = adicionar_item_sala(id_cas, tipo, item_id)
            if code == 200:
                print(f"[{code}] Item adicionado com sucesso.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "7":
            id_cas  = input("ID do casino: ")
            tipo    = input("Tipo (jogos/funcionarios/clientes): ")
            item_id = input("ID do item a remover: ")
            code, obj = remover_item_sala(id_cas, tipo, item_id)
            if code == 200:
                print(f"[{code}] Item removido com sucesso.")
                print(obj)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "8":
            id_cas = input("ID do casino: ")
            tipo   = input("Tipo (jogos/funcionarios/clientes): ")
            code, obj = listar_sala(id_cas, tipo)
            if code == 200:
                print(f"[{code}] {len(obj)} item(ns) encontrado(s).")
                for item in obj:
                    print(item)
            else:
                print(f"[{code}] Erro: {obj}")

        elif opcao == "0":
            break
        else:
            print("[400] Opcao invalida.")


# ══════════════════════════════════════════════════════════════
#  MENU PRINCIPAL
# ══════════════════════════════════════════════════════════════

def menu_principal():
    while True:
        print("\n====== MENU PRINCIPAL — CASINO ======")
        print("1 - Clientes")
        print("2 - Jogos")
        print("3 - Transacoes")
        print("4 - Casinos")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            menu_clientes()
        elif opcao == "2":
            menu_jogos()
        elif opcao == "3":
            menu_transacoes()
        elif opcao == "4":
            menu_casinos()
        elif opcao == "0":
            print("A sair...")
            break
        else:
            print("[400] Opcao invalida.")


if __name__ == "__main__":
    menu_principal()
