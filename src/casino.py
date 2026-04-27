# ══════════════════════════════════════════════════════════════
#  casino.py
#  CRUD de casinos — dicionarios de dicionarios
#  Estruturas: tuplos, listas, sets, dicionarios, date, defs
# ══════════════════════════════════════════════════════════════

# ── Tuplos de valores validos (imutaveis) ─────────────────────
MOEDAS_VALIDAS = ("EUR", "USD", "GBP", "CHF", "JPY")

# ── Dicionario principal: { "CAS0001": { campo: valor, ... } }
base_casinos = {}

# ── Lista usada como pilha para controlo do contador de IDs
pilha_ids_casino = [1]

# ── Tuplo dos campos editaveis
CAMPOS_EDITAVEIS_CASINO = (
    "nome", "localizacao", "taxa", "moeda", "capacidade_maxima"
)


# ══════════════════════════════════════════════════════════════
#  VALIDACOES INTERNAS
# ══════════════════════════════════════════════════════════════

def _validar_nome(nome):
    v = str(nome).strip()
    if len(v) < 2:
        return {"valido": False, "mensagem": "Nome deve ter pelo menos 2 caracteres.", "valor": None}
    return {"valido": True, "mensagem": "OK", "valor": v}

def _validar_localizacao(loc):
    v = str(loc).strip()
    if len(v) < 2:
        return {"valido": False, "mensagem": "Localizacao invalida.", "valor": None}
    return {"valido": True, "mensagem": "OK", "valor": v}

def _validar_taxa(taxa):
    try:
        v = float(taxa)
        if not (0.0 <= v <= 100.0):
            return {"valido": False, "mensagem": "Taxa deve estar entre 0 e 100.", "valor": None}
        return {"valido": True, "mensagem": "OK", "valor": round(v, 2)}
    except (ValueError, TypeError):
        return {"valido": False, "mensagem": "Taxa invalida. Deve ser um numero.", "valor": None}

def _validar_moeda(moeda):
    v = str(moeda).strip().upper()
    if v not in MOEDAS_VALIDAS:
        return {"valido": False, "mensagem": f"Moeda invalida. Validas: {' | '.join(MOEDAS_VALIDAS)}", "valor": None}
    return {"valido": True, "mensagem": "OK", "valor": v}

def _validar_capacidade(cap):
    try:
        v = int(cap)
        if v <= 0:
            return {"valido": False, "mensagem": "Capacidade deve ser maior que 0.", "valor": None}
        return {"valido": True, "mensagem": "OK", "valor": v}
    except (ValueError, TypeError):
        return {"valido": False, "mensagem": "Capacidade invalida. Deve ser um numero inteiro.", "valor": None}

# ── Dicionario de despacho de validacao — campo -> funcao
VALIDACOES_CASINO = {
    "nome"             : _validar_nome,
    "localizacao"      : _validar_localizacao,
    "taxa"             : _validar_taxa,
    "moeda"            : _validar_moeda,
    "capacidade_maxima": _validar_capacidade,
}


# ══════════════════════════════════════════════════════════════
#  CREATE — 201 Created
# ══════════════════════════════════════════════════════════════

def criar_casino(nome, localizacao, taxa, moeda, capacidade_maxima):
    try:
        rv = _validar_nome(nome)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        nome_ok = rv["valor"]

        rv = _validar_localizacao(localizacao)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        loc_ok = rv["valor"]

        rv = _validar_taxa(taxa)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        taxa_ok = rv["valor"]

        rv = _validar_moeda(moeda)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        moeda_ok = rv["valor"]

        rv = _validar_capacidade(capacidade_maxima)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        cap_ok = rv["valor"]

        # ── Construcao do registo ─────────────────────────────
        id_casino = f"CAS{pilha_ids_casino[0]:04d}"
        pilha_ids_casino[0] += 1

        casino = {
            "id"               : id_casino,
            "nome"             : nome_ok,
            "localizacao"      : loc_ok,
            "taxa"             : taxa_ok,
            "moeda"            : moeda_ok,
            "capacidade_maxima": cap_ok,
            "salas"            : {
                "jogos"        : [],
                "funcionarios" : [],
                "clientes"     : [],
            },
        }
        base_casinos[id_casino] = casino
        return 201, casino

    except Exception as e:
        return 500, f"Erro interno: {e}"


