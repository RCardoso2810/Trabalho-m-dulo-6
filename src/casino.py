# ══════════════════════════════════════════════════════════════
#  casino.py
#  CRUD de casinos — dicionarios de dicionarios
#  Estruturas: tuplos, listas, sets, dicionarios, date, defs
# ══════════════════════════════════════════════════════════════

from utils import (
    validar_nome,
    validar_localizacao,
    validar_taxa,
    validar_moeda,
    validar_capacidade,
    gerar_id_casino,
    MOEDAS_VALIDAS,
)

# ── Dicionario principal: { "J01": { campo: valor, ... } }
base_casinos = {}

# ── Dicionario auxiliar de contadores por casino — { "J01_cliente": 2, ... }
contadores_filhos = {}

# ── Tuplo dos campos editaveis
CAMPOS_EDITAVEIS_CASINO = (
    "nome", "localizacao", "taxa", "moeda", "capacidade_maxima"
)

# ── Dicionario de despacho de validacao — campo -> funcao
VALIDACOES_CASINO = {
    "nome"             : validar_nome,
    "localizacao"      : validar_localizacao,
    "taxa"             : validar_taxa,
    "moeda"            : validar_moeda,
    "capacidade_maxima": validar_capacidade,
}


# ══════════════════════════════════════════════════════════════
#  CREATE — 201 Created
# ══════════════════════════════════════════════════════════════

def criar_casino(nome, localizacao, taxa, moeda, capacidade_maxima):
    try:
        rv = validar_nome(nome)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        nome_ok = rv["valor"]

        rv = validar_localizacao(localizacao)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        loc_ok = rv["valor"]

        rv = validar_taxa(taxa)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        taxa_ok = rv["valor"]

        rv = validar_moeda(moeda)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        moeda_ok = rv["valor"]

        rv = validar_capacidade(capacidade_maxima)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        cap_ok = rv["valor"]

        # ── Construcao do registo ─────────────────────────────
        id_casino = gerar_id_casino(nome_ok)

        casino = {
            "id"               : id_casino,
            "nome"             : nome_ok,
            "localizacao"      : loc_ok,
            "taxa"             : taxa_ok,
            "moeda"            : moeda_ok,
            "capacidade_maxima": cap_ok,
            "total_clientes"   : 0,
            "total_jogos"      : 0,
            "ids_clientes"     : [],
            "ids_jogos"        : [],
        }
        base_casinos[id_casino] = casino
        return 201, casino

    except Exception as e:
        return 500, f"Erro interno: {e}"


# ══════════════════════════════════════════════════════════════
#  READ — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def ler_casino_por_id(id_casino):
    c = base_casinos.get(str(id_casino).strip().upper())
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

def listar_casinos_disponiveis():
    return [(c["id"], c["nome"]) for c in base_casinos.values()]




# ══════════════════════════════════════════════════════════════
#  UPDATE — 200 OK | 404 Not Found | 400/422 erros
# ══════════════════════════════════════════════════════════════

def atualizar_casino(id_casino, campo, valor):
    c = base_casinos.get(str(id_casino).strip().upper())
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
        return 200, c

    return 400, f"Campo '{campo}' nao pode ser editado."


# ══════════════════════════════════════════════════════════════
#  DELETE — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def remover_casino(id_casino):
    id_upper = str(id_casino).strip().upper()
    if id_upper not in base_casinos:
        return 404, f"Casino '{id_casino}' nao encontrado."
    c = base_casinos.pop(id_upper)
    return 200, f"Casino '{id_casino}' removido com sucesso."
