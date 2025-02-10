from pynput import keyboard
import time
import mss,mss.tools
import os
import pytesseract
from PIL import Image
import re


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

os.makedirs(r'screenshots', exist_ok=True)

def doScreen():
    with mss.mss() as sct:

        monitor = {"top": 60, "left": 0, "width": 650, "height": 120}

        output=r"screenshots\\screenshot.png".format(**monitor)
        sct_img = sct.grab(monitor)

        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

        return output



def Solution_Example(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang="eng+rus")


    match = re.search(r"(\d+)\s*\+\s*(\d+)", text)
    if match:
        num1, num2 = int(match.group(1)), int(match.group(2))
        return num1 + num2
    return None



def tupping_answer(answer):
    controller = keyboard.Controller()

    controller.press("y")
    controller.release("y")

    time.sleep(0.01)

    controller.type(str(answer))


    controller.press(keyboard.Key.enter)
    controller.release(keyboard.Key.enter)

screenshot_path = doScreen()
answer = Solution_Example(screenshot_path)

if answer != None:
    print(f"Ответ: {answer}")
    tupping_answer(answer)
else:
    print("Не увидел примера")