# ══════════════════════════════════════════════════════════════
#  READ — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def ler_casino_por_id(id_casino):
    c = base_casinos.get(str(id_casino).upper())
    if not c:
        return 404, "Casino nao encontrado."
    return 200, c

def ler_casino_por_nome(nome):
    for c in base_casinos.values():
        if c["nome"].lower() == str(nome).strip().lower():
            return 200, c
    return 404, f"Casino '{nome}' nao encontrado."

def listar_todos_casinos():
    lista = list(base_casinos.values())
    return 200, lista

def total_casinos():
    return len(base_casinos)


# ══════════════════════════════════════════════════════════════
#  UPDATE — 200 OK | 404 Not Found | 400/422 erros
# ══════════════════════════════════════════════════════════════

def atualizar_casino(id_casino, campo, valor):
    c = base_casinos.get(str(id_casino).upper())
    if not c:
        return 404, "Casino nao encontrado."

    campo = campo.lower().strip()
    if campo not in CAMPOS_EDITAVEIS_CASINO:
        return 400, f"Campo '{campo}' invalido. Editaveis: {' | '.join(CAMPOS_EDITAVEIS_CASINO)}"

    if campo in VALIDACOES_CASINO:
        rv = VALIDACOES_CASINO[campo](valor)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        c[campo] = rv["valor"]
        return 200, c  # ← devolve objeto completo

    return 400, f"Campo '{campo}' nao pode ser editado."


# ══════════════════════════════════════════════════════════════
#  SALAS — gerir jogos / funcionarios / clientes
# ══════════════════════════════════════════════════════════════

def adicionar_item_sala(id_casino, tipo, item_id):
    """
    tipo: 'jogos' | 'funcionarios' | 'clientes'
    item_id: ID do jogo / funcionario / cliente
    """
    c = base_casinos.get(str(id_casino).upper())
    if not c:
        return 404, "Casino nao encontrado."

    tipo = str(tipo).lower().strip()
    if tipo not in ("jogos", "funcionarios", "clientes"):
        return 400, "Tipo invalido. Use: jogos | funcionarios | clientes"

    item_id = str(item_id).strip().upper()
    if item_id in c["salas"][tipo]:
        return 409, f"'{item_id}' ja existe nas {tipo} deste casino."

    c["salas"][tipo].append(item_id)
    return 200, c

def remover_item_sala(id_casino, tipo, item_id):
    c = base_casinos.get(str(id_casino).upper())
    if not c:
        return 404, "Casino nao encontrado."

    tipo = str(tipo).lower().strip()
    if tipo not in ("jogos", "funcionarios", "clientes"):
        return 400, "Tipo invalido. Use: jogos | funcionarios | clientes"

    item_id = str(item_id).strip().upper()
    if item_id not in c["salas"][tipo]:
        return 404, f"'{item_id}' nao encontrado nas {tipo} deste casino."

    c["salas"][tipo].remove(item_id)
    return 200, c

def listar_sala(id_casino, tipo):
    c = base_casinos.get(str(id_casino).upper())
    if not c:
        return 404, "Casino nao encontrado."

    tipo = str(tipo).lower().strip()
    if tipo not in ("jogos", "funcionarios", "clientes"):
        return 400, "Tipo invalido. Use: jogos | funcionarios | clientes"

    return 200, c["salas"][tipo]


# ══════════════════════════════════════════════════════════════
#  DELETE — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def remover_casino(id_casino):
    id_upper = str(id_casino).upper()
    if id_upper not in base_casinos:
        return 404, f"Casino '{id_casino}' nao encontrado."
    c = base_casinos.pop(id_upper)
    return 200, f"Casino '{c['nome']}' removido com sucesso."
