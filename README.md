# Validador Masivo de CURP 

Automatización en Python para la validación y extracción de datos oficiales de CURP desde el portal de RENAPO. Este script permite procesar listas extensas de registros desde archivos Excel, garantizando la integridad de los datos mediante un sistema de auto-guardado incremental.

## 🚀 Características

* **Automatización con Selenium:** Navegación automática en el portal oficial de [gob.mx/curp/](https://www.gob.mx/curp/).
* **Extracción vía JavaScript:** Uso de `execute_script` para obtener datos precisos del DOM, evitando errores comunes de selectores CSS.
* **Gestión de Datos con Pandas:** Lectura y escritura eficiente de archivos `.xlsx`.
* **Persistencia de Datos:** Guardado automático cada 5 registros para evitar pérdidas por fallos de red o Timeouts.
* **Logs en Consola:** Seguimiento en tiempo real del progreso de procesamiento.

## 🛠️ Requisitos previos

Es necesario tener instalado **Python 3.x** y el navegador **Google Chrome**.

### Instalación de dependencias

Ejecuta el siguiente comando para instalar las librerías necesarias:

```bash
pip install pandas selenium webdriver-manager openpyxl
