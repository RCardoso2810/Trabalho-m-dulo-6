# ══════════════════════════════════════════════════════════════
#  utils.py
#  Validacoes com HTTP status codes
#  SEM modulo re — validacoes manuais
# ══════════════════════════════════════════════════════════════

from datetime import date

# ── Sets de caracteres validos ────────────────────────────────
LETRAS_NOME = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"
    "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ"
    " -"
)

LETRAS_JOGO = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"
    "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ"
    "0123456789 -'."
)

DIGITOS        = set("0123456789")
CHARS_TELEFONE = set("0123456789 +-() ")

# Tuplos de valores validos
GENEROS_VALIDOS = ("M", "F", "OUTRO")
NIVEIS_VALIDOS  = ("BRONZE", "PRATA", "OURO", "PLATINA", "VIP")
ESTADOS_VALIDOS = ("ATIVO", "INATIVO")


# ── Resultado de validacao ────────────────────────────────────

def _ok(valor):
    return {"status": 200, "ok": "200 OK", "valido": True, "mensagem": "", "valor": valor}

def _erro(mensagem, code=422):
    codigos = {
        400: "400 Bad Request",
        404: "404 Not Found",
        409: "409 Conflict",
        422: "422 Unprocessable Entity",
    }
    return {"status": code, "ok": codigos.get(code, str(code)), "valido": False, "mensagem": mensagem, "valor": None}


# ── Auxiliares internos ───────────────────────────────────────

def _tem_digito(texto):
    return any(c in DIGITOS for c in texto)

def _todos_chars_validos(texto, chars_validos):
    return all(c in chars_validos for c in texto)

def _e_email_valido(texto):
    partes = texto.split("@")
    if len(partes) != 2:
        return False
    antes, depois = partes
    if not antes or not depois or " " in antes or " " in depois:
        return False
    if "." not in depois:
        return False
    return all(p for p in depois.split("."))

def _e_telefone_valido(texto):
    sem_espacos = texto.replace(" ", "")
    return 7 <= len(sem_espacos) <= 20 and _todos_chars_validos(texto, CHARS_TELEFONE)


# ══════════════════════════════════════════════════════════════
#  VALIDACOES
# ══════════════════════════════════════════════════════════════

def validar_nome(nome):
    nome = str(nome).strip()
    if not nome:
        return _erro("Nome nao pode estar vazio.  Ex: Rodrigo Manel", 400)
    if _tem_digito(nome):
        return _erro(f"O nome nao pode conter numeros.  Recebido: \"{nome}\"", 422)
    if not _todos_chars_validos(nome, LETRAS_NOME):
        return _erro(f"O nome so pode conter letras, espacos e hifens.  Recebido: \"{nome}\"", 422)
    partes = nome.split()
    if len(partes) < 2:
        return _erro(f"Minimo dois nomes (proprio e apelido).  Recebido: \"{nome}\"", 422)
    for parte in partes:
        if len(parte) < 2:
            return _erro(f"A parte \"{parte}\" e demasiado curta (min. 2 letras).", 422)
    return _ok(nome)


def validar_data_nascimento(data_str, idade_minima=18):
    data_str = str(data_str).strip()
    if not data_str:
        return _erro("A data de nascimento nao pode estar vazia.  Ex: 20/10/1995", 400)
    partes = data_str.split("/")
    if len(partes) != 3:
        return _erro(f"Formato invalido. Use DD/MM/AAAA.  Recebido: \"{data_str}\"", 422)
    for p in partes:
        if not _todos_chars_validos(p, DIGITOS):
            return _erro(f"A data deve conter apenas numeros separados por '/'.  Recebido: \"{data_str}\"", 422)
    dia, mes, ano = int(partes[0]), int(partes[1]), int(partes[2])
    hoje = date.today()
    if ano < 1900 or ano > hoje.year:
        return _erro(f"Ano invalido: {ano}. Deve estar entre 1900 e {hoje.year}.", 422)
    if mes < 1 or mes > 12:
        return _erro(f"Mes invalido: {mes}. Deve estar entre 1 e 12.", 422)
    dias_por_mes = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    bissexto = (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0)
    max_dias = dias_por_mes[mes] if mes != 2 else (29 if bissexto else 28)
    if dia < 1 or dia > max_dias:
        return _erro(f"Dia invalido: {dia} para o mes {mes} (max {max_dias}).", 422)
    nasc = date(ano, mes, dia)
    if nasc > hoje:
        return _erro(f"A data de nascimento nao pode ser no futuro.  Recebido: {data_str}", 422)
    idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
    if idade < idade_minima:
        return _erro(f"Idade insuficiente: {idade} anos. Minimo: {idade_minima} anos.", 422)
    return _ok(f"{dia:02d}/{mes:02d}/{ano}")


def validar_genero(genero):
    mapa = {
        "M": "M", "MASCULINO": "M", "MALE": "M", "HOMEM": "M",
        "F": "F", "FEMININO": "F", "FEMALE": "F", "MULHER": "F",
        "OUTRO": "OUTRO", "OTHER": "OUTRO",
        "NAO BINARIO": "OUTRO", "NAO-BINARIO": "OUTRO",
    }
    g = str(genero).strip().upper()
    if g in mapa:
        return _ok(mapa[g])
    return _erro(f"Genero invalido: \"{genero}\".  Validos: {' | '.join(GENEROS_VALIDOS)}", 422)


