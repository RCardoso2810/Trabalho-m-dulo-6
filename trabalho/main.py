# ══════════════════════════════════════════════════════════════
#  FICHEIRO 3 — main.py
#  Menu principal — conecta cliente.py e jogo.py
#  Sem classes, sem __init__, sem self
# ══════════════════════════════════════════════════════════════

from cliente import (
    criar_cliente, ler_cliente_por_id,
    listar_todos_clientes, atualizar_cliente, remover_cliente,
    total_clientes, NIVEIS_VALIDOS, ESTADOS_VALIDOS, GENEROS_VALIDOS,
    base_clientes,
)
from jogo import (
    criar_jogo, ler_jogo_por_id,
    listar_todos_jogos, listar_jogos_ativos,
    atualizar_jogo, remover_jogo,
    total_jogos, NIVEIS_JOGO, ESTADOS_JOGO,
    base_jogos,
)

# ══════════════════════════════════════════════════════════════
#  CORES ANSI
# ══════════════════════════════════════════════════════════════
RESET    = "\033[0m"
NEGRITO  = "\033[1m"
DIM      = "\033[2m"
OURO     = "\033[38;5;220m"
BRANCO   = "\033[97m"
CINZA    = "\033[38;5;245m"
VERDE    = "\033[38;5;46m"
VERMELHO = "\033[38;5;196m"
AZUL     = "\033[38;5;39m"
ROXO     = "\033[38;5;135m"
CIANO    = "\033[38;5;51m"
LARANJA  = "\033[38;5;208m"
ROSA     = "\033[38;5;213m"
PRETO    = "\033[30m"
FUNDO_OURO  = "\033[48;5;220m"
FUNDO_AZUL  = "\033[48;5;17m"
FUNDO_VERDE = "\033[48;5;22m"
FUNDO_ROXO  = "\033[48;5;53m"

LARGURA = 68

BANNER = r"""
   ██████╗ █████╗ ███████╗██╗███╗   ██╗ ██████╗
  ██╔════╝██╔══██╗██╔════╝██║████╗  ██║██╔═══██╗
  ██║     ███████║███████╗██║██╔██╗ ██║██║   ██║
  ██║     ██╔══██║╚════██║██║██║╚██╗██║██║   ██║
  ╚██████╗██║  ██║███████║██║██║ ╚████║╚██████╔╝
   ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝
"""
SUB = "✦  SISTEMA DE GESTAO DE CASINO  ✦"

# ══════════════════════════════════════════════════════════════
#  FUNÇÕES VISUAIS
# ══════════════════════════════════════════════════════════════

def limpar():
    print("\033[2J\033[H", end="", flush=True)

def pausa(msg="  Prima ENTER para continuar..."):
    print(f"\n{CINZA}{msg}{RESET}")
    input()

def linha(estilo="=", cor=OURO):
    mapa = {"=": "═", "-": "─", ".": "·"}
    c = mapa.get(estilo, estilo)
    print(f"{cor}{c * LARGURA}{RESET}")

def titulo(texto, cor=OURO, fundo_cor=""):
    linha("=", cor)
    pad_esq = (LARGURA - len(texto) - 2) // 2
    pad_dir = LARGURA - len(texto) - pad_esq - 3
    print(f"{cor}║{fundo_cor}{' ' * pad_esq} {NEGRITO}{texto}{RESET}{cor}{' ' * pad_dir} ║{RESET}")
    linha("=", cor)

def badge(texto, fundo=FUNDO_OURO, cor_txt=PRETO):
    return f"{fundo}{cor_txt} {texto} {RESET}"

def pedir(prompt, cor=CIANO):
    return input(f"{cor}  ▶ {BRANCO}{prompt}{RESET} ").strip()

def mostrar_erro(msg):
    print(f"\n{VERMELHO}  ✖  {msg}{RESET}")
    pausa()

def mostrar_ok(msg):
    print(f"\n{VERDE}  ✔  {msg}{RESET}")

