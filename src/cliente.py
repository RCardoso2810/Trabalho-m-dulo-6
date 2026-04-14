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
            return 422, "Saldo nao pode ser negativo."

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

        return 201, cliente
    except Exception as e:
        return 500, "Error"


# ══════════════════════════════════════════════════════════════
#  READ — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def ler_cliente_por_id(id_cliente):
    c = base_clientes.get(str(id_cliente).upper())
    if not c:
        return 404, "Não encontrado"
    return 200, c

def ler_cliente_por_nome(nome):
    for c in base_clientes.values():
        if c["nome"].lower() == str(nome).strip().lower():
            return 200, c
    return 404, "Não encontrado"

def listar_todos_clientes():
    lista = list(base_clientes.values())
    return 200, "Cliente(s) encontrado(s)"

def total_clientes():
    return len(base_clientes)


# ══════════════════════════════════════════════════════════════
#  UPDATE — 200 OK | 404 Not Found | 400/422 erros
# ══════════════════════════════════════════════════════════════

def atualizar_cliente(id_cliente, campo, valor):
    c = base_clientes.get(str(id_cliente).upper())
    if not c:
        return 404,"Não encontrado"

    campo = campo.lower().strip()
    if campo not in CAMPOS_EDITAVEIS_CLIENTE:
        return 400, "Não foi encontrado nenhum campo com esse nome"

    try:
        if campo == "nome":
            if not str(valor).strip():
                return 400,"Nome não pode estar vazio"
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
                return 422,"Saldo não pode ser negativo"
            c["saldo"] = v

        elif campo == "nivel":
            v = str(valor).strip().upper()
            if v not in NIVEIS_VALIDOS:
                return 422,"Nivel não encotrado"
            c["nivel"] = v

        elif campo == "estado":
            v = str(valor).strip().upper()
            if v not in ESTADOS_VALIDOS:
                return 422,"Estado inválido"
            c["estado"] = v

        return 200,"Atualizado com sucesso"
    except Exception as e:
        return 500,"error"


# ══════════════════════════════════════════════════════════════
#  DELETE — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def remover_cliente(id_cliente):
    if id_cliente not in base_clientes:
        return 404,"Não encontrado"
    c = base_clientes.pop(id_cliente)
    return 200,"Eliminado com sucesso"
