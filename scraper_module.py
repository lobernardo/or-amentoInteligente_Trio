import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fazer_login(driver, wait):
    print("🔐 Acessando site...")
    driver.get("https://www.triodistribuidora.com.br/")
    botao_login = wait.until(EC.presence_of_element_located((By.ID, "botao-login")))
    driver.execute_script("arguments[0].click();", botao_login)

    print("🔐 Esperando botão de login...")
    campo_email = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    campo_senha = driver.find_element(By.NAME, "senha")
    campo_email.send_keys("milenesantos.intec@gmail.com")
    campo_senha.send_keys("66800")
    driver.find_element(By.ID, "btn-entrar").click()
    time.sleep(3)
    print("✅ Login efetuado.")

def buscar_produto(driver, wait, termo):
    print(f"🔎 Buscando: {termo}")
    driver.get("https://www.triodistribuidora.com.br/produtos")
    time.sleep(2)

    campo_busca = wait.until(EC.presence_of_element_located((By.NAME, "busca")))
    campo_busca.clear()
    campo_busca.send_keys(termo)
    campo_busca.submit()
    time.sleep(2)

    try:
        produtos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-produto-grid")))
        resultado = []

        for produto in produtos:
            try:
                nome = produto.find_element(By.CLASS_NAME, "CardProduto_tituloCardProduto__9LOZC").text.strip()
                preco_inteiro = produto.find_element(By.CLASS_NAME, "Produto_valorUnitarioDestaque__6RREL").text.strip().replace("R$", "").replace(",", ".").strip()
                preco_float = float(preco_inteiro.split()[0])

                resultado.append({
                    "nome": nome,
                    "preco": preco_float,
                    "disponivel": True
                })

                print(f"✅ Produto válido: {nome} - R$ {preco_float:.2f}")
            except Exception as e:
                print(f"⛔ Falha na conversão de preço: {e}")
                continue

        return resultado

    except Exception as e:
        print(f"❌ Erro ao buscar produto: {e}")
        return []
