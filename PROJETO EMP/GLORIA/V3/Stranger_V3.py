import pyautogui
import win32gui
import win32con
import random
import time
import sys
import cv2


# Configurações globais
WINDOW_TITLE = "Goodgame Empire - Brave"
imagem_castelo = r"C:\Users\Gustavo\Desktop\PROJETO EMP\castelo.png"
imagem_botao_ataque = r"C:\Users\Gustavo\Desktop\PROJETO EMP\botao_ataque.png"
imagem_x = r"C:\Users\Gustavo\Desktop\PROJETO EMP\x.png"
REGION_SIZE = 1  # Aumente para 10 ou mais
CLICK_DELAY = (0.4, 0.5)  # Atraso aleatório entre cliques


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

def localizar_castelo(imagem_castelo, region=None):
    """
    Localiza continuamente a imagem do castelo na tela.
    :param imagem_castelo: Caminho para a imagem do castelo (ex: "castelo.png").
    :param region: Região da tela para procurar a imagem (x, y, largura, altura).
    """
    print(f"Iniciando busca pelo castelo: {imagem_castelo}")
    while True:
        try:
            # Localiza a imagem do castelo na tela
            localizacao = pyautogui.locateOnScreen(imagem_castelo, region=region, confidence=0.8)
            if localizacao:
                print(f"Castelo encontrado em {localizacao}. Clicando...")
                # Centraliza o clique na imagem encontrada
                centro = pyautogui.center(localizacao)
                time.sleep(1)
                pyautogui.leftClick(centro.x, centro.y)
                time.sleep(1)
                return True  # Sai do loop após encontrar e clicar no castelo
            else:
                print("Castelo não encontrado. Continuando a busca...")
                time.sleep(1)  # Pequena pausa antes de tentar novamente
        except Exception as e:
            print(f"Erro ao localizar o castelo: {e}")
            time.sleep(1)  # Evita sobrecarregar o sistema em caso de erro


def localizar_botao_ataque(imagem_botao, region=None):
    """
    Localiza o botão de ataque após clicar no castelo.
    :param imagem_botao: Caminho para a imagem do botão de ataque (ex: "botao_ataque.png").
    :param region: Região da tela para procurar a imagem (x, y, largura, altura).
    :return: True se o botão de ataque for encontrado, False caso contrário.
    """
    print(f"Iniciando busca pelo botão de ataque: {imagem_botao}")
    try:
        # Localiza a imagem do botão de ataque na tela
        localizacao = pyautogui.locateOnScreen(imagem_botao, region=region, confidence=0.8)
        if localizacao:
            print(f"Botão de ataque encontrado em {localizacao}. Clicando...")
            # Centraliza o clique na imagem encontrada
            centro = pyautogui.center(localizacao)
            time.sleep(1)
            pyautogui.leftClick(centro.x, centro.y)
            time.sleep(1)
            return True  # Retorna True se o botão de ataque foi encontrado e clicado
        else:
            return False  # Retorna False se o botão de ataque não foi encontrado
    except Exception as e:
        print(f"Erro ao localizar o botão de ataque: {e}")
        return False

def localizar_e_fechar_x(imagem_x, region=None, confidence=0.8):
    """
    Localiza e clica no "X" com base em uma imagem fornecida.
    :param imagem_x: Caminho para a imagem do "X" (ex: "x.png").
    :param region: Região da tela para procurar o "X" (x, y, largura, altura).
    :param confidence: Nível de confiança para localizar a imagem (0.0 a 1.0).
    :return: True se o "X" foi encontrado e clicado, False caso contrário.
    """
    print(f"Procurando o 'X' na região {region} com confiança {confidence}...")
    try:
        # Localiza a imagem do "X" na tela
        localizacao = pyautogui.locateOnScreen(imagem_x, region=region, confidence=confidence)
        if localizacao:
            print(f"'X' encontrado em {localizacao}. Clicando para fechar...")
            centro = pyautogui.center(localizacao)
            pyautogui.leftClick(centro.x, centro.y)
            time.sleep(1)  # Pequena pausa após clicar
            return True
        else:
            print("Nenhum 'X' encontrado na região especificada.")
            return False
    except Exception as e:
        print(f"Erro ao localizar o 'X': {e}")
        return False

def localizar_todos_castelos(imagem_castelo, region=None):
    """
    Localiza todos os castelos na região especificada.
    :param imagem_castelo: Caminho para a imagem do castelo (ex: "castelo.png").
    :param region: Região da tela para procurar os castelos (x, y, largura, altura).
    :return: Lista de localizações dos castelos encontrados.
    """
    print(f"Procurando todos os castelos na região: {region}")
    try:
        # Localiza todas as ocorrências da imagem do castelo na região
        castelos = list(pyautogui.locateAllOnScreen(imagem_castelo, region=region, confidence=0.9))
        if castelos:
            print(f"{len(castelos)} castelo(s) encontrado(s).")
            return castelos
        else:
            print("Nenhum castelo encontrado.")
            return []
    except Exception as e:
        print(f"Erro ao localizar os castelos: {e}")
        return []


if __name__ == "__main__":
    if activate_window():
        try:
            while True:
                # Localiza todos os castelos na região
                castelos = localizar_todos_castelos("castelo.png", region=(268, 188, 1755, 859))
                time.sleep(1)
                
                if castelos:
                    for castelo in castelos:
                        # Centraliza o clique no castelo encontrado
                        centro = pyautogui.center(castelo)
                        time.sleep(1)
                        print(f"Atacando castelo em {centro}.")
                        time.sleep(1)
                        pyautogui.leftClick(centro.x, centro.y)
                        time.sleep(1)

                        # Localiza o botão de ataque após clicar no castelo
                        if localizar_botao_ataque("botao_ataque.png", region=(268, 188, 1755, 859)):
                            try:
                                time.sleep(1)
                                enviar_ataque()
                                time.sleep(2)
                            except Exception as e:
                                print(f"Erro durante o envio do ataque: {e}")
                                # Caso algo falhe na função enviar_ataque, tenta fechar páginas aleatórias
                                if not localizar_e_fechar_x("x.png", region=(1079, 459, 1379, 216), confidence=0.8):
                                    print("Nenhuma página aleatória encontrada. Voltando a procurar castelos...")
                        else:
                            # Caso não encontre o botão de ataque, tenta fechar páginas aleatórias
                            if not localizar_e_fechar_x("x.png", region=(1079, 459, 1379, 216), confidence=0.8):
                                print("Nenhuma página aleatória encontrada. Voltando a procurar castelos...")
                    # Após atacar todos os castelos, aguarda 13-15 minutos
                    print("Todos os castelos foram atacados. Aguardando 13-15 minutos antes de reiniciar.")
                    time.sleep(random.uniform(780, 900))  # 13-15 minutos em segundos
                else:
                    # Caso nenhum castelo seja encontrado, tenta fechar páginas aleatórias
                    if not localizar_e_fechar_x("x.png", region=(1079, 459, 1379, 216), confidence=0.8):
                        print("Nenhuma página aleatória encontrada. Voltando a procurar castelos...")

        except KeyboardInterrupt:
            print("Script encerrado pelo usuário")
    else:
        print("Janela do jogo não encontrada!")