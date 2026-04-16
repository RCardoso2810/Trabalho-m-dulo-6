# ══════════════════════════════════════════════════════════════
#  main.py
#  Menu terminal para testar CRUD de clientes e jogos
# ══════════════════════════════════════════════════════════════

from cliente import (
    criar_cliente,
    ler_cliente_por_id,
    listar_todos_clientes,
    atualizar_cliente,
    remover_cliente,
    CAMPOS_EDITAVEIS_CLIENTE,
)

from jogo import (
    criar_jogo,
    ler_jogo_por_id,
    listar_todos_jogos,
    listar_jogos_ativos,
    atualizar_jogo,
    remover_jogo,
    CAMPOS_EDITAVEIS_JOGO,
    CAMPOS_TIPOS,
)


# ══════════════════════════════════════════════════════════════
#  MENUS
# ══════════════════════════════════════════════════════════════

def menu():
    print("\n===== MENU CASINO =====")
    print("--- CLIENTES ---")
    print("1 - Criar cliente")
    print("2 - Listar clientes")
    print("3 - Consultar cliente")
    print("4 - Atualizar cliente")
    print("5 - Remover cliente")
    print("--- JOGOS ---")
    print("6 - Criar jogo")
    print("7 - Listar jogos")
    print("8 - Consultar jogo")
    print("9 - Atualizar jogo")
    print("10 - Remover jogo")
    print("0 - Sair")


# ══════════════════════════════════════════════════════════════
#  PROGRAMA PRINCIPAL
# ══════════════════════════════════════════════════════════════

def main():
    while True:
        menu()
        opcao = input("Escolha uma opcao: ").strip()

        # ── CLIENTES ─────────────────────────────────────────

        if opcao == "1":
            nome          = input("Nome: ")
            data_nasc     = input("Data nascimento (DD/MM/AAAA): ")
            genero        = input("Genero (M/F/OUTRO): ")
            nacionalidade = input("Nacionalidade: ")
            contacto      = input("Contacto (telefone / email): ")
            saldo         = input("Saldo inicial (EUR): ")
            nivel         = input("Nivel (BRONZE/PRATA/OURO/PLATINA/VIP): ")
            estado        = input("Estado (ATIVO/INATIVO): ")
            rc = criar_cliente(nome, data_nasc, genero, nacionalidade,
                               contacto, saldo, nivel, estado)
            if rc["status"] == ativo:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")
                print(rc["dados"])
            else:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")

        elif opcao == "2":
            rc = listar_todos_clientes()
            if rc["status"] == 200:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")
                for c in rc["dados"]:
                    print(c)
            else:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")

        elif opcao == "3":
            id_c = input("ID do cliente: ")
            rc = ler_cliente_por_id(id_c)
            if rc["status"] == 200:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")
                print(rc["dados"])
            else:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")

        elif opcao == "4":
            id_c  = input("ID do cliente: ")
            print(f"Campos editaveis: {' | '.join(CAMPOS_EDITAVEIS_CLIENTE)}")
            campo = input("Campo a editar: ")
            valor = input("Novo valor: ")
            rc = atualizar_cliente(id_c, campo, valor)
            if rc["status"] == 200:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")
            else:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")

        elif opcao == "5":
            id_c = input("ID do cliente: ")
            rc = remover_cliente(id_c)
            if rc["status"] == 200:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")
            else:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")

        # ── JOGOS ─────────────────────────────────────────────

        elif opcao == "6":
            nome       = input("Nome do jogo: ")
            custo_min  = input("Custo minimo (EUR): ")
            saldo_j    = input("Saldo da banca (EUR): ")
            retorno    = input("Retorno (ex: 35 ou -0.5): ")
            nivel_ac   = input("Nivel acesso (BRONZE/PRATA/OURO/PLATINA/VIP): ")
            estado     = input("Estado (ATIVO/INATIVO): ")
            dealer     = input("Tem dealer? (SIM/NAO): ")
            tabuleiro  = input("Tem tabuleiro? (SIM/NAO): ")
            pecas      = input("Tem pecas? (SIM/NAO): ")
            cartas     = input("Tem cartas? (SIM/NAO): ")
            dados      = input("Tem dados? (SIM/NAO): ")
            maquina    = input("E uma maquina/slot? (SIM/NAO): ")
            rc = criar_jogo(nome, custo_min, saldo_j, retorno, nivel_ac, estado,
                            dealer, tabuleiro, pecas, cartas, dados, maquina)
            if rc["status"] == 201:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")
                print(rc["dados"])
            else:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")

        elif opcao == "7":
            rc = listar_todos_jogos()
            if rc["status"] == 200:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")
                for j in rc["dados"]:
                    print(j)
            else:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")

        elif opcao == "8":
            id_j = input("ID do jogo: ")
            rc = ler_jogo_por_id(id_j)
            if rc["status"] == 200:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")
                print(rc["dados"])
            else:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")

        elif opcao == "9":
            id_j  = input("ID do jogo: ")
            print(f"Campos editaveis: {' | '.join(CAMPOS_EDITAVEIS_JOGO)}")
            campo = input("Campo a editar: ")
            valor = input("Novo valor: ")
            rc = atualizar_jogo(id_j, campo, valor)
            if rc["status"] == 200:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")
            else:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")

        elif opcao == "10":
            id_j = input("ID do jogo: ")
            rc = remover_jogo(id_j)
            if rc["status"] == 200:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")
            else:
                print(f"[{rc['status']}] {rc['ok']} - {rc['mensagem']}")

        elif opcao == "0":
            print("A sair...")
            break

        else:
            print("[400] Bad Request - Opcao invalida.")


if __name__ == "__main__":
    main()
