from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

def gerar_mensagem_llm(lista, total):
    prompt = f"""
    Você é um atendente. Crie uma resposta simpática com os seguintes produtos e valor:

    Produtos:
    {lista}

    Total: R$ {total:.2f}
    """

    resposta = openai.ChatCompletion.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return resposta.choices[0].message.content
