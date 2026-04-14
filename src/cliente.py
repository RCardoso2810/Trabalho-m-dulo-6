# ══════════════════════════════════════════════════════════════
#  cliente.py
#  CRUD de clientes — dicionarios de dicionarios
#  Estruturas: tuplos, listas, sets, dicionarios, date, defs
# ══════════════════════════════════════════════════════════════

from datetime import date
from utils import (
    validar_nome,
    validar_data_nascimento,
    validar_genero,
    validar_nacionalidade,
    validar_contacto,
    validar_saldo,
    validar_nivel,
    validar_estado,
)

# Tuplos de valores validos (imutaveis)
GENEROS_VALIDOS = ("M", "F", "OUTRO")
NIVEIS_VALIDOS  = ("BRONZE", "PRATA", "OURO", "PLATINA", "VIP")
ESTADOS_VALIDOS = ("ATIVO", "INATIVO")

# Dicionario principal: { "CLI0001": { campo: valor, ... } }
base_clientes = {}

# Lista usada como pilha para controlo do contador de IDs
pilha_ids_cliente = [1]

# Tuplo dos campos editaveis
CAMPOS_EDITAVEIS_CLIENTE = (
    "nome", "data_nascimento", "genero",
    "nacionalidade", "contacto", "saldo", "nivel", "estado"
)

# Dicionario de despacho de validacao — campo -> funcao
VALIDACOES_CLIENTE = {
    "nome"            : validar_nome,
    "data_nascimento" : validar_data_nascimento,
    "genero"          : validar_genero,
    "nacionalidade"   : validar_nacionalidade,
    "contacto"        : validar_contacto,
    "saldo"           : validar_saldo,
    "nivel"           : validar_nivel,
    "estado"          : validar_estado,
}


# ── Resultado de operacao CRUD ────────────────────────────────

def _resposta(code, dados=None, mensagem=""):
    codigos = {
        200: "200 OK",
        201: "201 Created",
        204: "204 No Content",
        400: "400 Bad Request",
        404: "404 Not Found",
        409: "409 Conflict",
        422: "422 Unprocessable Entity",
        500: "500 Internal Server Error",
    }
    return {
        "status"  : code,
        "ok"      : codigos.get(code, str(code)),
        "dados"   : dados,
        "mensagem": mensagem,
    }


# ══════════════════════════════════════════════════════════════
#  CREATE — 201 Created
# ══════════════════════════════════════════════════════════════

def criar_cliente(nome, data_nasc, genero, nacionalidade,
                  contacto, saldo, nivel, estado="ATIVO"):
    try:
        id_cliente = f"CLI{pilha_ids_cliente[0]:04d}"
        pilha_ids_cliente[0] += 1

        genero_upper = str(genero).strip().upper()
        if genero_upper not in GENEROS_VALIDOS:
            genero_upper = "OUTRO"

        nivel_upper = str(nivel).strip().upper()
        if nivel_upper not in NIVEIS_VALIDOS:
            nivel_upper = "BRONZE"

        estado_upper = str(estado).strip().upper()
        if estado_upper not in ESTADOS_VALIDOS:
            estado_upper = "ATIVO"

        if float(saldo) < 0:
            return _resposta(422, mensagem="Saldo nao pode ser negativo.")

        hoje = date.today()
        cliente = {
            "id"             : id_cliente,
            "nome"           : str(nome).strip(),
            "data_nascimento": str(data_nasc).strip(),
            "genero"         : genero_upper,
            "nacionalidade"  : str(nacionalidade).strip(),
            "contacto"       : str(contacto).strip(),
            "data_registo"   : f"{hoje.day:02d}/{hoje.month:02d}/{hoje.year}",
            "saldo"          : float(saldo),
            "nivel"          : nivel_upper,
            "estado"         : estado_upper,
        }
        base_clientes[id_cliente] = cliente
        return _resposta(201, dados=cliente, mensagem=f"Cliente '{id_cliente}' criado com sucesso.")
    except Exception as e:
        return _resposta(500, mensagem=str(e))


# ══════════════════════════════════════════════════════════════
#  READ — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def ler_cliente_por_id(id_cliente):
    c = base_clientes.get(str(id_cliente).upper())
    if not c:
        return _resposta(404, mensagem=f"Cliente '{id_cliente}' nao encontrado.")
    return _resposta(200, dados=c)

def ler_cliente_por_nome(nome):
    for c in base_clientes.values():
        if c["nome"].lower() == str(nome).strip().lower():
            return _resposta(200, dados=c)
    return _resposta(404, mensagem=f"Cliente '{nome}' nao encontrado.")

def listar_todos_clientes():
    lista = list(base_clientes.values())
    return _resposta(200, dados=lista, mensagem=f"{len(lista)} cliente(s) encontrado(s).")

def total_clientes():
    return len(base_clientes)


# ══════════════════════════════════════════════════════════════
#  UPDATE — 200 OK | 404 Not Found | 400/422 erros
# ══════════════════════════════════════════════════════════════

def atualizar_cliente(id_cliente, campo, valor):
    c = base_clientes.get(str(id_cliente).upper())
    if not c:
        return _resposta(404, mensagem=f"Cliente '{id_cliente}' nao encontrado.")

    campo = campo.lower().strip()
    if campo not in CAMPOS_EDITAVEIS_CLIENTE:
        return _resposta(400, mensagem=f"Campo '{campo}' invalido. Editaveis: {' | '.join(CAMPOS_EDITAVEIS_CLIENTE)}")

    try:
        if campo == "nome":
            if not str(valor).strip():
                return _resposta(400, mensagem="Nome nao pode estar vazio.")
            c["nome"] = str(valor).strip()

        elif campo == "data_nascimento":
            c["data_nascimento"] = str(valor).strip()

        elif campo == "genero":
            v = str(valor).strip().upper()
            c["genero"] = v if v in GENEROS_VALIDOS else "OUTRO"

        elif campo == "nacionalidade":
            c["nacionalidade"] = str(valor).strip()

        elif campo == "contacto":
            c["contacto"] = str(valor).strip()

        elif campo == "saldo":
            v = float(valor)
            if v < 0:
                return _resposta(422, mensagem="Saldo nao pode ser negativo.")
            c["saldo"] = v

        elif campo == "nivel":
            v = str(valor).strip().upper()
            if v not in NIVEIS_VALIDOS:
                return _resposta(422, mensagem=f"Nivel invalido. Validos: {' | '.join(NIVEIS_VALIDOS)}")
            c["nivel"] = v

        elif campo == "estado":
            v = str(valor).strip().upper()
            if v not in ESTADOS_VALIDOS:
                return _resposta(422, mensagem=f"Estado invalido. Validos: {' | '.join(ESTADOS_VALIDOS)}")
            c["estado"] = v

        return _resposta(200, dados=c, mensagem=f"Campo '{campo}' actualizado com sucesso.")
    except Exception as e:
        return _resposta(500, mensagem=str(e))


# ══════════════════════════════════════════════════════════════
#  DELETE — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def remover_cliente(id_cliente):
    if id_cliente not in base_clientes:
        return _resposta(404, mensagem=f"Cliente '{id_cliente}' nao encontrado.")
    c = base_clientes.pop(id_cliente)
    return _resposta(200, dados=c, mensagem=f"Cliente '{c['nome']}' removido com sucesso.")