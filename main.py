import time,os,mss,mss.tools,pytesseract,re,threading,datetime,clipboard
from PIL import Image, ImageEnhance, ImageFilter
from pynput import keyboard
from colorama import init, Fore

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.makedirs(r'C:\\Windows\\Temp', exist_ok=True)

def get_climboard():
    last_text = eval(clipboard.paste())
    def on_press(key):
        if key == keyboard.Key.f7:
            tupping_answer(last_text,1)
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    
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

def tupping_answer(answer,tupping_count):
    controller = keyboard.Controller()
    controller.release(keyboard.Key.shift)
    if tupping_count == 0:
        time.sleep(0.01)
        controller.press("y")
        controller.release("y")
        time.sleep(0.1)
    controller.type(str(answer))
    time.sleep(0.01)
    controller.press(keyboard.Key.enter)
    controller.release(keyboard.Key.enter)

def Get_Current_Time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return current_time

def always_screen():
    Cooldown = 2
    answer = Solution_Example(doScreen())
    if answer is not None:
        print(f"[{Get_Current_Time()}]{Fore.GREEN} Ответ{Fore.RESET}:{Fore.LIGHTCYAN_EX}{answer}")
        tupping_answer(answer,0)
        Cooldown = 8
    else:
        print(f"[{Get_Current_Time()}]{Fore.RED} Не увидел примера")
    threading.Timer(Cooldown, always_screen).start()
    time.sleep(0.1)

def bind_screen():
    print(f"\n{Fore.CYAN}Press F7 to screenshot {Fore.RESET}| {Fore.MAGENTA}Нажми F7 для скриншота")
    def on_press(key):
        if key == keyboard.Key.f7:
            answer = Solution_Example(doScreen())
            if answer is not None:
                print(f"[{Get_Current_Time()}]{Fore.GREEN} Ответ{Fore.RESET}:{Fore.LIGHTCYAN_EX}{answer}")
                tupping_answer(answer,0)
            else:
                print(f"[{Get_Current_Time()}]{Fore.RED} Не увидел примера")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    init(autoreset=True)
    try:
        question = int(input(f"{Fore.CYAN}Clipboard(3) {Fore.RESET}| {Fore.MAGENTA}Буфер обмена(3)\n{Fore.CYAN}Always(2) {Fore.RESET}| {Fore.MAGENTA}Всегда(2)\n{Fore.CYAN}Bind(1) {Fore.RESET}| {Fore.MAGENTA}Бинд(1){Fore.RESET}: "))
        if question == 1:
            bind_screen()
        elif question == 2:
            always_screen()
        elif question == 3:
            get_climboard()
        else:
            print("Число должно быть из списка выше!")
    except ValueError:
        print(f"Писать можно только числа!")