def tag_nivel(nivel):
    mapa = {
        "BRONZE" : "\033[38;5;130m",
        "PRATA"  : "\033[38;5;250m",
        "OURO"   : OURO,
        "PLATINA": CIANO,
        "VIP"    : ROSA,
    }
    cor = mapa.get(nivel, BRANCO)
    return f"{cor}{NEGRITO}{nivel}{RESET}"

def tag_estado(estado):
    cor = VERDE if estado == "ATIVO" else VERMELHO
    return f"{cor}{estado}{RESET}"

def sim_nao_cor(valor):
    return f"{VERDE}SIM{RESET}" if valor == "SIM" else f"{CINZA}NAO{RESET}"

# ══════════════════════════════════════════════════════════════
#  CABEÇALHOS
# ══════════════════════════════════════════════════════════════

def splash():
    limpar()
    print(f"{OURO}{BANNER}{RESET}")
    pad = (LARGURA - len(SUB)) // 2
    print(" " * pad + f"{NEGRITO}{OURO}{SUB}{RESET}\n")
    linha("=", OURO)
    print(f"\n  {CINZA}Bem-vindo ao sistema de gestao do Casino.{RESET}")
    print(f"  {VERDE}Sistema inicializado com sucesso!{RESET}\n")
    pausa("  Prima ENTER para entrar no sistema...")

def cabecalho():
    limpar()
    print(f"{OURO}{BANNER}{RESET}")
    pad = (LARGURA - len(SUB)) // 2
    print(" " * pad + f"{NEGRITO}{OURO}{SUB}{RESET}")
    linha("=", OURO)

def cabecalho_mini(secao, cor=OURO):
    limpar()
    print(f"{DIM}{OURO}{BANNER}{RESET}")
    titulo(secao, cor)

# ══════════════════════════════════════════════════════════════
#  MENU PRINCIPAL
# ══════════════════════════════════════════════════════════════

def menu_principal():
    while True:
        cabecalho()
        n_cli  = total_clientes()
        n_jogo = total_jogos()
        n_ativ = len(listar_jogos_ativos())
        print(f"\n  Clientes: {badge(str(n_cli),  FUNDO_AZUL,  BRANCO)}   "
              f"Jogos: {badge(str(n_jogo), FUNDO_ROXO,  BRANCO)}   "
              f"Activos: {badge(str(n_ativ), FUNDO_VERDE, BRANCO)}\n")
        linha("-", CINZA)

        print(f"\n  {OURO}╔══  CLIENTES  ══════════════════════════════════╗{RESET}")
        print(f"  {OURO}║{RESET}  {AZUL}[1]{RESET}  Adicionar cliente")
        print(f"  {OURO}║{RESET}  {AZUL}[2]{RESET}  Editar cliente")
        print(f"  {OURO}║{RESET}  {AZUL}[3]{RESET}  Remover cliente")
        print(f"  {OURO}║{RESET}  {AZUL}[4]{RESET}  Ver todos os clientes")
        print(f"  {OURO}║{RESET}  {AZUL}[5]{RESET}  Ficha detalhada de cliente")
        print(f"  {OURO}╚════════════════════════════════════════════════╝{RESET}")

        print(f"\n  {OURO}╔══  JOGOS  ══════════════════════════════════════╗{RESET}")
        print(f"  {OURO}║{RESET}  {ROXO}[6]{RESET}  Criar novo jogo")
        print(f"  {OURO}║{RESET}  {ROXO}[7]{RESET}  Editar jogo")
        print(f"  {OURO}║{RESET}  {ROXO}[8]{RESET}  Remover jogo")
        print(f"  {OURO}║{RESET}  {ROXO}[9]{RESET}  Ver todos os jogos")
        print(f"  {OURO}║{RESET}  {ROXO}[10]{RESET} Ficha detalhada de jogo")
        print(f"  {OURO}╚════════════════════════════════════════════════╝{RESET}")

        print(f"\n  {CINZA}[0]{RESET}  {VERMELHO}Sair{RESET}\n")
        linha("=", OURO)

        op = pedir("Escolha uma opcao")

        if   op == "1":  adicionar_cliente()
        elif op == "2":  editar_cliente()
        elif op == "3":  remover_cliente_menu()
        elif op == "4":  listar_clientes()
        elif op == "5":  ficha_cliente()
        elif op == "6":  criar_jogo_menu()
        elif op == "7":  editar_jogo_menu()
        elif op == "8":  remover_jogo_menu()
        elif op == "9":  listar_jogos()
        elif op == "10": ficha_jogo()
        elif op == "0":  confirmar_saida()
        else:            mostrar_erro("Opcao invalida.")

