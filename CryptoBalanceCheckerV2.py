import requests
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
import time
import threading

DARK_BG = "#121212"
DARK_FG = "#ffffff"
BLUE_ACCENT = "#00a8ff"
BLUE_DARK = "#005a8c"
LIGHT_BG = "#1e1e1e"
ENTRY_BG = "#2d2d2d"

def get_bnb_balance(address, api_key):
    url = f"https://api.bscscan.com/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "1":
                balance_in_bnb = int(data["result"]) / 10**18
                return f"{balance_in_bnb:.6f} BNB"
            else:
                return "Invalid BNB address or another error occurred."
        else:
            return "Error connecting to BSC API."
    except Exception as e:
        return f"Error: {str(e)}"

def get_btc_balance(address):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            balance_in_btc = data['final_balance'] / 10**8
            return f"{balance_in_btc:.8f} BTC"
        else:
            return f"Error: Unable to fetch BTC balance (Status Code: {response.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"

def get_eth_balance(address):
    url = f"https://api.blockcypher.com/v1/eth/main/addrs/{address}/balance"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            balance_in_eth = data['final_balance'] / 10**18
            return f"{balance_in_eth:.6f} ETH"
        else:
            return f"Error: Unable to fetch ETH balance (Status Code: {response.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"

class LoadingAnimation:
    def __init__(self, canvas, x, y, size=30, color=BLUE_ACCENT):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.arc = None
        self.angle = 0
        self.animation_id = None
        
    def start(self):
        self._animate()
        
    def _animate(self):
        self.canvas.delete(self.arc)
        self.angle = (self.angle + 5) % 360
        extent = 300 * (abs((self.angle % 180) - 90)/90)
        
        self.arc = self.canvas.create_arc(
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size,
            start=self.angle, extent=extent,
            style=tk.ARC, outline=self.color, width=3
        )
        self.animation_id = self.canvas.after(20, self._animate)
        
    def stop(self):
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
        self.canvas.delete(self.arc)

def check_balance():
    currency = currency_var.get()
    address = address_entry.get().strip()

    if not address:
        messagebox.showwarning("Missing Input", "Please enter a wallet address.")
        return
    
    loading_canvas.place(x=200, y=180, anchor="center")
    loading_animation.start()
    check_button.config(state=tk.DISABLED)
    result_label.config(text="")
    root.update()
    
    def fetch_balance():
        if currency == "BNB":
            api_key = "YJYHB6CP8G82YF8UTPSD1UFDWZ8FGRD4MH"
            result = get_bnb_balance(address, api_key)
        elif currency == "BTC":
            result = get_btc_balance(address)
        elif currency == "ETH":
            result = get_eth_balance(address)
        else:
            result = "Please select a valid currency."
        
        root.after(0, lambda: show_result(result))
    
    threading.Thread(target=fetch_balance, daemon=True).start()

def show_result(result):
    loading_animation.stop()
    loading_canvas.place_forget()
    check_button.config(state=tk.NORMAL)
    
    result_label.config(text=result)
    result_label.place(x=200, y=180, anchor="center")
    result_label.config(fg=BLUE_ACCENT)
    
    for i in range(1, 11):
        size = 10 + i
        result_label.config(font=("Arial", size, "bold"))
        root.update()
        time.sleep(0.02)
    
    if "Error" in result:
        result_label.config(fg="#ff5555")
    else:
        result_label.config(fg="#55ff55")

root = tk.Tk()
root.title("Digital Wallet Balance Checker")
root.geometry("450x300")
root.resizable(False, False)
root.configure(bg=DARK_BG)

title_font = Font(family="Helvetica", size=14, weight="bold")
label_font = Font(family="Arial", size=11)
button_font = Font(family="Arial", size=11, weight="bold")

header_frame = tk.Frame(root, bg=DARK_BG)
header_frame.pack(fill=tk.X, pady=(10, 5))

logo_canvas = tk.Canvas(header_frame, width=40, height=40, bg=DARK_BG, highlightthickness=0)
logo_canvas.pack(side=tk.LEFT, padx=10)
logo_canvas.create_oval(5, 5, 35, 35, outline=BLUE_ACCENT, width=2)
logo_canvas.create_line(20, 10, 20, 30, fill=BLUE_ACCENT, width=2)
logo_canvas.create_line(10, 20, 30, 20, fill=BLUE_ACCENT, width=2)

title_label = tk.Label(
    header_frame, 
    text="Digital Wallet Balance", 
    font=title_font, 
    fg=BLUE_ACCENT, 
    bg=DARK_BG
)
title_label.pack(side=tk.LEFT, padx=5)

main_frame = tk.Frame(root, bg=DARK_BG)
main_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

tk.Label(
    main_frame, 
    text="Select Currency:", 
    font=label_font, 
    fg=DARK_FG, 
    bg=DARK_BG
).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

currency_var = tk.StringVar(value="BTC")
currency_dropdown = ttk.Combobox(
    main_frame, 
    textvariable=currency_var, 
    values=["BTC", "ETH", "BNB"], 
    state="readonly",
    font=label_font,
    background=ENTRY_BG,
    foreground=DARK_FG
)
currency_dropdown.grid(row=0, column=1, sticky=tk.EW, pady=(0, 10), padx=(10, 0))

tk.Label(
    main_frame, 
    text="Wallet Address:", 
    font=label_font, 
    fg=DARK_FG, 
    bg=DARK_BG
).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))

address_entry = tk.Entry(
    main_frame, 
    width=40,
    font=label_font,
    bg=ENTRY_BG,
    fg=DARK_FG,
    insertbackground=DARK_FG,
    relief=tk.FLAT,
    highlightthickness=1,
    highlightbackground=BLUE_DARK,
    highlightcolor=BLUE_ACCENT
)
address_entry.grid(row=1, column=1, sticky=tk.EW, pady=(0, 10), padx=(10, 0))

button_frame = tk.Frame(main_frame, bg=DARK_BG)
button_frame.grid(row=2, column=0, columnspan=2, pady=(5, 0))

check_button = tk.Button(
    button_frame,
    text="Check Balance",
    command=check_balance,
    font=button_font,
    bg=BLUE_DARK,
    fg=DARK_FG,
    activebackground=BLUE_ACCENT,
    activeforeground=DARK_FG,
    relief=tk.FLAT,
    bd=0,
    padx=20,
    pady=5
)
check_button.pack()

loading_canvas = tk.Canvas(root, width=60, height=60, bg=DARK_BG, highlightthickness=0)
loading_animation = LoadingAnimation(loading_canvas, 30, 30)

result_label = tk.Label(
    root, 
    text="", 
    font=("Arial", 10, "bold"), 
    fg=BLUE_ACCENT, 
    bg=DARK_BG,
    wraplength=350
)

def start_animation():
    for i in range(0, 101, 5):
        root.attributes('-alpha', i/100)
        root.update()
        time.sleep(0.01)

start_animation()

main_frame.columnconfigure(1, weight=1)
for i in range(3):
    main_frame.rowconfigure(i, weight=1)

root.mainloop()
