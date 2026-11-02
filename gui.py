"""CustomTkinter desktop interface for CipherLab."""
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk
import customtkinter as ctk
from customtkinter.windows.widgets.core_rendering import DrawEngine
from encryption import caesar, rot13, fernet_cipher, atbash, vigenere, rail_fence


class CipherLab(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        # Vector rendering keeps borders smooth when the bundled shape font is unavailable.
        DrawEngine.preferred_drawing_method = "polygon_shapes"
        super().__init__()
        DrawEngine.preferred_drawing_method = "polygon_shapes"
        self.title("CipherLab · v1.0")
        self.geometry("800x550")
        self.minsize(680, 550)
        self.configure(fg_color="#080b12")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.algorithm = tk.StringVar(value="Caesar Cipher")
        self.mode = tk.StringVar(value="Encrypt")
        self.status = tk.StringVar(value="")
        self.pending = None
        panel = ctk.CTkFrame(self, fg_color="#101725", border_color="#343d4b",
                             border_width=1, corner_radius=22)
        panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(7, weight=1)
        header = ctk.CTkFrame(panel, fg_color="transparent", height=28)
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 10))
        icon = tk.Canvas(header, width=18, height=22, bg="#101725", highlightthickness=0)
        icon.pack(side="left", padx=(0, 7))
        icon.create_polygon(9, 3, 15, 6, 14, 13, 12, 16, 9, 18, 6, 16, 4, 13, 3, 6,
                            fill="", outline="#ad8bfa", width=1.5, smooth=True)
        icon.create_line(6, 10, 8, 12, 12, 8, fill="#ad8bfa", width=1.5)
        ctk.CTkLabel(header, text="CipherLab", font=("Segoe UI", 16, "bold"),
                     text_color="#e5e7eb").pack(side="left")
        ctk.CTkLabel(header, text="v1.0", width=36, height=21, corner_radius=10,
                     fg_color="#29313e", text_color="#e5e7eb", font=("Segoe UI", 12, "bold")).pack(side="right")
        ctk.CTkLabel(panel, text="Secure text encryption playground", height=20,
                     anchor="w", font=("Segoe UI", 12), text_color="#d4d4d8").grid(
                         row=1, column=0, sticky="ew", padx=18, pady=(0, 10))
        tabs = ctk.CTkFrame(panel, fg_color="transparent", height=32)
        tabs.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 12))
        tabs.grid_columnconfigure((0, 1), weight=1)
        self.tab_buttons = {}
        for column, name in enumerate(("Encrypt", "Decrypt")):
            button = ctk.CTkButton(tabs, text=name, height=36, corner_radius=18,
                font=("Segoe UI", 14, "bold"), hover_color="#2b303b",
                command=lambda mode=name: self.select_mode(mode))
            button.grid(row=0, column=column, sticky="ew")
            self.tab_buttons[name] = button
        ctk.CTkLabel(panel, text="Algorithm", anchor="w", height=20,
                     text_color="#bfc2c9", font=("Segoe UI", 14, "bold")).grid(
                         row=3, column=0, sticky="ew", padx=18, pady=(0, 4))
        selector = ctk.CTkFrame(panel, height=42, corner_radius=21,
            border_width=1, border_color="#3e4653", fg_color="#101725")
        selector.grid(row=4, column=0, sticky="ew", padx=18, pady=(0, 10))
        self.algorithm_menu = ctk.CTkOptionMenu(selector, values=["Caesar Cipher", "ROT13", "Vigenère", "Atbash", "Rail Fence", "Fernet"],
            variable=self.algorithm, command=self.settings_changed, dynamic_resizing=False,
            height=36, corner_radius=18, fg_color="#101725", button_color="#101725",
            button_hover_color="#222c3c", dropdown_fg_color="#182131",
            dropdown_hover_color="#293348", text_color="#e5e7eb", font=("Segoe UI", 14))
        self.algorithm_menu.pack(fill="x", padx=6, pady=3)
        options = ctk.CTkFrame(panel, fg_color="transparent")
        options.grid(row=5, column=0, sticky="ew", padx=18)
        options.grid_columnconfigure(0, weight=1)
        self.shift_frame = ctk.CTkFrame(options, fg_color="transparent", height=30)
        self.shift_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self.shift_label = ctk.CTkLabel(self.shift_frame, text="Shift amount", text_color="#bfc2c9",
                     font=("Segoe UI", 14, "bold"))
        self.shift_label.pack(side="left")
        self.plus = ctk.CTkButton(self.shift_frame, text="+", width=36, height=30,
            corner_radius=15, fg_color="transparent", border_width=1, border_color="#3e4653",
            hover_color="#222c3c", font=("Segoe UI", 18), command=lambda: self.step_shift(1))
        self.plus.pack(side="right")
        self.shift = ctk.CTkEntry(self.shift_frame, width=30, height=30, border_width=0,
            fg_color="#101725", justify="center", font=("Segoe UI", 14, "bold"))
        self.shift.insert(0, "3")
        self.shift.pack(side="right", padx=3)
        self.shift.bind("<KeyRelease>", self.invalidate)
        ctk.CTkButton(self.shift_frame, text="−", width=36, height=30, corner_radius=14,
            fg_color="transparent", border_width=1, border_color="#3e4653", hover_color="#222c3c",
            font=("Segoe UI", 18), command=lambda: self.step_shift(-1)).pack(side="right")
        self.keyword_frame = ctk.CTkFrame(options, fg_color="transparent")
        self.keyword_frame.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        self.keyword_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.keyword_frame, text="Keyword", text_color="#bfc2c9",
            font=("Segoe UI", 14, "bold")).grid(row=0, column=0, padx=(0, 16))
        self.keyword = ctk.CTkEntry(self.keyword_frame, height=32, border_width=1,
            border_color="#3e4653", fg_color="#101725", placeholder_text="English letters A–Z")
        self.keyword.grid(row=0, column=1, sticky="ew")
        self.keyword.insert(0, "LEMON")
        self.keyword.bind("<KeyRelease>", self.invalidate)
        self.keyword_frame.grid_remove()
        self.key_frame = ctk.CTkFrame(options, fg_color="transparent")
        self.key_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        self.key_frame.grid_columnconfigure(0, weight=1)
        self.key = ctk.CTkEntry(self.key_frame, placeholder_text="Fernet key — generate or load", show="•",
            height=32, fg_color="#101725", border_color="#3e4653", border_width=1)
        self.key.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0, 8))
        self.key.bind("<KeyRelease>", self.invalidate)
        for col, (label, action) in enumerate([("Generate key", self.generate_key), ("Load key", self.load_key),
                                               ("Save key", self.save_key), ("Show / hide", self.toggle_key)]):
            ctk.CTkButton(self.key_frame, text=label, width=100, height=28,
                fg_color="#242e3f", hover_color="#34425a", command=action).grid(row=1, column=col, padx=(0, 6))
        self.run_button = ctk.CTkButton(self.key_frame, text="Encrypt text", width=110, height=28,
            fg_color="#7155b0", hover_color="#8566c8", command=self.transform)
        self.run_button.grid(row=1, column=4)
        self.key_frame.grid_remove()
        ctk.CTkLabel(panel, text="Input text", height=20, anchor="w", text_color="#bfc2c9",
            font=("Segoe UI", 14, "bold")).grid(row=6, column=0, sticky="ew", padx=18, pady=(0, 4))
        self.input = ctk.CTkTextbox(panel, height=96, corner_radius=10, border_width=1,
            border_color="#3e4653", fg_color="#101725", text_color="#e5e7eb",
            font=("Segoe UI", 16), wrap="word")
        self.input.grid(row=7, column=0, sticky="nsew", padx=18, pady=(0, 12))
        self.input.insert("1.0", "Hello World!")
        self.input.bind("<KeyRelease>", self.invalidate)
        output_card = ctk.CTkFrame(panel, fg_color="#202b3a", corner_radius=14)
        output_card.grid(row=8, column=0, sticky="ew", padx=18, pady=(0, 8))
        output_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(output_card, text="Output", anchor="w", text_color="#bfc2c9",
            font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 0))
        copy_group = ctk.CTkFrame(output_card, fg_color="transparent")
        copy_group.grid(row=0, column=1, padx=12, pady=(8, 0))
        copy_icon = tk.Canvas(copy_group, width=18, height=20, bg="#202b3a", highlightthickness=0,
                              cursor="hand2")
        copy_icon.pack(side="left")
        copy_icon.create_rectangle(7, 3, 15, 12, outline="#c8cbd1", width=1)
        copy_icon.create_rectangle(3, 7, 11, 16, fill="#202b3a", outline="#c8cbd1", width=1)
        copy_icon.bind("<Button-1>", lambda event: self.copy())
        ctk.CTkButton(copy_group, text="Copy", width=48, height=28, fg_color="transparent",
            hover_color="#303d50", text_color="#c8cbd1", font=("Segoe UI", 14, "bold"),
            command=self.copy).pack(side="left")
        self.output = ctk.CTkTextbox(output_card, height=48, corner_radius=0, fg_color="#202b3a",
            text_color="#e5e7eb", font=("Segoe UI", 16), state="disabled", wrap="word")
        self.output.grid(row=1, column=0, columnspan=2, sticky="ew", padx=6, pady=(2, 8))
        self.notice = ctk.CTkLabel(panel, text="", anchor="w", justify="left", height=22,
            wraplength=730, text_color="#bfc2c9", font=("Segoe UI", 13))
        self.notice.grid(row=9, column=0, sticky="ew", padx=18, pady=(0, 8))
        self.status_label = ctk.CTkLabel(panel, textvariable=self.status, anchor="w", justify="left",
            wraplength=730, text_color="#bc9cf2", font=("Segoe UI", 12))
        self.status_label.grid(row=10, column=0, sticky="ew", padx=18, pady=(0, 8))
        self.status_label.grid_remove()
        self.bind("<Control-Return>", lambda event: self.transform())
        self.status.trace_add("write", self.show_status)
        panel.bind("<Configure>", self.resize_labels)
        self.settings_changed()

    def resize_labels(self, event):
        width = max(300, event.width - 36)
        self.notice.configure(wraplength=width)
        self.status_label.configure(wraplength=width)

    def show_status(self, *args):
        if self.status.get() and (self.algorithm.get() == "Fernet" or
                not self.status.get().startswith(("Encrypt complete", "Decrypt complete", "Ready"))):
            self.status_label.grid()
        else:
            self.status_label.grid_remove()

    def select_mode(self, mode):
        self.mode.set(mode)
        self.settings_changed()

    def step_shift(self, delta):
        try:
            value = int(self.shift.get()) + delta
        except ValueError:
            value = 3
        self.shift.delete(0, "end")
        self.shift.insert(0, str(value))
        self.invalidate()

    def set_output(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def invalidate(self, event=None):
        if self.pending is not None:
            self.after_cancel(self.pending)
            self.pending = None
        self.set_output("")
        self.status.set("")
        if self.algorithm.get() != "Fernet":
            self.pending = self.after(120, self.transform)

    def settings_changed(self, value=None):
        self.invalidate()
        self.run_button.configure(text=f"{self.mode.get()} text")
        for name, button in self.tab_buttons.items():
            button.configure(fg_color="#282637" if name == self.mode.get() else "transparent",
                             text_color="#e5dcff" if name == self.mode.get() else "#a6a7ad")
        self.shift_frame.grid_remove()
        self.key_frame.grid_remove()
        self.keyword_frame.grid_remove()
        if self.algorithm.get() in ("Caesar Cipher", "Rail Fence"):
            self.shift_label.configure(text="Rail count (2–100)" if self.algorithm.get() == "Rail Fence" else "Shift amount")
            self.shift_frame.grid()
        elif self.algorithm.get() == "Vigenère":
            self.keyword_frame.grid()
        elif self.algorithm.get() == "Fernet":
            self.key_frame.grid()
        self.notice.configure(text=("Fernet: пази ключа — без него текстът не може да бъде възстановен."
                                    if self.algorithm.get() == "Fernet" else
                                    "Интерактивна демонстрация с учебни алгоритми — не е подходяща за защита на поверителни данни."))
        # Preserve the user's window size when switching algorithms.
        if self.algorithm.get() == "Fernet" and self.winfo_height() < 630:
            self.geometry(f"{max(800, self.winfo_width())}x630")
        if self.algorithm.get() != "Fernet":
            self.transform()

    def transform(self):
        if self.pending is not None:
            self.after_cancel(self.pending)
            self.pending = None
        self.set_output("")
        text = self.input.get("1.0", "end-1c")
        try:
            operation = "encrypt" if self.mode.get() == "Encrypt" else "decrypt"
            algorithm = self.algorithm.get()
            if algorithm == "Caesar Cipher":
                try:
                    shift = int(self.shift.get())
                except ValueError:
                    raise ValueError("Shift amount must be a whole number.") from None
                result = getattr(caesar, operation)(text, shift)
            elif algorithm == "ROT13":
                result = getattr(rot13, operation)(text)
            elif algorithm == "Atbash":
                result = getattr(atbash, operation)(text)
            elif algorithm == "Vigenère":
                result = getattr(vigenere, operation)(text, self.keyword.get())
            elif algorithm == "Rail Fence":
                try:
                    rails = int(self.shift.get())
                except ValueError:
                    raise ValueError("Rail count must be a whole number between 2 and 100.") from None
                result = getattr(rail_fence, operation)(text, rails)
            else:
                result = getattr(fernet_cipher, operation)(text, self.key.get().strip())
            self.set_output(result)
            self.status.set(f"{self.mode.get()} complete · {len(result):,} characters")
        except ValueError as exc:
            self.status.set(str(exc))

    def copy(self):
        text = self.output.get("1.0", "end-1c")
        if not text:
            self.status.set("No output to copy.")
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status.set("Copied · Clipboard contents may be visible to other apps")
        except tk.TclError:
            self.status.set("Clipboard is unavailable.")

    def replace_key(self, key):
        self.key.delete(0, "end")
        self.key.insert(0, key)
        self.invalidate()

    def generate_key(self):
        if self.key.get() and not messagebox.askyesno("Replace key?", "Save your current key first. Replace it with a new key?", parent=self):
            return
        self.replace_key(fernet_cipher.generate_key())
        self.status.set("New key generated · Save it before closing the app")

    def toggle_key(self):
        self.key.configure(show="" if self.key.cget("show") else "•")

    def load_key(self):
        path = filedialog.askopenfilename(parent=self, title="Load Fernet key", filetypes=[("Key files", "*.key"), ("All files", "*.*")])
        if not path:
            return
        try:
            key = Path(path).read_text(encoding="ascii").strip()
            fernet_cipher.validate_key(key)
            self.replace_key(key)
            self.status.set("Key loaded")
        except (OSError, ValueError) as exc:
            self.status.set(f"Cannot load key: {exc}")

    def save_key(self):
        try:
            key = self.key.get().strip()
            fernet_cipher.validate_key(key)
            path = filedialog.asksaveasfilename(parent=self, title="Save secret key", defaultextension=".key", filetypes=[("Key files", "*.key")])
            if path:
                Path(path).write_text(key, encoding="ascii")
                self.status.set("Key saved as plaintext · Store it separately from encrypted text")
        except (OSError, ValueError) as exc:
            self.status.set(f"Cannot save key: {exc}")
