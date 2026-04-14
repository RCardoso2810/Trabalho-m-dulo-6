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


# ── Resultado de operacao CRUD ────────────────────────────────




# ── Auxiliar interno ──────────────────────────────────────────

def _sn(v):
    return "SIM" if str(v).strip().upper() == "SIM" else "NAO"


# ══════════════════════════════════════════════════════════════
#  CREATE — 201 Created
# ══════════════════════════════════════════════════════════════

def criar_jogo(nome, custo_minimo, saldo_jogo, retorno,
               nivel_acesso, estado,
               tem_dealer, tem_tabuleiro, tem_pecas,
               tem_cartas, tem_dados, tem_maquina):
    try:
        id_jogo = f"JOG{pilha_ids_jogo[0]:04d}"
        pilha_ids_jogo[0] += 1

        nivel_upper = str(nivel_acesso).strip().upper()
        if nivel_upper not in NIVEIS_JOGO:
            nivel_upper = "BRONZE"

        estado_upper = str(estado).strip().upper()
        if estado_upper not in ESTADOS_JOGO:
            estado_upper = "ATIVO"

        custo = float(custo_minimo)
        if custo < 0:
            return 422,"Custo minimo nao pode ser negativo."

        saldo = float(saldo_jogo)
        if saldo < 0:
            return 422,"Saldo do jogo nao pode ser negativo."

        hoje = date.today()
        tipos = {
            "dealer"    : _sn(tem_dealer),
            "tabuleiro" : _sn(tem_tabuleiro),
            "pecas"     : _sn(tem_pecas),
            "cartas"    : _sn(tem_cartas),
            "dados"     : _sn(tem_dados),
            "maquina"   : _sn(tem_maquina),
        }

        jogo = {
            "id"           : id_jogo,
            "nome"         : str(nome).strip(),
            "custo_minimo" : custo,
            "saldo_jogo"   : saldo,
            "retorno"      : float(retorno),
            "nivel_acesso" : nivel_upper,
            "estado"       : estado_upper,
            "data_criacao" : f"{hoje.day:02d}/{hoje.month:02d}/{hoje.year}",
            "tipos"        : tipos,
        }
        base_jogos[id_jogo] = jogo
        return 201,"criado com sucesso."
    except Exception as e:
        return 500,"Error"


# ══════════════════════════════════════════════════════════════
#  READ — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def ler_jogo_por_id(id_jogo):
    j = base_jogos.get(str(id_jogo).upper())
    if not j:
        return 404,"ID nao encontrado."
    return 200, j

def ler_jogo_por_nome(nome):
    for j in base_jogos.values():
        if j["nome"].lower() == str(nome).strip().lower():
            return 200, j
    return 404,f"Jogo '{nome}' nao encontrado."

def listar_todos_jogos():
    lista = list(base_jogos.values())
    return 200,f"{len(lista)} jogo(s) encontrado(s)."

def listar_jogos_ativos():
    lista = [j for j in base_jogos.values() if j["estado"] == "ATIVO"]
    return 200,f"{len(lista)} jogo(s) activo(s)."

def total_jogos():
    return len(base_jogos)


# ══════════════════════════════════════════════════════════════
#  UPDATE — 200 OK | 404 Not Found | 400/422 erros
# ══════════════════════════════════════════════════════════════

def atualizar_jogo(id_jogo, campo, valor):
    j = base_jogos.get(str(id_jogo).upper())
    if not j:
        return 404,f"Jogo '{id_jogo}' nao encontrado."

    campo = campo.lower().strip()
    if campo not in CAMPOS_EDITAVEIS_JOGO:
        return 400,f"Campo '{campo}' invalido. Editaveis: {' | '.join(CAMPOS_EDITAVEIS_JOGO)}"

    try:
        if campo == "nome":
            if not str(valor).strip():
                return 400,"Nome nao pode estar vazio."
            j["nome"] = str(valor).strip()

        elif campo == "custo_minimo":
            v = float(valor)
            if v < 0:
                return 422,"Custo minimo nao pode ser negativo."
            j["custo_minimo"] = v

        elif campo == "saldo_jogo":
            v = float(valor)
            if v < 0:
                return 422,"Saldo nao pode ser negativo."
            j["saldo_jogo"] = v

        elif campo == "retorno":
            j["retorno"] = float(valor)

        elif campo == "nivel_acesso":
            v = str(valor).strip().upper()
            if v not in NIVEIS_JOGO:
                return 422,f"Nivel invalido. Validos: {' | '.join(NIVEIS_JOGO)}"
            j["nivel_acesso"] = v

        elif campo == "estado":
            v = str(valor).strip().upper()
            if v not in ESTADOS_JOGO:
                return 422,f"Estado invalido. Validos: {' | '.join(ESTADOS_JOGO)}"
            j["estado"] = v

        elif campo in CAMPOS_TIPOS:
            j["tipos"][campo] = _sn(valor)

        return 200,f"Campo '{campo}' actualizado com sucesso."
    except Exception as e:
        return 500,str(e)


# ══════════════════════════════════════════════════════════════
#  DELETE — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def remover_jogo(id_jogo):
    if id_jogo not in base_jogos:
        return 404,f"Jogo '{id_jogo}' nao encontrado."
    j = base_jogos.pop(id_jogo)
    return 200,f"Jogo '{j['nome']}' removido com sucesso."
