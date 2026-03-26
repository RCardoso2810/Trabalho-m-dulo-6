# ══════════════════════════════════════════════════════════════
#  FICHEIRO 4 — utils.py
#  Validacoes com mensagens de erro amigaveis e exemplos
#  Estruturas: tuplos, listas, sets, dicionarios, date, defs
#  SEM modulo re — validacoes manuais com loops e defs
# ══════════════════════════════════════════════════════════════

from datetime import date

# ══════════════════════════════════════════════════════════════
#  SETS DE CARACTERES VALIDOS — usados nas validacoes
# ══════════════════════════════════════════════════════════════

# Set de letras aceites em nomes (minusculas e maiusculas + acentuadas)
LETRAS_NOME = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"
    "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ"
    " -"
)

# Set de letras para nomes de jogos (mais permissivo)
LETRAS_JOGO = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"
    "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ"
    "0123456789 -'."
)

# Set de digitos
DIGITOS = set("0123456789")

# Set de caracteres validos num numero de telefone
CHARS_TELEFONE = set("0123456789 +-() ")

# Tuplos de valores validos
GENEROS_VALIDOS = ("M", "F", "OUTRO")
NIVEIS_VALIDOS  = ("BRONZE", "PRATA", "OURO", "PLATINA", "VIP")
ESTADOS_VALIDOS = ("ATIVO", "INATIVO")


# ══════════════════════════════════════════════════════════════
#  CORES ANSI (para mostrar erros formatados)
# ══════════════════════════════════════════════════════════════

RESET    = "\033[0m"
VERMELHO = "\033[38;5;196m"
AMARELO  = "\033[38;5;220m"
CINZA    = "\033[38;5;245m"


# ══════════════════════════════════════════════════════════════
#  RESULTADO DE VALIDACAO
#  Dicionario: { "valido": bool, "mensagem": str, "valor": any }
# ══════════════════════════════════════════════════════════════

def _ok(valor):
    return {"valido": True, "mensagem": "", "valor": valor}

def _erro(mensagem):
    return {"valido": False, "mensagem": mensagem, "valor": None}


# ══════════════════════════════════════════════════════════════
#  AUXILIARES INTERNOS
# ══════════════════════════════════════════════════════════════

def _title(texto):
    # Title case manual sem modulo re
    palavras = str(texto).strip().split()
    resultado = []
    for p in palavras:
        if len(p) > 0:
            resultado.append(p[0].upper() + p[1:].lower())
    return " ".join(resultado)


def _tem_digito(texto):
    # Verifica se algum caracter esta no set DIGITOS
    for c in texto:
        if c in DIGITOS:
            return True
    return False


def _todos_chars_validos(texto, chars_validos):
    # Verifica se todos os caracteres estao no set fornecido
    for c in texto:
        if c not in chars_validos:
            return False
    return True


def _e_email_valido(texto):
    # Validacao basica de email sem re:
    # deve ter exactamente um '@', com texto antes e depois,
    # e um '.' apos o '@'
    partes_arroba = texto.split("@")
    if len(partes_arroba) != 2:
        return False
    antes  = partes_arroba[0]
    depois = partes_arroba[1]
    if len(antes) == 0 or len(depois) == 0:
        return False
    if " " in antes or " " in depois:
        return False
    # Deve ter pelo menos um ponto apos o '@'
    if "." not in depois:
        return False
    # Parte apos o ultimo ponto nao pode estar vazia
    partes_ponto = depois.split(".")
    for parte in partes_ponto:
        if len(parte) == 0:
            return False
    return True


def _e_telefone_valido(texto):
    # Validacao basica de telefone sem re:
    # so pode ter digitos, espacos, +, -, (, )
    # deve ter entre 7 e 20 caracteres (sem espacos)
    sem_espacos = texto.replace(" ", "")
    if len(sem_espacos) < 7 or len(sem_espacos) > 20:
        return False
    return _todos_chars_validos(texto, CHARS_TELEFONE)


