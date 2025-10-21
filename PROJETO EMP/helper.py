import pyautogui
import time
import pygetwindow as gw 
from PIL import ImageGrab
import random
import sys
import win32gui
import win32con
import cv2
import numpy as np
import keyboard  # Biblioteca para capturar eventos do teclado

# Configurações
WINDOW_TITLE = "Goodgame Empire - Brave"
beri_botao = r"C:\Users\Gustavo\Desktop\PROJETO EMP\BERI_REINO\Beri_btn.png"
btn_ataque = r"C:\Users\Gustavo\Desktop\PROJETO EMP\BERI_REINO\botao_ataque.png"
COOLDOWN = 6  # Tempo de espera entre as verificações (em segundos)
REGION = (767, 567, 1194, 885)  # Região de busca para pop-ups
X_TEMPLATES = [ 'v.png', 'x.png']  # Templates dos "X"
THRESHOLD = 0.8  # Sensibilidade do template matching

def ativar_pagina_especifica():
    """
    Ativa a janela do navegador com o título especificado.
    """
    hwnd = win32gui.FindWindow(None, WINDOW_TITLE)
    if not hwnd:
        print(f"Janela '{WINDOW_TITLE}' não encontrada.")
        return False

    # Garante que a janela esteja visível
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    time.sleep(0.1)

    # Traz a janela para o primeiro plano
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print(f"Erro ao ativar a janela: {e}")
        return False

    # Espera adaptativa
    time.sleep(0.3 if win32gui.IsWindowVisible(hwnd) else 1)
    print(f"Janela '{WINDOW_TITLE}' ativada.")
    return True

def get_window_rect():
    """Obtém as coordenadas da janela do jogo"""
    hwnd = win32gui.FindWindow(None, WINDOW_TITLE)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    return None

def close_popup():
    """
    Procura imagens de "X" na tela, move o mouse até elas e clica com o botão direito.
    """
    # Captura a tela na região especificada
    screen = pyautogui.screenshot(region=REGION)
    screen_cv = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    for template_file in X_TEMPLATES:
        # Carrega o template
        template = cv2.imread(template_file)
        if template is None:
            print(f"Template '{template_file}' não encontrado ou inválido.")
            continue

        # Realiza a correspondência de templates
        res = cv2.matchTemplate(screen_cv, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= THRESHOLD)  # Filtra correspondências com base no threshold
        w, h = template.shape[:-1]

        # Itera sobre os pontos detectados
        for pt in zip(*loc[::-1]):
            x = pt[0] + REGION[0] + w // 2
            y = pt[1] + REGION[1] + h // 2

            # Move o mouse e clica com o botão direito
            pyautogui.moveTo(x, y, duration=0.2)
            pyautogui.leftClick()
            print(f"Clicou com o botão direito em ({x}, {y}).")
            time.sleep(0.3)  # Pequena pausa entre os cliques

def procurar_e_clicar(imagem, regiao, confidence=0.8):
    """
    Procura uma imagem em uma região específica da tela e clica nela se encontrada.
    """
    try:
        posicao = pyautogui.locateOnScreen(imagem, region=regiao, confidence=0.8)
        if posicao:
            centro = pyautogui.center(posicao)
            pyautogui.leftClick(centro.x, centro.y)
            print(f"Imagem '{imagem}' encontrada e clicada!")
            return True
        else:
            print(f"Imagem '{imagem}' não encontrada na região especificada.")
            return False
    except pyautogui.ImageNotFoundException:
        print(f"Erro ao procurar a imagem '{imagem}'.")
        return False



def clicar_e_arrastar(x_inicial, y_inicial, x_final, y_final, duracao=0.5):
    """
    Realiza um clique e arraste do ponto inicial (x_inicial, y_inicial)
    até o ponto final (x_final, y_final).
    """
    
    pyautogui.moveTo(630, 501, duration=random.uniform(0.2, 0.5))
    pyautogui.mouseDown()  # Pressiona o botão do mouse
    pyautogui.dragTo(626, 560, duration=duracao)  # Arrasta até o ponto final
    pyautogui.mouseUp()  # Solta o botão do mouse

def convert_color(color):
    """Converte cor hexadecimal para RGB"""
    if isinstance(color, str):
        color = int(color, 16)
    return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