# ══════════════════════════════════════════════════════════════
#  AUXILIARES VISUAIS
# ══════════════════════════════════════════════════════════════

def _listar_ids_clientes():
    todos = listar_todos_clientes()
    if not todos:
        return
    print(f"\n  {CINZA}Clientes registados:{RESET}")
    for c in todos:
        print(f"    {AZUL}{c['id']}{RESET}  {BRANCO}{c['nome']:<26}{RESET}"
              f"  {tag_nivel(c['nivel']):<21}  {tag_estado(c['estado'])}")
    print()

def _listar_ids_jogos():
    todos = listar_todos_jogos()
    if not todos:
        return
    print(f"\n  {CINZA}Jogos registados:{RESET}")
    for j in todos:
        print(f"    {ROXO}{j['id']}{RESET}  {BRANCO}{j['nome']:<26}{RESET}"
              f"  {tag_nivel(j['nivel_acesso']):<21}  {tag_estado(j['estado'])}")
    print()

# ══════════════════════════════════════════════════════════════
#  CLIENTES — CRUD
# ══════════════════════════════════════════════════════════════

def adicionar_cliente():
    cabecalho_mini("NOVO CLIENTE", AZUL)
    try:
        print(f"\n  {CINZA}Preencha os dados do novo cliente:{RESET}\n")

        nome = pedir("Nome completo                  :")
        if not nome:
            raise ValueError("Nome obrigatorio.")

        data_nasc = pedir("Data de nascimento (DD/MM/AAAA):")

        print(f"\n  {CINZA}Generos: {' | '.join(GENEROS_VALIDOS)}{RESET}")
        genero = pedir("Genero                         :")

        nacionalidade = pedir("Nacionalidade                  :")

        print(f"\n  {CINZA}Email ou numero de telefone{RESET}")
        contacto = pedir("Contacto                       :")

        saldo = pedir("Saldo inicial (EUR)            :")

        print(f"\n  {CINZA}Niveis: {' | '.join(NIVEIS_VALIDOS)}{RESET}")
        nivel = pedir("Nivel                          :")

        print(f"\n  {CINZA}Estados: {' | '.join(ESTADOS_VALIDOS)}{RESET}")
        estado = pedir("Estado                         :")

        c = criar_cliente(nome, data_nasc, genero, nacionalidade,
                          contacto, float(saldo), nivel, estado)

        linha("-", CINZA)
        mostrar_ok(f"Cliente criado com sucesso!")
        print(f"\n  {CINZA}ID           : {OURO}{NEGRITO}{c['id']}{RESET}")
        print(f"  {CINZA}Nome         : {BRANCO}{c['nome']}{RESET}")
        print(f"  {CINZA}Nascimento   : {BRANCO}{c['data_nascimento']}  ({c['idade']} anos){RESET}")
        print(f"  {CINZA}Nivel        : {tag_nivel(c['nivel'])}")
        print(f"  {CINZA}Estado       : {tag_estado(c['estado'])}")
        print(f"  {CINZA}Registo      : {BRANCO}{c['data_registo']}{RESET}\n")

    except (ValueError, TypeError) as e:
        mostrar_erro(str(e))
        return
    pausa()