# ══════════════════════════════════════════════════════════════
#  VALIDAR NOME DE CLIENTE
# ══════════════════════════════════════════════════════════════

def validar_nome(nome):
    nome = str(nome).strip()

    if not nome:
        return _erro(
            "✖  Nome nao pode estar vazio.\n"
            "   Ex: Rodrigo Manel"
        )

    if _tem_digito(nome):
        return _erro(
            "✖  O nome nao pode conter numeros.\n"
            "   Ex: Rodrigo Manel  (sem digitos)"
        )

    if not _todos_chars_validos(nome, LETRAS_NOME):
        return _erro(
            "✖  O nome so pode conter letras, espacos e hifens.\n"
            "   Ex: Ana-Rita Sousa"
        )

    # Lista de palavras do nome
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
            # Construir sugestao corrigida numa lista e juntar
            sugestao = []
            for p in partes:
                sugestao.append(p[0].upper() + p[1:].lower() if p else p)
            return _erro(
                "✖  Cada parte do nome deve comecar com letra maiuscula.\n"
                f"   Recebido : \"{nome}\"\n"
                f"   Correcto : \"{' '.join(sugestao)}\"\n"
                "   Ex       : Rodrigo Manel"
            )

    return _ok(_title(nome))


# ══════════════════════════════════════════════════════════════
#  VALIDAR DATA DE NASCIMENTO
# ══════════════════════════════════════════════════════════════

def validar_data_nascimento(data_str, idade_minima=18):
    data_str = str(data_str).strip()

    if not data_str:
        return _erro(
            "✖  A data de nascimento nao pode estar vazia.\n"
            "   Ex: 20/10/1995"
        )

    # Dividir em lista de partes
    partes = data_str.split("/")
    if len(partes) != 3:
        return _erro(
            "✖  Formato de data invalido. Use DD/MM/AAAA (com barras).\n"
            f"   Recebido : \"{data_str}\"\n"
            "   Ex       : 20/10/1995"
        )

    # Verificar que cada parte e composta apenas por digitos
    for parte in partes:
        if not _todos_chars_validos(parte, DIGITOS):
            return _erro(
                "✖  A data deve conter apenas numeros separados por '/'.\n"
                f"   Recebido : \"{data_str}\"\n"
                "   Ex       : 20/10/1995"
            )

    dia = int(partes[0])
    mes = int(partes[1])
    ano = int(partes[2])

    hoje = date.today()

    if ano < 1900 or ano > hoje.year:
        return _erro(
            f"✖  Ano invalido: {ano}. Deve estar entre 1900 e {hoje.year}.\n"
            "   Ex: 20/10/1995"
        )

    # Tuplo com os dias maximos por mes (ano comum)
    dias_por_mes = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    # Verificar ano bissexto
    bissexto = (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0)
    max_dias = dias_por_mes[mes] if mes != 2 else (29 if bissexto else 28)

    if mes < 1 or mes > 12:
        return _erro(
            f"✖  Mes invalido: {mes}. Deve estar entre 1 e 12.\n"
            "   Ex: 20/10/1995"
        )

    if dia < 1 or dia > max_dias:
        return _erro(
            f"✖  Dia invalido: {dia} para o mes {mes} (maximo {max_dias} dias).\n"
            "   Ex: 20/10/1995"
        )

    nasc = date(ano, mes, dia)

    if nasc > hoje:
        return _erro(
            "✖  A data de nascimento nao pode ser no futuro.\n"
            f"   Recebido : {data_str}\n"
            "   Ex       : 20/10/1995"
        )

    # Tuplo de comparacao (mes, dia)
    hoje_par = (hoje.month, hoje.day)
    nasc_par = (nasc.month, nasc.day)
    idade = hoje.year - nasc.year - (hoje_par < nasc_par)

    if idade < idade_minima:
        limite = date(hoje.year - idade_minima, hoje.month, hoje.day)
        return _erro(
            f"✖  Idade insuficiente: {idade} anos.\n"
            f"   A idade minima para registo e {idade_minima} anos.\n"
            f"   Ex: se hoje e {hoje.day:02d}/{hoje.month:02d}/{hoje.year}, "
            f"deve ter nascido antes de "
            f"{limite.day:02d}/{limite.month:02d}/{limite.year}."
        )

    data_fmt = f"{dia:02d}/{mes:02d}/{ano}"
    # Devolve dicionario com data e idade
    return _ok({"data": data_fmt, "idade": idade})


