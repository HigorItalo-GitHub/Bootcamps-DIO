
import os
from openai import OpenAI

class GPTService:
    def __init__(self, api_key=None, model="gpt-4.1-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def gerar_mensagem(self, user_id: int) -> str:
        prompt = (
            f"Crie uma breve mensagem de marketing personalizada para o cliente "
            f"de ID {user_id}. O tom deve ser amigável, curto e voltado ao engajamento."
        )

        resposta = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return resposta.output[0].content[0].text
