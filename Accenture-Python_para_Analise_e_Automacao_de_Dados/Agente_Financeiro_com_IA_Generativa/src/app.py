import json
import pandas as pd
import requests
import streamlit as st
from pathlib import Path

# ==============================
# CAMINHOS
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# ==============================
# CONFIGURAÇÕES
# ==============================

API_URL = "http://localhost:1234/v1/chat/completions"
MODELO = "qwen2.5-0.5b-instruct"

# ==============================
# CARREGAR DADOS
# ==============================

perfil_df = pd.read_csv(DATA_DIR / "perfis_financeiros.csv")

transacoes_df = pd.read_csv(DATA_DIR / "transacoes.csv")

with open(DATA_DIR / "metas_financeiras.json", "r", encoding="utf-8") as f:
    metas_json = json.load(f)


# ==============================
# FUNÇÕES AUXILIARES
# ==============================

def obter_contexto_usuario(user_id):
    perfil = perfil_df[perfil_df["user_id"] == user_id]

    if perfil.empty:
        return "Usuário não encontrado."

    perfil = perfil.iloc[0]

    transacoes = transacoes_df[
        transacoes_df["user_id"] == user_id
        ].head(10)

    metas = next(
        (m for m in metas_json if m["user_id"] == user_id),
        None
    )

    contexto = f"""
    CLIENTE ID: {perfil['user_id']}

    IDADE: {perfil['idade']}
    RENDA MENSAL: R$ {perfil["renda_mensal"]}
    DESPESAS FIXAS: R$ {perfil['despesas_fixas']}
    DESPESAS VARIÁVEIS: R$ {perfil['despesas_variaveis']}
    DÍVIDAS: R$ {perfil['dividas']}
    RESERVA ATUAL: R$ {perfil['reserva_atual']}

    TRANSAÇÕES RECENTES:
    {transacoes.to_string(index=False)}

    METAS FINANCEIRAS:
    {json.dumps(metas, indent=2, ensure_ascii=False)}
    """

    return contexto


# ==============================
# SYSTEM PROMPT
# ==============================

SYSTEM_PROMPT = """
Você é o Planner, um assistente financeiro amigável,
didático e responsável.

OBJETIVO:
Auxiliar usuários na definição de metas financeiras
de curto, médio e longo prazo.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos;
2. Nunca invente informações financeiras;
3. Seja prudente em recomendações financeiras;
4. Explique o raciocínio de forma clara;
5. Sugira organização financeira antes de investimentos arriscados;
6. Sempre pergunte se o cliente entendeu;
7. Responda em português brasileiro.
"""


# ==============================
# CHAMAR OLLAMA
# ==============================

def perguntar(user_id, pergunta_usuario):
    contexto = obter_contexto_usuario(user_id)

    mensagens = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"""
            CONTEXTO:
            {contexto}

            PERGUNTA:
            {pergunta_usuario}
            """
        }
    ]

    try:

        response = requests.post(
            API_URL,
            json={
                "model": MODELO,
                "messages": mensagens,
                "temperature": 0.7
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Erro ao acessar LM Studio: {e}"


# ==============================
# INTERFACE STREAMLIT
# ==============================

st.set_page_config(page_title="Planner IA")

st.title("💰 Planner IA")
st.subheader("Assistente de Planejamento Financeiro")

# Seleção de usuário

user_id = st.number_input(
    "Selecione o ID do usuário",
    min_value=1,
    max_value=200,
    value=1
)

# Mostrar dados resumidos

perfil_usuario = perfil_df[
    perfil_df["user_id"] == user_id
    ].iloc[0]

st.write("### Perfil Financeiro")

st.write({
    "Renda": int(perfil_usuario["renda_mensal"]),
    "Dívidas": int(perfil_usuario["dividas"]),
    "Reserva": int(perfil_usuario["reserva_atual"])
})

# Chat

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

pergunta = st.chat_input(
    "Digite sua dúvida financeira..."
)

if pergunta:
    st.session_state.messages.append({
        "role": "user",
        "content": pergunta
    })

    st.chat_message("user").write(pergunta)

    with st.spinner("Pensando..."):
        resposta = perguntar(user_id, pergunta)

        st.session_state.messages.append({
            "role": "assistant",
            "content": resposta
        })

        st.chat_message("assistant").write(resposta)
