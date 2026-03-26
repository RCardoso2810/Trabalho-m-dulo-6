# ══════════════════════════════════════════════════════════════
#  FICHEIRO 4 — utils.py
#  Validacoes com mensagens de erro amigaveis e exemplos
#  Usado por cliente.py, jogo.py e main.py
#  Sem classes, sem __init__, sem self
# ══════════════════════════════════════════════════════════════

import re
from datetime import date

# ══════════════════════════════════════════════════════════════
#  RESULTADO DE VALIDACAO
#  Cada funcao devolve um dicionario com:
#    { "valido": True/False, "mensagem": "...", "valor": ... }
# ══════════════════════════════════════════════════════════════

def _ok(valor):
    """Devolve resultado de validacao bem-sucedida."""
    return {"valido": True, "mensagem": "", "valor": valor}

def _erro(mensagem):
    """Devolve resultado de validacao falhada com mensagem de ajuda."""
    return {"valido": False, "mensagem": mensagem, "valor": None}


# ══════════════════════════════════════════════════════════════
#  VALIDAR NOME
# ══════════════════════════════════════════════════════════════

def validar_nome(nome):
    """
    Valida nome completo.
    Regras:
      - Nao pode estar vazio
      - Deve ter pelo menos 2 palavras
      - Cada palavra deve comecar com maiuscula
      - So pode conter letras, espacos e hifens
      - Minimo 2 caracteres por palavra
    """
    nome = str(nome).strip()

    if not nome:
        return _erro(
            "✖  Nome nao pode estar vazio.\n"
            "   Ex: Rodrigo Manel"
        )

    if re.search(r"[0-9]", nome):
        return _erro(
            "✖  O nome nao pode conter numeros.\n"
            "   Ex: Rodrigo Manel  (sem digitos)"
        )

    if re.search(r"[^A-Za-zÀ-ÿ\s\-]", nome):
        return _erro(
            "✖  O nome so pode conter letras, espacos e hifens.\n"
            "   Ex: Ana-Rita Sousa"
        )

    partes = nome.split()

    if len(partes) < 2:
        return _erro(
            "✖  O nome deve ter pelo menos dois nomes (proprio e apelido).\n"
            "   Recebido : \"" + nome + "\"\n"
            "   Ex       : Rodrigo Manel"
        )

    for parte in partes:
        if len(parte) < 2:
            return _erro(
                f"✖  A parte \"{parte}\" e demasiado curta (minimo 2 letras).\n"
                "   Ex: Rodrigo Manel"
            )
        if not parte[0].isupper():
            return _erro(
                f"✖  Cada parte do nome deve comecar com letra maiuscula.\n"
                f"   Recebido : \"{nome}\"\n"
                f"   Correcto : \"{' '.join(p.capitalize() for p in partes)}\"\n"
                "   Ex       : Rodrigo Manel"
            )

    return _ok(nome.title())


# ══════════════════════════════════════════════════════════════
#  VALIDAR DATA DE NASCIMENTO
# ══════════════════════════════════════════════════════════════

