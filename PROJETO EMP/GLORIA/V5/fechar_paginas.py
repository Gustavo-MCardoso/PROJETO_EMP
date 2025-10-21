import pyautogui
import cv2
import numpy as np
import time 


def fechar_paginas(imagem, threshold=0.8, region=None, confidence=0.9, usar_opencv=False):
    """
    Verifica se a imagem está presente na tela e move o cursor até ela.
    Pode usar pyautogui ou OpenCV para localizar a imagem.
    """
    try:
        if usar_opencv:
            # Captura a tela atual e converte para escala de cinza
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

            # Carrega a imagem de referência
            img = cv2.imread(imagem, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"Erro: Não foi possível carregar a imagem '{imagem}'.")
                return False

            # Realiza a correspondência de template
            resultado = cv2.matchTemplate(screenshot_gray, img, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

            if max_val >= threshold:
                # Calcula o centro da imagem encontrada
                x, y = max_loc
                x += img.shape[1] // 2
                y += img.shape[0] // 2
                print(f"Imagem '{imagem}' encontrada com confiança: {max_val}. Movendo o cursor para ({x}, {y})...")
                pyautogui.moveTo(x, y, duration=0.5)
                pyautogui.leftClick(x, y)  # Clica na posição encontrada
                time.sleep(0.5)  # Espera
                return True
            else:
                print(f"Imagem '{imagem}' não encontrada com OpenCV.")
                return False
        else:
            # Usa pyautogui para localizar a imagem
            pos = pyautogui.locateOnScreen(imagem, region=region, confidence=confidence)
            if pos:
                x, y = pyautogui.center(pos)
                print(f"Imagem '{imagem}' encontrada na posição: ({x}, {y}). Movendo o cursor...")
                pyautogui.moveTo(x, y, duration=0.5)
                return True
            else:
                print(f"Imagem '{imagem}' não encontrada com pyautogui.")
                return False
    except Exception as e:
        print(f"Erro ao verificar a tela: {e}")
        return False
    
imagem = 'x.png'
region = (1082, 449, 1472, 138)
confidence = 0.3    

# Usando OpenCV
#fechar_paginas('x.png', threshold=0.5, usar_opencv=True)