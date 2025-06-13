import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from tkinter import filedialog, messagebox
from tkinter import Frame, Label
import time
import webbrowser
from selenium.webdriver.common.by import By

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

        self.action_blocks = {}

        self.notebook = ttk.Notebook(root, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.add_tab(self.ChromeSetup_page(), "Custom Chrome Setup")
        self.add_tab(self.Action_page(), "Action")
        self.add_tab(self.About_page(), "About")

    def add_tab(self, frame, title):
        self.notebook.add(frame, text=title)

    def ChromeSetup_page(self):
        frame = Frame(self.notebook, bg="#1f1f2e")

        ttk.Label(frame, text="Setup Chrome for dev", font=("Helvetica", 20), bootstyle="info").pack(pady=(10, 0))
        ttk.Label(frame, text="ก่อนนะจ้ะ", bootstyle="secondary").pack()

        # === Profile Entry ===
        ttk.Label(frame, text="ตำแหน่ง Profile Folder", bootstyle="info").pack(pady=(10, 0))
        self.profile_entry = ttk.Entry(frame, width=60)
        self.profile_entry.pack(pady=(0, 10))
        ttk.Button(frame, text="เลือกโฟลเดอร์ Profile", command=self.select_profile, bootstyle="outline-info").pack(pady=(0, 15))

        # === Chrome Path ===
        ttk.Label(frame, text="ตำแหน่ง Chrom.exe", bootstyle="info").pack(pady=(10))

        
        self.chrome_entry = ttk.Entry(frame, width=60)
        self.chrome_entry.pack(pady=(0, 5))

        chrome_row = ttk.Frame(frame)
        chrome_row.pack(pady=(0, 10))


        ttk.Button(chrome_row, text="เลือก Chrome.exe", command=self.select_chrome, bootstyle="outline-info").pack(side="left", padx=(0, 5))

        ttk.Button(chrome_row, text="📥 Download", command=self.download_chrome, bootstyle="secondary-outline").pack(side="left")

        # === Driver Path ===
        
        ttk.Label(frame, text="ตำแหน่ง Chromedriver.exe", bootstyle="info").pack(pady=(10))

        self.driver_entry = ttk.Entry(frame, width=60)
        self.driver_entry.pack(pady=(0, 10))

        driver_row = ttk.Frame(frame)
        driver_row.pack(pady=(0, 10))

        ttk.Button(driver_row, text="เลือก Chromedriver.exe", command=self.select_driver, bootstyle="outline-info").pack(side="left", padx=(0, 5))

        ttk.Button(driver_row, text="📥 Download", command=self.download_chrome,bootstyle="secondary-outline").pack(side="left")


        # === Version ===
        ttk.Label(frame, text="เวอร์ชั่น Chrome (optional)", bootstyle="info").pack(pady=(10))
        self.version_entry = ttk.Entry(frame, width=20)
        self.version_entry.pack()

        # === Start Button ===
        ttk.Button(frame, text="เริ่มทำงาน", command=self.start_browser, bootstyle="light").pack(pady=10)

        return frame

    # ===== ฟังก์ชันย่อยสำหรับหน้าแรก =====
    def download_chrome(self):
        webbrowser.open("https://googlechromelabs.github.io/chrome-for-testing/")

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
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            time.sleep(2)
            self.driver.get("https://google.com")
            messagebox.showinfo("Success", "เปิด Chrome สำเร็จแล้ว!")
        except Exception as e:
            messagebox.showerror("Error", f"เปิด Chrome ไม่ได้:\n{e}")

    def Action_page(self):
        frame = Frame(self.notebook, bg="#1f1f2e")
    # === ซ้าย: กล่องม่วง Command set ===
        self.left_block = ttk.Frame(frame, style="white.TFrame", width=300, height=600)
        self.left_block.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        

        ttk.Label(
    self.left_block,
    text="Command set",
    bootstyle="light",
    anchor="center",
    font=("Helvetica", 12, "bold"),
    background="white",
    foreground="#333333",
    padding=5
).pack(fill="x")

    # === ขวา: ปุ่ม ===
        right = Frame(frame, bg="white", width=250)
        right.pack(side="right", fill="y", padx=10, pady=10)

        self.create_command_button(right, "find text")
        self.create_command_button(right, "find attribute")
        self.create_command_button(right, "click")
        self.create_command_button(right, "input text")

        ttk.Button(self.left_block, text="🚀 Execute All", command=self.execute_all, bootstyle="success-outline").pack(pady=20)

        return frame

    def About_page(self):
        frame = Frame(self.notebook, bg="#2b1e4d")
        Label(frame, text="Visit my github https://github.com/Bamjr", font=("Helvetica", 16), bg="#2b1e4d", fg="#a0f5c0").pack(pady=20)
        return frame
    
    def create_command_button(self, parent, text,command=None):
        commands = {
        "find text": self.find_text_block,
        "find attribute": self.find_attribute_block, 
        # "click": self.click_block,                   # (ไว้ค่อยเพิ่ม)
        # "input text": self.input_text_block          # (ไว้ค่อยเพิ่ม)
    }
        ttk.Button(parent, text=text, command=commands.get(text), bootstyle="outline-info", width=20).pack(pady=10)

    # ===== Action block =====
    def find_text_block(self):
        frame = ttk.Frame(self.left_block, padding=10)
        frame.pack(fill="x", pady=5)

        label = ttk.Label(frame, text="Find text:")
        label.pack(side="left")

        entry = ttk.Entry(frame, width=30)
        entry.pack(side="left", padx=5)

    # เก็บไว้ใน action_blocks["find_text"] เป็น list
        if "find_text" not in self.action_blocks:
            self.action_blocks["find_text"] = []

        self.action_blocks["find_text"].append(entry)

    def find_attribute_block(self):
        frame = ttk.Frame(self.left_block, padding=10)
        frame.pack(fill="x", pady=5)
        label = ttk.Label(frame, text="Find attribute:")
        label.pack(side="left")
        
        label2 = ttk.Label(frame, text="Tag name:")
        label2.pack(side="left", padx=(10, 0))
        entryTAG = ttk.Entry(frame, width=15)
        entryTAG.pack(side="left", padx=5)
        label3 = ttk.Label(frame, text="class name:")
        label3.pack(side="left", padx=(10, 0))
        entryCLASS = ttk.Entry(frame, width=15)
        entryCLASS.pack(side="left", padx=5)

        if "find_attribute" not in self.action_blocks:
            self.action_blocks["find_attribute"] = []

        self.action_blocks["find_attribute"].append((entryTAG, entryCLASS))


        

    # ===== Action Functions =====

    def find_text(self):
        if not hasattr(self, "driver") or not self.driver:
            messagebox.showerror("Error", "กรุณาเปิด Chrome ก่อนใช้งาน find_text")
            return

        text_entries = self.action_blocks.get("find_text", [])
        for entry in text_entries:                # ← วนทุกช่อง
            keyword = entry.get().strip()
            if not keyword:                       # ← ข้ามช่องว่าง
                continue
            try:
                elements = self.driver.find_elements(
                    By.XPATH,
                    f"//*[contains(normalize-space(text()), '{keyword}')]"
                )
                for el in elements:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                    self.driver.execute_script("arguments[0].style.border='2px solid red'", el)
            except Exception as e:
                print(f"[find_text] {e}")
    
    def build_xpath(self,tag_name: str, class_name: str) -> str:
        tag = tag_name or '*'                     # ว่าง = wildcard
        cls = class_name.strip()
        if not cls:
            return f"//{tag}"                     # หาเฉพาะ tag

        # รองรับหลาย class แยกด้วยช่องว่าง, ต้องครบทุกคลาส
        parts = [
            f"contains(concat(' ', normalize-space(@class), ' '), ' {c} ')"
            for c in cls.split()
        ]
        return f"//{tag}[{' and '.join(parts)}]"

    def find_attribute(self):
        if not hasattr(self, "driver") or not self.driver:
            messagebox.showerror("Error", "กรุณาเปิด Chrome ก่อนใช้งาน find_attribute")
            return

        for tag_entry, cls_entry in self.action_blocks.get("find_attribute", []):
            tag_name  = tag_entry.get().strip()
            class_name = cls_entry.get().strip()

            xpath = self.build_xpath(tag_name, class_name)
            try:
                elements = self.driver.find_elements(By.XPATH, xpath)
                if not elements:
                    print(f"[find_attribute] ไม่พบ {xpath}")
                    continue
                for el in elements:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
                    self.driver.execute_script("arguments[0].style.border='2px solid red'", el)
            except Exception as e:
                print(f"[find_attribute] {e}")


    

    # ===== Execute =====

    def execute_all(self):
        if not hasattr(self, "driver") or not self.driver:
            messagebox.showerror("Error", "กรุณาเปิด Chrome ก่อนทำการ Execute")
            return

        if "find_text" in self.action_blocks:
            self.find_text()

        if "find_attribute" in self.action_blocks:
            self.find_attribute()

    # future: เพิ่ม block อื่นได้ที่นี่

        messagebox.showinfo("Success", "Executed all actions successfully!")





# ===== Run Application =====
if __name__ == "__main__":
    app = ttk.Window(themename="vapor")
    TabbedApp(app)
    app.mainloop()