def validar_data_nascimento(data_str, idade_minima=18):
    """
    Valida data no formato DD/MM/AAAA e verifica idade minima.
    """
    data_str = str(data_str).strip()

    if not data_str:
        return _erro(
            "✖  A data de nascimento nao pode estar vazia.\n"
            "   Ex: 20/10/1995"
        )

    partes = data_str.split("/")
    if len(partes) != 3:
        return _erro(
            "✖  Formato de data invalido. Use DD/MM/AAAA (com barras).\n"
            f"   Recebido : \"{data_str}\"\n"
            "   Ex       : 20/10/1995"
        )

    try:
        dia, mes, ano = int(partes[0]), int(partes[1]), int(partes[2])
    except ValueError:
        return _erro(
            "✖  A data deve conter apenas numeros separados por '/'.\n"
            f"   Recebido : \"{data_str}\"\n"
            "   Ex       : 20/10/1995"
        )

    if ano < 1900 or ano > date.today().year:
        return _erro(
            f"✖  Ano invalido: {ano}. Deve estar entre 1900 e {date.today().year}.\n"
            "   Ex: 20/10/1995"
        )

    try:
        nasc = date(ano, mes, dia)
    except ValueError:
        return _erro(
            f"✖  Data invalida: {data_str} nao existe no calendario.\n"
            "   Verifique o dia e o mes (ex: nao existe 30/02).\n"
            "   Ex: 20/10/1995"
        )

    hoje  = date.today()
    idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))

    if nasc > hoje:
        return _erro(
            "✖  A data de nascimento nao pode ser no futuro.\n"
            f"   Recebido : {data_str}\n"
            "   Ex       : 20/10/1995"
        )

    if idade < idade_minima:
        return _erro(
            f"✖  Idade insuficiente: {idade} anos.\n"
            f"   A idade minima para registo e {idade_minima} anos.\n"
            f"   Ex: se hoje e {hoje.strftime('%d/%m/%Y')}, "
            f"o cliente deve ter nascido antes de "
            f"{date(hoje.year - idade_minima, hoje.month, hoje.day).strftime('%d/%m/%Y')}."
        )

    data_fmt = f"{dia:02d}/{mes:02d}/{ano}"
    return _ok({"data": data_fmt, "idade": idade})


# ══════════════════════════════════════════════════════════════
#  VALIDAR GENERO
# ══════════════════════════════════════════════════════════════

GENEROS_VALIDOS = ("M", "F", "OUTRO")

def validar_genero(genero):
    """
    Valida genero. Aceita variacoes comuns (ex: 'masculino', 'feminino').
    """
    g = str(genero).strip().upper()

    mapa = {
        "M": "M", "MASCULINO": "M", "MALE": "M", "HOMEM": "M",
        "F": "F", "FEMININO": "F", "FEMALE": "F", "MULHER": "F",
        "OUTRO": "OUTRO", "OTHER": "OUTRO", "N/A": "OUTRO",
        "NAO BINARIO": "OUTRO", "NAO-BINARIO": "OUTRO"
    }

    if g in mapa:
        return _ok(mapa[g])

    return _erro(
        f"✖  Genero invalido: \"{genero}\".\n"
        f"   Opcoes validas : {' | '.join(GENEROS_VALIDOS)}\n"
        "   Ex            : M  ou  F  ou  OUTRO"
    )


# ══════════════════════════════════════════════════════════════
#  VALIDAR NACIONALIDADE
# ══════════════════════════════════════════════════════════════

def validar_nacionalidade(nacionalidade):
    """
    Valida nacionalidade. Nao pode ser vazia e so pode ter letras.
    """
    n = str(nacionalidade).strip()

    if not n:
        return _erro(
            "✖  A nacionalidade nao pode estar vazia.\n"
            "   Ex: Portuguesa"
        )

    if re.search(r"[0-9]", n):
        return _erro(
            "✖  A nacionalidade nao pode conter numeros.\n"
            f"   Recebido : \"{n}\"\n"
            "   Ex       : Portuguesa"
        )

    if re.search(r"[^A-Za-zÀ-ÿ\s\-]", n):
        return _erro(
            "✖  A nacionalidade so pode conter letras, espacos e hifens.\n"
            f"   Recebido : \"{n}\"\n"
            "   Ex       : Portuguesa  ou  Britanico-Americana"
        )

    if len(n) < 3:
        return _erro(
            "✖  Nacionalidade demasiado curta (minimo 3 letras).\n"
            "   Ex: Portuguesa"
        )

    return _ok(n.title())


# ══════════════════════════════════════════════════════════════
#  VALIDAR CONTACTO
# ══════════════════════════════════════════════════════════════

