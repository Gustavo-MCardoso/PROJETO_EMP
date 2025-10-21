import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

# Configurações
DEBUG_WINDOW = 'Debug Mask (Q para sair)'
BLUR_THRESHOLD = 50  # Valor inicial (ajuste com o slider)

# Cria janela do OpenCV e slider
cv2.namedWindow(DEBUG_WINDOW)
cv2.createTrackbar('Blur Threshold', DEBUG_WINDOW, BLUR_THRESHOLD, 255, lambda x: None)

while True:
    # Captura a tela
    screenshot = ImageGrab.grab()
    screen_np = np.array(screenshot)
    screen_cv = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
    
    # Converte para HSV e extrai a saturação
    hsv = cv2.cvtColor(screen_cv, cv2.COLOR_BGR2HSV)
    _, saturation, _ = cv2.split(hsv)
    
    # Atualiza o threshold do slider
    blur_threshold = cv2.getTrackbarPos('Blur Threshold', DEBUG_WINDOW)
    
    # Cria a máscara binária
    _, mask = cv2.threshold(saturation, blur_threshold, 255, cv2.THRESH_BINARY)
    
    # Redimensiona para melhor visualização
    scale_percent = 50  # % da tela original
    width = int(screen_cv.shape[1] * scale_percent / 100)
    height = int(screen_cv.shape[0] * scale_percent / 100)
    resized_screen = cv2.resize(screen_cv, (width, height))
    resized_mask = cv2.resize(mask, (width, height))
    
    # Concatena tela original + máscara
    combined = np.hstack((resized_screen, cv2.cvtColor(resized_mask, cv2.COLOR_GRAY2BGR)))
    
    # Mostra a imagem combinada
    cv2.imshow(DEBUG_WINDOW, combined)
    
    # Sai ao pressionar 'Q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

#active_regions = detect_active_windows(screen_cv, blur_threshold=175)