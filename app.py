from flask import Flask, request, jsonify
from selenium.webdriver.support.ui import WebDriverWait
from scraper_module import iniciar_driver, fazer_login, buscar_produto
import os  # Para ler a porta do ambiente Railway

app = Flask(__name__)

@app.route('/consulta', methods=['POST'])
def consulta():
    dados = request.get_json()
    termos = dados.get("produtos", [])

    if not termos:
        return jsonify({"erro": "Nenhum produto informado"}), 400

    driver = iniciar_driver()
    wait = WebDriverWait(driver, 20)

    resultados = []
    total = 0.0

    try:
        fazer_login(driver, wait)

        for termo in termos:
            produtos = buscar_produto(driver, wait, termo)
            if produtos:
                produto = produtos[0]  # primeiro da lista
                preco = produto["preco"]  # já vem como float
                total += preco
                resultados.append(produto)
            else:
                resultados.append({
                    "nome": termo,
                    "disponivel": False,
                    "preco": None
                })

        mensagem = "Orçamento:\n"
        for p in resultados:
            status = "✅" if p["disponivel"] else "❌"
            preco = f"R$ {p['preco']:.2f}" if p["preco"] is not None else "Indisponível"
            mensagem += f"{status} {p['nome']} - {preco}\n"

        mensagem += f"\nTotal: R$ {total:.2f}"

        return jsonify({
            "mensagem": mensagem,
            "total": round(total, 2),
            "produtos": resultados
        })

    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return jsonify({"erro": str(e)}), 500

    finally:
        driver.quit()

# 🚀 Rodar app na nuvem com configuração dinâmica de porta
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