# ══════════════════════════════════════════════════════════════
#  VALIDAR GENERO
# ══════════════════════════════════════════════════════════════

def validar_genero(genero):
    g = str(genero).strip().upper()

    # Dicionario de mapeamento de variacoes para valor canonico
    mapa_genero = {
        "M"          : "M",
        "MASCULINO"  : "M",
        "MALE"       : "M",
        "HOMEM"      : "M",
        "F"          : "F",
        "FEMININO"   : "F",
        "FEMALE"     : "F",
        "MULHER"     : "F",
        "OUTRO"      : "OUTRO",
        "OTHER"      : "OUTRO",
        "NAO BINARIO": "OUTRO",
        "NAO-BINARIO": "OUTRO",
    }

    if g in mapa_genero:
        return _ok(mapa_genero[g])

    return _erro(
        f"✖  Genero invalido: \"{genero}\".\n"
        f"   Opcoes validas : {' | '.join(GENEROS_VALIDOS)}\n"
        "   Ex            : M  ou  F  ou  OUTRO"
    )


# ══════════════════════════════════════════════════════════════
#  VALIDAR NACIONALIDADE
# ══════════════════════════════════════════════════════════════

def validar_nacionalidade(nacionalidade):
    n = str(nacionalidade).strip()

    if not n:
        return _erro(
            "✖  A nacionalidade nao pode estar vazia.\n"
            "   Ex: Portuguesa"
        )

    if _tem_digito(n):
        return _erro(
            "✖  A nacionalidade nao pode conter numeros.\n"
            f"   Recebido : \"{n}\"\n"
            "   Ex       : Portuguesa"
        )

    if not _todos_chars_validos(n, LETRAS_NOME):
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

    return _ok(_title(n))


# ══════════════════════════════════════════════════════════════
#  VALIDAR CONTACTO
# ══════════════════════════════════════════════════════════════

def validar_contacto(contacto):
    c = str(contacto).strip()

    if not c:
        return _erro(
            "✖  O contacto nao pode estar vazio.\n"
            "   Ex: 912345678\n"
            "   Ex: jose@email.com\n"
            "   Ex: 912345678 / jose@email.com"
        )

    # Dividir em lista de partes (telefone e/ou email separados por '/')
    partes = []
    for parte in c.split("/"):
        partes.append(parte.strip())

    for parte in partes:
        eh_telefone = _e_telefone_valido(parte)
        eh_email    = _e_email_valido(parte)
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
    # Substituir virgula por ponto para aceitar formato europeu
    s = str(saldo).replace(",", ".").strip()

    # Verificar que e um numero valido manualmente
    # Permitido: digitos, um ponto decimal, sinal negativo no inicio
    chars_numero = set("0123456789.")
    s_teste = s[1:] if s.startswith("-") else s
    if not s_teste or not _todos_chars_validos(s_teste, chars_numero):
        return _erro(
            f"✖  Saldo invalido: \"{saldo}\".\n"
            "   Deve ser um numero (inteiro ou decimal).\n"
            "   Ex: 500   ou   1250.75   ou   0"
        )

    # Nao pode ter mais de um ponto
    if s_teste.count(".") > 1:
        return _erro(
            f"✖  Saldo invalido: \"{saldo}\".\n"
            "   Deve ser um numero com no maximo um ponto decimal.\n"
            "   Ex: 500   ou   1250.75   ou   0"
        )

    v = float(s)

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