def editar_cliente():
    cabecalho_mini("EDITAR CLIENTE", LARANJA)
    if not base_clientes:
        mostrar_erro("Nenhum cliente registado.")
        return

    _listar_ids_clientes()
    id_c = pedir("ID do cliente (ex: CLI0001) :").upper()
    c = ler_cliente_por_id(id_c)
    if not c:
        mostrar_erro(f"Cliente '{id_c}' nao encontrado.")
        return

    print(f"\n  {OURO}Cliente:{RESET} {NEGRITO}{c['nome']}{RESET}  {CINZA}[{c['id']}]{RESET}\n")
    linha("-", CINZA)

    campos_vals = [
        ("nome",             c["nome"]),
        ("data_nascimento",  c["data_nascimento"]),
        ("genero",           c["genero"]),
        ("nacionalidade",    c["nacionalidade"]),
        ("contacto",         c["contacto"]),
        ("saldo",            f"EUR {c['saldo']:.2f}"),
        ("nivel",            c["nivel"]),
        ("estado",           c["estado"]),
    ]
    for i, (campo, atual) in enumerate(campos_vals, 1):
        print(f"  {OURO}[{i}]{RESET} {CINZA}{campo:<20}{RESET}  {BRANCO}{atual}{RESET}")

    linha("-", CINZA)
    campo = pedir("Campo a editar (escreve o nome) :").lower()
    novo  = pedir(f"Novo valor para '{campo}'        :")
    try:
        atualizar_cliente(id_c, campo, novo)
        mostrar_ok(f"Campo '{campo}' actualizado com sucesso!")
    except (KeyError, ValueError) as e:
        mostrar_erro(str(e))
        return
    pausa()


def remover_cliente_menu():
    cabecalho_mini("REMOVER CLIENTE", VERMELHO)
    if not base_clientes:
        mostrar_erro("Nenhum cliente registado.")
        return

    _listar_ids_clientes()
    id_c = pedir("ID do cliente a remover :").upper()
    c = ler_cliente_por_id(id_c)
    if not c:
        mostrar_erro(f"Cliente '{id_c}' nao encontrado.")
        return

    linha("-", CINZA)
    print(f"  {VERMELHO}Vai remover:{RESET}  {NEGRITO}{c['nome']}{RESET}  {CINZA}[{c['id']}]{RESET}")
    linha("-", CINZA)
    conf = pedir("Confirmar remocao? (s/n) :")
    if conf.lower() == "s":
        remover_cliente(id_c)
        mostrar_ok(f"Cliente '{c['nome']}' removido com sucesso.")
    else:
        print(f"\n  {CINZA}Operacao cancelada.{RESET}")
    pausa()


def listar_clientes():
    cabecalho_mini(f"TODOS OS CLIENTES  ({total_clientes()})", AZUL)
    todos = listar_todos_clientes()
    if not todos:
        print(f"\n{CINZA}  Nenhum cliente registado ainda.{RESET}\n")
        pausa()
        return

    print(f"\n  {OURO}{'ID':<10}{'NOME':<24}{'NASC.':<13}{'NIVEL':<12}"
          f"{'SALDO':>10}  {'ESTADO':<9}{'CONTACTO'}{RESET}")
    linha("-", CINZA)
    for c in todos:
        print(f"  {AZUL}{c['id']:<10}{RESET}"
              f"{BRANCO}{c['nome']:<24}{RESET}"
              f"{CINZA}{c['data_nascimento']:<13}{RESET}"
              f"{tag_nivel(c['nivel']):<21}"
              f"{VERDE}EUR{c['saldo']:>7.2f}{RESET}  "
              f"{tag_estado(c['estado']):<18}"
              f"{CINZA}{c['contacto']}{RESET}")
    linha("-", CINZA)
    print(f"\n  {OURO}Total: {total_clientes()} cliente(s){RESET}\n")
    pausa()


