from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # invisível
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


def fazer_login(driver, wait):
    print("🔐 Acessando site...")
    driver.get("https://www.triodistribuidora.com.br/")

    print("🔐 Esperando botão de login...")
    botao_login = wait.until(EC.presence_of_element_located((By.ID, "botao-login")))
    driver.execute_script("arguments[0].click();", botao_login)

    campo_email = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    campo_senha = driver.find_element(By.NAME, "senha")

    campo_email.send_keys("milenesantos.intec@gmail.com")
    campo_senha.send_keys("66800")

    driver.find_element(By.ID, "btn-entrar").click()
    print("✅ Login efetuado.")
    time.sleep(3)


def buscar_produto(driver, wait, termo):
    print(f"🔎 Buscando: {termo}")
    url = f"https://www.triodistribuidora.com.br/produtos?busca={termo}"
    driver.get(url)
    time.sleep(3)

    produtos = []

    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "card-produto-grid")))
        cards = driver.find_elements(By.CLASS_NAME, "card-produto-grid")

        for card in cards:
            try:
                nome = card.find_element(By.CLASS_NAME, "CardProduto_tituloCardProduto__9LOZC").text.strip()
            except:
                nome = ""

            try:
                preco_el = card.find_element(By.CLASS_NAME, "Produto_valorUnitarioDestaque__6RREL")
                preco_inteiro_raw = preco_el.text.strip().replace("R$", "").replace(" ", "").replace(",", ".")
                preco_inteiro = float(preco_inteiro_raw)
            except:
                preco_inteiro = None

            try:
                centavos = card.find_elements(By.CLASS_NAME, "Produto_valorUnitario__qy7Ms")
                preco_decimal_raw = centavos[1].text.strip() if len(centavos) > 1 else "00"
                preco_decimal = int(preco_decimal_raw.zfill(2)) / 100
            except:
                preco_decimal = 0

            if preco_inteiro is not None:
                preco_float = round(preco_inteiro + preco_decimal, 2)
            else:
                preco_float = None

            if termo.lower() not in nome.lower():
                print(f"⚠️ Produto ignorado (nome não contém termo): {nome}")
                continue

            if nome and preco_float is not None:
                produtos.append({
                    "nome": nome,
                    "preco": preco_float,
                    "disponivel": True
                })
                print(f"✅ Produto válido: {nome} - R$ {preco_float:.2f}")
            else:
                print(f"⛔ Produto ignorado: nome={nome}, preco={preco_float}")

        return produtos

    except Exception as e:
        print(f"❌ Erro ao buscar '{termo}': {e}")
        return []
