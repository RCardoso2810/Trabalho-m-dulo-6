# ══════════════════════════════════════════════════════════════
#  FICHEIRO 2 — jogo.py
#  CRUD de jogos usando dicionarios de dicionarios
#  Estruturas: tuplos, listas, sets, dicionarios, date, defs
#  As validacoes de jogo vivem aqui (importadas de utils)
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

# ── Re-exportar para que a main possa importar tudo de jogo ──
# A main nao precisa de saber que as utils existem
validar_nome_jogo_pub    = validar_nome_jogo
validar_custo_minimo_pub = validar_custo_minimo
validar_saldo_jogo_pub   = validar_saldo_jogo
validar_retorno_pub      = validar_retorno
validar_sim_nao_pub      = validar_sim_nao

# Tuplos de valores validos (imutaveis)
ESTADOS_JOGO = ("ATIVO", "INATIVO")
NIVEIS_JOGO  = ("BRONZE", "PRATA", "OURO", "PLATINA", "VIP")

# Dicionario principal: { "JOG0001": { campo: valor, ... } }
base_jogos = {}

# Lista usada como pilha para controlo do contador de IDs
pilha_ids_jogo = [1]

# Set dos campos que sao tipos (sub-dicionario "tipos")
CAMPOS_TIPOS = {"dealer", "tabuleiro", "pecas", "cartas", "dados", "maquina"}

# Dicionario de despacho de validacao — campo -> funcao
# Exportado para a main usar directamente sem importar utils
VALIDACOES_JOGO = {
    "nome"         : validar_nome_jogo,
    "custo_minimo" : validar_custo_minimo,
    "saldo_jogo"   : validar_saldo_jogo,
    "retorno"      : validar_retorno,
    "nivel_acesso" : lambda v: validar_nivel(v, "Nivel de acesso"),
    "estado"       : validar_estado,
}

# Dicionario de despacho para campos SIM/NAO
VALIDACOES_TIPOS_JOGO = {
    "dealer"    : lambda v: validar_sim_nao(v, "dealer"),
    "tabuleiro" : lambda v: validar_sim_nao(v, "tabuleiro"),
    "pecas"     : lambda v: validar_sim_nao(v, "pecas"),
    "cartas"    : lambda v: validar_sim_nao(v, "cartas"),
    "dados"     : lambda v: validar_sim_nao(v, "dados"),
    "maquina"   : lambda v: validar_sim_nao(v, "maquina"),
}


# ══════════════════════════════════════════════════════════════
#  AUXILIAR — title case sem modulo re
# ══════════════════════════════════════════════════════════════

def _title(texto):
    palavras = str(texto).strip().split()
    capitalizadas = []
    for p in palavras:
        if len(p) > 0:
            capitalizadas.append(p[0].upper() + p[1:].lower())
    return " ".join(capitalizadas)


# ══════════════════════════════════════════════════════════════
#  AUXILIAR — converter valor para SIM/NAO
# ══════════════════════════════════════════════════════════════

def _sn(v):
    return "SIM" if str(v).strip().upper() == "SIM" else "NAO"


# ══════════════════════════════════════════════════════════════
#  CREATE
# ══════════════════════════════════════════════════════════════