def ficha_cliente():
    cabecalho_mini("FICHA DE CLIENTE", AZUL)
    if not base_clientes:
        mostrar_erro("Nenhum cliente registado.")
        return

    _listar_ids_clientes()
    id_c = pedir("ID do cliente :").upper()
    c = ler_cliente_por_id(id_c)
    if not c:
        mostrar_erro(f"Cliente '{id_c}' nao encontrado.")
        return

    linha("=", AZUL)
    print(f"  {NEGRITO}{AZUL}FICHA DO CLIENTE{RESET}  {CINZA}[{c['id']}]{RESET}")
    linha("-", CINZA)
    print(f"  {CINZA}Nome            : {NEGRITO}{BRANCO}{c['nome']}{RESET}")
    print(f"  {CINZA}Data Nascimento : {BRANCO}{c['data_nascimento']}  ({c['idade']} anos){RESET}")
    print(f"  {CINZA}Genero          : {BRANCO}{c['genero']}{RESET}")
    print(f"  {CINZA}Nacionalidade   : {BRANCO}{c['nacionalidade']}{RESET}")
    print(f"  {CINZA}Contacto        : {BRANCO}{c['contacto']}{RESET}")
    print(f"  {CINZA}Data Registo    : {BRANCO}{c['data_registo']}{RESET}")
    linha("-", CINZA)
    print(f"  {CINZA}Saldo Actual    : {VERDE}EUR {c['saldo']:.2f}{RESET}")
    print(f"  {CINZA}Nivel           : {tag_nivel(c['nivel'])}")
    print(f"  {CINZA}Estado          : {tag_estado(c['estado'])}")
    linha("=", AZUL)
    pausa()


# ══════════════════════════════════════════════════════════════
#  JOGOS — CRUD
# ══════════════════════════════════════════════════════════════

def criar_jogo_menu():
    cabecalho_mini("CRIAR NOVO JOGO", ROXO)
    try:
        print(f"\n  {CINZA}Preencha os dados do novo jogo:{RESET}\n")

        nome = pedir("Nome do jogo                       :")
        if not nome:
            raise ValueError("Nome obrigatorio.")

        custo_min = pedir("Custo minimo de entrada (EUR)      :")
        saldo_j   = pedir("Saldo inicial da banca (EUR)       :")
        retorno   = pedir("Retorno financeiro (ex: 2.0/-0.5)  :")

        print(f"\n  {CINZA}Niveis: {' | '.join(NIVEIS_JOGO)}{RESET}")
        nivel_ac = pedir("Nivel minimo de acesso             :")

        print(f"\n  {CINZA}Estados: {' | '.join(ESTADOS_JOGO)}{RESET}")
        estado = pedir("Estado                             :")

        print(f"\n  {CINZA}Caracteristicas do jogo (SIM ou NAO):{RESET}")
        dealer    = pedir("Tem dealer?                        :")
        tabuleiro = pedir("Tem tabuleiro?                     :")
        pecas     = pedir("Tem pecas?                         :")
        cartas    = pedir("Tem cartas?                        :")
        dados     = pedir("Tem dados?                         :")
        maquina   = pedir("E uma maquina (slot)?              :")

        j = criar_jogo(nome, float(custo_min), float(saldo_j), float(retorno),
                       nivel_ac, estado,
                       dealer, tabuleiro, pecas, cartas, dados, maquina)

        linha("-", CINZA)
        mostrar_ok(f"Jogo criado com sucesso!")
        print(f"\n  {CINZA}ID           : {OURO}{NEGRITO}{j['id']}{RESET}")
        print(f"  {CINZA}Nome         : {NEGRITO}{BRANCO}{j['nome']}{RESET}")
        print(f"  {CINZA}Custo min.   : {VERDE}EUR {j['custo_minimo']:.2f}{RESET}")
        print(f"  {CINZA}Saldo banca  : {VERDE}EUR {j['saldo_jogo']:.2f}{RESET}")
        print(f"  {CINZA}Nivel acesso : {tag_nivel(j['nivel_acesso'])}")
        print(f"  {CINZA}Estado       : {tag_estado(j['estado'])}\n")

    except (ValueError, TypeError) as e:
        mostrar_erro(str(e))
        return
    pausa()


