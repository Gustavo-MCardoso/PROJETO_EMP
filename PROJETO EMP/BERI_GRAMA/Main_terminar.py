import pyautogui
import win32gui
import win32con
import random
import time
import sys

# Configurações globais
WINDOW_TITLE = "Goodgame Empire - Brave"
REGION_SIZE = 1  # Aumente para 10 ou mais
CLICK_DELAY = (0.2, 0.3)  # Atraso aleatório entre cliques

def get_window_rect():
    """Obtém as coordenadas da janela do jogo"""
    hwnd = win32gui.FindWindow(None, WINDOW_TITLE)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    return None

def activate_window():
    hwnd = win32gui.FindWindow(None, WINDOW_TITLE)
    if not hwnd:
        return False
    
    # Força foco
    win32gui.BringWindowToTop(hwnd)
    win32gui.SetForegroundWindow(hwnd)
    
    # Espera adaptativa
    time.sleep(0.3 if win32gui.IsWindowVisible(hwnd) else 1)
    return True

def convert_color(color):
    """Converte cor hexadecimal para RGB"""
    if isinstance(color, str):
        color = int(color, 16)
    return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

def is_color_close(color1, color2, tolerance=50):
    """Verifica se duas cores estão próximas dentro de uma tolerância"""
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))

def is_color_in_region(x, y, expected_color, region_size=1, tolerance=50):
    """Verifica se a cor está presente na região especificada com tolerância"""
    expected = convert_color(expected_color)
    
    for dx in range(-region_size//2, region_size//2 + 1):
        for dy in range(-region_size//2, region_size//2 + 1):
            current = pyautogui.pixel(x + dx, y + dy)
            if is_color_close(current, expected, tolerance):
                return True
    return False

def click_if_color(x, y, expected_color, region_size=1, tolerance=50):
    """Clica nas coordenadas apenas se a cor estiver presente com tolerância"""
    window_rect = get_window_rect()
    if not window_rect:
        return False

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
        print(f"Cor não encontrada em ({x}, {y}) dentro da tolerância de {tolerance}!")
        sys.exit()

def click_no_color(x, y):
    """Clica nas coordenadas sem verificar cor"""
    window_rect = get_window_rect()
    if window_rect:
        wx = window_rect[0] + x
        wy = window_rect[1] + y
        pyautogui.click(wx, wy)
        time.sleep(random.uniform(*CLICK_DELAY))

def enviar_ataque():
    """Executa sequência de ataques"""
    click_if_color(1046, 688, 0x1f6c65, 1, 50)
    time.sleep(random.uniform(2.0, 2.35))
    
    click_if_color(1309, 827, 0x2C9662)
    click_if_color(1485, 946, 0x2C9662)
    click_if_color(1087, 778, 0x34AE73)

def atacar_acampamentos_beri(num_repeticoes):
    """Automatiza ataques aos acampamentos"""
    for _ in range(num_repeticoes):
        click_if_color(958, 579, 0xf8e7a3)
        
        # Primeiro acampamento
        click_no_color(512, 506)
        click_no_color(600, 531)
        enviar_ataque()
        time.sleep(random.uniform(0.5, 1.5))

        # Demais acampamentos 

if __name__ == "__main__":
    if activate_window():
        try:
            while True:
                atacar_acampamentos_beri(8)
                time.sleep(random.uniform(290, 390))
        except KeyboardInterrupt:
            print("Script encerrado pelo usuário")
    else:
        print("Janela do jogo não encontrada!")