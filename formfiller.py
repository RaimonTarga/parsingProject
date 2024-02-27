import json
import os
import xpathstrings
from time import sleep
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # Project Root
INPUT_FILE_NAME = 'Listados.json'
INPUT_PATH = os.path.join(ROOT_DIR, INPUT_FILE_NAME)
URL = 'https://angular.specialisternespain.com/gestion-datos/#/tramitacion-pedidos'
USERNAME = ''
OPTIONS = webdriver.ChromeOptions() 
OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging']) 
SERVICE = Service('chromedriver.exe') 

# si el valor es 0, no saltara ninguna ID y empezara por el principio
try:
    SKIP_ID = int(input('¿Quieres saltar a una ID en particular? Introduce 0 en el caso contrario\n'))
except ValueError:
    SKIP_ID = 0

try:
    #intentamos abrir el archivo de listados
    with open(INPUT_PATH , 'r') as f:
        input_data = json.load(f)
    #abrimos el driver
    driver = webdriver.Chrome(service=SERVICE, options=OPTIONS)
    driver.get(URL)
    #alta
    driver.find_element(By.XPATH, xpathstrings.BUTTON_ALTA_XPATH).click()
    #introducir contraseña
    driver.find_element(By.XPATH, xpathstrings.PASS_XPATH).send_keys(USERNAME)
    driver.find_element(By.XPATH, xpathstrings.PASS_BUTTON_XPATH).click()
    sleep(2)

    for item in input_data:
        #salta el elemento si hemos especificado una ID a la que queremos salta
        if (SKIP_ID != 0 and int(item['ID_Cliente']) < SKIP_ID):
            continue
        #introduce ID cliente
        driver.find_element(By.XPATH, xpathstrings.ID_CLIENTE_XPATH).send_keys(item['ID_Cliente'])
        driver.find_element(By.XPATH, xpathstrings.ID_CLIENTE_BUTTON_XPATH).click()
        try:
            #hemos encontrado el mensaje de error
            overlay = driver.find_element(By.CLASS_NAME, xpathstrings.OVERLAY_CLASS)
            #cierra el mensaje de error
            driver.find_element(By.XPATH, xpathstrings.ERRORBUTTON_XPATH).click()
            #borra el campo de ID
            driver.find_element(By.XPATH, xpathstrings.ID_CLIENTE_XPATH).click()
            driver.find_element(By.XPATH, xpathstrings.ID_CLIENTE_XPATH).send_keys(Keys.CONTROL + "a")
            driver.find_element(By.XPATH, xpathstrings.ID_CLIENTE_XPATH).send_keys(Keys.DELETE)
            sleep(1)
        except NoSuchElementException:
            #no hemos encontrado el mensaje de error y por lo tanto, la ID es valida
            #introduce ID de facturacion
            driver.find_element(By.XPATH, xpathstrings.ID_FACTURACION_XPATH).send_keys(item['ID_Facturacion'])
            driver.find_element(By.XPATH, xpathstrings.ID_FACTURACION_BUTTON_XPATH).click()
            #guarda los valores que necesitaremos para llenar los campos
            pin1 = driver.find_element(By.XPATH, xpathstrings.PIN1_XPATH).get_attribute('value')
            clave1 = driver.find_element(By.XPATH, xpathstrings.CLAVE1_XPATH).get_attribute('value')
            pin2 = driver.find_element(By.XPATH, xpathstrings.PIN2_XPATH).get_attribute('value')
            clave2 = driver.find_element(By.XPATH, xpathstrings.CLAVE2_XPATH).get_attribute('value')
            pedido = driver.find_element(By.XPATH, xpathstrings.PEDIDO_XPATH).get_attribute('value')
            cantidad = driver.find_element(By.XPATH, xpathstrings.CANTIDAD_XPATH).get_attribute('value')
            #introduce valores de control 1
            driver.find_element(By.XPATH, xpathstrings.CONTROL_PIN1_XPATH).send_keys(pin1)
            driver.find_element(By.XPATH, xpathstrings.CONTROL_CLAVE1_XPATH).send_keys(clave1)
            driver.find_element(By.XPATH, xpathstrings.CONTROL_BUTTON1_XPATH).click()
            #guarda numero de control 1
            control1 = driver.find_element(By.XPATH, xpathstrings.DIGITO_CONTROL1_XPATH).get_attribute('value')
            #introduce valores de control 2
            driver.find_element(By.XPATH, xpathstrings.CONTROL_PIN2_XPATH).send_keys(pin2)
            driver.find_element(By.XPATH, xpathstrings.CONTROL_CLAVE2_XPATH).send_keys(clave2)
            driver.find_element(By.XPATH, xpathstrings.CONTROL_BUTTON2_XPATH).click()
            #guarda numero de control 2
            control2 = driver.find_element(By.XPATH, xpathstrings.DIGITO_CONTROL2_XPATH).get_attribute('value')
            #introduce numeros de control, n. pedido y cantidad
            driver.find_element(By.XPATH, xpathstrings.TRANSACCION_CONTROL1_XPATH).send_keys(control1)
            driver.find_element(By.XPATH, xpathstrings.TRANSACCION_CONTROL2_XPATH).send_keys(control2)
            driver.find_element(By.XPATH, xpathstrings.TRANSACCION_PEDIDO_XPATH).send_keys(pedido)
            driver.find_element(By.XPATH, xpathstrings.TRANSACCION_CANTIDAD_XPATH).send_keys(cantidad)    
            driver.find_element(By.XPATH, xpathstrings.SIGUIENTE_BUTTON_XPATH).click()
            sleep(2)
            #introduce numero de articulos y codigo internacional
            driver.find_element(By.XPATH, xpathstrings.NUMARTICULOS_XPATH).send_keys(item['N_Articulos'])
            driver.find_element(By.XPATH, xpathstrings.CODIGO_XPATH).send_keys(item['Cod_Internacional'])
            #si necesitamos generar factura, activa el checkbox
            if bool(item['Generar_factura']):
                driver.find_element(By.XPATH, xpathstrings.CHECKBOX_XPATH).click()
            driver.find_element(By.XPATH, xpathstrings.GENERAR_BUTTON_XPATH).click()
            sleep(2)
    #cierra el driver
    driver.quit()
except IOError:
    print('Error: el archivo ' + INPUT_FILE_NAME + ' no existe o no se puede encontrar')

    
    