
# Digital Wallet Balance Checker - Documentation

This Python GUI application allows users to check the balance of cryptocurrency wallets (BTC, ETH, BNB) using public blockchain APIs. The GUI is built with `tkinter`, and threading is used for smooth UI operation during network calls.

---

## 📦 Dependencies

```bash
pip install requests pillow
```

---

## 📁 Code Overview

### ✅ Imports

```python
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
import time
import threading
```
- `requests`: for API calls to get wallet balances.
- `tkinter`: for GUI components.
- `PIL`: used here for potential image support.
- `time`, `threading`: for delay effects and async-like behavior.

---

### 🎨 Color Definitions

```python
DARK_BG = "#121212"
DARK_FG = "#ffffff"
BLUE_ACCENT = "#00a8ff"
BLUE_DARK = "#005a8c"
LIGHT_BG = "#1e1e1e"
ENTRY_BG = "#2d2d2d"
```

---

### 🔗 API Calls

#### Get BNB Balance

```python
def get_bnb_balance(address, api_key):
```
Uses the BscScan API to fetch BNB balance and returns the value in BNB.

#### Get BTC Balance

```python
def get_btc_balance(address):
```
Uses BlockCypher to fetch BTC balance, converting satoshis to BTC.

#### Get ETH Balance

```python
def get_eth_balance(address):
```
Also uses BlockCypher, returning ETH in standard format.

---

### ⏳ Loading Animation Class

```python
class LoadingAnimation:
```
Creates a rotating arc to show a loading indicator using a `Canvas` widget. Methods: `start`, `_animate`, and `stop`.

---

### 🧮 Main Logic: Balance Checker

```python
def check_balance():
```
Triggered on button press. Validates input, shows animation, and starts a background thread to fetch balance.

#### Balance Fetching

```python
def fetch_balance():
```
Uses selected currency to call the appropriate balance-fetching function.

#### Result Display

```python
def show_result(result):
```
Stops animation, updates GUI, animates the result font size, and colorizes result (green for success, red for errors).

---

### 🪟 GUI Setup

```python
root = tk.Tk()
root.title("Digital Wallet Balance Checker")
...
```
- Sets up the main window and applies a dark theme.
- Adds a custom "plus" icon using lines and ovals on a `Canvas`.
- Organizes the interface using `Frame`, `Label`, `Entry`, `Button`, and `Combobox`.

---

### 💫 Animation on Start

```python
def start_animation():
```
Fades in the window on startup.

---

## 🚀 Run the Application

Just run the script with Python 3.7+.

---

## 🧠 Notes

- Uses a free public API. Rate-limits may apply.
- GUI is responsive thanks to `threading.Thread`.

---


## Contact

For any questions or feedback, please contact:  
✉️ sajjaddavoodi1387@gmail.com
