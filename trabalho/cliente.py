# ══════════════════════════════════════════════════════════════
#  FICHEIRO 1 — cliente.py
#  CRUD de clientes usando dicionarios de dicionarios
#  Sem classes, sem __init__, sem self
# ══════════════════════════════════════════════════════════════

from datetime import date

GENEROS_VALIDOS = ("M", "F", "OUTRO")
NIVEIS_VALIDOS  = ("BRONZE", "PRATA", "OURO", "PLATINA", "VIP")
ESTADOS_VALIDOS = ("ATIVO", "INATIVO")

# Base de dados: dicionario de dicionarios
# { "CLI0001": { "id": ..., "nome": ..., ... } }
base_clientes = {}
_contador_id  = [1]


# ══════════════════════════════════════════════════════════════
#  AUXILIAR
# ══════════════════════════════════════════════════════════════

def _calcular_idade(data_nasc_str):
    partes = str(data_nasc_str).strip().split("/")
    if len(partes) != 3:
        raise ValueError("Formato invalido. Use DD/MM/AAAA")
    dia, mes, ano = int(partes[0]), int(partes[1]), int(partes[2])
    nasc  = date(ano, mes, dia)
    hoje  = date.today()
    idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
    if idade < 18:
        raise ValueError(f"Cliente tem {idade} anos — idade minima e 18.")
    return f"{dia:02d}/{mes:02d}/{ano}", idade


# ══════════════════════════════════════════════════════════════
#  CREATE
# ══════════════════════════════════════════════════════════════

def criar_cliente(nome, data_nasc, genero, nacionalidade,
                  contacto, saldo, nivel, estado="ATIVO"):
    """
    Cria um novo cliente e guarda-o na base_clientes.
    Devolve o dicionario do cliente criado.

    Estrutura:
    {
        "id"             : "CLI0001",
        "nome"           : "Jose Silva",
        "data_nascimento": "20/10/2000",
        "idade"          : 24,
        "genero"         : "M",
        "nacionalidade"  : "Portuguesa",
        "contacto"       : "912345678 / jose@email.com",
        "data_registo"   : "24/03/2026",
        "saldo"          : 500.0,
        "nivel"          : "BRONZE",
        "estado"         : "ATIVO"
    }
    """
    id_cliente = f"CLI{_contador_id[0]:04d}"
    _contador_id[0] += 1

    data_fmt, idade = _calcular_idade(data_nasc)

    genero = str(genero).strip().upper()
    if genero not in GENEROS_VALIDOS:
        genero = "OUTRO"

    nivel = str(nivel).strip().upper()
    if nivel not in NIVEIS_VALIDOS:
        nivel = "BRONZE"

    estado = str(estado).strip().upper()
    if estado not in ESTADOS_VALIDOS:
        estado = "ATIVO"

    if float(saldo) < 0:
        raise ValueError("Saldo nao pode ser negativo.")

    cliente = {
        "id"             : id_cliente,
        "nome"           : str(nome).strip().title(),
        "data_nascimento": data_fmt,
        "idade"          : idade,
        "genero"         : genero,
        "nacionalidade"  : str(nacionalidade).strip().title(),
        "contacto"       : str(contacto).strip(),
        "data_registo"   : date.today().strftime("%d/%m/%Y"),
        "saldo"          : float(saldo),
        "nivel"          : nivel,
        "estado"         : estado
    }
    base_clientes[id_cliente] = cliente
    return cliente


# ══════════════════════════════════════════════════════════════
#  READ
# ══════════════════════════════════════════════════════════════

def ler_cliente_por_id(id_cliente):
    return base_clientes.get(str(id_cliente).upper(), None)


def ler_cliente_por_nome(nome):
    nome = nome.strip().title()
    for c in base_clientes.values():
        if c["nome"] == nome:
            return c
    return None


def listar_todos_clientes():
    return list(base_clientes.values())


def total_clientes():
    return len(base_clientes)


# ══════════════════════════════════════════════════════════════
#  UPDATE
# ══════════════════════════════════════════════════════════════

CAMPOS_EDITAVEIS = (
    "nome", "data_nascimento", "genero",
    "nacionalidade", "contacto", "saldo", "nivel", "estado"
)

def atualizar_cliente(id_cliente, campo, valor):
    c = ler_cliente_por_id(id_cliente)
    if not c:
        raise KeyError(f"Cliente '{id_cliente}' nao encontrado.")
    campo = campo.lower().strip()
    if campo not in CAMPOS_EDITAVEIS:
        raise KeyError(f"Campo '{campo}' invalido. Editaveis: {CAMPOS_EDITAVEIS}")

    if campo == "nome":
        if not str(valor).strip():
            raise ValueError("Nome nao pode estar vazio.")
        c["nome"] = str(valor).strip().title()

    elif campo == "data_nascimento":
        data_fmt, idade = _calcular_idade(valor)
        c["data_nascimento"] = data_fmt
        c["idade"] = idade

    elif campo == "genero":
        v = str(valor).strip().upper()
        c["genero"] = v if v in GENEROS_VALIDOS else "OUTRO"

    elif campo == "nacionalidade":
        c["nacionalidade"] = str(valor).strip().title()

    elif campo == "contacto":
        c["contacto"] = str(valor).strip()

    elif campo == "saldo":
        v = float(valor)
        if v < 0:
            raise ValueError("Saldo nao pode ser negativo.")
        c["saldo"] = v

    elif campo == "nivel":
        v = str(valor).strip().upper()
        if v not in NIVEIS_VALIDOS:
            raise ValueError(f"Nivel invalido. Validos: {NIVEIS_VALIDOS}")
        c["nivel"] = v

    elif campo == "estado":
        v = str(valor).strip().upper()
        if v not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado invalido. Validos: {ESTADOS_VALIDOS}")
        c["estado"] = v


# ══════════════════════════════════════════════════════════════
#  DELETE
# ══════════════════════════════════════════════════════════════

def remover_cliente(id_cliente):
    if id_cliente not in base_clientes:
        raise KeyError(f"Cliente '{id_cliente}' nao encontrado.")
    return base_clientes.pop(id_cliente)