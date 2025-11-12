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

botao_criar_usuario = driver.find_element(By.CLASS_NAME, 'btn-primary')
botao_criar_usuario.click()

# Preenche os campos
driver.find_element(By.NAME, 'matricula').send_keys('123456')
driver.find_element(By.NAME, 'nome').send_keys('João Silva')
driver.find_element(By.NAME, 'email').send_keys('joao@email.com')
driver.find_element(By.NAME, 'ativoDeRegistro').send_keys('01/01/2024')

# Seleciona opções
Select(driver.find_element(By.NAME, 'tipo')).select_by_visible_text('Aluno')
Select(driver.find_element(By.NAME, 'status')).select_by_visible_text('Ativo')

# Clica em salvar
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
