"""
Wilma Kurssivalitsin — portable GUI-sovellus kurssien automaattiseen valintaan
Selenium 4.6+ hakee ChromeDriverin automaattisesti, ei erillistä asennusta!
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os
import sys
import threading

# ── Asetustiedosto tallennetaan EXEn viereen (tai .py-tiedoston viereen) ────
def get_base_dir():
    # PyInstaller pakkauksessa käytetään sys.executable hakemistoa
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

SETTINGS_FILE = os.path.join(get_base_dir(), "wilma_settings.json")
DEFAULT_URL    = "https://helsinki.inschool.fi/!02716814/selection/view?"
PERIOD_KEYS    = ["periodi_1", "periodi_2", "periodi_3", "periodi_4", "periodi_5"]
PERIOD_LABELS  = ["1. Periodi", "2. Periodi", "3. Periodi", "4. Periodi", "5. Periodi"]
PERIOD_NAV_TEXTS = [
    "1. periodi",
    "2. periodi",
    "3. periodi",
    "4. periodi",
    "5. periodi",
]

# ── Värit ────────────────────────────────────────────────────────────────────
BG      = "#0f1117"
CARD    = "#21253a"
ACCENT  = "#4f8ef7"
ACCENT2 = "#7c3aed"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER  = "#ef4444"
TEXT    = "#e8eaf6"
SUBTEXT = "#8892b0"
BORDER  = "#2d3258"

FONT_TITLE = ("Georgia", 22, "bold")
FONT_HEAD  = ("Georgia", 13, "bold")
FONT_LABEL = ("Courier New", 10)
FONT_ENTRY = ("Courier New", 11)
FONT_BTN   = ("Courier New", 11, "bold")
FONT_LOG   = ("Courier New", 9)


# ── Asetukset ────────────────────────────────────────────────────────────────
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"email": "", "password": "", "url": DEFAULT_URL,
            "periodi_1": "", "periodi_2": "", "periodi_3": "",
            "periodi_4": "", "periodi_5": ""}

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── Selenium-automatisointi ──────────────────────────────────────────────────
def run_automation(settings, log_fn):
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time
    except ImportError:
        log_fn("❌ VIRHE: selenium-kirjasto puuttuu!", "error")
        return

    course_lists = []
    for key in PERIOD_KEYS:
        raw = settings.get(key, "")
        codes = [c.strip() for c in raw.replace("\n", ",").split(",") if c.strip()]
        course_lists.append(codes)

    log_fn("🚀 Käynnistetään Chrome...", "info")
    log_fn("   (Ensimmäisellä kerralla voi kestää hetki — ladataan ChromeDriver)", "info")

    try:
        options = Options()
        options.add_argument("--start-maximized")
        # Selenium Manager hakee automaattisesti oikean ChromeDriverin
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        log_fn(f"❌ Chromen käynnistys epäonnistui: {e}", "error")
        log_fn("   Varmista että Google Chrome on asennettuna.", "warn")
        return

    wait = WebDriverWait(driver, 10)

    try:
        driver.get(settings["url"])
        log_fn("🌐 Avataan Wilma...", "info")

        wait.until(EC.presence_of_element_located((By.ID, "login-frontdoor")))
        driver.find_element(By.ID, "login-frontdoor").send_keys(settings["email"] + Keys.ENTER)
        log_fn("📧 Sähköposti syötetty", "info")

        wait.until(EC.presence_of_element_located((By.ID, "password")))
        driver.find_element(By.ID, "password").send_keys(settings["password"] + Keys.ENTER)
        log_fn("🔑 Salasana syötetty", "info")

        wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "periodi")))
        try:
            driver.find_element(By.ID, "tray-selection-on-first-click").click()
            log_fn("⚡ Pikavalinta aktivoitu", "info")
        except Exception:
            log_fn("⚠️  Pikavalintanappia ei löytynyt — jatketaan silti", "warn")

        for nav_text, codes, label in zip(PERIOD_NAV_TEXTS, course_lists, PERIOD_LABELS):
            if not codes:
                log_fn(f"⏭  {label}: ei kursseja, ohitetaan", "warn")
                continue

            log_fn(f"\n📅 {label} — valitaan {len(codes)} kurssia", "head")
            try:
                period_btn = wait.until(EC.presence_of_element_located(
                    (By.PARTIAL_LINK_TEXT, nav_text)
                ))
                period_btn.click()
                time.sleep(0.6)

                for code in codes:
                    found = False
                    # Yritys 1: XPATH tekstin/titlen perusteella
                    try:
                        el = wait.until(EC.presence_of_element_located((By.XPATH,
                            f"//*[contains(@class,'course') and (contains(text(),'{code}') "
                            f"or contains(@title,'{code}')) or text()='{code}']"
                        )))
                        el.click()
                        log_fn(f"  ✓ {code}", "ok")
                        found = True
                    except Exception:
                        pass

                    # Yritys 2: linkkiteksti
                    if not found:
                        try:
                            driver.find_element(By.PARTIAL_LINK_TEXT, code).click()
                            log_fn(f"  ✓ {code} (linkkihaku)", "ok")
                            found = True
                        except Exception:
                            pass

                    if not found:
                        log_fn(f"  ✗ {code} — ei löytynyt", "error")

                    time.sleep(0.15)

                period_btn.click()
                log_fn(f"  📁 {label} suljettu", "info")
                time.sleep(0.5)

            except Exception as e:
                log_fn(f"  ❌ {label} virhe: {e}", "error")

        log_fn("\n✅ Valmis! Ikkuna suljetaan 8 sekunnin kuluttua.", "ok")
        time.sleep(8)

    except Exception as e:
        log_fn(f"\n❌ Kriittinen virhe: {e}", "error")
    finally:
        driver.quit()
        log_fn("🔒 Chrome suljettu.", "info")


# ── GUI ──────────────────────────────────────────────────────────────────────
class WilmaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wilma Kurssivalitsin")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.settings = load_settings()
        self._build_ui()
        self._load_into_fields()
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{(self.winfo_screenwidth()-w)//2}+{(self.winfo_screenheight()-h)//2}")

    def _build_ui(self):
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=30, pady=(28, 0))
        tk.Label(hdr, text="WILMA", font=FONT_TITLE, fg=ACCENT, bg=BG).pack(side="left")
        tk.Label(hdr, text=" kurssivalitsin", font=("Georgia", 16), fg=SUBTEXT, bg=BG).pack(side="left", pady=(6,0))

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=30, pady=14)

        body = tk.Frame(self, bg=BG)
        body.pack(padx=30, pady=0, fill="both")

        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="y", padx=(0, 24))

        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        self._section(left, "🔐 Kirjautumistiedot")
        self.email_var = tk.StringVar()
        self._field(left, "Sähköposti", self.email_var)
        self.pass_var = tk.StringVar()
        self._field(left, "Salasana", self.pass_var, show="●")
        self.url_var = tk.StringVar()
        self._field(left, "Wilma-URL", self.url_var, width=36)

        tk.Frame(left, bg=BG, height=12).pack()

        self.run_btn = tk.Button(
            left, text="▶  KÄYNNISTÄ VALINTA", font=FONT_BTN,
            bg=ACCENT, fg="white", activebackground=ACCENT2, activeforeground="white",
            relief="flat", cursor="hand2", padx=16, pady=10,
            command=self._start
        )
        self.run_btn.pack(fill="x", pady=(4, 6))

        tk.Button(
            left, text="💾  Tallenna asetukset", font=FONT_LABEL,
            bg=CARD, fg=SUBTEXT, activebackground=BORDER, activeforeground=TEXT,
            relief="flat", cursor="hand2", padx=10, pady=6,
            command=self._save
        ).pack(fill="x")

        tk.Frame(left, bg=BG, height=10).pack()

        tk.Label(left,
            text="💡 Kurssikoodit pilkuilla tai\n   riveittäin, esim:\n   BIO1.i, MAA05.1\n   ENA01.+ENA02.g",
            font=("Courier New", 9), fg=SUBTEXT, bg=BG, justify="left"
        ).pack(anchor="w")

        self._section(right, "📅 Valittavat kurssit")
        self.period_texts = []
        for label in PERIOD_LABELS:
            row = tk.Frame(right, bg=BG)
            row.pack(fill="x", pady=(0, 10))
            tk.Label(row, text=label, font=FONT_HEAD, fg=TEXT, bg=BG).pack(anchor="w")
            t = tk.Text(row, height=4, width=52,
                        font=FONT_ENTRY, bg=CARD, fg=TEXT,
                        insertbackground=ACCENT, relief="flat", bd=0,
                        padx=8, pady=6, highlightthickness=1,
                        highlightbackground=BORDER, highlightcolor=ACCENT)
            t.pack(fill="x")
            self.period_texts.append(t)

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=30, pady=(14, 0))

        log_frame = tk.Frame(self, bg=BG)
        log_frame.pack(padx=30, pady=(10, 20), fill="both")

        tk.Label(log_frame, text="📋 Loki", font=FONT_HEAD, fg=SUBTEXT, bg=BG).pack(anchor="w")
        self.log = scrolledtext.ScrolledText(
            log_frame, height=8, font=FONT_LOG,
            bg="#0a0c14", fg=TEXT, insertbackground=ACCENT,
            relief="flat", bd=0, padx=8, pady=6,
            highlightthickness=1, highlightbackground=BORDER, state="disabled"
        )
        self.log.pack(fill="both")
        self.log.tag_config("ok",    foreground=SUCCESS)
        self.log.tag_config("error", foreground=DANGER)
        self.log.tag_config("warn",  foreground=WARNING)
        self.log.tag_config("info",  foreground=TEXT)
        self.log.tag_config("head",  foreground=ACCENT)

    def _section(self, parent, text):
        tk.Label(parent, text=text, font=FONT_HEAD, fg=ACCENT, bg=BG).pack(anchor="w", pady=(0, 8))

    def _field(self, parent, label, var, show=None, width=28):
        tk.Label(parent, text=label, font=FONT_LABEL, fg=SUBTEXT, bg=BG).pack(anchor="w")
        kw = dict(textvariable=var, font=FONT_ENTRY, bg=CARD, fg=TEXT,
                  insertbackground=ACCENT, relief="flat", bd=0,
                  highlightthickness=1, highlightbackground=BORDER,
                  highlightcolor=ACCENT, width=width)
        if show:
            kw["show"] = show
        tk.Entry(parent, **kw).pack(fill="x", pady=(2, 10), ipady=6)

    def _load_into_fields(self):
        self.email_var.set(self.settings.get("email", ""))
        self.pass_var.set(self.settings.get("password", ""))
        self.url_var.set(self.settings.get("url", DEFAULT_URL))
        for t, key in zip(self.period_texts, PERIOD_KEYS):
            t.delete("1.0", "end")
            t.insert("1.0", self.settings.get(key, ""))

    def _collect_settings(self):
        d = {
            "email": self.email_var.get().strip(),
            "password": self.pass_var.get(),
            "url": self.url_var.get().strip() or DEFAULT_URL,
        }
        for key, t in zip(PERIOD_KEYS, self.period_texts):
            d[key] = t.get("1.0", "end-1c").strip()
        return d

    def _save(self):
        self.settings = self._collect_settings()
        save_settings(self.settings)
        self._log("💾 Asetukset tallennettu.", "ok")

    def _start(self):
        self.settings = self._collect_settings()
        save_settings(self.settings)
        if not self.settings["email"] or not self.settings["password"]:
            messagebox.showwarning("Puuttuvat tiedot", "Syötä sähköposti ja salasana!")
            return
        self.run_btn.config(state="disabled", text="⏳  Käynnissä...")
        self._log("─" * 40, "info")

        def job():
            run_automation(self.settings, self._log)
            self.after(0, lambda: self.run_btn.config(state="normal", text="▶  KÄYNNISTÄ VALINTA"))

        threading.Thread(target=job, daemon=True).start()

    def _log(self, msg, tag="info"):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")


if __name__ == "__main__":
    app = WilmaApp()
    app.mainloop()
