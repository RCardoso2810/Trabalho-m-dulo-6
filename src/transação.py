# ══════════════════════════════════════════════════════════════
#  transacao.py
#  CRUD de transacoes — dicionarios de dicionarios
#  Estruturas: tuplos, listas, sets, dicionarios, date, defs
# ══════════════════════════════════════════════════════════════

import json
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
    validar_base_para_guardar,
    validar_ficheiro_para_carregar,
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

# ── Caminho do ficheiro JSON de persistencia
FICHEIRO_TRANSACOES = "transacoes.json"


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
    return 200, t


# ══════════════════════════════════════════════════════════════
#  PERSISTENCIA — guardar / carregar JSON
# ══════════════════════════════════════════════════════════════

def guardar_ficheiro_transacoes():
    """Guarda base_transacoes e o contador de IDs em JSON."""
    rv = validar_base_para_guardar(base_transacoes, "transacoes")
    if not rv["valido"]:
        return 404, rv["mensagem"]
    try:
        dados = {
            "base_transacoes"    : base_transacoes,
            "pilha_ids_transacao": pilha_ids_transacao,
        }
        with open(FICHEIRO_TRANSACOES, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return 200, f"Transacoes guardadas com sucesso em '{FICHEIRO_TRANSACOES}' ({len(base_transacoes)} registo(s))."
    except Exception as e:
        return 500, f"Erro ao guardar ficheiro: {e}"


def carregar_ficheiro_transacoes():
    """Carrega base_transacoes e o contador de IDs a partir do JSON."""
    rv = validar_ficheiro_para_carregar(FICHEIRO_TRANSACOES, "transacoes")
    if not rv["valido"]:
        return 404, rv["mensagem"]
    try:
        with open(FICHEIRO_TRANSACOES, "r", encoding="utf-8") as f:
            dados = json.load(f)
        base_transacoes.clear()
        base_transacoes.update(dados.get("base_transacoes", {}))
        contador_guardado = dados.get("pilha_ids_transacao", [1])
        pilha_ids_transacao[0] = contador_guardado[0]
        return 200, f"Transacoes carregadas com sucesso de '{FICHEIRO_TRANSACOES}' ({len(base_transacoes)} registo(s))."
    except Exception as e:
        return 500, f"Erro ao carregar ficheiro: {e}"