def validar_nivel(nivel, etiqueta="Nivel"):
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

def validar_estado(estado, etiqueta="Estado"):
    v = str(estado).strip().upper()

    # Dicionario de mapeamento de variacoes para valor canonico
    mapa_estado = {
        "ATIVO"   : "ATIVO",
        "ACTIVO"  : "ATIVO",
        "ACTIVE"  : "ATIVO",
        "A"       : "ATIVO",
        "INATIVO" : "INATIVO",
        "INACTIVO": "INATIVO",
        "INACTIVE": "INATIVO",
        "I"       : "INATIVO",
    }

    if v in mapa_estado:
        return _ok(mapa_estado[v])

    return _erro(
        f"✖  {etiqueta} invalido: \"{estado}\".\n"
        f"   Opcoes validas : {' | '.join(ESTADOS_VALIDOS)}\n"
        "   Ex            : ATIVO  ou  INATIVO"
    )


# ══════════════════════════════════════════════════════════════
#  VALIDAR SIM/NAO
# ══════════════════════════════════════════════════════════════

def validar_sim_nao(valor, campo="Campo"):
    v = str(valor).strip().upper()

    # Dicionario de mapeamento de variacoes
    mapa_sn = {
        "SIM": "SIM", "S": "SIM", "YES": "SIM", "Y": "SIM",
        "NAO": "NAO", "N": "NAO", "NO" : "NAO",
    }

    if v in mapa_sn:
        return _ok(mapa_sn[v])

    return _erro(
        f"✖  Resposta invalida para '{campo}': \"{valor}\".\n"
        "   Opcoes validas : SIM  ou  NAO\n"
        "   Tambem aceite  : S / N   ou   YES / NO\n"
        "   Ex            : SIM"
    )


# ══════════════════════════════════════════════════════════════
#  VALIDAR CUSTO MINIMO
# ══════════════════════════════════════════════════════════════

def validar_custo_minimo(valor):
    s = str(valor).replace(",", ".").strip()
    chars_numero = set("0123456789.")
    s_teste = s[1:] if s.startswith("-") else s

    if not s_teste or not _todos_chars_validos(s_teste, chars_numero):
        return _erro(
            f"✖  Custo minimo invalido: \"{valor}\".\n"
            "   Deve ser um numero igual ou maior que 0.\n"
            "   Ex: 5   ou   10.50   ou   0.25"
        )

    v = float(s)
    if v < 0:
        return _erro(
            f"✖  O custo minimo nao pode ser negativo: {v:.2f} EUR.\n"
            "   Use 0 se o jogo for gratuito.\n"
            "   Ex: 5   ou   0"
        )

    return _ok(round(v, 2))


# ══════════════════════════════════════════════════════════════
#  VALIDAR RETORNO
# ══════════════════════════════════════════════════════════════

def validar_retorno(valor):
    s = str(valor).replace(",", ".").strip()
    chars_numero = set("0123456789.")
    s_teste = s[1:] if s.startswith("-") else s

    if not s_teste or not _todos_chars_validos(s_teste, chars_numero):
        return _erro(
            f"✖  Retorno invalido: \"{valor}\".\n"
            "   Deve ser um numero (pode ser negativo para indicar perda).\n"
            "   Ex: 35   ou   2.5   ou   -0.5"
        )

    return _ok(round(float(s), 2))


# ══════════════════════════════════════════════════════════════
#  VALIDAR SALDO DE JOGO
# ══════════════════════════════════════════════════════════════

def validar_saldo_jogo(valor):
    s = str(valor).replace(",", ".").strip()
    chars_numero = set("0123456789.")
    s_teste = s[1:] if s.startswith("-") else s

    if not s_teste or not _todos_chars_validos(s_teste, chars_numero):
        return _erro(
            f"✖  Saldo do jogo invalido: \"{valor}\".\n"
            "   Deve ser um numero igual ou maior que 0.\n"
            "   Ex: 50000   ou   1000.00"
        )

    v = float(s)
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

    if not _todos_chars_validos(n, LETRAS_JOGO):
        return _erro(
            f"✖  Nome do jogo contem caracteres invalidos.\n"
            f"   Recebido : \"{n}\"\n"
            "   Permitido : letras, numeros, espacos, hifens e apostrofos.\n"
            "   Ex: Poker Texas  ou  Texas Hold'em  ou  Blackjack 21"
        )

    return _ok(_title(n))


