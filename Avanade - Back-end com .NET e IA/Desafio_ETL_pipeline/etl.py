
import pandas as pd
from gpt_service import GPTService

def extract(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)

def transform(df: pd.DataFrame, gpt: GPTService) -> pd.DataFrame:
    mensagens = []

    for _, row in df.iterrows():
        user_id = row["UserID"]
        print(f"Gerando mensagem para UserID: {user_id} ...")

        msg = gpt.gerar_mensagem(user_id)
        mensagens.append(msg)

    df["MarketingMessage"] = mensagens
    return df

def load(df: pd.DataFrame, output_path: str):
    df.to_csv(output_path, index=False)
    print(f"\nArquivo salvo em: {output_path}")

def run_etl():
    input_file = "data/users.csv"
    output_file = "output/messages.csv"
    gpt = GPTService()
    df = extract(input_file)
    df = transform(df, gpt)
    load(df, output_file)

if __name__ == "__main__":
    run_etl()
