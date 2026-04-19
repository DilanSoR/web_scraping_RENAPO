import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# --- CONFIGURACIÓN ---
archivo_entrada = "entrada_curps.xlsx"
archivo_salida = "resultados_acreditaciones.xlsx"

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

try:
    df_entrada = pd.read_excel(archivo_entrada)
    print(f"Excel cargado con {len(df_entrada)} registros.")
except Exception as e:
    print(f"Error al leer Excel: {e}")
    exit()

resultados_finales = []

for index, row in df_entrada.iterrows():
    curp = str(row['persona_curp']).strip().upper()
    print(f"[{index + 1}/{len(df_entrada)}] Procesando: {curp}")

    driver.get("https://www.gob.mx/curp/")
    registro = {
        "persona_curp": curp,
        "persona_nombre": "",
        "persona_primer_apellido": "",
        "persona_segundo_apellido": "",
        "estatus": "No válido",
        "observaciones": ""
    }

    try:
        wait = WebDriverWait(driver, 20)
        input_f = wait.until(EC.element_to_be_clickable((By.ID, "curpinput")))
        input_f.send_keys(curp)
        driver.find_element(By.ID, "searchButton").click()

        # Esperar confirmación de éxito
        wait.until(EC.presence_of_element_located((By.ID, "download")))
        time.sleep(4)

        # Extracción vía JavaScript
        try:
            script_get_val = "return Array.from(document.querySelectorAll('td')).find(el => el.textContent.includes(arguments[0])).nextElementSibling.innerText;"

            registro["persona_nombre"] = driver.execute_script(
                script_get_val, "Nombre(s):")
            registro["persona_primer_apellido"] = driver.execute_script(
                script_get_val, "Primer apellido:")
            registro["persona_segundo_apellido"] = driver.execute_script(
                script_get_val, "Segundo apellido:")

            if registro["persona_nombre"]:
                registro["estatus"] = "Válido ✅"
                print(f"   ✨ Guardado: {registro['persona_nombre']}")
            else:
                registro["observaciones"] = "Datos no encontrados por JS"
        except Exception:
            registro["observaciones"] = "Error en script de extracción"

    except Exception:
        if "Los datos ingresados no son correctos" in driver.page_source:
            registro["observaciones"] = "CURP no encontrada"
        else:
            registro["observaciones"] = "Timeout o CAPTCHA pendiente"

    # Añadir a la lista de resultados
    resultados_finales.append(registro)

    # --- LÓGICA DE AUTO-GUARDADO CADA 5 REGISTROS ---
    actual = index + 1
    if actual % 5 == 0 or actual == len(df_entrada):
        df_temporal = pd.DataFrame(resultados_finales)
        df_temporal.to_excel(archivo_salida, index=False)
        print(
            f"[AUTO-GUARDADO] Progreso guardado en '{archivo_salida}' ({actual} registros).")

    time.sleep(2)

driver.quit()
print(
    f"\n Proceso finalizado. Total de registros procesados: {len(resultados_finales)}")
