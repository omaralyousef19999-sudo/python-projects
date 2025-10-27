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

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.wm_geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            self.main_frame,
            text=f"المعهد: {account['institute']}" if lang == "ar" else f"Institute: {account['institute']}",
            font=("Cairo" if lang == "ar" else "Arial", 24, "bold")
        ).pack(pady=15)

        search_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        search_frame.pack(pady=10, padx=40, fill="x")

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="ابحث عن طالب..." if lang == "ar" else "Search for a student...",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        self.search_entry.pack(side="right" if lang == "ar" else "left", fill="x", expand=True, padx=5)

        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 بحث" if lang == "ar" else "🔍 Search",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.filter_students,
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8,
            width=100
        )
        search_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        self.stats_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color="#37474F")
        self.stats_frame.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(
            self.stats_frame,
            text="📈 الإحصائيات" if lang == "ar" else "📈 Statistics",
            font=("Cairo" if lang == "ar" else "Arial", 16, "bold")
        ).pack(pady=5)

        self.stats_labels = {
            "count": ctk.CTkLabel(self.stats_frame, text="", font=("Cairo" if lang == "ar" else "Arial", 14)),
            "avg": ctk.CTkLabel(self.stats_frame, text="", font=("Cairo" if lang == "ar" else "Arial", 14)),
            "max": ctk.CTkLabel(self.stats_frame, text="", font=("Cairo" if lang == "ar" else "Arial", 14)),
            "min": ctk.CTkLabel(self.stats_frame, text="", font=("Cairo" if lang == "ar" else "Arial", 14)),
            "above_90": ctk.CTkLabel(self.stats_frame, text="", font=("Cairo" if lang == "ar" else "Arial", 14))
        }
        for label in self.stats_labels.values():
            label.pack(pady=2, anchor="w" if lang == "ar" else "e")

        student_input_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        student_input_frame.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(
            student_input_frame,
            text="إضافة طالب" if self.lang == "ar" else "Add Student",
            font=("Cairo" if self.lang == "ar" else "Arial", 16, "bold")
        ).pack(pady=5)

        self.student_entry = ctk.CTkEntry(
            student_input_frame,
            placeholder_text="اسم الطالب" if lang == "ar" else "Student Name",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        self.student_entry.pack(side="left" if self.lang == "ar" else "right", padx=5, fill="x", expand=True)
        self.student_entry.bind("<Return>", lambda event: self.add_student())

        add_btn = ctk.CTkButton(
            student_input_frame,
            text="➕ إضافة" if self.lang == "ar" else "➕ Add",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.add_student,
            fg_color="#2E7D32",
            hover_color="#4CAF50",
            corner_radius=8
        )
        add_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

        remove_btn = ctk.CTkButton(
            student_input_frame,
            text="🗑️ حذف" if self.lang == "ar" else "🗑️ Remove",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=self.remove_student,
            fg_color="#D32F2F",
            hover_color="#F44336",
            corner_radius=8
        )
        remove_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

        save_btn = ctk.CTkButton(
            student_input_frame,
            text="💾 حفظ" if self.lang == "ar" else "💾 Save",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=self.save_students,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        )
        save_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

        button_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        button_frame.pack(pady=10, fill="x")

        export_btn = ctk.CTkButton(
            button_frame,
            text="📊 تصدير إلى Excel" if lang == "ar" else "📊 Export to Excel",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.export_to_excel,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        )
        export_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        restart_btn = ctk.CTkButton(
            button_frame,
            text="🔄 إعادة بدء" if lang == "ar" else "🔄 Restart",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.restart_students,
            fg_color="#D32F2F",
            hover_color="#F44336",
            corner_radius=8
        )
        restart_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        return_btn = ctk.CTkButton(
            button_frame,
            text="⬅️ رجوع إلى إدارة الحسابات" if lang == "ar" else "⬅️ Back to Account Manager",
            font=("Cairo" if lang == "ar" else "Arial", 14),
            command=self.back_to_manager,
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8
        )
        return_btn.pack(side="right" if lang == "ar" else "left", padx=5)

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

        mode_btn = ctk.CTkButton(
            button_frame,
            text="☀️ الوضع النهاري" if lang == "ar" and mode == "dark" else "🌙 الوضع الليلي" if lang == "ar" and mode == "light" else "☀️ Light Mode" if mode == "dark" else "🌙 Dark Mode",
            font=("Cairo" if lang == "ar" else "Arial", 12),
            command=self.toggle_mode,
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8
        )
        mode_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        self.table_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=8, width=window_width - 100)
        self.table_frame.pack(pady=10, fill="both", expand=True)

        # إعداد الرأس باستخدام grid
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="#37474F")
        header_frame.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        header_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        headers = [
            ("رقم" if self.lang == "ar" else "No.", 50),
            ("الاسم" if self.lang == "ar" else "Name", 200),
            ("المجموع" if self.lang == "ar" else "Total", 100),
            ("ملاحظات" if self.lang == "ar" else "Notes", 300),
            ("إجراءات" if self.lang == "ar" else "Actions", 100)
        ]

        for col, (text, width) in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=text,
                font=("Cairo" if self.lang == "ar" else "Arial", 14, "bold"),
                width=width
            ).grid(row=0, column=col, padx=5, sticky="ew")

        self.load_students()

    def update_stats(self):
        students = self.account["students"]
        count = len(students)
        totals = [sum(g["grade"] for g in s.get("grades", [])) for s in students]
        avg = sum(totals) / count if count > 0 else 0
        max_grade = max(totals) if totals else 0
        min_grade = min(totals) if totals else 0
        above_90 = sum(1 for t in totals if (t / MAX_GRADES) * 100 >= 90) if totals else 0

        max_students = [s["name"] for s in students if sum(g["grade"] for g in s.get("grades", [])) == max_grade]
        min_students = [s["name"] for s in students if sum(g["grade"] for g in s.get("grades", [])) == min_grade]

        stats_text = {
            "count": f"عدد الطلاب: {count}" if self.lang == "ar" else f"Number of Students: {count}",
            "avg": f"متوسط العلامات: {avg:.2f}" if self.lang == "ar" else f"Average Grade: {avg:.2f}",
            "max": f"أعلى درجة: {max_grade} ({', '.join(max_students)})" if self.lang == "ar" else f"Highest Grade: {max_grade} ({', '.join(max_students)})",
            "min": f"أدنى درجة: {min_grade} ({', '.join(min_students)})" if self.lang == "ar" else f"Lowest Grade: {min_grade} ({', '.join(min_students)})",
            "above_90": f"الطلاب فوق 90%: {above_90}" if self.lang == "ar" else f"Students above 90%: {above_90}"
        }

        for key, label in self.stats_labels.items():
            label.configure(text=stats_text[key])

    def toggle_language(self):
        new_lang = "en" if self.lang == "ar" else "ar"
        self.destroy()
        StudentWindow(self.account, new_lang, self.mode).mainloop()

    def toggle_mode(self):
        new_mode = "light" if self.mode == "dark" else "dark"
        self.destroy()
        StudentWindow(self.account, self.lang, new_mode).mainloop()

    def filter_students(self):
        search_term = self.search_entry.get().strip().lower()
        filtered_students = [
            s for s in self.account["students"]
            if search_term in s["name"].lower()
        ]
        self.load_students(filtered_students if search_term else self.account["students"])

    def load_students(self, students=None):
        for widget in self.table_frame.winfo_children()[1:]:
            widget.destroy()

        students = students or self.account["students"]
        sorted_students = sorted(students, key=lambda x: sum(g["grade"] for g in x.get("grades", [])), reverse=True)

        self.table_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        for i, student in enumerate(sorted_students):
            total = sum(g["grade"] for g in student.get("grades", []))
            row = ctk.CTkFrame(self.table_frame, corner_radius=5, fg_color="#424242")
            row.grid(row=i+1, column=0, sticky="ew", pady=2, padx=5)
            row.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            rank_icon = ""
            if i == 0 and len(sorted_students) >= 1:
                rank_icon = "🥇"
            elif i == 1 and len(sorted_students) >= 2:
                rank_icon = "🥈"
            elif i == 2 and len(sorted_students) >= 3:
                rank_icon = "🥉"
            elif i == len(sorted_students) - 1 and len(sorted_students) >= 1:
                rank_icon = "🦓"

            ctk.CTkLabel(
                row,
                text=str(i+1),
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=50
            ).grid(row=0, column=0, padx=5, sticky="ew")

            name_label = ctk.CTkLabel(
                row,
                text=f"{rank_icon} {student['name']}" if rank_icon else student["name"],
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=200,
                anchor="w" if self.lang == "ar" else "e"
            )
            name_label.grid(row=0, column=1, padx=5, sticky="ew")
            if rank_icon == "🥇":
                name_label.configure(cursor="hand2")
                name_label.bind("<Button-1>", lambda e: show_fireworks(self, self.lang))

            ctk.CTkLabel(
                row,
                text=str(total),
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=100
            ).grid(row=0, column=2, padx=5, sticky="ew")

            ctk.CTkLabel(
                row,
                text=student.get("info", "")[:30] + ("..." if len(student.get("info", "")) > 30 else ""),
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=300,
                anchor="w" if self.lang == "ar" else "e"
            ).grid(row=0, column=3, padx=5, sticky="ew")

            ctk.CTkButton(
                row,
                text="✏️ تعديل" if self.lang == "ar" else "✏️ Edit",
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                width=100,
                command=lambda s=student: self.edit_student(s),
                fg_color="#0288D1",
                hover_color="#03A9F4",
                corner_radius=8
            ).grid(row=0, column=4, padx=5, sticky="ew")

        self.update_stats()

    def add_student(self):
        name = self.student_entry.get().strip()
        if name and re.match(r"^[a-zA-Z\sأ-ي]+$", name):
            if any(s["name"] == name for s in self.account["students"]):
                messagebox.showerror(
                    "خطأ" if self.lang == "ar" else "Error",
                    "اسم الطالب موجود بالفعل." if self.lang == "ar" else "Student name already exists."
                )
                return
            self.account["students"].append({"name": name, "grades": [], "info": "", "attendance": []})
            self.student_entry.delete(0, "end")
            self.load_students()
            self.update_stats()
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
            self.update_stats()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                f"تم حذف الطالب {name} بنجاح." if self.lang == "ar" else f"Student {name} removed successfully."
            )
        elif name:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "اسم الطالب غير موجود." if self.lang == "ar" else "Student name not found."
            )

    def save_students(self):
        full_data = load_data()
        for acc in full_data["accounts"]:
            if acc["institute"] == self.account["institute"] and acc["teacher"] == self.account["teacher"]:
                acc["students"] = self.account["students"]
                break
        save_data(full_data)
        messagebox.showinfo(
            "تم" if self.lang == "ar" else "Success",
            "تم حفظ قائمة الطلاب بنجاح ✅" if self.lang == "ar" else "Student list saved successfully ✅"
        )

    def restart_students(self):
        if messagebox.askyesno(
            "تأكيد" if self.lang == "ar" else "Confirm",
            "هل تريد إعادة بدء وتفريغ قائمة الطلاب؟" if self.lang == "ar" else "Do you want to restart and clear the student list?"
        ):
            self.account["students"] = []
            self.load_students()
            self.update_stats()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                "تم تفريغ قائمة الطلاب بنجاح." if self.lang == "ar" else "Student list cleared successfully."
            )

    def edit_student(self, student):
        creation_date = datetime.strptime(self.account["created_at"], "%Y-%m-%d")
        if datetime.now() > creation_date + timedelta(days=EDIT_DAYS_LIMIT):
            messagebox.showinfo(
                "تنبيه" if self.lang == "ar" else "Alert",
                "انتهت فترة تعديل البيانات." if self.lang == "ar" else "Editing period has expired."
            )
            return

        popup = ctk.CTkToplevel(self)
        popup.title(f"تعديل بيانات {student['name']}" if self.lang == "ar" else f"Edit {student['name']} Data")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.7)
        popup.wm_geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")
        popup.transient(self)
        popup.grab_set()

        edit_frame = ctk.CTkFrame(popup, corner_radius=10)
        edit_frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(
            edit_frame,
            text="اسم الطالب:" if self.lang == "ar" else "Student Name:",
            font=("Cairo" if self.lang == "ar" else "Arial", 14)
        ).pack(pady=5)
        name_entry = ctk.CTkEntry(
            edit_frame,
            width=400,
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        name_entry.insert(0, student["name"])
        name_entry.pack(pady=10)

        # Grades section
        ctk.CTkLabel(
            edit_frame,
            text="العلامات:" if self.lang == "ar" else "Grades:",
            font=("Cairo" if self.lang == "ar" else "Arial", 14)
        ).pack(pady=5)

        grades_frame = ctk.CTkScrollableFrame(edit_frame, corner_radius=8, height=150)
        grades_frame.pack(fill="x", pady=10)

        self.grade_rows = []
        self.load_grades(grades_frame, student)

        add_grade_frame = ctk.CTkFrame(edit_frame, corner_radius=10)
        add_grade_frame.pack(fill="x", pady=10)

        self.grade_entry = ctk.CTkEntry(
            add_grade_frame,
            placeholder_text="العلامة" if self.lang == "ar" else "Grade",
            width=100
        )
        self.grade_entry.pack(side="left" if self.lang == "ar" else "right", padx=5)

        self.date_entry = ctk.CTkEntry(
            add_grade_frame,
            placeholder_text="التاريخ (YYYY-MM-DD)" if self.lang == "ar" else "Date (YYYY-MM-DD)",
            width=150
        )
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(side="left" if self.lang == "ar" else "right", padx=5)

        self.reason_entry = ctk.CTkEntry(
            add_grade_frame,
            placeholder_text="السبب (اختياري)" if self.lang == "ar" else "Reason (optional)",
            width=200
        )
        self.reason_entry.pack(side="left" if self.lang == "ar" else "right", padx=5)

        add_grade_btn = ctk.CTkButton(
            add_grade_frame,
            text="➕ إضافة علامة" if self.lang == "ar" else "➕ Add Grade",
            command=lambda: self.add_grade(student, grades_frame)
        )
        add_grade_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

        save_grades_btn = ctk.CTkButton(
            edit_frame,
            text="💾 حفظ العلامات" if self.lang == "ar" else "💾 Save Grades",
            command=lambda: self.save_grades(student, grades_frame, popup),
            fg_color="#2E7D32",
            hover_color="#4CAF50",
            corner_radius=8
        )
        save_grades_btn.pack(pady=10)

        ctk.CTkLabel(
            edit_frame,
            text="ملاحظات:" if self.lang == "ar" else "Notes:",
            font=("Cairo" if self.lang == "ar" else "Arial", 14)
        ).pack(pady=5)
        info_entry = ctk.CTkTextbox(
            edit_frame,
            width=400,
            height=120,
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            corner_radius=8
        )
        info_entry.insert("end", student.get("info", ""))
        info_entry.pack(pady=10)

        def save_changes():
            new_name = name_entry.get().strip()
            if new_name and re.match(r"^[a-zA-Z\sأ-ي]+$", new_name):
                student["name"] = new_name
            else:
                messagebox.showerror(
                    "خطأ" if self.lang == "ar" else "Error",
                    "اسم الطالب غير صالح." if self.lang == "ar" else "Invalid student name."
                )
                return

            student["info"] = info_entry.get("1.0", "end").strip()
            self.load_students()
            self.update_stats()
            popup.destroy()
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                "تم حفظ التغييرات بنجاح ✅" if self.lang == "ar" else "Changes saved successfully ✅"
            )

        ctk.CTkButton(
            edit_frame,
            text="💾 حفظ" if self.lang == "ar" else "💾 Save",
            font=("Cairo" if self.lang == "ar" else "Arial", 14),
            command=save_changes,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        ).pack(pady=15)

    def save_grades(self, student, grades_frame, popup):
        today = datetime.now().strftime("%Y-%m-%d")
        full_data = load_data()
        total_daily_grade = sum(g["grade"] for g in student["grades"] if g["date"] == today)

        for acc in full_data["accounts"]:
            if acc["institute"] == self.account["institute"] and acc["teacher"] == self.account["teacher"]:
                for s in acc["students"]:
                    if s["name"] == student["name"]:
                        s["grades"] = student["grades"]
                        break
                break
        save_data(full_data)
        messagebox.showinfo(
            "تم" if self.lang == "ar" else "Success",
            f"تم حفظ العلامات بنجاح ✅\nإجمالي العلامات لليوم: {total_daily_grade}" if self.lang == "ar" else f"Grades saved successfully ✅\nTotal grades for today: {total_daily_grade}"
        )
        self.load_grades(grades_frame, student)

    def load_grades(self, frame, student):
        for widget in frame.winfo_children():
            widget.destroy()

        self.grade_rows = []
        from collections import defaultdict
        daily_grades = defaultdict(list)
        for g in student.get("grades", []):
            daily_grades[g["date"]].append(g)

        for date, grades in sorted(daily_grades.items()):
            total_daily = sum(g["grade"] for g in grades)
            row = ctk.CTkFrame(frame, corner_radius=5)
            row.pack(fill="x", pady=5)

            date_label = ctk.CTkLabel(row, text=f"{date}: {total_daily}", width=150)
            date_label.pack(side="left" if self.lang == "ar" else "right", padx=5)

            for idx, g in enumerate(grades):
                sub_row = ctk.CTkFrame(row)
                sub_row.pack(fill="x", padx=20)

                grade_label = ctk.CTkLabel(sub_row, text=str(g["grade"]), width=50)
                grade_label.pack(side="left" if self.lang == "ar" else "right", padx=5)

                reason_label = ctk.CTkLabel(sub_row, text=g.get("reason", ""), width=150)
                reason_label.pack(side="left" if self.lang == "ar" else "right", padx=5)

                global_idx = student["grades"].index(g)
                edit_btn = ctk.CTkButton(
                    sub_row,
                    text="✏️",
                    width=30,
                    command=lambda gi=global_idx: self.edit_grade(student, gi, frame)
                )
                edit_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

                delete_btn = ctk.CTkButton(
                    sub_row,
                    text="🗑️",
                    width=30,
                    fg_color="#D32F2F",
                    hover_color="#F44336",
                    command=lambda gi=global_idx: self.delete_grade(student, gi, frame)
                )
                delete_btn.pack(side="right" if self.lang == "ar" else "left", padx=5)

            self.grade_rows.append(row)

    def add_grade(self, student, frame):
        try:
            grade = int(self.grade_entry.get())
            if grade < 0 or grade > MAX_GRADES:
                raise ValueError
            date = self.date_entry.get()
            datetime.strptime(date, "%Y-%m-%d")  # validate date
            reason = self.reason_entry.get().strip()

            student["grades"].append({"grade": grade, "date": date, "reason": reason})
            self.grade_entry.delete(0, "end")
            self.reason_entry.delete(0, "end")
            self.load_grades(frame, student)
        except ValueError:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "العلامة غير صالحة أو التاريخ غير صحيح." if self.lang == "ar" else "Invalid grade or date."
            )

    def edit_grade(self, student, idx, frame):
        g = student["grades"][idx]
        edit_popup = ctk.CTkToplevel(self)
        edit_popup.title("تعديل العلامة" if self.lang == "ar" else "Edit Grade")
        edit_popup.geometry("300x200")

        grade_entry = ctk.CTkEntry(edit_popup, placeholder_text="العلامة")
        grade_entry.insert(0, str(g["grade"]))
        grade_entry.pack(pady=10)

        date_entry = ctk.CTkEntry(edit_popup, placeholder_text="التاريخ")
        date_entry.insert(0, g["date"])
        date_entry.pack(pady=10)

        reason_entry = ctk.CTkEntry(edit_popup, placeholder_text="السبب")
        reason_entry.insert(0, g.get("reason", ""))
        reason_entry.pack(pady=10)

        def save_edit():
            try:
                grade = int(grade_entry.get())
                if grade < 0 or grade > MAX_GRADES:
                    raise ValueError
                date = date_entry.get()
                datetime.strptime(date, "%Y-%m-%d")
                reason = reason_entry.get().strip()
                student["grades"][idx] = {"grade": grade, "date": date, "reason": reason}
                self.load_grades(frame, student)
                edit_popup.destroy()
            except ValueError:
                messagebox.showerror("خطأ", "بيانات غير صالحة.")

        save_btn = ctk.CTkButton(edit_popup, text="حفظ", command=save_edit)
        save_btn.pack(pady=10)

    def delete_grade(self, student, idx, frame):
        if messagebox.askyesno("تأكيد", "هل تريد حذف هذه العلامة؟"):
            del student["grades"][idx]
            self.load_grades(frame, student)

    def back_to_manager(self):
        self.destroy()
        AccountManagerWindow(self.lang, self.mode).mainloop()

    def export_to_excel(self):
        self.attributes("-disabled", True)
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Students"
            ws.append([
                "الاسم" if self.lang == "ar" else "Name",
                "العلامات" if self.lang == "ar" else "Grades",
                "المجموع" if self.lang == "ar" else "Total",
                "ملاحظات" if self.lang == "ar" else "Notes"
            ])

            for student in self.account["students"]:
                grades_str = " ".join([f"{g['grade']} ({g['date']}, {g.get('reason', '')})" for g in student.get("grades", [])])
                total = sum(g["grade"] for g in student.get("grades", []))
                ws.append([
                    student["name"],
                    grades_str,
                    total,
                    student.get("info", "")
                ])

            wb.save("students_data.xlsx")
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                "تم تصدير البيانات إلى ملف Excel بنجاح ✅" if self.lang == "ar" else "Data exported to Excel successfully ✅"
            )
        except PermissionError:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "الملف مفتوح في برنامج آخر. أغلق الملف وحاول مجدداً." if self.lang == "ar" else "File is open in another program. Close it and try again."
            )
        except Exception as e:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                f"حدث خطأ أثناء التصدير: {str(e)}" if self.lang == "ar" else f"Error during export: {str(e)}"
            )
        finally:
            self.attributes("-disabled", False)