def validar_nacionalidade(nacionalidade):
    n = str(nacionalidade).strip()
    if not n:
        return _erro("A nacionalidade nao pode estar vazia.  Ex: Portuguesa", 400)
    if _tem_digito(n):
        return _erro(f"A nacionalidade nao pode conter numeros.  Recebido: \"{n}\"", 422)
    if not _todos_chars_validos(n, LETRAS_NOME):
        return _erro(f"Apenas letras, espacos e hifens.  Recebido: \"{n}\"", 422)
    if len(n) < 3:
        return _erro("Nacionalidade demasiado curta (min. 3 letras).  Ex: Portuguesa", 422)
    return _ok(n)


def validar_contacto(contacto):
    c = str(contacto).strip()
    if not c:
        return _erro("O contacto nao pode estar vazio.  Ex: 912345678 / jose@email.com", 400)
    for parte in [p.strip() for p in c.split("/")]:
        if not _e_telefone_valido(parte) and not _e_email_valido(parte):
            return _erro(f"Contacto invalido: \"{parte}\".  Deve ser telefone ou email.", 422)
    return _ok(c)


def validar_saldo(saldo):
    s = str(saldo).replace(",", ".").strip()
    s_teste = s[1:] if s.startswith("-") else s
    chars_numero = set("0123456789.")
    if not s_teste or not _todos_chars_validos(s_teste, chars_numero) or s_teste.count(".") > 1:
        return _erro(f"Saldo invalido: \"{saldo}\".  Ex: 500  ou  1250.75  ou  0", 422)
    v = float(s)
    if v < 0:
        return _erro(f"O saldo nao pode ser negativo: {v:.2f} EUR.", 422)
    return _ok(round(v, 2))


def validar_nivel(nivel, etiqueta="Nivel"):
    v = str(nivel).strip().upper()
    if v in NIVEIS_VALIDOS:
        return _ok(v)
    return _erro(f"{etiqueta} invalido: \"{nivel}\".  Validos: {' | '.join(NIVEIS_VALIDOS)}", 422)


def validar_estado(estado, etiqueta="Estado"):
    mapa = {
        "ATIVO": "ATIVO", "ACTIVO": "ATIVO", "ACTIVE": "ATIVO", "A": "ATIVO",
        "INATIVO": "INATIVO", "INACTIVO": "INATIVO", "INACTIVE": "INATIVO", "I": "INATIVO",
    }
    v = str(estado).strip().upper()
    if v in mapa:
        return _ok(mapa[v])
    return _erro(f"{etiqueta} invalido: \"{estado}\".  Validos: {' | '.join(ESTADOS_VALIDOS)}", 422)


def validar_sim_nao(valor, campo="Campo"):
    mapa = {
        "SIM": "SIM", "S": "SIM", "YES": "SIM", "Y": "SIM",
        "NAO": "NAO", "N": "NAO", "NO": "NAO",
    }
    v = str(valor).strip().upper()
    if v in mapa:
        return _ok(mapa[v])
    return _erro(f"Resposta invalida para '{campo}': \"{valor}\".  Validos: SIM | NAO", 422)


def validar_custo_minimo(valor):
    s = str(valor).replace(",", ".").strip()
    s_teste = s[1:] if s.startswith("-") else s
    chars_numero = set("0123456789.")
    if not s_teste or not _todos_chars_validos(s_teste, chars_numero):
        return _erro(f"Custo minimo invalido: \"{valor}\".  Ex: 5  ou  10.50  ou  0", 422)
    v = float(s)
    if v < 0:
        return _erro(f"O custo minimo nao pode ser negativo: {v:.2f} EUR.", 422)
    return _ok(round(v, 2))


def validar_retorno(valor):
    s = str(valor).replace(",", ".").strip()
    s_teste = s[1:] if s.startswith("-") else s
    chars_numero = set("0123456789.")
    if not s_teste or not _todos_chars_validos(s_teste, chars_numero):
        return _erro(f"Retorno invalido: \"{valor}\".  Ex: 35  ou  2.5  ou  -0.5", 422)
    return _ok(round(float(s), 2))


def validar_saldo_jogo(valor):
    s = str(valor).replace(",", ".").strip()
    s_teste = s[1:] if s.startswith("-") else s
    chars_numero = set("0123456789.")
    if not s_teste or not _todos_chars_validos(s_teste, chars_numero):
        return _erro(f"Saldo do jogo invalido: \"{valor}\".  Ex: 50000  ou  1000.00", 422)
    v = float(s)
    if v < 0:
        return _erro(f"O saldo da banca nao pode ser negativo: {v:.2f} EUR.", 422)
    return _ok(round(v, 2))


def validar_nome_jogo(nome):
    n = str(nome).strip()
    if not n:
        return _erro("O nome do jogo nao pode estar vazio.  Ex: Roleta", 400)
    if len(n) < 2:
        return _erro("Nome do jogo demasiado curto (min. 2 caracteres).  Ex: Roleta", 422)
    if len(n) > 60:
        return _erro(f"Nome do jogo demasiado longo ({len(n)} chars, max 60).", 422)
    if not _todos_chars_validos(n, LETRAS_JOGO):
        return _erro(f"Nome do jogo contem caracteres invalidos.  Recebido: \"{n}\"", 422)
    return _ok(n)
