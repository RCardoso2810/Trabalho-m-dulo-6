readme_projeto = """
ESTRUTURA DA ARQUITETURA LÓGICA E MODELO DE DADOS (VERSÃO INTEGRADA)

🏗️ MODELAGEM DAS ENTIDADES
O sistema baseia-se num ecossistema onde o Casino gere o espaço, o Cliente fornece a liquidez, o Jogo gera o entretenimento e a Transação garante a integridade financeira.

🏛️ ENTIDADE: CASINO (ESTABELECIMENTO)
O "Contentor Master" que detém a licença e as regras globais.
- Atributos: Nome, ID, Localização, Taxa(Imposto), Moeda, Capacidade Máxima.
- Listas: Jogos, Funcionários, Clientes (presentes no edifício) e Salas.

👤 ENTIDADE: CLIENTE (USUÁRIO)
- Atributos: Nome, Nº Cliente, Data Nasc, Género, Saldo Atual, Nível (VIP/Standard), Estado.

🔄 ENTIDADE: TRANSAÇÃO (AUDITORIA E SEGURANÇA)
Esta é a entidade de controlo. O saldo do cliente nunca deve ser alterado sem um registo correspondente aqui.
- ID Transação: Identificador único (UUID) para rastreio.
- Nº Cliente: Chave estrangeira ligada ao autor da movimentação.
- Tipo: Categoria da operação (Depósito, Levantamento, Aposta, Prémio).
- Tipo de Movimento: Entrada ou Saída de capital para o cliente.
- Montante: Valor exato da operação.
- Método de Pagamento: Dinheiro físico, Cartão, Voucher ou Fichas.
- Data e Hora: Timestamp preciso para evitar duplicação.
- Estado: (Pendente / Concluída / Cancelada / Suspeita).

🎮 ENTIDADE: JOGO (GAME INSTANCE)
- Atributos: Nome, ID, Custo Mínimo, Tipo (Dealer/Peças/Tabuleiros), Nível de Acesso.

📊 TABELAS TÉCNICAS (MODELO DE DADOS)

| ENTIDADE    | ATRIBUTO CHAVE      | FUNÇÃO NO SISTEMA                          |
|:------------|:--------------------|:-------------------------------------------|
| **Casino** | Taxa_Imposto        | Define a margem legal retida pelo estado.  |
| **Cliente** | Saldo_Atual         | Reflete a liquidez momentânea do jogador.  |
| **Jogo** | Nivel_Acesso        | Filtra quem pode entrar em certas mesas.   |
| **Transação**| ID_Transacao        | Garante que o dinheiro não "desaparece".   |

🔄 LÓGICA DE INTERAÇÃO (WORKFLOW DE SEGURANÇA)

1. ENTRADA: O Cliente entra no Casino (valida-se Lotação e Data de Nasc).
2. DEPÓSITO: O Cliente vai à Caixa. Cria-se uma TRANSAÇÃO (Tipo: Depósito, Movimento: Entrada). O Saldo do Cliente é atualizado.
3. JOGO: O Cliente faz uma aposta. Cria-se uma TRANSAÇÃO (Tipo: Aposta, Movimento: Saída).
4. RESULTADO:
   - Se Ganhar: Nova TRANSAÇÃO (Tipo: Prémio, Movimento: Entrada).
   - Se Perder: O saldo permanece deduzido, o lucro vai para o Balanço do Casino.
5. AUDITORIA: O administrador pode cruzar a soma de todas as Transações com o Saldo Final do Cliente para validar que não houve fraude.

📈 REGRAS DE NEGÓCIO
- Integridade: Uma transação, após ser marcada como "Concluída", nunca pode ser eliminada, apenas estornada por uma nova transação de correção.
- Fiscalidade: O Casino aplica a Taxa(Imposto) sobre o lucro bruto gerado nas transações de "Aposta vs Prémio".
"""