def editar_jogo_menu():
    cabecalho_mini("EDITAR JOGO", LARANJA)
    if not base_jogos:
        mostrar_erro("Nenhum jogo registado.")
        return

    _listar_ids_jogos()
    id_j = pedir("ID do jogo (ex: JOG0001) :").upper()
    j = ler_jogo_por_id(id_j)
    if not j:
        mostrar_erro(f"Jogo '{id_j}' nao encontrado.")
        return

    print(f"\n  {OURO}Jogo:{RESET} {NEGRITO}{j['nome']}{RESET}  {CINZA}[{j['id']}]{RESET}\n")
    linha("-", CINZA)

    campos_vals = [
        ("nome",         j["nome"]),
        ("custo_minimo", f"EUR {j['custo_minimo']:.2f}"),
        ("saldo_jogo",   f"EUR {j['saldo_jogo']:.2f}"),
        ("retorno",      str(j["retorno"])),
        ("nivel_acesso", j["nivel_acesso"]),
        ("estado",       j["estado"]),
        ("dealer",       j["tipos"]["dealer"]),
        ("tabuleiro",    j["tipos"]["tabuleiro"]),
        ("pecas",        j["tipos"]["pecas"]),
        ("cartas",       j["tipos"]["cartas"]),
        ("dados",        j["tipos"]["dados"]),
        ("maquina",      j["tipos"]["maquina"]),
    ]
    for i, (campo, atual) in enumerate(campos_vals, 1):
        print(f"  {OURO}[{i:>2}]{RESET} {CINZA}{campo:<16}{RESET}  {BRANCO}{atual}{RESET}")

    linha("-", CINZA)
    campo = pedir("Campo a editar (escreve o nome) :").lower()
    novo  = pedir(f"Novo valor para '{campo}'        :")
    try:
        atualizar_jogo(id_j, campo, novo)
        mostrar_ok(f"Campo '{campo}' actualizado com sucesso!")
    except (KeyError, ValueError) as e:
        mostrar_erro(str(e))
        return
    pausa()


def remover_jogo_menu():
    cabecalho_mini("REMOVER JOGO", VERMELHO)
    if not base_jogos:
        mostrar_erro("Nenhum jogo registado.")
        return

    _listar_ids_jogos()
    id_j = pedir("ID do jogo a remover :").upper()
    j = ler_jogo_por_id(id_j)
    if not j:
        mostrar_erro(f"Jogo '{id_j}' nao encontrado.")
        return

    linha("-", CINZA)
    print(f"  {VERMELHO}Vai remover:{RESET}  {NEGRITO}{j['nome']}{RESET}  {CINZA}[{j['id']}]{RESET}")
    linha("-", CINZA)
    conf = pedir("Confirmar remocao? (s/n) :")
    if conf.lower() == "s":
        remover_jogo(id_j)
        mostrar_ok(f"Jogo '{j['nome']}' removido com sucesso.")
    else:
        print(f"\n  {CINZA}Operacao cancelada.{RESET}")
    pausa()


