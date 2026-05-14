# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `perfis_financeiros.csv` | CSV | Informações sobre renda, despesas, dívidas, reserva |
| `metas_financeiras.json` | JSON | Informações de metas de curto, médio e lonog prazo |
| `transacoes.csv` | CSV | Informações sobre receitas e despesas categorizadas |

---

## Adaptações nos Dados

Os dados foram gerados artificialmente para permitir a análise pelo agente, compondo um dataset com dados de usuários, transações e metas financeiras).

---

## Estratégia de Integração

### Como os dados são carregados?

Os JSON/CSV são carregados no início da sessão e incluídos no contexto do prompt

### Como os dados são usados no prompt?

Para simplificar, podemos simplesmente "injetar" os dados em nosso prompt, garantindo que o Agente tenha o melhot contexto possível. Lembrando que, em soluções mais robustas, o ideal é que essas informações sejma carregadasdinamicamente para que possamos ganhar flexibilidade.

Perfil Financeiro:

user_id, idade, renda_mensal, despesas_fixas, despesas_variaveis, dividas, reserva_atual

1,28,3500,1800,900,1200,500

2,35,8000,3000,2000,0,15000

3,22,1800,900,600,500,200

4,45,12000,5000,3000,2000,40000

5,31,5000,2200,1500,8000,1000

...

Transações:

user_id,data,tipo,categoria,valor

1,2026-01-05,despesa,alimentacao,450

1,2026-01-10,despesa,transporte,200

1,2026-01-15,receita,salario,3500

1,2026-01-20,despesa,lazer,300

2,2026-01-05,despesa,alimentacao,800

2,2026-01-10,receita,salario,8000

2,2026-01-12,despesa,viagem,1500

3,2026-01-07,receita,salario,1800

3,2026-01-08,despesa,alimentacao,300

4,2026-01-03,receita,salario,12000

4,2026-01-15,despesa,educacao,2000

5,2026-01-01,receita,salario,5000

5,2026-01-09,despesa,dividas,1200

...

Metas Financeiras:

```[
  {
    "user_id": 1,
    "metas": [
      {
        "tipo": "curto_prazo",
        "descricao": "Quitar dívida",
        "valor_objetivo": 1200,
        "prazo_meses": 6,
        "prioridade": "alta"
      },
      {
        "tipo": "medio_prazo",
        "descricao": "Montar reserva de emergência",
        "valor_objetivo": 6000,
        "prazo_meses": 24,
        "prioridade": "alta"
      }
    ]
  },
  {
    "user_id": 2,
    "metas": [
      {
        "tipo": "longo_prazo",
        "descricao": "Aposentadoria",
        "valor_objetivo": 1000000,
        "prazo_meses": 240,
        "prioridade": "alta"
      }
    ]
  },
  ...
  ]
```
---

## Exemplo de Contexto Montado

O exemplo de contexto montado abaixo se baseia nos dados originais da base de conhecimento, mas os sintetiza deixando apenas as informações mais relevantes, otimizando assim o consumo de tokens. Entretanto, vale lembrar que mais importante do que economizar tokens, é ter todas as informações disponíveis em seu contexto.

```
Perfil Financeiro (Dados do Cliente):
- user_id: 1
- idade: 28
- renda_mensal: 3500
- despesas_fixas: 1800
- despesas_variaveis: 900
- dividas: 1200
- reserva_atual: 500

Transações:
- user_id: 1
- data: 2026-01-05
- tipo: despesa
- categoria: alimentacao
- valor: 450

Metas Financeiras:
- tipo: curto_prazo,
- descricao: Quitar dívida,
- valor_objetivo: 1200,
- prazo_meses: 6,
- prioridade: "alta"
```
