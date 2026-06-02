# Pitch — Planner IA: Assistente Inteligente de Planejamento Financeiro

## 1. O Problema

Muitas pessoas enfrentam dificuldades para organizar suas finanças, definir metas realistas e compreender sua própria situação financeira.

Grande parte das soluções disponíveis é complexa, pouco acessível ou exige conhecimentos técnicos em finanças. Como consequência, muitas pessoas:

- acumulam dívidas;
- não conseguem formar uma reserva de emergência;
- tomam decisões financeiras impulsivas;
- não sabem por onde começar seu planejamento financeiro.

Diante desse cenário, surge a necessidade de transformar dados financeiros em orientações simples, acessíveis e personalizadas.

---

## 2. A Solução

O **Planner IA** é um agente inteligente de planejamento financeiro desenvolvido para auxiliar usuários na organização e tomada de decisões financeiras.

A solução foi construída utilizando:

- Python;
- Streamlit;
- Ollama;
- Modelos de Linguagem (LLMs) executados localmente.

O sistema utiliza dados financeiros estruturados em arquivos `.csv` e `.json`, contendo informações sobre:

- perfis financeiros;
- transações;
- metas financeiras.

Com base nesses dados, o agente é capaz de:

- analisar renda, despesas, dívidas e reservas financeiras;
- responder perguntas relacionadas à situação financeira do usuário;
- sugerir prioridades financeiras;
- auxiliar na definição de metas;
- oferecer recomendações alinhadas ao perfil financeiro informado.

O projeto foi desenvolvido com foco em:

- privacidade dos dados;
- segurança;
- explicabilidade das respostas;
- execução local, sem dependência de APIs externas pagas.

Além disso, foram desenvolvidos:

- datasets fictícios;
- exemplos *Few-Shot*;
- casos de teste (*Edge Cases*);
- avaliações para validação do comportamento do agente.

---

## 3. Demonstração

Durante a demonstração do projeto é possível observar:

### Interface

- aplicação desenvolvida em Streamlit;
- seleção de usuários a partir do dataset financeiro.

### Exemplos de Perguntas

- "Qual deve ser minha prioridade financeira?"
- "Como posso organizar melhor minhas finanças?"
- "Devo investir ou quitar minhas dívidas?"

### Funcionamento

O agente consulta os dados financeiros do usuário e produz respostas contextualizadas com base em seu perfil.

Também são demonstrados:

- recuperação correta das informações financeiras;
- recomendações personalizadas;
- tratamento de perguntas fora do escopo;
- reconhecimento de informações inexistentes.

Todo o processamento é realizado localmente por meio do Ollama, sem necessidade de serviços externos.

---

## 4. Diferenciais e Impacto

O principal diferencial do Planner IA é combinar:

- Inteligência Artificial local;
- privacidade dos dados;
- planejamento financeiro personalizado.

A solução pode ser adaptada para diferentes contextos, incluindo:

- educação financeira;
- suporte bancário;
- orientação financeira básica;
- plataformas de gestão financeira.

O impacto esperado é democratizar o acesso a orientações financeiras mais claras, acessíveis e responsáveis, especialmente para pessoas que enfrentam dificuldades na organização de suas finanças.

Além disso, o projeto demonstra a viabilidade da integração de modelos LLM executados localmente em aplicações reais desenvolvidas com ferramentas *open source*.

---

## Checklist do Pitch

- ✅ Duração máxima de 3 minutos
- ✅ Problema claramente definido
- ✅ Solução demonstrada na prática
- ✅ Diferencial apresentado
- ✅ Boa qualidade de áudio e vídeo