def is_color_close(color1, color2, tolerance=100):
    """Verifica se duas cores estão próximas dentro de uma tolerância"""
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))

def is_color_in_region(x, y, expected_color, region_size=1, tolerance=100):
    """Verifica se a cor está presente na região especificada com tolerância"""
    expected = convert_color(expected_color)
    
    for dx in range(-region_size//2, region_size//2 + 1):
        for dy in range(-region_size//2, region_size//2 + 1):
            current = pyautogui.pixel(x + dx, y + dy)
            if is_color_close(current, expected, tolerance):
                return True
    return False

def click_if_color(x, y, expected_color, region_size=1, tolerance=100):
    """Clica nas coordenadas apenas se a cor estiver presente com tolerância"""
    window_rect = get_window_rect()
    if not window_rect:
        raise ValueError("Não foi possível obter as coordenadas da janela.")

    # Ajusta coordenadas relativas à janela
    wx = window_rect[0] + x
    wy = window_rect[1] + y

    pyautogui.moveTo(wx, wy, duration=0.1)
    time.sleep(0.1)
    
    if is_color_in_region(wx, wy, expected_color, region_size, tolerance):
        pyautogui.click(wx, wy)
        time.sleep(random.uniform(0.5, 1.0))
        return True
    else:
        raise ValueError(f"Cor não encontrada em ({x}, {y}) dentro da tolerância de {tolerance}!")

def tela_ataque():
    time.sleep(1)
    click_if_color(1046, 688, 0x1f6c65)
    time.sleep(random.uniform(2.5, 3.0))

    pyautogui.moveTo(623, 443)
    time.sleep(0.5)  
    pyautogui.leftClick(623, 443)
    time.sleep(0.5)
    clicar_e_arrastar(630, 501, 626, 560, duracao=0.5)
    time.sleep(0.5)
    pyautogui.moveTo(492, 880)
    time.sleep(0.5) 
    pyautogui.leftClick(492, 880)
    time.sleep(0.5)

    click_if_color(1400, 835, 0x237A50)
    time.sleep(0.5)
    click_if_color(1373, 949, 0x2C9662)
    time.sleep(0.5)
    click_if_color(1192, 590, 0x87A6BF)
    time.sleep(0.5)
    click_if_color(1086, 773, 0x36B275)
    time.sleep(0.5)

script_running = True

def stop_script():
    """Função para parar o script."""
    global script_running
    script_running = False
    print("Tecla 'P' pressionada. Encerrando o script...")
    sys.exit()  # Encerra o programa imediatamente

# Configura o atalho para parar o script
keyboard.add_hotkey("p", stop_script)

def main_loop():
    global script_running
    while script_running:
        # Restaura e ativa a janela do jogo
        janela_ativa = gw.getWindowsWithTitle(WINDOW_TITLE)
        if janela_ativa:
            ativar_pagina_especifica()
            print("Janela ativada. Iniciando sequência...")

            # Fecha pop-ups antes de continuar
            close_popup()

            # Procura e clica na primeira imagem (beri_botao)
            if procurar_e_clicar(beri_botao, (1639, 979, 1737, 1041), 0.8):
                print("Primeira imagem encontrada e clicada.")

                # Procura e clica na segunda imagem (btn_ataque)
                if procurar_e_clicar(btn_ataque, (818, 392, 1195, 726), 0.8):
                    print("Segunda imagem encontrada e clicada.")

                    # Chama a função tela_ataque com tratamento de erro
                    try:
                        tela_ataque()
                        print("Função tela_ataque executada.")
                    except ValueError as e:
                        print(f"Erro em tela_ataque: {e}")
                        close_popup()  # Fecha pop-ups e tenta novamente
                        continue  # Reinicia o loop principal

                    # Espera 20 segundos antes de reiniciar o loop
                    time.sleep(20)
                else:
                    close_popup()
                    print("Segunda imagem não encontrada.")
            else:
                close_popup()
                print("Primeira imagem não encontrada.")
        else:
            print("Janela do jogo não está ativa. Tentando novamente em 5 segundos...")
            time.sleep(5)  # Espera antes de tentar novamente

if __name__ == "__main__":
    pyautogui.PAUSE = 0.3  # Segurança contra falhas
    print("Pressione 'P' para parar o script.")
    main_loop()