def criar_jogo(nome, custo_minimo, saldo_jogo, retorno,
               nivel_acesso, estado,
               tem_dealer, tem_tabuleiro, tem_pecas,
               tem_cartas, tem_dados, tem_maquina):
    """
    Cria um novo jogo e guarda-o em base_jogos.
    Devolve o dicionario do jogo criado.

    Estrutura do dicionario:
    {
        "id"           : "JOG0001",
        "nome"         : "Roleta",
        "custo_minimo" : 5.0,
        "saldo_jogo"   : 50000.0,
        "retorno"      : 35.0,
        "nivel_acesso" : "BRONZE",
        "estado"       : "ATIVO",
        "data_criacao" : "19/03/2026",
        "tipos"        : {
            "dealer"    : "SIM",
            "tabuleiro" : "SIM",
            "pecas"     : "NAO",
            "cartas"    : "NAO",
            "dados"     : "NAO",
            "maquina"   : "NAO"
        }
    }
    """
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
        raise ValueError("Custo minimo nao pode ser negativo.")

    saldo = float(saldo_jogo)
    if saldo < 0:
        raise ValueError("Saldo do jogo nao pode ser negativo.")

    hoje = date.today()

    # Dicionario de tipos do jogo (sub-dicionario)
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
        "nome"         : _title(str(nome).strip()),
        "custo_minimo" : custo,
        "saldo_jogo"   : saldo,
        "retorno"      : float(retorno),
        "nivel_acesso" : nivel_upper,
        "estado"       : estado_upper,
        "data_criacao" : f"{hoje.day:02d}/{hoje.month:02d}/{hoje.year}",
        "tipos"        : tipos,
    }
    base_jogos[id_jogo] = jogo
    return jogo


# ══════════════════════════════════════════════════════════════
#  READ
# ══════════════════════════════════════════════════════════════

def ler_jogo_por_id(id_jogo):
    return base_jogos.get(str(id_jogo).upper(), None)


def ler_jogo_por_nome(nome):
    nome_fmt = _title(str(nome).strip())
    for j in base_jogos.values():
        if j["nome"] == nome_fmt:
            return j
    return None


def listar_todos_jogos():
    return list(base_jogos.values())


def listar_jogos_ativos():
    return [j for j in base_jogos.values() if j["estado"] == "ATIVO"]


def total_jogos():
    return len(base_jogos)


# ══════════════════════════════════════════════════════════════
#  UPDATE
# ══════════════════════════════════════════════════════════════

# Tuplo dos campos editaveis de jogo
CAMPOS_EDITAVEIS_JOGO = (
    "nome", "custo_minimo", "saldo_jogo", "retorno",
    "nivel_acesso", "estado",
    "dealer", "tabuleiro", "pecas", "cartas", "dados", "maquina"
)

def atualizar_jogo(id_jogo, campo, valor):
    j = ler_jogo_por_id(id_jogo)
    if not j:
        raise KeyError(f"Jogo '{id_jogo}' nao encontrado.")
    campo = campo.lower().strip()
    if campo not in CAMPOS_EDITAVEIS_JOGO:
        raise KeyError(f"Campo '{campo}' invalido. Editaveis: {CAMPOS_EDITAVEIS_JOGO}")

    if campo == "nome":
        if not str(valor).strip():
            raise ValueError("Nome nao pode estar vazio.")
        j["nome"] = _title(str(valor).strip())

    elif campo == "custo_minimo":
        v = float(valor)
        if v < 0:
            raise ValueError("Custo minimo nao pode ser negativo.")
        j["custo_minimo"] = v

    elif campo == "saldo_jogo":
        v = float(valor)
        if v < 0:
            raise ValueError("Saldo nao pode ser negativo.")
        j["saldo_jogo"] = v

    elif campo == "retorno":
        j["retorno"] = float(valor)

    elif campo == "nivel_acesso":
        v = str(valor).strip().upper()
        if v not in NIVEIS_JOGO:
            raise ValueError(f"Nivel invalido. Validos: {NIVEIS_JOGO}")
        j["nivel_acesso"] = v

    elif campo == "estado":
        v = str(valor).strip().upper()
        if v not in ESTADOS_JOGO:
            raise ValueError(f"Estado invalido. Validos: {ESTADOS_JOGO}")
        j["estado"] = v

    elif campo in CAMPOS_TIPOS:
        j["tipos"][campo] = _sn(valor)


# ══════════════════════════════════════════════════════════════
#  DELETE
# ══════════════════════════════════════════════════════════════

def remover_jogo(id_jogo):
    if id_jogo not in base_jogos:
        raise KeyError(f"Jogo '{id_jogo}' nao encontrado.")
    return base_jogos.pop(id_jogo)
