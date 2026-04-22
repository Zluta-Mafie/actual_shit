import cv2
import numpy as np
import math
from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.go2.video.video_client import VideoClient

ChannelFactoryInitialize(0)
client = VideoClient()
client.SetTimeout(3.0)
client.Init()
def ShootImage():
    code, data = client.GetImageSample()
    imageName = "./img.jpg"
    print("ImageName:", imageName)
    with open(imageName, "+wb") as f:
        f.write(bytes(data))

def GetVisualInfo():
    ShootImage()
    img = cv2.imread('img.jpg')
    h, w = img.shape[:2]

    # 1. Převod na šedou a prahování
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)

    # --- VÝPOČET PRO 90 % (blízko u robota) ---
    roi_h1 = int(h * 0.99)
    # Vezmeme malý proužek od 90 % výšky (např. 20 pixelů vysoký)
    roi1 = thresh[roi_h1 : roi_h1 + 20, :]
    M1 = cv2.moments(roi1)

    # --- VÝPOČET PRO 60 % (vzdálenější výhled) ---
    roi_h2 = int(h * 0.9)
    # Vezmeme malý proužek od 60 % výšky
    roi2 = thresh[roi_h2 : roi_h2 + 20, :]
    M2 = cv2.moments(roi2)


    # Ověř si skutečnou šířku, kterou Python vidí
    #print(f"Skutečná šířka obrazu (w): {w}")
    #print(f"Střed obrazu (w // 2): {w // 2}")

    # Upravený výpočet s kontrolou
    def get_deviation(M, width):
        if M["m00"] > 0:
            cX = int(M["m10"] / M["m00"])
            mid = width // 2
            offset = cX - mid
            return cX, offset
        return None, None

    pos1, offset1 = get_deviation(M1, w)
    pos2, offset2 = get_deviation(M2, w)

    angle = math.degrees(math.atan2(h*0.3, pos2-pos1))

    return (offset1, angle)
