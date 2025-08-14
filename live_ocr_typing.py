import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image
import keyboard
import time
import difflib
import os
import re

# Auto-detect Tesseract path (Windows)
common_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
]
for path in common_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        break

start_point = None
end_point = None
cropping = False
selection_done = False

def select_area(event, x, y, flags, param):
    global start_point, end_point, cropping, selection_done
    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        cropping = True
    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        end_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        cropping = False
        selection_done = True

def get_selection():
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    clone = img.copy()

    cv2.namedWindow("Select Area", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Select Area", select_area)

    while True:
        display_img = clone.copy()
        if cropping and start_point and end_point:
            cv2.rectangle(display_img, start_point, end_point, (0, 255, 0), 2)
        elif selection_done and start_point and end_point:
            cv2.rectangle(display_img, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow("Select Area", display_img)
        if selection_done:
            break
        if cv2.waitKey(1) & 0xFF == 27:
            cv2.destroyAllWindows()
            return None
    cv2.destroyAllWindows()

    x1, y1 = start_point
    x2, y2 = end_point
    return (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))

def clean_text(text):
    # Normalize spaces and remove weird OCR artifacts
    text = re.sub(r"[ \t]+", " ", text)
    text = text.replace("\r", "").replace("\u200b", "")  # Remove invisible chars
    return text.strip()

def ocr_image(region):
    screenshot = pyautogui.screenshot(region=region)
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    text = pytesseract.image_to_string(Image.fromarray(img))
    return clean_text(text)

def first_diff_index(a, b):
    min_len = min(len(a), len(b))
    for i in range(min_len):
        if a[i] != b[i]:
            return i
    if len(b) > len(a):
        return len(a)
    return None

def main():
    print("Select the area to OCR...")
    region = get_selection()
    if not region:
        print("Selection cancelled.")
        return

    wpm = 129
    cps = (wpm * 5) / 60.0  # characters per second

    print("Beast mode typing started. Press ESC to stop.")
    last_text = ""
    stable_text = ""

    while not keyboard.is_pressed("esc"):
        current_text = ocr_image(region)

        # Skip tiny random OCR glitches (require stability for 2 frames)
        if current_text != stable_text:
            stable_text = current_text
            time.sleep(0.1)
            continue

        if current_text != last_text:
            diff_index = first_diff_index(last_text, current_text)
            if diff_index is not None:
                pyautogui.typewrite(current_text[diff_index:], interval=1.0/cps)
            last_text = current_text

        time.sleep(0.2)

if __name__ == "__main__":
    main()