def validar_contacto(contacto):
    """
    Valida contacto. Aceita numero de telefone e/ou email.
    Formato aceite: telefone, email, ou 'telefone / email'.
    """
    c = str(contacto).strip()

    if not c:
        return _erro(
            "✖  O contacto nao pode estar vazio.\n"
            "   Ex: 912345678\n"
            "   Ex: jose@email.com\n"
            "   Ex: 912345678 / jose@email.com"
        )

    # Separar por '/' caso tenha telefone e email
    partes = [p.strip() for p in c.split("/")]

    telefone_regex = re.compile(r"^(\+?[0-9\s\-\(\)]{7,20})$")
    email_regex    = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    for parte in partes:
        eh_telefone = bool(telefone_regex.match(parte))
        eh_email    = bool(email_regex.match(parte))
        if not eh_telefone and not eh_email:
            return _erro(
                f"✖  Contacto invalido: \"{parte}\".\n"
                "   Deve ser um numero de telefone ou endereco de email.\n"
                "   Ex (telefone) : 912345678  ou  +351912345678\n"
                "   Ex (email)    : jose@email.com\n"
                "   Ex (ambos)    : 912345678 / jose@email.com"
            )

    return _ok(c)


# ══════════════════════════════════════════════════════════════
#  VALIDAR SALDO
# ══════════════════════════════════════════════════════════════

def validar_saldo(saldo):
    """
    Valida saldo monetario. Deve ser um numero nao negativo.
    """
    try:
        v = float(str(saldo).replace(",", ".").strip())
    except (ValueError, TypeError):
        return _erro(
            f"✖  Saldo invalido: \"{saldo}\".\n"
            "   Deve ser um numero (inteiro ou decimal).\n"
            "   Ex: 500   ou   1250.75   ou   0"
        )

    if v < 0:
        return _erro(
            f"✖  O saldo nao pode ser negativo: {v:.2f} EUR.\n"
            "   Introduza 0 (zero) se o saldo inicial for nulo.\n"
            "   Ex: 500   ou   0"
        )

    return _ok(round(v, 2))


# ══════════════════════════════════════════════════════════════
#  VALIDAR NIVEL
# ══════════════════════════════════════════════════════════════

NIVEIS_VALIDOS = ("BRONZE", "PRATA", "OURO", "PLATINA", "VIP")

def validar_nivel(nivel, etiqueta="Nivel"):
    """
    Valida nivel (BRONZE, PRATA, OURO, PLATINA, VIP).
    """
    v = str(nivel).strip().upper()

    if v in NIVEIS_VALIDOS:
        return _ok(v)

    return _erro(
        f"✖  {etiqueta} invalido: \"{nivel}\".\n"
        f"   Opcoes validas : {' | '.join(NIVEIS_VALIDOS)}\n"
        "   Ex            : BRONZE  ou  OURO  ou  VIP"
    )


# ══════════════════════════════════════════════════════════════
#  VALIDAR ESTADO
# ══════════════════════════════════════════════════════════════

ESTADOS_VALIDOS = ("ATIVO", "INATIVO")

def validar_estado(estado, etiqueta="Estado"):
    """
    Valida estado (ATIVO ou INATIVO).
    """
    v = str(estado).strip().upper()

    mapa = {
        "ATIVO": "ATIVO", "ACTIVO": "ATIVO", "ACTIVE": "ATIVO",
        "INATIVO": "INATIVO", "INACTIVO": "INATIVO", "INACTIVE": "INATIVO",
        "A": "ATIVO", "I": "INATIVO"
    }

    if v in mapa:
        return _ok(mapa[v])

    return _erro(
        f"✖  {etiqueta} invalido: \"{estado}\".\n"
        f"   Opcoes validas : {' | '.join(ESTADOS_VALIDOS)}\n"
        "   Ex            : ATIVO  ou  INATIVO"
    )


# ══════════════════════════════════════════════════════════════
#  VALIDAR SIM/NAO  (para tipos de jogo)
# ══════════════════════════════════════════════════════════════

