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
        pyautogui.leftClick(wx, wy)
        time.sleep(random.uniform(*CLICK_DELAY))

def enviar_ataque():
    """Executa sequência de ataques"""
    click_if_color(1046, 688, 0x1f6c65)
    time.sleep(random.uniform(2.5, 3.0))
    
    click_if_color(1400, 835, 0x237A50)
    time.sleep(1.0)
    click_if_color(1370, 750, 0x2C9662)
    time.sleep(1.0)
    click_if_color(1373, 949, 0x2C9662)
    time.sleep(1.0)
    click_if_color(1192, 590, 0x87A6BF)
    time.sleep(1.0)
    click_if_color(1086, 773, 0x36B275)

def atacar(num_repeticoes):
    """Automatiza ataques aos acampamentos"""
    for _ in range(num_repeticoes):
        click_if_color(958, 579, 0xf8e7a3)
        
        # Primeiro acampamento
        click_no_color(699, 632)  # CP
        time.sleep(1.0)
        click_no_color(798, 658)  # BTN
        time.sleep(1.0)
        enviar_ataque()
        time.sleep(random.uniform(2.5, 3.0))

        # Segundo acampamento
        click_no_color(698, 509)  # CP
        time.sleep(1.0)
        click_no_color(800, 526)  # BTN
        enviar_ataque()
        time.sleep(random.uniform(2.5, 4.0))

        # Terceiro acampamento
        click_no_color(769, 444)  # CP
        time.sleep(1.0)
        click_no_color(856, 464)  # BTN
        enviar_ataque()
        time.sleep(random.uniform(2.5, 4.0))

        # Quarto acampamento
        click_no_color(829, 254)  # CP
        time.sleep(1.0)
        click_no_color(921, 271)  # BTN
        enviar_ataque()
        time.sleep(random.uniform(2.5, 4.0))

        # Quinto acampamento
        click_no_color(376, 502)  # CP
        time.sleep(1.0)
        click_no_color(478, 530)  # BTN
        time.sleep(1.0)
        enviar_ataque()
        time.sleep(random.uniform(2.5, 4.0))

        # Sexto acampamento
        click_no_color(386, 375)  # CP
        time.sleep(1.0)
        click_no_color(478, 399)  # BTN
        time.sleep(1.0)
        enviar_ataque()
        time.sleep(random.uniform(2.5, 4.0))

        # Sétimo acampamento
        click_no_color(1490, 635)  # CP
        time.sleep(1.0)
        click_no_color(1569, 659)  # BTN
        time.sleep(1.0)
        enviar_ataque()
        time.sleep(random.uniform(2.5, 4.0))

        # Oitavo acampamento
        click_no_color(1597, 570)  # CP
        time.sleep(1.0)
        click_no_color(1699, 590)  # BTN
        time.sleep(1.0)
        enviar_ataque()
        time.sleep(random.uniform(2.5, 4.0))

        # Nono acampamento
        click_no_color(1536, 251)  # CP
        time.sleep(1.0)
        click_no_color(1630, 273)  # BTN
        time.sleep(1.0)
        enviar_ataque()
        time.sleep(random.uniform(2.5, 4.0))

if __name__ == "__main__":
    if activate_window():
        try:
            while True:
                atacar(1)
                time.sleep(random.uniform(2300, 2700))  # Espera entre ataques
        except KeyboardInterrupt:
            print("Script encerrado pelo usuário")
    else:
        print("Janela do jogo não encontrada!")