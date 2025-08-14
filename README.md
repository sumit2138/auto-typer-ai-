Description:
This Python script allows you to select a region on your screen, then continuously reads (OCR) any text inside that region and types it out at 129 WPM.
It only types new or changed text, ignoring tiny OCR mistakes, so it doesn’t erase and retype unnecessarily.

Features:

Screen selection with click-and-drag

Transparent selection overlay

OCR with Tesseract (auto-detects path on Windows)

Fast typing speed (129 WPM)

Smart diff detection — only types changed text

Ignores tiny OCR glitches to avoid chaos

Works until you press ESC to stop

Requirements:
Install the following Python packages:

pip install opencv-python numpy pyautogui pytesseract pillow keyboard


Also Install Tesseract OCR:

Download from: https://github.com/UB-Mannheim/tesseract/wiki

Install

Make sure the path to tesseract.exe is correct in the script.

How to Use:

Run the script:

python ocr_auto_typer.py


Click and drag to select the area containing the text you want typed.

Release the mouse — OCR will start automatically.

The script will type the text wherever your cursor is.

Press ESC to stop.

Notes:

Works best on clear, readable fonts.

Avoid moving the selection box after starting — re-run if needed.

Use with caution — this script can type very fast!