def validar_sim_nao(valor, campo="Campo"):
    """
    Valida resposta SIM ou NAO.
    Aceita variacoes como 's', 'n', 'yes', 'no'.
    """
    v = str(valor).strip().upper()

    mapa = {
        "SIM": "SIM", "S": "SIM", "YES": "SIM", "Y": "SIM",
        "NAO": "NAO", "N": "NAO", "NO": "NAO", "NAO": "NAO"
    }

    if v in mapa:
        return _ok(mapa[v])

    return _erro(
        f"✖  Resposta invalida para '{campo}': \"{valor}\".\n"
        "   Opcoes validas : SIM  ou  NAO\n"
        "   Tambem aceite  : S / N   ou   YES / NO\n"
        "   Ex            : SIM"
    )


# ══════════════════════════════════════════════════════════════
#  VALIDAR CUSTO MINIMO / RETORNO  (numericos com contexto)
# ══════════════════════════════════════════════════════════════

def validar_custo_minimo(valor):
    """
    Valida custo minimo de entrada de um jogo. Deve ser >= 0.
    """
    try:
        v = float(str(valor).replace(",", ".").strip())
    except (ValueError, TypeError):
        return _erro(
            f"✖  Custo minimo invalido: \"{valor}\".\n"
            "   Deve ser um numero igual ou maior que 0.\n"
            "   Ex: 5   ou   10.50   ou   0.25"
        )

    if v < 0:
        return _erro(
            f"✖  O custo minimo nao pode ser negativo: {v:.2f} EUR.\n"
            "   Use 0 se o jogo for gratuito.\n"
            "   Ex: 5   ou   0"
        )

    return _ok(round(v, 2))


def validar_retorno(valor):
    """
    Valida retorno financeiro do jogo. Pode ser positivo ou negativo.
    """
    try:
        v = float(str(valor).replace(",", ".").strip())
    except (ValueError, TypeError):
        return _erro(
            f"✖  Retorno invalido: \"{valor}\".\n"
            "   Deve ser um numero (pode ser negativo para indicar perda).\n"
            "   Ex: 35   ou   2.5   ou   -0.5"
        )

    return _ok(round(v, 2))


def validar_saldo_jogo(valor):
    """
    Valida saldo da banca de um jogo. Deve ser >= 0.
    """
    try:
        v = float(str(valor).replace(",", ".").strip())
    except (ValueError, TypeError):
        return _erro(
            f"✖  Saldo do jogo invalido: \"{valor}\".\n"
            "   Deve ser um numero igual ou maior que 0.\n"
            "   Ex: 50000   ou   1000.00"
        )

    if v < 0:
        return _erro(
            f"✖  O saldo da banca nao pode ser negativo: {v:.2f} EUR.\n"
            "   Ex: 50000   ou   1000.00   ou   0"
        )

    return _ok(round(v, 2))


# ══════════════════════════════════════════════════════════════
#  VALIDAR NOME DE JOGO
# ══════════════════════════════════════════════════════════════

def validar_nome_jogo(nome):
    """
    Valida nome de jogo. Regras mais flexiveis que o nome de cliente
    (permite numeros e simbolos comuns como em 'Texas Hold'em').
    """
    n = str(nome).strip()

    if not n:
        return _erro(
            "✖  O nome do jogo nao pode estar vazio.\n"
            "   Ex: Roleta  ou  Blackjack  ou  Poker Texas"
        )

    if len(n) < 2:
        return _erro(
            "✖  Nome do jogo demasiado curto (minimo 2 caracteres).\n"
            "   Ex: Roleta"
        )

    if len(n) > 60:
        return _erro(
            f"✖  Nome do jogo demasiado longo ({len(n)} caracteres, maximo 60).\n"
            "   Ex: Roleta Europeia"
        )

    if re.search(r"[^A-Za-zÀ-ÿ0-9\s\-\'\.]", n):
        return _erro(
            f"✖  Nome do jogo contem caracteres invalidos.\n"
            f"   Recebido : \"{n}\"\n"
            "   Permitido : letras, numeros, espacos, hifens e apostrofos.\n"
            "   Ex: Poker Texas  ou  Texas Hold'em  ou  Blackjack 21"
        )

    return _ok(n.title())


