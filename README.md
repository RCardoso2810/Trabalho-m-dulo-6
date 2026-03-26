# PROJETO: SISTEMA DE GESTÃO DE CASSINO
# DOCUMENTAÇÃO TÉCNICA EM FORMATO PYTHON STRING

readme_projeto = """
ESTRUTURA DA ARQUITETURA LÓGICA E MODELO DE DADOS

🏗️ MODELAGEM DAS ENTIDADES
O sistema está estruturado em dois pilares fundamentais: Cliente e Jogo.

👤 ENTIDADE: CLIENTE (USUÁRIO)
A entidade Cliente é o centro da operação. Além dos dados demográficos, 
o sistema gere o estado financeiro e a reputação (Nível) do usuário.

ATRIBUTO          | DESCRIÇÃO                      | OBSERVAÇÕES
------------------|--------------------------------|---------------------------
Identificação     | Nome, Nº de Cliente            | Chave único de registro.
Demografia        | Data Nasc, Género, Nac.        | Compliance Legal.
Contacto          | Email / Telemóvel              | Comunicação e Segurança.
Financeiro        | Saldo Atual                    | Valor para apostas 24/7.
Fidelização       | Nível (VIP / Padrão)           | Benefícios e Limites.
Estado            | Ativo / Inativo                | Controlo de acesso.

🎮 ENTIDADE: JOGO (GAME INSTANCE)
Define as regras e os requisitos de entrada para cada modalidade.

- Categorização Técnica: Com Dealer, Tabuleiros, Peças ou Slots.
- Controlo de Acesso: Nível de Acesso bloqueia clientes Standard de mesas High Roller.
- Mecânica de Custo: Custo Mínimo para garantir a cobertura económica da casa.

🔄 LÓGICA DE INTERAÇÃO (WORKFLOW)
1. VALIDAÇÃO DE ENTRADA: Sistema verifica se o cliente está Ativo e tem Nível compatível.
2. APOSTA: Retirada de quantia do Saldo validando o Custo Mínimo.
3. PROCESSAMENTO (RNG): Cálculo baseado em probabilidades:
   - Lucro (Ganho): Retorno > Gasto.
   - Break-even (Empate): Retorno = Gasto.
   - Perda: Retorno < Gasto.
4. ATUALIZAÇÃO: Saldo atualizado instantaneamente e registado para auditoria.

📈 REGRAS DE NEGÓCIO E SEGURANÇA
- Restrição de Idade: Validação obrigatória da Data de Nascimento.
- Gestão de Risco: Bloqueio automático por comportamento suspeito (Inativo).
- Configuração de Retorno: House Edge ajustável pelo administrador.
"""


