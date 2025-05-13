from tkinter import filedialog, messagebox, Tk, Label, Entry, Button
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import time

# === เก็บค่า config ที่กรอกใน GUI
browser_config = {
    "part_profile": None,
    "chrome_path": None,
    "driver_path": None,
    "version": None
}

def select_profile():
    path = filedialog.askdirectory()
    if path:
        profile_entry.delete(0, "end")
        profile_entry.insert(0, path)
        browser_config["part_profile"] = path

def select_chrome():
    path = filedialog.askopenfilename(filetypes=[("Chrome Executable", "chrome.exe")])
    if path:
        chrome_entry.delete(0, "end")
        chrome_entry.insert(0, path)
        browser_config["chrome_path"] = path

def select_driver():
    path = filedialog.askopenfilename(filetypes=[("Chromedriver Executable", "chromedriver.exe")])
    if path:
        driver_entry.delete(0, "end")
        driver_entry.insert(0, path)
        browser_config["driver_path"] = path

def start_browser():
    browser_config["version"] = version_entry.get().strip()

    if not all([browser_config["part_profile"], browser_config["chrome_path"], browser_config["driver_path"]]):
        messagebox.showerror("Error", "กรุณาเลือก path ให้ครบก่อนเริ่มทำงาน")
        return

    try:
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={browser_config['part_profile']}")
        chrome_options.add_argument(f"--profile-directory=Default")
        chrome_options.binary_location = browser_config["chrome_path"]

        service = Service(browser_config["driver_path"])
        driver = webdriver.Chrome(service=service, options=chrome_options)

        time.sleep(2)
        driver.get("https://google.com")  # ทดสอบเปิดเว็บ

        messagebox.showinfo("Success", "เปิด Chrome สำเร็จแล้ว!")
    except Exception as e:
        messagebox.showerror("Error", f"เปิด Chrome ไม่ได้:\n{e}")

# === GUI
root = Tk()
root.title("Webautomatic")
root.geometry("500x500")
root.configure(bg='black')

Label(root, text="Setup Chrome for dev", fg="green", bg="black", font=("Helvetica", 20)).pack(pady=(10, 0))
Label(root, text="ก่อนนะจ้ะ", fg="green", bg="black").pack()

Label(root, text="ตำแหน่ง Profile Folder", fg="green", bg="black").pack(pady=(10, 0))
profile_entry = Entry(root, width=60)
profile_entry.pack(pady=(0, 10))
Button(root, text="เลือกโฟลเดอร์ Profile", fg="green", bg="black", command=select_profile).pack(pady=(0, 15))

Label(root, text="ตำแหน่ง Chrome.exe", fg="green", bg="black").pack(pady=(10))
chrome_entry = Entry(root, width=60)
chrome_entry.pack()
Button(root, text="เลือก Chrome.exe", fg="green", bg="black", command=select_chrome).pack(pady=(10))

Label(root, text="ตำแหน่ง Chromedriver.exe", fg="green", bg="black").pack(pady=(10))
driver_entry = Entry(root, width=60)
driver_entry.pack()
Button(root, text="เลือก Chromedriver.exe", fg="green", bg="black", command=select_driver).pack(pady=(10))

Label(root, text="เวอร์ชั่น Chrome (optional)", fg="green", bg="black").pack(pady=(10))
version_entry = Entry(root, width=20)
version_entry.pack()

Button(root, text="เริ่มทำงาน", bg="green", fg="white", command=start_browser).pack(pady=10)

root.mainloop()