# ══════════════════════════════════════════════════════════════
#  FUNCAO PRINCIPAL DE VALIDACAO — usada nos menus
# ══════════════════════════════════════════════════════════════

def validar_campo_cliente(campo, valor):
    """
    Valida um campo de cliente pelo nome e devolve resultado.
    Centraliza todas as validacoes de cliente num unico ponto.

    Uso:
        res = validar_campo_cliente("nome", "rodrigo")
        if not res["valido"]:
            print(res["mensagem"])
        else:
            valor_correcto = res["valor"]
    """
    campo = str(campo).lower().strip()

    if campo == "nome":
        return validar_nome(valor)
    elif campo == "data_nascimento":
        return validar_data_nascimento(valor)
    elif campo == "genero":
        return validar_genero(valor)
    elif campo == "nacionalidade":
        return validar_nacionalidade(valor)
    elif campo == "contacto":
        return validar_contacto(valor)
    elif campo == "saldo":
        return validar_saldo(valor)
    elif campo == "nivel":
        return validar_nivel(valor)
    elif campo == "estado":
        return validar_estado(valor)
    else:
        return _erro(
            f"✖  Campo desconhecido: \"{campo}\".\n"
            "   Campos validos: nome | data_nascimento | genero | "
            "nacionalidade | contacto | saldo | nivel | estado"
        )


def validar_campo_jogo(campo, valor):
    """
    Valida um campo de jogo pelo nome e devolve resultado.

    Uso:
        res = validar_campo_jogo("custo_minimo", "-5")
        if not res["valido"]:
            print(res["mensagem"])
        else:
            valor_correcto = res["valor"]
    """
    campo = str(campo).lower().strip()

    if campo == "nome":
        return validar_nome_jogo(valor)
    elif campo == "custo_minimo":
        return validar_custo_minimo(valor)
    elif campo == "saldo_jogo":
        return validar_saldo_jogo(valor)
    elif campo == "retorno":
        return validar_retorno(valor)
    elif campo == "nivel_acesso":
        return validar_nivel(valor, "Nivel de acesso")
    elif campo == "estado":
        return validar_estado(valor)
    elif campo in ("dealer", "tabuleiro", "pecas", "cartas", "dados", "maquina"):
        return validar_sim_nao(valor, campo)
    else:
        return _erro(
            f"✖  Campo desconhecido: \"{campo}\".\n"
            "   Campos validos: nome | custo_minimo | saldo_jogo | retorno | "
            "nivel_acesso | estado | dealer | tabuleiro | pecas | cartas | dados | maquina"
        )


# ══════════════════════════════════════════════════════════════
#  FUNCAO VISUAL — mostra erro formatado no terminal (usa cores)
# ══════════════════════════════════════════════════════════════

RESET    = "\033[0m"
VERMELHO = "\033[38;5;196m"
AMARELO  = "\033[38;5;220m"
CINZA    = "\033[38;5;245m"
BRANCO   = "\033[97m"

def mostrar_validacao(resultado, pausa_auto=True):
    """
    Recebe o dicionario devolvido pelas funcoes de validacao
    e imprime a mensagem de erro formatada.

    Retorna True se valido, False se invalido.

    Uso:
        res = validar_nome("rodrigo")
        if not mostrar_validacao(res):
            return  # volta atras
        nome_correcto = res["valor"]
    """
    if resultado["valido"]:
        return True

    linhas = resultado["mensagem"].split("\n")
    print()
    for i, linha in enumerate(linhas):
        linha = linha.strip()
        if not linha:
            continue
        if linha.startswith("✖"):
            print(f"  {VERMELHO}{linha}{RESET}")
        elif linha.lower().startswith("ex"):
            print(f"  {AMARELO}{linha}{RESET}")
        else:
            print(f"  {CINZA}{linha}{RESET}")

    if pausa_auto:
        print(f"\n  {CINZA}Prima ENTER para tentar novamente...{RESET}")
        input()

    return False
