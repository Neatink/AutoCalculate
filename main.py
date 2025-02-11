from pynput import keyboard
import time
import mss,mss.tools
import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
import threading

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.makedirs(r'C:\\Windows\\Temp', exist_ok=True)

def upgrade_image(image_path):
    img = Image.open(image_path).convert('L')
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageEnhance.Contrast(img).enhance(2)
    img = img.point(lambda x: 0 if x < 140 else 255)
    return img

def doScreen():
    with mss.mss() as sct:
        monitor = {"top": 60, "left": 0, "width": 650, "height": 120}
        output=r"C:\\Windows\\Temp\\screenshot.png"
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        return output

def Solution_Example(image_path):
    img = upgrade_image(image_path)
    text = pytesseract.image_to_string(img, lang="eng+rus+ukr")
    match = re.search(r"(\d+)\s*\+\s*(\d+)", text)
    if match:
        num1, num2 = int(match.group(1)), int(match.group(2))
        return num1 + num2
    return None

def tupping_answer(answer):
    controller = keyboard.Controller()
    controller.press("y")
    controller.release("y")
    time.sleep(0.2)
    controller.type(str(answer))
    controller.press(keyboard.Key.enter)
    controller.release(keyboard.Key.enter)

def always_screen():
    answer = Solution_Example(doScreen())
    if answer is not None:
        print(f"Ответ: {answer}")
        tupping_answer(answer)
    else:
        print("Не увидел примера")

    threading.Timer(2.0, always_screen).start()
    time.sleep(0.1)

def bind_screen():
    print("\nPress F7 to screenshot | Нажми F7 для скриншота.")
    def on_press(key):
        if key == keyboard.Key.f7:
            answer = Solution_Example(doScreen())
            if answer is not None:
                print(f"Ответ: {answer}")
                tupping_answer(answer)
            else:
                print("Не увидел примера")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    try:
        question = int(input("Всегда(BETA)(1) | По бинду(2)\nAlways(BETA)(1) | Bind(2): "))
        if question == 1:
            always_screen()
        elif question == 2:
            bind_screen()
        else:
            print("Есть варианты: 1 или 2")
    except ValueError as error:
        print(f"Писать можно только числа!")

