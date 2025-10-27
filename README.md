# ============================================================
# 🔹 واجهة إدارة الحضور
# ============================================================
class AttendanceWindow(ctk.CTkToplevel):
    def __init__(self, master, account, lang="ar", mode="dark"):
        super().__init__(master)
        ctk.set_appearance_mode(mode)
        self.account = account
        self.lang = lang
        self.mode = mode
        self.title("إدارة الحضور" if lang == "ar" else "Manage Attendance")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.wm_geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")

        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(fill="both", expand=True)

        # Left section: Students list for attendance and grades
        left_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        left_frame.pack(side="left" if lang == "ar" else "right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            left_frame,
            text="قائمة الطلاب" if lang == "ar" else "Students List",
            font=("Cairo" if lang == "ar" else "Arial", 18, "bold")
        ).pack(pady=10)

        self.attendance_frame = ctk.CTkScrollableFrame(left_frame, corner_radius=8)
        self.attendance_frame.pack(fill="both", expand=True, pady=10)

        self.load_attendance_students()

        # Buttons for saving attendance and grades
        button_frame = ctk.CTkFrame(left_frame, corner_radius=10)
        button_frame.pack(pady=10)

        save_attendance_btn = ctk.CTkButton(
            button_frame,
            text="💾 حفظ الحضور" if lang == "ar" else "💾 Save Attendance",
            command=self.save_attendance,
            fg_color="#5E2A7E",
            hover_color="#7B1FA2",
            corner_radius=8
        )
        save_attendance_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        save_grades_btn = ctk.CTkButton(
            button_frame,
            text="💾 حفظ العلامات" if lang == "ar" else "💾 Save Grades",
            command=self.save_grades,
            fg_color="#2E7D32",
            hover_color="#4CAF50",
            corner_radius=8
        )
        save_grades_btn.pack(side="right" if lang == "ar" else "left", padx=5)

        # Right section: Date, day, sessions per week
        right_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, width=300)
        right_frame.pack(side="right" if lang == "ar" else "left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(
            right_frame,
            text="إعدادات اليوم" if lang == "ar" else "Day Settings",
            font=("Cairo" if lang == "ar" else "Arial", 18, "bold")
        ).pack(pady=10)

        today = datetime.now()
        ctk.CTkLabel(
            right_frame,
            text=f"التاريخ: {today.strftime('%Y-%m-%d')}" if lang == "ar" else f"Date: {today.strftime('%Y-%m-%d')}",
            font=("Cairo" if lang == "ar" else "Arial", 14)
        ).pack(pady=5)

        day_name = today.strftime("%A")
        arabic_days = {"Monday": "الإثنين", "Tuesday": "الثلاثاء", "Wednesday": "الأربعاء", "Thursday": "الخميس", "Friday": "الجمعة", "Saturday": "السبت", "Sunday": "الأحد"}
        ctk.CTkLabel(
            right_frame,
            text=f"اليوم: {arabic_days.get(day_name, day_name)}" if lang == "ar" else f"Day: {day_name}",
            font=("Cairo" if lang == "ar" else "Arial", 14)
        ).pack(pady=5)

        ctk.CTkLabel(
            right_frame,
            text="عدد الجلسات في الأسبوع:" if lang == "ar" else "Sessions per Week:",
            font=("Cairo" if lang == "ar" else "Arial", 14)
        ).pack(pady=5)

        self.sessions_entry = ctk.CTkEntry(
            right_frame,
            font=("Cairo" if lang == "ar" else "Arial", 14),
            corner_radius=8,
            height=40
        )
        self.sessions_entry.insert(0, str(self.account.get("course_days", 5)))
        self.sessions_entry.pack(pady=5)

        update_sessions_btn = ctk.CTkButton(
            right_frame,
            text="تحديث" if lang == "ar" else "Update",
            command=self.update_sessions,
            fg_color="#0288D1",
            hover_color="#03A9F4",
            corner_radius=8
        )
        update_sessions_btn.pack(pady=10)

    def load_attendance_students(self):
        for widget in self.attendance_frame.winfo_children():
            widget.destroy()

        today = datetime.now().strftime("%Y-%m-%d")
        self.grade_entries = {}  # Store grade entry fields for each student
        for i, student in enumerate(self.account["students"]):
            row = ctk.CTkFrame(self.attendance_frame, corner_radius=5, fg_color="#424242")
            row.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(
                row,
                text=f"{i+1}. {student['name']}",
                font=("Cairo" if self.lang == "ar" else "Arial", 14),
                anchor="w" if self.lang == "ar" else "e"
            ).pack(side="left" if self.lang == "ar" else "right", padx=10, fill="x", expand=True)

            # Grade entry field
            grade_entry = ctk.CTkEntry(
                row,
                placeholder_text="العلامة" if self.lang == "ar" else "Grade",
                width=100,
                font=("Cairo" if self.lang == "ar" else "Arial", 14)
            )
            grade_entry.pack(side="right" if self.lang == "ar" else "left", padx=5)
            self.grade_entries[student["name"]] = grade_entry

            # Attendance switch
            present_var = ctk.BooleanVar(value=any(a["date"] == today and a["present"] for a in student.get("attendance", [])))
            present_switch = ctk.CTkSwitch(
                row,
                text="حاضر" if self.lang == "ar" else "Present",
                variable=present_var,
                command=lambda s=student, var=present_var: self.toggle_attendance(s, today, var.get())
            )
            present_switch.pack(side="right" if self.lang == "ar" else "left", padx=5)

    def toggle_attendance(self, student, date, present):
        attendance = student.get("attendance", [])
        # Remove existing for today if any
        attendance = [a for a in attendance if a["date"] != date]
        attendance.append({"date": date, "present": present})
        student["attendance"] = attendance

    def save_attendance(self):
        full_data = load_data()
        for acc in full_data["accounts"]:
            if acc["institute"] == self.account["institute"] and acc["teacher"] == self.account["teacher"]:
                acc["students"] = self.account["students"]
                break
        save_data(full_data)
        messagebox.showinfo(
            "تم" if self.lang == "ar" else "Success",
            "تم حفظ الحضور بنجاح ✅" if self.lang == "ar" else "Attendance saved successfully ✅"
        )

    def save_grades(self):
        today = datetime.now().strftime("%Y-%m-%d")
        full_data = load_data()
        total_grades = 0
        graded_students = 0

        for student in self.account["students"]:
            grade_str = self.grade_entries.get(student["name"], "").get().strip()
            if grade_str:
                try:
                    grade = int(grade_str)
                    if grade < 0 or grade > MAX_GRADES:
                        raise ValueError
                    student["grades"].append({"grade": grade, "date": today, "reason": "Daily grade"})
                    total_grades += grade
                    graded_students += 1
                except ValueError:
                    messagebox.showerror(
                        "خطأ" if self.lang == "ar" else "Error",
                        f"العلامة غير صالحة للطالب {student['name']}" if self.lang == "ar" else f"Invalid grade for student {student['name']}"
                    )
                    return

        # Save updated data
        for acc in full_data["accounts"]:
            if acc["institute"] == self.account["institute"] and acc["teacher"] == self.account["teacher"]:
                acc["students"] = self.account["students"]
                break
        save_data(full_data)

        # Calculate and show total grades for the day
        if graded_students > 0:
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                f"تم حفظ العلامات بنجاح ✅\nإجمالي العلامات لليوم: {total_grades}" if self.lang == "ar" else f"Grades saved successfully ✅\nTotal grades for today: {total_grades}"
            )
        else:
            messagebox.showinfo(
                "تنبيه" if self.lang == "ar" else "Alert",
                "لم يتم إدخال أي علامات." if self.lang == "ar" else "No grades were entered."
            )

        # Clear grade entries after saving
        for entry in self.grade_entries.values():
            entry.delete(0, "end")

    def update_sessions(self):
        try:
            sessions = int(self.sessions_entry.get())
            if sessions < 1:
                raise ValueError
            self.account["course_days"] = sessions
            full_data = load_data()
            for acc in full_data["accounts"]:
                if acc["institute"] == self.account["institute"] and acc["teacher"] == self.account["teacher"]:
                    acc["course_days"] = sessions
                    break
            save_data(full_data)
            messagebox.showinfo(
                "تم" if self.lang == "ar" else "Success",
                "تم تحديث عدد الجلسات بنجاح ✅" if self.lang == "ar" else "Sessions updated successfully ✅"
            )
        except ValueError:
            messagebox.showerror(
                "خطأ" if self.lang == "ar" else "Error",
                "يرجى إدخال رقم صحيح إيجابي." if self.lang == "ar" else "Please enter a positive integer."
            )
