from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()

driver.get('http://localhost:8000')

useredit = driver.find_elements(By.CLASS_NAME, 'user')[-1]
useredit.click()

input_nome = driver.find_element(By.NAME, 'nome')
input_nome.clear()

input_nome.send_keys('Teste por selenium Editado')

input_email = driver.find_element(By.NAME, 'email')
input_email.clear()

input_email.send_keys('teste@teste.com')

botao_salvar = driver.find_elements(By.CLASS_NAME, 'btn-primary')[-1]  # pega o último botão (caso haja 2)
botao_salvar.click()

# Aguarda o alerta de sucesso aparecer
try:
    mensagem_sucesso = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'alert-success'))
    )
    print("Mensagem:", mensagem_sucesso.text)
    assert "Dados recebidos com sucesso!" in mensagem_sucesso.text
    print("✅ Teste passou!")

except TimeoutException:
    print("❌ A mensagem de sucesso não apareceu em até 10 segundos.")

finally:
    driver.quit()