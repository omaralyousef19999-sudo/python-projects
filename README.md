# ============================================================
# 🔹 واجهة إدارة الطلاب
# ============================================================
class StudentWindow(ctk.CTk):
    def __init__(self, account, lang="ar", mode="dark"):
        super().__init__()
        ctk.set_appearance_mode(mode)
        self.account = account
        self.lang = lang
        self.mode = mode
        self.title("إدارة الطلاب" if lang == "ar" else "Manage Students")

        # إعداد حجم الشاشة
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.wm_geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

        # الإطار الرئيسي
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#2C3E50" if mode == "dark" else "#ECF0F1")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # عنوان المعهد
        ctk.CTkLabel(
            self.main_frame,
            text=f"المعهد: {account['institute']}" if lang == "ar" else f"Institute: {account['institute']}",
            font=("Cairo" if lang == "ar" else "Arial", 22, "bold"),
            text_color="#FFFFFF" if mode == "dark" else "#2C3E50"
        ).pack(pady=15)

        # إطار البحث
        search_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        search_frame.pack(pady=10, fill="x")

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="ابحث عن طالب..." if lang == "ar" else "Search for a student...",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            corner_radius=10,
            height=40
        )
        self.search_entry.pack(side="right" if lang == "ar" else "left", fill="x", expand=True, padx=10)

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 بحث" if lang == "ar" else "🔍 Search",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.filter_students,
            fg_color="#3498DB",
            hover_color="#2980B9",
            corner_radius=10
        )
        search_btn.pack(side="right" if lang == "ar" else "left", padx=10)

        # إطار الجدول
        self.table_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=10)
        self.table_frame.pack(pady=10, fill="both", expand=True)

        # إعداد الرأس
        header_frame = ctk.CTkFrame(self.table_frame, corner_radius=10, fg_color="#34495E" if mode == "dark" else "#BDC3C7")
        header_frame.pack(fill="x")
        headers = [
            ("رقم" if lang == "ar" else "No.", 50),
            ("الاسم" if lang == "ar" else "Name", 200),
            ("المجموع" if lang == "ar" else "Total", 100),
            ("علامة اليوم" if lang == "ar" else "Daily Grade", 120),
            ("إجراءات" if lang == "ar" else "Actions", 100)
        ]
        for col, (text, width) in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=text,
                font=("Cairo" if lang == "ar" else "Arial", 14, "bold"),
                width=width,
                text_color="#FFFFFF" if mode == "dark" else "#2C3E50",
                anchor="e" if lang == "ar" else "w"
            ).pack(side="right" if lang == "ar" else "left", padx=5)

        # إطار الأزرار
        action_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        action_frame.pack(pady=10, fill="x")

        self.student_entry = ctk.CTkEntry(
            action_frame,
            placeholder_text="اسم الطالب" if lang == "ar" else "Student Name",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            corner_radius=10,
            height=40
        )
        self.student_entry.pack(side="right" if lang == "ar" else "left", fill="x", expand=True, padx=10)

        add_btn = ctk.CTkButton(
            action_frame,
            text="➕ إضافة" if lang == "ar" else "➕ Add",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.add_student,
            fg_color="#2ECC71",
            hover_color="#27AE60",
            corner_radius=10
        )
        add_btn.pack(side="left" if lang == "ar" else "right", padx=5)

        remove_btn = ctk.CTkButton(
            action_frame,
            text="🗑️ حذف" if lang == "ar" else "🗑️ Remove",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.remove_student,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            corner_radius=10
        )
        remove_btn.pack(side="left" if lang == "ar" else "right", padx=5)

        save_grades_btn = ctk.CTkButton(
            action_frame,
            text="💾 حفظ العلامات" if lang == "ar" else "💾 Save Grades",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.save_daily_grades,
            fg_color="#8E44AD",
            hover_color="#6C3483",
            corner_radius=10
        )
        save_grades_btn.pack(side="left" if lang == "ar" else "right", padx=5)

        # زر الرجوع
        back_btn = ctk.CTkButton(
            self.main_frame,
            text="⬅️ رجوع" if lang == "ar" else "⬅️ Back",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.back_to_manager,
            fg_color="#3498DB",
            hover_color="#2980B9",
            corner_radius=10
        )
        back_btn.pack(pady=10)

        self.load_students()

    def load_students(self, students=None):
        for widget in self.table_frame.winfo_children()[1:]:
            widget.destroy()

        students = students or self.account["students"]
        sorted_students = sorted(students, key=lambda x: sum(g["grade"] for g in x.get("grades", [])), reverse=True)
        self.grade_entries = {}  # لتخزين حقول إدخال العلامات

        for i, student in enumerate(sorted_students):
            total = sum(g["grade"] for g in student.get("grades", []))
            today_grade = next((g["grade"] for g in student.get("grades", []) if g["date"] == datetime.now().strftime("%Y-%m-%d")), 0)

            row = ctk.CTkFrame(self.table_frame, corner_radius=8, fg_color="#34495E" if self.mode == "dark" else "#D5DBDB")
            row.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(
                row,
                text=str(i+1),
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=50,
                anchor="e" if self.lang == "ar" else "w",
                text_color="#FFFFFF" if self.mode == "dark" else "#2C3E50"
            ).pack(side="right" if lang == "ar" else "left", padx=5)

            ctk.CTkLabel(
                row,
                text=student["name"],
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=200,
                anchor="e" if self.lang == "ar" else "w",
                text_color="#FFFFFF" if self.mode == "dark" else "#2C3E50"
            ).pack(side="right" if self.lang == "ar" else "left", padx=5)

            ctk.CTkLabel(
                row,
                text=str(total),
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=100,
                anchor="e" if self.lang == "ar" else "w",
                text_color="#FFFFFF" if self.mode == "dark" else "#2C3E50"
            ).pack(side="right" if self.lang == "ar" else "left", padx=5)

            grade_entry = ctk.CTkEntry(
                row,
                placeholder_text=str(today_grade) if today_grade else ("علامة اليوم" if lang == "ar" else "Daily Grade"),
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=120,
                corner_radius=8
            )
            grade_entry.pack(side="right" if lang == "ar" else "left", padx=5)
            self.grade_entries[student["name"]] = grade_entry

            edit_btn = ctk.CTkButton(
                row,
                text="✏️ تعديل" if lang == "ar" else "✏️ Edit",
                font=("Cairo" if lang == "ar" else "Arial", 14),
                command=lambda s=student: self.edit_student(s),
                fg_color="#3498DB",
                hover_color="#2980B9",
                corner_radius=8,
                width=100
            )
            edit_btn.pack(side="right" if lang == "ar" else "left", padx=5)

    def filter_students(self):
        search_term = self.search_entry.get().strip().lower()
        filtered_students = [
            s for s in self.account["students"]
            if search_term in s["name"].lower()
        ]
        self.load_students(filtered_students if search_term else self.account["students"])

    def add_student(self):
        name = self.student_entry.get().strip()
        if name and re.match(r"^[a-zA-Z\sأ-ي]+$", name):
            if any(s["name"] == name for s in self.account["students"]):
                messagebox.showerror(
                    "خطأ" if self.lang == "ar" else "Error",
                    "اسم الطالب موجود بالفعل." if self.lang == "ar" else "Student name already exists."
                )
                return
            self.account["students"].append({"name": name, "grades": [], "info": ""})
            self.student_entry.delete(0, "end")
            self.load_students()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                f"تم إضافة الطالب {name} بنجاح." if self.lang == "ar" else f"Student {name} added successfully."
            )
        elif name:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "الاسم يجب أن يحتوي على حروف فقط." if self.lang == "ar" else "Name must contain letters only."
            )

    def remove_student(self):
        name = self.student_entry.get().strip()
        if name and any(s["name"] == name for s in self.account["students"]):
            self.account["students"] = [s for s in self.account["students"] if s["name"] != name]
            self.student_entry.delete(0, "end")
            self.load_students()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                f"تم حذف الطالب {name} بنجاح." if self.lang == "ar" else f"Student {name} removed successfully."
            )
        elif name:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "اسم الطالب غير موجود." if self.lang == "ar" else "Student name not found."
            )

    def save_daily_grades(self):
        today = datetime.now().strftime("%Y-%m-%d")
        full_data = load_data()
        total_grades = 0
        updated = False

        for acc in full_data["accounts"]:
            if acc["institute"] == self.account["institute"] and acc["teacher"] == self.account["teacher"]:
                for student in acc["students"]:
                    if student["name"] in self.grade_entries:
                        grade_text = self.grade_entries[student["name"]].get().strip()
                        if grade_text and grade_text.isdigit():
                            grade = int(grade_text)
                            if 0 <= grade <= MAX_GRADES:
                                # تحديث العلامة اليومية
                                existing_grade = next((g for g in student["grades"] if g["date"] == today), None)
                                if existing_grade:
                                    existing_grade["grade"] = grade
                                else:
                                    student["grades"].append({"grade": grade, "date": today, "reason": ""})
                                total_grades += grade
                                updated = True
                break

        if updated:
            save_data(full_data)
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                f"تم حفظ العلامات بنجاح ✅\nإجمالي العلامات اليوم: {total_grades}" if self.lang == "ar" else f"Grades saved successfully ✅\nTotal grades today: {total_grades}"
            )
            self.load_students()
        else:
            messagebox.showwarning(
                "تحذير" if self.lang == "ar" else "Warning",
                "لا توجد علامات للحفظ." if self.lang == "ar" else "No grades to save."
            )

    def edit_student(self, student):
        popup = ctk.CTkToplevel(self)
        popup.title(f"تعديل بيانات {student['name']}" if self.lang == "ar" else f"Edit {student['name']} Data")
        popup.geometry("400x300")
        popup.transient(self)
        popup.grab_set()

        frame = ctk.CTkFrame(popup, corner_radius=10)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="اسم الطالب:", font=("Cairo" if self.lang == "ar" else "Arial", 14)).pack(pady=5)
        name_entry = ctk.CTkEntry(frame, font=("Cairo" if self.lang == "ar" else "Arial", 14), corner_radius=8)
        name_entry.insert(0, student["name"])
        name_entry.pack(pady=10, side="right" if self.lang == "ar" else "left")

        ctk.CTkLabel(frame, text="ملاحظات:", font=("Cairo" if self.lang == "ar" else "Arial", 14)).pack(pady=5)
        info_entry = ctk.CTkTextbox(frame, font=("Cairo" if self.lang == "ar" else "Arial", 14), corner_radius=8, height=100)
        info_entry.insert("end", student.get("info", ""))
        info_entry.pack(pady=10, side="right" if self.lang == "ar" else "left")

        def save_changes():
            new_name = name_entry.get().strip()
            if new_name and re.match(r"^[a-zA-Z\sأ-ي]+$", new_name):
                student["name"] = new_name
                student["info"] = info_entry.get("1.0", "end").strip()
                self.load_students()
                popup.destroy()
                messagebox.showinfo(
                    "تم" if self.lang == "ar" else "Success",
                    "تم حفظ التغييرات بنجاح ✅" if self.lang == "ar" else "Changes saved successfully ✅"
                )
            else:
                messagebox.showerror(
                    "خطأ" if self.lang == "ar" else "Error",
                    "اسم الطالب غير صالح." if self.lang == "ar" else "Invalid student name."
                )

        ctk.CTkButton(
            frame,
            text="💾 حفظ" if lang == "ar" else "💾 Save",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=save_changes,
            fg_color="#8E44AD",
            hover_color="#6C3483",
            corner_radius=10
        ).pack(pady=15, side="left" if self.lang == "ar" else "right")

    def back_to_manager(self):
        self.destroy()
        AccountManagerWindow(self.lang, self.mode).mainloop()
