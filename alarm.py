import tkinter as tk
from tkinter import messagebox
import sqlite3
import time
import threading

# Database setup
conn = sqlite3.connect('alarms.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS alarms (
        id INTEGER PRIMARY KEY,
        time TEXT,
        tone TEXT,
        active INTEGER
    )
''')
conn.commit()

class AlarmClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")

        self.current_time_label = tk.Label(root, text="", font=('Helvetica', 48))
        self.current_time_label.pack()

        self.set_alarm_frame = tk.Frame(root)
        self.set_alarm_frame.pack(pady=20)

        tk.Label(self.set_alarm_frame, text="Set Alarm Time (HH:MM):").grid(row=0, column=0, padx=10)
        self.alarm_time_entry = tk.Entry(self.set_alarm_frame)
        self.alarm_time_entry.grid(row=0, column=1, padx=10)

        tk.Label(self.set_alarm_frame, text="Choose Alarm Tone:").grid(row=1, column=0, padx=10)
        self.alarm_tone_entry = tk.Entry(self.set_alarm_frame)
        self.alarm_tone_entry.grid(row=1, column=1, padx=10)

        tk.Button(self.set_alarm_frame, text="Set Alarm", command=self.set_alarm).grid(row=2, column=0, columnspan=2, pady=10)

        self.alarms_frame = tk.Frame(root)
        self.alarms_frame.pack(pady=20)

        self.update_time()
        self.load_alarms()
        self.check_alarms()

    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        self.current_time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def load_alarms(self):
        for widget in self.alarms_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        c.execute('SELECT * FROM alarms')
        alarms = c.fetchall()
        conn.close()

        for alarm in alarms:
            frame = tk.Frame(self.alarms_frame)
            frame.pack(fill='x')

            tk.Label(frame, text=alarm[1], width=10).pack(side='left')
            tk.Label(frame, text=alarm[2], width=10).pack(side='left')
            active_text = 'Active' if alarm[3] else 'Inactive'
            tk.Label(frame, text=active_text, width=10).pack(side='left')

            tk.Button(frame, text="Toggle", command=lambda a=alarm: self.toggle_alarm(a)).pack(side='left')
            tk.Button(frame, text="Delete", command=lambda a=alarm: self.delete_alarm(a)).pack(side='left')

    def set_alarm(self):
        alarm_time = self.alarm_time_entry.get()
        alarm_tone = self.alarm_tone_entry.get()

        if not alarm_time or not alarm_tone:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return

        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        c.execute('INSERT INTO alarms (time, tone, active) VALUES (?, ?, ?)', (alarm_time, alarm_tone, 1))
        conn.commit()
        conn.close()

        self.load_alarms()
        messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")

    def toggle_alarm(self, alarm):
        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        new_status = 0 if alarm[3] else 1
        c.execute('UPDATE alarms SET active = ? WHERE id = ?', (new_status, alarm[0]))
        conn.commit()
        conn.close()

        self.load_alarms()

    def delete_alarm(self, alarm):
        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        c.execute('DELETE FROM alarms WHERE id = ?', (alarm[0],))
        conn.commit()
        conn.close()

        self.load_alarms()

    def check_alarms(self):
        current_time = time.strftime('%H:%M')
        conn = sqlite3.connect('alarms.db')
        c = conn.cursor()
        c.execute('SELECT * FROM alarms WHERE time = ? AND active = 1', (current_time,))
        alarms = c.fetchall()
        conn.close()

        for alarm in alarms:
            self.trigger_alarm(alarm)

        self.root.after(60000, self.check_alarms)

    def trigger_alarm(self, alarm):
        messagebox.showinfo("Alarm Ringing", f"Alarm for {alarm[1]} is ringing! Tone: {alarm[2]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClockApp(root)
    root.mainloop()
