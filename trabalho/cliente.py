# ══════════════════════════════════════════════════════════════
#  FICHEIRO 1 — cliente.py
#  CRUD de clientes usando dicionarios de dicionarios
#  Estruturas: tuplos, listas, sets, dicionarios, date, defs
# ══════════════════════════════════════════════════════════════

from datetime import date

# Tuplos de valores validos (imutaveis por definicao)
GENEROS_VALIDOS = ("M", "F", "OUTRO")
NIVEIS_VALIDOS  = ("BRONZE", "PRATA", "OURO", "PLATINA", "VIP")
ESTADOS_VALIDOS = ("ATIVO", "INATIVO")

# Dicionario principal: { "CLI0001": { campo: valor, ... } }
base_clientes = {}

# Lista usada como pilha para controlo do contador de IDs
# pilha_ids[0] guarda sempre o proximo numero disponivel
pilha_ids_cliente = [1]


# ══════════════════════════════════════════════════════════════
#  AUXILIAR — calcular idade a partir de data
# ══════════════════════════════════════════════════════════════

def _calcular_idade(data_nasc_str):
    # Separar a string em partes usando lista
    partes = str(data_nasc_str).strip().split("/")
    if len(partes) != 3:
        raise ValueError("Formato invalido. Use DD/MM/AAAA")
    dia  = int(partes[0])
    mes  = int(partes[1])
    ano  = int(partes[2])
    nasc = date(ano, mes, dia)
    hoje = date.today()
    # Tuplo usado para comparacao de (mes, dia)
    nascimento_par = (nasc.month, nasc.day)
    hoje_par       = (hoje.month, hoje.day)
    idade = hoje.year - nasc.year - (hoje_par < nascimento_par)
    if idade < 18:
        raise ValueError(f"Cliente tem {idade} anos — idade minima e 18.")
    # Devolve tuplo (data_formatada, idade)
    return (f"{dia:02d}/{mes:02d}/{ano}", idade)


# ══════════════════════════════════════════════════════════════
#  AUXILIAR — formatar nome com title case sem modulo re
# ══════════════════════════════════════════════════════════════

def _title(texto):
    # Divide em lista de palavras e capitaliza cada uma
    palavras = str(texto).strip().split()
    capitalizadas = []
    for p in palavras:
        if len(p) > 0:
            capitalizadas.append(p[0].upper() + p[1:].lower())
    return " ".join(capitalizadas)


# ══════════════════════════════════════════════════════════════
#  CREATE
# ══════════════════════════════════════════════════════════════

def criar_cliente(nome, data_nasc, genero, nacionalidade,
                  contacto, saldo, nivel, estado="ATIVO"):
    """
    Cria um novo cliente e guarda-o na base_clientes.
    Devolve o dicionario do cliente criado.

    Estrutura do dicionario:
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
    # Gerar ID usando a pilha de contador
    id_cliente = f"CLI{pilha_ids_cliente[0]:04d}"
    pilha_ids_cliente[0] += 1

    # Tuplo devolvido por _calcular_idade: (data_fmt, idade)
    resultado_data = _calcular_idade(data_nasc)
    data_fmt = resultado_data[0]
    idade    = resultado_data[1]

    # Validar genero contra o tuplo de valores validos
    genero_upper = str(genero).strip().upper()
    if genero_upper not in GENEROS_VALIDOS:
        genero_upper = "OUTRO"

    # Validar nivel contra o tuplo de valores validos
    nivel_upper = str(nivel).strip().upper()
    if nivel_upper not in NIVEIS_VALIDOS:
        nivel_upper = "BRONZE"

    # Validar estado contra o tuplo de valores validos
    estado_upper = str(estado).strip().upper()
    if estado_upper not in ESTADOS_VALIDOS:
        estado_upper = "ATIVO"

    if float(saldo) < 0:
        raise ValueError("Saldo nao pode ser negativo.")

    hoje = date.today()

    # Dicionario do cliente com todos os campos
    cliente = {
        "id"             : id_cliente,
        "nome"           : _title(nome),
        "data_nascimento": data_fmt,
        "idade"          : idade,
        "genero"         : genero_upper,
        "nacionalidade"  : _title(str(nacionalidade).strip()),
        "contacto"       : str(contacto).strip(),
        "data_registo"   : f"{hoje.day:02d}/{hoje.month:02d}/{hoje.year}",
        "saldo"          : float(saldo),
        "nivel"          : nivel_upper,
        "estado"         : estado_upper,
    }
    # Guardar no dicionario principal usando o ID como chave
    base_clientes[id_cliente] = cliente
    return cliente


# ══════════════════════════════════════════════════════════════
#  READ
# ══════════════════════════════════════════════════════════════

def ler_cliente_por_id(id_cliente):
    # Acesso directo ao dicionario pela chave
    return base_clientes.get(str(id_cliente).upper(), None)


def ler_cliente_por_nome(nome):
    nome_fmt = _title(str(nome).strip())
    # Iterar sobre os values do dicionario
    for c in base_clientes.values():
        if c["nome"] == nome_fmt:
            return c
    return None


def listar_todos_clientes():
    # Devolve lista de todos os values do dicionario
    return list(base_clientes.values())


def total_clientes():
    return len(base_clientes)


# ══════════════════════════════════════════════════════════════
#  UPDATE
# ══════════════════════════════════════════════════════════════

# Tuplo dos campos que podem ser editados
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
        c["nome"] = _title(str(valor).strip())

    elif campo == "data_nascimento":
        resultado = _calcular_idade(valor)
        c["data_nascimento"] = resultado[0]
        c["idade"]           = resultado[1]

    elif campo == "genero":
        v = str(valor).strip().upper()
        c["genero"] = v if v in GENEROS_VALIDOS else "OUTRO"

    elif campo == "nacionalidade":
        c["nacionalidade"] = _title(str(valor).strip())

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