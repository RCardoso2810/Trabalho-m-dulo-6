# ══════════════════════════════════════════════════════════════
#  FICHEIRO 2 — jogo.py
#  CRUD de jogos usando dicionarios de dicionarios
#  Sem classes, sem __init__, sem self
# ══════════════════════════════════════════════════════════════

from datetime import date

ESTADOS_JOGO = ("ATIVO", "INATIVO")
NIVEIS_JOGO  = ("BRONZE", "PRATA", "OURO", "PLATINA", "VIP")

# Base de dados: dicionario de dicionarios
# { "JOG0001": { "id": ..., "nome": ..., "tipos": {...}, ... } }
base_jogos   = {}
_contador_id = [1]


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

    Estrutura:
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
    id_jogo = f"JOG{_contador_id[0]:04d}"
    _contador_id[0] += 1

    nivel_acesso = str(nivel_acesso).strip().upper()
    if nivel_acesso not in NIVEIS_JOGO:
        nivel_acesso = "BRONZE"

    estado = str(estado).strip().upper()
    if estado not in ESTADOS_JOGO:
        estado = "ATIVO"

    custo_minimo = float(custo_minimo)
    if custo_minimo < 0:
        raise ValueError("Custo minimo nao pode ser negativo.")

    saldo_jogo = float(saldo_jogo)
    if saldo_jogo < 0:
        raise ValueError("Saldo do jogo nao pode ser negativo.")

    def _sn(v):
        return "SIM" if str(v).strip().upper() == "SIM" else "NAO"

    jogo = {
        "id"           : id_jogo,
        "nome"         : str(nome).strip().title(),
        "custo_minimo" : custo_minimo,
        "saldo_jogo"   : saldo_jogo,
        "retorno"      : float(retorno),
        "nivel_acesso" : nivel_acesso,
        "estado"       : estado,
        "data_criacao" : date.today().strftime("%d/%m/%Y"),
        "tipos"        : {
            "dealer"    : _sn(tem_dealer),
            "tabuleiro" : _sn(tem_tabuleiro),
            "pecas"     : _sn(tem_pecas),
            "cartas"    : _sn(tem_cartas),
            "dados"     : _sn(tem_dados),
            "maquina"   : _sn(tem_maquina)
        }
    }
    base_jogos[id_jogo] = jogo
    return jogo


# ══════════════════════════════════════════════════════════════
#  READ
# ══════════════════════════════════════════════════════════════

def ler_jogo_por_id(id_jogo):
    return base_jogos.get(str(id_jogo).upper(), None)


def ler_jogo_por_nome(nome):
    nome = nome.strip().title()
    for j in base_jogos.values():
        if j["nome"] == nome:
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
        j["nome"] = str(valor).strip().title()

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

    elif campo in ("dealer", "tabuleiro", "pecas", "cartas", "dados", "maquina"):
        j["tipos"][campo] = "SIM" if str(valor).strip().upper() == "SIM" else "NAO"


# ══════════════════════════════════════════════════════════════
#  DELETE
# ══════════════════════════════════════════════════════════════

def remover_jogo(id_jogo):
    if id_jogo not in base_jogos:
        raise KeyError(f"Jogo '{id_jogo}' nao encontrado.")
    return base_jogos.pop(id_jogo)