def listar_jogos():
    cabecalho_mini(f"TODOS OS JOGOS  ({total_jogos()})", ROXO)
    todos = listar_todos_jogos()
    if not todos:
        print(f"\n{CINZA}  Nenhum jogo registado ainda.{RESET}\n")
        pausa()
        return

    print(f"\n  {OURO}{'ID':<10}{'NOME':<22}{'NIVEL':<12}{'CUSTO MIN':>10}"
          f"{'SALDO BANCA':>13}{'RETORNO':>9}  {'ESTADO'}{RESET}")
    linha("-", CINZA)
    for j in todos:
        ret_cor = VERDE if j["retorno"] >= 0 else VERMELHO
        print(f"  {ROXO}{j['id']:<10}{RESET}"
              f"{BRANCO}{j['nome']:<22}{RESET}"
              f"{tag_nivel(j['nivel_acesso']):<21}"
              f"{CINZA}EUR{j['custo_minimo']:>6.2f}{RESET}"
              f"  {CINZA}EUR{j['saldo_jogo']:>9.2f}{RESET}"
              f"  {ret_cor}{j['retorno']:>6.2f}x{RESET}  "
              f"{tag_estado(j['estado'])}")
    linha("-", CINZA)
    print(f"\n  {OURO}Total: {total_jogos()} jogo(s){RESET}\n")
    pausa()


def ficha_jogo():
    cabecalho_mini("FICHA DE JOGO", ROXO)
    if not base_jogos:
        mostrar_erro("Nenhum jogo registado.")
        return

    _listar_ids_jogos()
    id_j = pedir("ID do jogo :").upper()
    j = ler_jogo_por_id(id_j)
    if not j:
        mostrar_erro(f"Jogo '{id_j}' nao encontrado.")
        return

    linha("=", ROXO)
    print(f"  {NEGRITO}{ROXO}FICHA DO JOGO{RESET}  {CINZA}[{j['id']}]{RESET}")
    linha("-", CINZA)
    print(f"  {CINZA}Nome           : {NEGRITO}{BRANCO}{j['nome']}{RESET}")
    print(f"  {CINZA}Data Criacao   : {BRANCO}{j['data_criacao']}{RESET}")
    print(f"  {CINZA}Nivel Acesso   : {tag_nivel(j['nivel_acesso'])}")
    print(f"  {CINZA}Estado         : {tag_estado(j['estado'])}")
    linha("-", CINZA)
    ret_cor = VERDE if j["retorno"] >= 0 else VERMELHO
    print(f"  {CINZA}Custo Minimo   : {VERDE}EUR {j['custo_minimo']:.2f}{RESET}")
    print(f"  {CINZA}Saldo da Banca : {VERDE}EUR {j['saldo_jogo']:.2f}{RESET}")
    print(f"  {CINZA}Retorno        : {ret_cor}{j['retorno']:.2f}x{RESET}")
    linha("-", CINZA)
    t = j["tipos"]
    print(f"  {CINZA}Dealer         : {sim_nao_cor(t['dealer'])}")
    print(f"  {CINZA}Tabuleiro      : {sim_nao_cor(t['tabuleiro'])}")
    print(f"  {CINZA}Pecas          : {sim_nao_cor(t['pecas'])}")
    print(f"  {CINZA}Cartas         : {sim_nao_cor(t['cartas'])}")
    print(f"  {CINZA}Dados          : {sim_nao_cor(t['dados'])}")
    print(f"  {CINZA}Maquina        : {sim_nao_cor(t['maquina'])}")
    linha("=", ROXO)
    pausa()


# ══════════════════════════════════════════════════════════════
#  SAÍDA
# ══════════════════════════════════════════════════════════════

def confirmar_saida():
    limpar()
    titulo("SAIR DO SISTEMA", VERMELHO)
    print(f"\n  {BRANCO}Tem a certeza que quer sair?{RESET}\n")
    op = pedir("(s/n)", VERMELHO)
    if op.lower() == "s":
        limpar()
        print(f"\n{OURO}{BANNER}{RESET}")
        print(f"\n  {CINZA}Obrigado por utilizar o Casino Manager.{RESET}")
        print(f"  {OURO}Bom jogo — jogue com responsabilidade! ✦{RESET}\n")
        raise SystemExit(0)


# ══════════════════════════════════════════════════════════════
#  PONTO DE ENTRADA
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    splash()
    menu_principal()