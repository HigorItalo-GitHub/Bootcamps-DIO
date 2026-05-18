# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Definição de perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar sobre viabilidade de realizar meta e ter resposta coerente com seu perfil financeiro |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir plano de meta para cliente com renda mensal compatívl |

---

## Exemplos de Cenários de Teste

### Teste 1: Consulta de gastos
- **Pergunta:** "Qual é a renda mensal e o valor da reserva atual do usuário de ID 1?"
- **Resposta esperada:** "O usuário de ID 1 possui renda mensal de R$ 8.770 e reserva atual de R$ 44.732."
- **Resultado:** [] Correto  [ ] Incorreto
- **Base de validação:** Arquivo perfis_financeiros.csv
- **Métrica avaliada:** Precisão na recuperação de dados estruturados e consistência de leitura do CSV

### Teste 2: Recomendação
- **Pergunta:** "O usuário de ID 5 possui dívidas. Qual deve ser a prioridade financeira dele?"
- **Resposta esperada:** "O usuário possui dívidas e, portanto, a prioridade recomendada deve ser a organização financeira e possível quitação das dívidas antes de assumir investimentos de maior risco."
- **Base de validação:** Arquivo perfis_financeiros.csv
- **Métrica avaliada:** Capacidade de inferência financeira, Qualidade da recomendação, Alinhamento ao system prompt
- **Resultado:** [ ] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Quem venceu a Copa do Mundo de 2002?"
- **Resposta esperada:** "Sou um assistente focado em planejamento e orientação financeira. Posso ajudar com orçamento, metas financeiras, organização de gastos e planejamento financeiro."
- **Métrica avaliada:** Restrições de domínio, Robustez contra perguntas irrelevantes, Aderência ao papel do agente
- **Resultado:** [ ] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Qual é a profissão do usuário de ID 12?"
- **Resposta esperada:** "Não possuo informações sobre a profissão desse usuário nos dados disponíveis."
- **Base de validação:** Arquivos 'perfis_financeiros.csv', 'transacoes.csv', 'metas_financeiras.json'
- **Métrica avaliada:** Honestidade factual, Não alucinação, Capacidade de reconhecer ausência de dados
- **Resultado:** [ ] Correto  [ ] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- O agente conseguiu recuperar corretamente informações estruturadas presentes nos arquivos .csv e .json.
- As respostas financeiras permaneceram coerentes com os dados fornecidos no contexto.
- O system prompt ajudou o agente a manter comportamento prudente e didático.
- O chatbot respondeu adequadamente perguntas fora do escopo financeiro.
- O agente demonstrou capacidade de admitir ausência de informações quando os dados não existiam.
- A integração entre Streamlit e Ollama permitiu execução local simples e funcional.
- O uso de contexto financeiro personalizado por user_id tornou as respostas mais relevantes.

**O que pode melhorar:**
- Adicionar memória conversacional para manter contexto entre múltiplas perguntas.
- Adicionar validação de inconsistências financeiras nos dados do usuário.
- Implementar autenticação e gerenciamento real de usuários.
- Adicionar métricas automáticas de avaliação das respostas do agente.
- Criar datasets com exemplos mais variados e edge cases adicionais.
- Adicionar histórico persistente de conversas em banco de dados.
- Criar testes automatizados para validação contínua do agente.
- Implementar streaming de respostas para melhorar experiência do usuário.

---

## Métricas Avançadas

Para explorar mais, algumas métricas técnicas de observabilidade também podem fazer parte da solução, como:

- Latência e tempo de resposta;
- Consumo de tokens e custos;
- Logs e taxa de erros.

Ferramentas especializadas em LLMs, como [LangWatch](https://langwatch.ai/) e [LangFuse](https://langfuse.com/), são exemplos que podem ajudar nesse monitoramento.
