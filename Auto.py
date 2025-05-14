import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from tkinter import filedialog, messagebox
from tkinter import Frame, Label
import time

class TabbedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Webautomation")
        self.root.geometry("700x600")

        self.browser_config = {
            "part_profile": None,
            "chrome_path": None,
            "driver_path": None,
            "version": None
        }

        self.notebook = ttk.Notebook(root, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.add_tab(self.create_page1(), "Custom Chrome Setup")
        self.add_tab(self.create_page2(), "Logs")
        self.add_tab(self.create_page3(), "About")

    def add_tab(self, frame, title):
        self.notebook.add(frame, text=title)

    def create_page1(self):
        frame = Frame(self.notebook, bg="#1f1f2e")

        ttk.Label(frame, text="Setup Chrome for dev", font=("Helvetica", 20), bootstyle="info").pack(pady=(10, 0))
        ttk.Label(frame, text="ก่อนนะจ้ะ", bootstyle="secondary").pack()

        # === Profile Entry ===
        ttk.Label(frame, text="ตำแหน่ง Profile Folder", bootstyle="info").pack(pady=(10, 0))
        self.profile_entry = ttk.Entry(frame, width=60)
        self.profile_entry.pack(pady=(0, 10))
        ttk.Button(frame, text="เลือกโฟลเดอร์ Profile", command=self.select_profile, bootstyle="outline-info").pack(pady=(0, 15))

        # === Chrome Path ===
        ttk.Label(frame, text="ตำแหน่ง Chrome.exe", bootstyle="info").pack(pady=(10))
        self.chrome_entry = ttk.Entry(frame, width=60)
        self.chrome_entry.pack()
        ttk.Button(frame, text="เลือก Chrome.exe", command=self.select_chrome, bootstyle="outline-info").pack(pady=(10))

        # === Driver Path ===
        ttk.Label(frame, text="ตำแหน่ง Chromedriver.exe", bootstyle="info").pack(pady=(10))
        self.driver_entry = ttk.Entry(frame, width=60)
        self.driver_entry.pack()
        ttk.Button(frame, text="เลือก Chromedriver.exe", command=self.select_driver, bootstyle="outline-info").pack(pady=(10))

        # === Version ===
        ttk.Label(frame, text="เวอร์ชั่น Chrome (optional)", bootstyle="info").pack(pady=(10))
        self.version_entry = ttk.Entry(frame, width=20)
        self.version_entry.pack()

        # === Start Button ===
        ttk.Button(frame, text="เริ่มทำงาน", command=self.start_browser, bootstyle="light").pack(pady=10)

        return frame

    # ===== ฟังก์ชันย่อยสำหรับหน้าแรก =====
    def select_profile(self):
        path = filedialog.askdirectory()
        if path:
            self.profile_entry.delete(0, "end")
            self.profile_entry.insert(0, path)
            self.browser_config["part_profile"] = path

    def select_chrome(self):
        path = filedialog.askopenfilename(filetypes=[("Chrome Executable", "chrome.exe")])
        if path:
            self.chrome_entry.delete(0, "end")
            self.chrome_entry.insert(0, path)
            self.browser_config["chrome_path"] = path

    def select_driver(self):
        path = filedialog.askopenfilename(filetypes=[("Chromedriver Executable", "chromedriver.exe")])
        if path:
            self.driver_entry.delete(0, "end")
            self.driver_entry.insert(0, path)
            self.browser_config["driver_path"] = path

    def start_browser(self):
        self.browser_config["version"] = self.version_entry.get().strip()

        if not all([self.browser_config["part_profile"], self.browser_config["chrome_path"], self.browser_config["driver_path"]]):
            messagebox.showerror("Error", "กรุณาเลือก path ให้ครบก่อนเริ่มทำงาน")
            return

        try:
            chrome_options = Options()
            chrome_options.add_argument(f"--user-data-dir={self.browser_config['part_profile']}")
            chrome_options.add_argument(f"--profile-directory=Default")
            chrome_options.binary_location = self.browser_config["chrome_path"]

            service = Service(self.browser_config["driver_path"])
            driver = webdriver.Chrome(service=service, options=chrome_options)

            time.sleep(2)
            driver.get("https://google.com")
            messagebox.showinfo("Success", "เปิด Chrome สำเร็จแล้ว!")
        except Exception as e:
            messagebox.showerror("Error", f"เปิด Chrome ไม่ได้:\n{e}")

    def create_page2(self):
        frame = Frame(self.notebook, bg="#261d3d")
        Label(frame, text="นี่คือหน้า Logs", font=("Helvetica", 16), bg="#261d3d", fg="#ffafff").pack(pady=20)
        return frame

    def create_page3(self):
        frame = Frame(self.notebook, bg="#2b1e4d")
        Label(frame, text="Vapor mode activated!", font=("Helvetica", 16), bg="#2b1e4d", fg="#a0f5c0").pack(pady=20)
        return frame

# ===== Run Application =====
if __name__ == "__main__":
    app = ttk.Window(themename="vapor")
    TabbedApp(app)