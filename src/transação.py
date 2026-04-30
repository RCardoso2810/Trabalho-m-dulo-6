# ══════════════════════════════════════════════════════════════
#  transacao.py
#  CRUD de transacoes — dicionarios de dicionarios
#  Estruturas: tuplos, listas, sets, dicionarios, date, defs
# ══════════════════════════════════════════════════════════════

from datetime import datetime
from utils import (
    validar_id_cliente,
    validar_tipo_transacao,
    validar_tipo_movimento,
    validar_montante,
    validar_metodo_pagamento,
    validar_estado_transacao,
    TIPOS_TRANSACAO_VALIDOS,
    TIPOS_MOVIMENTO_VALIDOS,
    METODOS_PAGAMENTO_VALIDOS,
    ESTADOS_TRANSACAO_VALIDOS,
)

# ── Dicionario principal: { "TRN00001": { campo: valor, ... } }
base_transacoes = {}

# ── Lista usada como pilha para controlo do contador de IDs
pilha_ids_transacao = [1]

# ── Tuplo dos campos editaveis
CAMPOS_EDITAVEIS_TRANSACAO = (
    "tipo", "tipo_movimento", "montante",
    "metodo_pagamento", "estado"
)

# ── Dicionario de despacho de validacao — campo -> funcao
VALIDACOES_TRANSACAO = {
    "tipo"             : validar_tipo_transacao,
    "tipo_movimento"   : validar_tipo_movimento,
    "montante"         : validar_montante,
    "metodo_pagamento" : validar_metodo_pagamento,
    "estado"           : validar_estado_transacao,
}


# ══════════════════════════════════════════════════════════════
#  CREATE — 201 Created
# ══════════════════════════════════════════════════════════════

def criar_transacao(id_cliente, tipo, tipo_movimento,
                    montante, metodo_pagamento, estado="PENDENTE"):
    try:
        rv = validar_id_cliente(id_cliente)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        id_cli_ok = rv["valor"]

        rv = validar_tipo_transacao(tipo)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        tipo_ok = rv["valor"]

        rv = validar_tipo_movimento(tipo_movimento)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        tipo_mov_ok = rv["valor"]

        rv = validar_montante(montante)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        montante_ok = rv["valor"]

        rv = validar_metodo_pagamento(metodo_pagamento)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        metodo_ok = rv["valor"]

        rv = validar_estado_transacao(estado)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        estado_ok = rv["valor"]

        # ── Construcao do registo ─────────────────────────────
        id_transacao = f"TRN{pilha_ids_transacao[0]:05d}"
        pilha_ids_transacao[0] += 1

        agora = datetime.now()
        transacao = {
            "id"               : id_transacao,
            "id_cliente"       : id_cli_ok,
            "tipo"             : tipo_ok,
            "tipo_movimento"   : tipo_mov_ok,
            "montante"         : montante_ok,
            "metodo_pagamento" : metodo_ok,
            "data_hora"        : agora.strftime("%d/%m/%Y %H:%M:%S"),
            "estado"           : estado_ok,
        }
        base_transacoes[id_transacao] = transacao
        return 201, transacao

    except Exception as e:
        return 500, f"Erro interno: {e}"


# ══════════════════════════════════════════════════════════════
#  READ — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def ler_transacao_por_id(id_transacao):
    t = base_transacoes.get(str(id_transacao).upper())
    if not t:
        return 404, "Transacao nao encontrada."
    return 200, t

def listar_transacoes_por_cliente(id_cliente):
    id_cli = str(id_cliente).strip().upper()
    lista = [t for t in base_transacoes.values() if t["id_cliente"] == id_cli]
    if not lista:
        return 404, f"Nenhuma transacao encontrada para o cliente '{id_cliente}'."
    return 200, lista

def listar_todas_transacoes():
    lista = list(base_transacoes.values())
    return 200, lista

def total_transacoes():
    return len(base_transacoes)


# ══════════════════════════════════════════════════════════════
#  UPDATE — 200 OK | 404 Not Found | 400/422 erros
# ══════════════════════════════════════════════════════════════

def atualizar_transacao(id_transacao, campo, valor):
    t = base_transacoes.get(str(id_transacao).upper())
    if not t:
        return 404, "Transacao nao encontrada."

    campo = campo.lower().strip()
    if campo not in CAMPOS_EDITAVEIS_TRANSACAO:
        return 400, f"Campo '{campo}' invalido. Editaveis: {' | '.join(CAMPOS_EDITAVEIS_TRANSACAO)}"

    if campo in VALIDACOES_TRANSACAO:
        rv = VALIDACOES_TRANSACAO[campo](valor)
        if not rv["valido"]:
            return 422, rv["mensagem"]
        t[campo] = rv["valor"]
        return 200, t

    return 400, f"Campo '{campo}' nao pode ser editado."


# ══════════════════════════════════════════════════════════════
#  DELETE — 200 OK | 404 Not Found
# ══════════════════════════════════════════════════════════════

def remover_transacao(id_transacao):
    id_upper = str(id_transacao).upper()
    if id_upper not in base_transacoes:
        return 404, f"Transacao '{id_transacao}' nao encontrada."
    t = base_transacoes.pop(id_upper)
    return 200, f"Transacao '{t['id']}' removida com sucesso."
