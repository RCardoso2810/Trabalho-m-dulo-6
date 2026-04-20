# ══════════════════════════════════════════════════════════════
#  jogo.py
#  CRUD de jogos — dicionarios de dicionarios
#  Estruturas: tuplos, listas, sets, dicionarios, date, defs
# ══════════════════════════════════════════════════════════════

from datetime import date
from utils import (
    validar_nome_jogo,
    validar_custo_minimo,
    validar_saldo_jogo,
    validar_retorno,
    validar_nivel,
    validar_estado,
    validar_sim_nao,
)

# Tuplos de valores validos (imutaveis)
ESTADOS_JOGO = ("ATIVO", "INATIVO")
NIVEIS_JOGO  = ("BRONZE", "PRATA", "OURO", "PLATINA", "VIP")

# Dicionario principal: { "JOG0001": { campo: valor, ... } }
base_jogos = {}

# Lista usada como pilha para controlo do contador de IDs
pilha_ids_jogo = [1]

# Set dos campos que sao tipos (sub-dicionario "tipos")
CAMPOS_TIPOS = {"dealer", "tabuleiro", "pecas", "cartas", "dados", "maquina"}

# Tuplo dos campos editaveis
CAMPOS_EDITAVEIS_JOGO = (
    "nome", "custo_minimo", "saldo_jogo", "retorno",
    "nivel_acesso", "estado",
    "dealer", "tabuleiro", "pecas", "cartas", "dados", "maquina"
)

# Dicionarios de despacho de validacao — campo -> funcao
VALIDACOES_JOGO = {
    "nome"         : validar_nome_jogo,
    "custo_minimo" : validar_custo_minimo,
    "saldo_jogo"   : validar_saldo_jogo,
    "retorno"      : validar_retorno,
    "nivel_acesso" : lambda v: validar_nivel(v, "Nivel de acesso"),
    "estado"       : validar_estado,
}

VALIDACOES_TIPOS_JOGO = {
    "dealer"    : lambda v: validar_sim_nao(v, "dealer"),
    "tabuleiro" : lambda v: validar_sim_nao(v, "tabuleiro"),
    "pecas"     : lambda v: validar_sim_nao(v, "pecas"),
    "cartas"    : lambda v: validar_sim_nao(v, "cartas"),
    "dados"     : lambda v: validar_sim_nao(v, "dados"),
    "maquina"   : lambda v: validar_sim_nao(v, "maquina"),
}


# ══════════════════════════════════════════════════════════════
#  CREATE — 201 Created
# ══════════════════════════════════════════════════════════════

def criar_jogo(nome, custo_minimo, saldo_jogo, retorno,
               nivel_acesso, estado,
               tem_dealer, tem_tabuleiro, tem_pecas,
               tem_cartas, tem_dados, tem_maquina):
    try:
        # ── Validacoes via dicionarios de despacho ────────────
        rv = validar_nome_jogo(nome)
        if not rv["valido"]:
            return 422, rv["mensagem"]

        rv = validar_custo_minimo(custo_minimo)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        custo_ok = rv["valor"]

        rv = validar_saldo_jogo(saldo_jogo)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        saldo_ok = rv["valor"]

        rv = validar_retorno(retorno)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        retorno_ok = rv["valor"]

        rv = validar_nivel(nivel_acesso, "Nivel de acesso")
        if not rv["valido"]:
            return 422, rv["mensagem"]
        nivel_ok = rv["valor"]

        rv = validar_estado(estado)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        estado_ok = rv["valor"]

        # ── Validacao dos tipos (sub-dicionario) ──────────────
        entradas_tipos = (
            ("dealer",    tem_dealer),
            ("tabuleiro", tem_tabuleiro),
            ("pecas",     tem_pecas),
            ("cartas",    tem_cartas),
            ("dados",     tem_dados),
            ("maquina",   tem_maquina),
        )
        tipos = {}
        for campo_t, valor_t in entradas_tipos:
            rv = VALIDACOES_TIPOS_JOGO[campo_t](valor_t)
            if not rv["valido"]:
                return 422, rv["mensagem"]
            tipos[campo_t] = rv["valor"]

        # ── Construcao do registo ─────────────────────────────
        id_jogo = f"JOG{pilha_ids_jogo[0]:04d}"
        pilha_ids_jogo[0] += 1

        hoje = date.today()
        jogo = {
            "id"           : id_jogo,
            "nome"         : str(nome).strip(),
            "custo_minimo" : custo_ok,
            "saldo_jogo"   : saldo_ok,
            "retorno"      : retorno_ok,
            "nivel_acesso" : nivel_ok,
            "estado"       : estado_ok,
            "data_criacao" : f"{hoje.day:02d}/{hoje.month:02d}/{hoje.year}",
            "tipos"        : tipos,
        }
        base_jogos[id_jogo] = jogo
        return 201, jogo

    except Exception as e:
        return 500, f"Erro interno: {e}"


# ══════════════════════════════════════════════════════════════
#  READ — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def ler_jogo_por_id(id_jogo):
    j = base_jogos.get(str(id_jogo).upper())
    if not j:
        return 404, "Jogo nao encontrado."
    return 200, j

def ler_jogo_por_nome(nome):
    for j in base_jogos.values():
        if j["nome"].lower() == str(nome).strip().lower():
            return 200, j
    return 404, f"Jogo '{nome}' nao encontrado."

def listar_todos_jogos():
    lista = list(base_jogos.values())
    return 200, lista

def listar_jogos_ativos():
    lista = [j for j in base_jogos.values() if j["estado"] == "ATIVO"]
    return 200, lista

def total_jogos():
    return len(base_jogos)


# ══════════════════════════════════════════════════════════════
#  UPDATE — 200 OK | 404 Not Found | 400/422 erros
# ══════════════════════════════════════════════════════════════

def atualizar_jogo(id_jogo, campo, valor):
    j = base_jogos.get(str(id_jogo).upper())
    if not j:
        return 404, f"Jogo '{id_jogo}' nao encontrado."

    campo = campo.lower().strip()
    if campo not in CAMPOS_EDITAVEIS_JOGO:
        return 400, f"Campo '{campo}' invalido. Editaveis: {' | '.join(CAMPOS_EDITAVEIS_JOGO)}"

    # ── Validacao via dicionarios de despacho ─────────────────
    if campo in VALIDACOES_JOGO:
        rv = VALIDACOES_JOGO[campo](valor)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        j[campo] = rv["valor"]
        return 200, f"Campo '{campo}' actualizado com sucesso."

    if campo in CAMPOS_TIPOS:
        rv = VALIDACOES_TIPOS_JOGO[campo](valor)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        j["tipos"][campo] = rv["valor"]
        return 200, f"Campo '{campo}' actualizado com sucesso."

    return 400, f"Campo '{campo}' nao pode ser editado."


# ══════════════════════════════════════════════════════════════
#  DELETE — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def remover_jogo(id_jogo):
    id_upper = str(id_jogo).upper()
    if id_upper not in base_jogos:
        return 404, f"Jogo '{id_jogo}' nao encontrado."
    j = base_jogos.pop(id_upper)
    return 200, f"Jogo '{j['nome']}' removido com sucesso."

