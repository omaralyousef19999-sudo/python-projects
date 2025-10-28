# ... (الكود السابق للدوال العامة مثل hash_password, save_data, load_data يبقى كما هو)

# ============================================================
# 🔹 واجهة إدارة الحسابات
# ============================================================
class AccountManagerWindow(ctk.CTk):
    def __init__(self, lang="ar"):
        super().__init__()
        self.title("إدارة الحسابات" if lang == "ar" else "Account Manager")
        self.lang = lang
        self.data = load_data()
        self.accounts = self.data.get("accounts", [])

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.wm_geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

        try:
            self.background_image = ctk.CTkImage(dark_image=Image.open("background.png"), size=(window_width, window_height))
        except FileNotFoundError:
            messagebox.showwarning(
                "تحذير" if lang == "ar" else "Warning",
                "ملف الخلفية غير موجود." if lang == "ar" else "Background image not found."
            )
            self.background_image = None

        self.canvas = Canvas(self, width=window_width, height=window_height, bg="#1E1E1E" if not self.background_image else None)
        self.canvas.pack(fill="both", expand=True)
        if self.background_image:
            self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.main_frame,
            text="إدارة الحسابات" if lang == "ar" else "Manage Accounts",
            font=("Cairo" if lang == "ar" else "Arial", 24, "bold")
        ).pack(pady=15)

        self.account_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=8)
        self.account_frame.pack(pady=10, fill="both", expand=True)

        button_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        button_frame.pack(pady=10, fill="x", padx=10)

        lang_btn = ctk.CTkButton(
            button_frame,
            text="🇬🇧 English" if lang == "ar" else "🇸🇦 العربية",
            font=("Cairo" if lang == "ar" else "Arial", 12),
            command=self.toggle_language,
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8
        )
        lang_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        add_btn = ctk.CTkButton(
            button_frame,
            text="➕ إنشاء حساب جديد" if lang == "ar" else "➕ Create New Account",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.create_new_account,
            fg_color="#2E7D32",
            hover_color="#4CAF50",
            corner_radius=8
        )
        add_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        self.load_accounts()

    def load_accounts(self):
        for widget in self.account_frame.winfo_children():
            widget.destroy()

        for i, account in enumerate(self.accounts):
            row = ctk.CTkFrame(self.account_frame, corner_radius=5, fg_color="#424242")
            row.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(
                row,
                text=f"{i+1}. {account['teacher']} - {account['institute']}",
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                anchor="w" if self.lang == "ar" else "e"
            ).pack(side="left" if self.lang == "ar" else "right", padx=10, fill="x", expand=True)

            open_btn = ctk.CTkButton(
                row,
                text="📂 فتح" if self.lang == "ar" else "📂 Open",
                width=80,
                command=lambda acc=account: self.show_password_prompt(acc)
            )
            open_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

            delete_btn = ctk.CTkButton(
                row,
                text="🗑️ حذف" if self.lang == "ar" else "🗑️ Delete",
                width=80,
                fg_color="#D32F2F",
                hover_color="#F44336",
                command=lambda idx=i: self.delete_account(idx)
            )
            delete_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

    def toggle_language(self):
        new_lang = "en" if self.lang == "ar" else "ar"
        self.destroy()
        AccountManagerWindow(new_lang).mainloop()

    def create_new_account(self):
        self.destroy()
        CreateAccountWindow(self.lang).mainloop()

    def show_password_prompt(self, account):
        popup = ctk.CTkToplevel(self)
        popup.title("تأكيد كلمة المرور" if self.lang == "ar" else "Password Confirmation")
        popup.geometry("400x300")
        popup.transient(self)
        popup.grab_set()

        frame = ctk.CTkFrame(popup, corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(
            frame,
            text="أدخل كلمة المرور:" if self.lang == "ar" else "Enter Password:",
            font=("Cairo" if self.lang == "ar" else "Arial", 14)
        ).pack(pady=10)

        password_entry = ctk.CTkEntry(
            frame,
            show="*",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        password_entry.pack(pady=10, padx=20, fill="x")
        password_entry.focus_set()

        password_entry.bind("<Return>", lambda event: verify_password())

        show_password_switch = ctk.CTkSwitch(
            frame,
            text="إظهار كلمة المرور" if self.lang == "ar" else "Show Password",
            command=lambda: password_entry.configure(show="" if show_password_switch.get() else "*"),
            font=("Cairo" if self.lang == "ar" else "Arial", 12)
        )
        show_password_switch.pack(pady=10)

        def verify_password():
            entered_password = password_entry.get().strip()
            hashed_entered_password = hash_password(entered_password)
            if hashed_entered_password == account.get("password", ""):
                popup.destroy()
                # تأخير تدمير النافذة الأم حتى بعد فتح StudentWindow
                student_window = StudentWindow(account, self.lang)
                student_window.after(100, self.destroy)  # تأخير 100ms
                student_window.mainloop()
            else:
                messagebox.showerror(
                    "خطأ" if self.lang == "ar" else "Error",
                    "كلمة المرور غير صحيحة." if self.lang == "ar" else "Incorrect password."
                )

        verify_btn = ctk.CTkButton(
            frame,
            text="تحقق" if self.lang == "ar" else "Verify",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=verify_password,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        )
        verify_btn.pack(pady=10)

        cancel_btn = ctk.CTkButton(
            frame,
            text="إلغاء" if self.lang == "ar" else "Cancel",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=popup.destroy,
            fg_color="#D32F2F",
            hover_color="#F44336",
            corner_radius=8
        )
        cancel_btn.pack(pady=5)

        forgot_password_btn = ctk.CTkButton(
            frame,
            text="نسيت كلمة المرور؟" if self.lang == "ar" else "Forgot Password?",
            font=("Cairo" if self.lang == "ar" else "Arial", 12),
            command=lambda: self.show_forgot_password(account, popup),
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8
        )
        forgot_password_btn.pack(pady=10)

    def show_forgot_password(self, account, parent_popup):
        forgot_popup = ctk.CTkToplevel(self)
        forgot_popup.title("نسيت كلمة المرور" if self.lang == "ar" else "Forgot Password")
        forgot_popup.geometry("400x250")
        forgot_popup.transient(self)
        forgot_popup.grab_set()

        frame = ctk.CTkFrame(forgot_popup, corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(
            frame,
            text="أدخل بريدك الإلكتروني:" if self.lang == "ar" else "Enter your email:",
            font=("Cairo" if self.lang == "ar" else "Arial", 14)
        ).pack(pady=10)

        email_entry = ctk.CTkEntry(
            frame,
            placeholder_text="البريد الإلكتروني" if self.lang == "ar" else "Email",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        email_entry.pack(pady=10, padx=20, fill="x")
        email_entry.focus_set()

        def verify_email():
            entered_email = email_entry.get().strip()
            if entered_email == EMAIL:
                parent_popup.destroy()
                forgot_popup.destroy()
                messagebox.showinfo(
                    "تم" if self.lang == "ar" else "Success",
                    f"كلمة المرور الخاصة بك هي: {account.get('raw_password', 'غير متوفرة')}" if self.lang == "ar" else f"Your password is: {account.get('raw_password', 'Not available')}"
                )
            else:
                messagebox.showerror(
                    "خطأ" if self.lang == "ar" else "Error",
                    "البريد الإلكتروني غير صحيح." if self.lang == "ar" else "Incorrect email."
                )

        email_entry.bind("<Return>", lambda event: verify_email())

        verify_email_btn = ctk.CTkButton(
            frame,
            text="تحقق" if self.lang == "ar" else "Verify",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=verify_email,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        )
        verify_email_btn.pack(pady=15)

        cancel_email_btn = ctk.CTkButton(
            frame,
            text="إلغاء" if self.lang == "ar" else "Cancel",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=forgot_popup.destroy,
            fg_color="#D32F2F",
            hover_color="#F44336",
            corner_radius=8
        )
        cancel_email_btn.pack(pady=5)

    def delete_account(self, index):
        if messagebox.askyesno(
            "تأكيد" if self.lang == "ar" else "Confirm",
            "هل تريد حذف هذا الحساب؟" if self.lang == "ar" else "Do you want to delete this account?"
        ):
            del self.accounts[index]
            self.data["accounts"] = self.accounts
            save_data(self.data)
            self.load_accounts()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                "تم حذف الحساب بنجاح." if self.lang == "ar" else "Account deleted successfully."
            )
