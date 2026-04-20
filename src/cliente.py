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


# ══════════════════════════════════════════════════════════════
#  CREATE — 201 Created
# ══════════════════════════════════════════════════════════════

def criar_cliente(nome, data_nasc, genero, nacionalidade,
                  contacto, saldo, nivel, estado="ATIVO"):
    try:
        # ── Validacoes via dicionario de despacho ─────────────
        rv = validar_nome(nome)
        if not rv["valido"]:
            return 422, rv["mensagem"]

        rv = validar_data_nascimento(data_nasc)
        if not rv["valido"]:
            return 422, rv["mensagem"]

        rv = validar_genero(genero)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        genero_ok = rv["valor"]

        rv = validar_nacionalidade(nacionalidade)
        if not rv["valido"]:
            return 422, rv["mensagem"]

        rv = validar_contacto(contacto)
        if not rv["valido"]:
            return 422, rv["mensagem"]

        rv = validar_saldo(saldo)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        saldo_ok = rv["valor"]

        rv = validar_nivel(nivel)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        nivel_ok = rv["valor"]

        rv = validar_estado(estado)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        estado_ok = rv["valor"]

        # ── Construcao do registo ─────────────────────────────
        id_cliente = f"CLI{pilha_ids_cliente[0]:04d}"
        pilha_ids_cliente[0] += 1

        hoje = date.today()
        cliente = {
            "id"             : id_cliente,
            "nome"           : str(nome).strip(),
            "data_nascimento": str(data_nasc).strip(),
            "genero"         : genero_ok,
            "nacionalidade"  : str(nacionalidade).strip(),
            "contacto"       : str(contacto).strip(),
            "data_registo"   : f"{hoje.day:02d}/{hoje.month:02d}/{hoje.year}",
            "saldo"          : saldo_ok,
            "nivel"          : nivel_ok,
            "estado"         : estado_ok,
        }
        base_clientes[id_cliente] = cliente
        return 201, cliente

    except Exception as e:
        return 500, f"Erro interno: {e}"


# ══════════════════════════════════════════════════════════════
#  READ — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def ler_cliente_por_id(id_cliente):
    c = base_clientes.get(str(id_cliente).upper())
    if not c:
        return 404, "Cliente nao encontrado."
    return 200, c

def ler_cliente_por_nome(nome):
    for c in base_clientes.values():
        if c["nome"].lower() == str(nome).strip().lower():
            return 200, c
    return 404, f"Cliente '{nome}' nao encontrado."

def listar_todos_clientes():
    lista = list(base_clientes.values())
    return 200, lista

def total_clientes():
    return len(base_clientes)


# ══════════════════════════════════════════════════════════════
#  UPDATE — 200 OK | 404 Not Found | 400/422 erros
# ══════════════════════════════════════════════════════════════

def atualizar_cliente(id_cliente, campo, valor):
    c = base_clientes.get(str(id_cliente).upper())
    if not c:
        return 404, "Cliente nao encontrado."

    campo = campo.lower().strip()
    if campo not in CAMPOS_EDITAVEIS_CLIENTE:
        return 400, f"Campo '{campo}' invalido. Editaveis: {' | '.join(CAMPOS_EDITAVEIS_CLIENTE)}"

    # ── Validacao via dicionario de despacho ──────────────────
    if campo in VALIDACOES_CLIENTE:
        rv = VALIDACOES_CLIENTE[campo](valor)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        c[campo] = rv["valor"]
        return 200, f"Campo '{campo}' actualizado com sucesso."

    return 400, f"Campo '{campo}' nao pode ser editado."


# ══════════════════════════════════════════════════════════════
#  DELETE — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def remover_cliente(id_cliente):
    id_upper = str(id_cliente).upper()
    if id_upper not in base_clientes:
        return 404, f"Cliente '{id_cliente}' nao encontrado."
    c = base_clientes.pop(id_upper)
    return 200, f"Cliente '{c['nome']}' removido com sucesso."
