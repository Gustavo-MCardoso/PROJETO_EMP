import cv2
import pyautogui
import time
import sys
import random
from collections import deque
import win32gui
import win32con
from GLORIA.V4.fechar_paginas import fechar_paginas


# Configurações
WINDOW_TITLE = "Goodgame Empire - Brave"
imagem_castelo = r"C:\Users\Gustavo\Desktop\PROJETO EMP\castelo.png"
imagem_botao_ataque = r"C:\Users\Gustavo\Desktop\PROJETO EMP\botao_ataque.png"
imagem_x = r"C:\Users\Gustavo\Desktop\PROJETO EMP\x.png"
CONFIANCA_CASTELO = 0.9
TEMPO_ENTRE_ACOES = 0.3
COOLDOWN_BASE = 840  # 13 minutos
REGIAO_BUSCA = (268, 188, 1755, 859)  # (x1, y1, x2, y2) para limitar área de busca

class LocalizadorCastelos:
    def __init__(self):
        self.castelos_encontrados = deque()
        self.ultimas_posicoes = {}
        self.contador = 0

    def localizar_castelos(self):
        try:
            return list(pyautogui.locateAllOnScreen('castelo.png', 
                      confidence=CONFIANCA_CASTELO, 
                      region=REGIAO_BUSCA))
        except Exception as e:
            print(f"Erro na localização: {e}")
            return []

    def atualizar_posicoes(self):
        novos = self.localizar_castelos()
        if not novos:
            return False
            
        for castelo in novos:
            x, y = pyautogui.center(castelo)
            if (x, y) not in self.ultimas_posicoes:
                self.castelos_encontrados.append((x, y))
                self.ultimas_posicoes[(x, y)] = time.time()
                self.contador += 1
                print(f"Castelo {self.contador} registrado em ({x}, {y})")
        
        return True

def mover_e_clicar(x, y):
    pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.5))
    pyautogui.click()
    time.sleep(random.uniform(0.1, 0.3))
    pyautogui.moveTo(random.randint(100, 500), random.randint(100, 500))  # Movimento aleatório

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


def fechar_janelas(imagem, region=None, confidence=0.9):
    if localizar_e_clicar('x.png', region=(1082, 449, 1472, 138), confidence=0.3):
        print("Janela indesejada fechada")
        time.sleep(1)
        return True
    return False

def localizar_e_clicar(imagem, region=None, confidence=0.9):
    try:
        pos = pyautogui.locateOnScreen(imagem, confidence=0.9)
        if pos:
            x, y = pyautogui.center(pos)
            pyautogui.click(x, y)
            return True
    except:
        return False

def ciclo_ataque():
    localizador = LocalizadorCastelos()
    
    while True:
        # Etapa 1: Ativar página
        ativar_pagina_especifica()
        
        # Tentar fechar janelas indesejadas
        if fechar_paginas('x.png', threshold=0.5, usar_opencv=True):
            print("Janelas indesejadas fechadas. Continuando...")

        # Etapa 2: Localizar castelos
        if not localizador.atualizar_posicoes():
            if fechar_paginas('x.png', threshold=0.5, usar_opencv=True):
                continue
            else:
                print("Nenhum castelo encontrado")
                time.sleep(5)
                continue
                
        print(f"{len(localizador.castelos_encontrados)} castelos para atacar")
        
        # Etapa 3: Processar cada castelo
        while localizador.castelos_encontrados:
            x, y = localizador.castelos_encontrados.popleft()
            
            print(f"Atacando castelo em ({x}, {y})")
            mover_e_clicar(x, y)
            
            # Verificar botão de ataque
            if not localizar_e_clicar('botao_ataque.png'):
                if fechar_paginas('x.png', threshold=0.5, usar_opencv=True):
                    localizador.castelos_encontrados.appendleft((x, y))  # Reinsere na fila
                    break
                else:
                    print("Botão de ataque não encontrado")
                    continue
                    
            # Executar ataque
            realizar_ataque()
        
        # Limpar posições antigas
        localizador.ultimas_posicoes.clear()
        
        # Atualizar cooldown após atacar todos os castelos
        cooldown = random.randint(COOLDOWN_BASE, COOLDOWN_BASE + 120)
        print(f"Cooldown de {cooldown//60} minutos iniciado")
        time.sleep(cooldown)

def realizar_ataque():
    print("Executando sequência de ataque...")
    time.sleep(1)
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
    time.sleep(1)

def get_window_rect():
    """Obtém as coordenadas da janela do jogo"""
    hwnd = win32gui.FindWindow(None, WINDOW_TITLE)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        return rect
    return None

def ativar_pagina_especifica():
    hwnd = win32gui.FindWindow(None, WINDOW_TITLE)
    if not hwnd:
        print(f"Janela '{WINDOW_TITLE}' não encontrada.")
        return False

    # Força foco na janela
    win32gui.BringWindowToTop(hwnd)
    time.sleep(0.5)
    win32gui.SetForegroundWindow(hwnd)

    # Espera adaptativa
    time.sleep(0.3 if win32gui.IsWindowVisible(hwnd) else 1)
    print(f"Janela '{WINDOW_TITLE}' ativada.")
    return True

if __name__ == "__main__":
    try:
        ciclo_ataque()
    except KeyboardInterrupt:
        print("\nExecução finalizada pelo usuário")
        sys.exit()