# ══════════════════════════════════════════════════════════════
#  FUNCOES CENTRAIS DE VALIDACAO POR MODULO
# ══════════════════════════════════════════════════════════════

def validar_campo_cliente(campo, valor):
    """
    Valida um campo de cliente pelo nome.
    Devolve dicionario: { "valido": bool, "mensagem": str, "valor": any }
    """
    campo = str(campo).lower().strip()

    # Dicionario de despacho: campo -> funcao de validacao
    despacho = {
        "nome"            : validar_nome,
        "data_nascimento" : validar_data_nascimento,
        "genero"          : validar_genero,
        "nacionalidade"   : validar_nacionalidade,
        "contacto"        : validar_contacto,
        "saldo"           : validar_saldo,
        "nivel"           : validar_nivel,
        "estado"          : validar_estado,
    }

    if campo not in despacho:
        # Lista dos campos validos para mostrar no erro
        campos_lista = list(despacho.keys())
        return _erro(
            f"✖  Campo desconhecido: \"{campo}\".\n"
            f"   Campos validos: {' | '.join(campos_lista)}"
        )

    fn = despacho[campo]
    return fn(valor)


def validar_campo_jogo(campo, valor):
    """
    Valida um campo de jogo pelo nome.
    Devolve dicionario: { "valido": bool, "mensagem": str, "valor": any }
    """
    campo = str(campo).lower().strip()

    # Dicionario de despacho para campos simples
    despacho = {
        "nome"         : validar_nome_jogo,
        "custo_minimo" : validar_custo_minimo,
        "saldo_jogo"   : validar_saldo_jogo,
        "retorno"      : validar_retorno,
        "nivel_acesso" : lambda v: validar_nivel(v, "Nivel de acesso"),
        "estado"       : validar_estado,
    }

    # Set dos campos de tipo SIM/NAO
    campos_sn = {"dealer", "tabuleiro", "pecas", "cartas", "dados", "maquina"}

    if campo in despacho:
        return despacho[campo](valor)

    if campo in campos_sn:
        return validar_sim_nao(valor, campo)

    # Lista de todos os campos validos
    todos_campos = list(despacho.keys()) + list(campos_sn)
    return _erro(
        f"✖  Campo desconhecido: \"{campo}\".\n"
        f"   Campos validos: {' | '.join(todos_campos)}"
    )


# ══════════════════════════════════════════════════════════════
#  MOSTRAR VALIDACAO — formata e imprime o erro no terminal
# ══════════════════════════════════════════════════════════════

def mostrar_validacao(resultado, pausa_auto=True):
    """
    Recebe o dicionario de validacao e imprime a mensagem formatada.
    Devolve True se valido, False se invalido.
    """
    if resultado["valido"]:
        return True

    # Dividir a mensagem em lista de linhas
    linhas = resultado["mensagem"].split("\n")
    print()
    for linha_msg in linhas:
        linha_msg = linha_msg.strip()
        if not linha_msg:
            continue
        if linha_msg.startswith("✖"):
            print(f"  {VERMELHO}{linha_msg}{RESET}")
        elif linha_msg.lower().startswith("ex") or linha_msg.lower().startswith("correcto") or linha_msg.lower().startswith("recebido"):
            print(f"  {AMARELO}{linha_msg}{RESET}")
        else:
            print(f"  {CINZA}{linha_msg}{RESET}")

    if pausa_auto:
        print(f"\n  {CINZA}Prima ENTER para tentar novamente...{RESET}")
        input()

    return False