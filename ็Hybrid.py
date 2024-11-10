import tkinter as tk
from tkinter import messagebox, colorchooser
from tkcalendar import Calendar
from datetime import datetime, timedelta

class Task:
    def __init__(self, name, details, start_date, end_date, start_time, end_time, color, from_teacher=False):
        self._name = name
        self._details = details
        self._start_date = start_date
        self._end_date = end_date
        self._start_time = start_time
        self._end_time = end_time
        self._color = color
        self._from_teacher = from_teacher

    # Getters and Setters
    def get_name(self): return self._name
    def set_name(self, name): self._name = name

    def get_details(self): return self._details
    def set_details(self, details): self._details = details

    def get_start_date(self): return self._start_date
    def set_start_date(self, start_date): self._start_date = start_date

    def get_end_date(self): return self._end_date
    def set_end_date(self, end_date): self._end_date = end_date

    def get_start_time(self): return self._start_time
    def set_start_time(self, start_time): self._start_time = start_time

    def get_end_time(self): return self._end_time
    def set_end_time(self, end_time): self._end_time = end_time

    def get_color(self): return self._color
    def set_color(self, color): self._color = color

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management")

        # Calendar Setup
        self.calendar = Calendar(root, selectmode='day', command=self.show_tasks)
        self.calendar.grid(row=0, column=0, columnspan=3, padx=20, pady=10)

        # Task Input Frame
        self.task_frame = tk.Frame(root)
        self.task_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10)

        # Labels and Inputs
        labels = ["Task Name:", "Details:", "Start Date (YYYY-MM-DD):", "End Date (YYYY-MM-DD):", "Start Time (HH:MM):", "End Time (HH:MM):"]
        self.entries = {}

        for i, text in enumerate(labels):
            tk.Label(self.task_frame, text=text).grid(row=i, column=0, sticky="w")
            entry = tk.Entry(self.task_frame, width=30)
            entry.grid(row=i, column=1, columnspan=2, pady=2)
            self.entries[text] = entry

        # Color Picker Button
        self.selected_color = "blue"
        self.color_button = tk.Button(self.task_frame, text="Choose Color", command=self.choose_color, bg=self.selected_color)
        self.color_button.grid(row=6, column=1, pady=5)

        # Action Buttons
        tk.Button(self.task_frame, text="Add Task", command=self.add_task).grid(row=7, column=0, pady=5)
        tk.Button(self.task_frame, text="Update Task", command=self.update_task).grid(row=7, column=1, pady=5)
        tk.Button(self.task_frame, text="Delete Task", command=self.delete_task).grid(row=7, column=2, pady=5)

        # Task Listbox
        self.task_listbox = tk.Listbox(root, width=50)
        self.task_listbox.grid(row=2, column=0, columnspan=3, padx=20, pady=10)
        self.task_listbox.bind("<<ListboxSelect>>", self.on_task_select)

        self.tasks = {}
        self.event_ids = {}

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.selected_color = color
            self.color_button.config(bg=color)

    def show_tasks(self, event):
        date = self.calendar.get_date()
        self.refresh_task_listbox(date)

    def add_task(self):
        task_name = self.entries["Task Name:"].get()
        details = self.entries["Details:"].get()
        start_date = self.entries["Start Date (YYYY-MM-DD):"].get()
        end_date = self.entries["End Date (YYYY-MM-DD):"].get()
        start_time = self.entries["Start Time (HH:MM):"].get()
        end_time = self.entries["End Time (HH:MM):"].get()

        if task_name:
            date = self.calendar.get_date()
            new_task = Task(task_name, details, start_date, end_date, start_time, end_time, self.selected_color)
            if date not in self.tasks:
                self.tasks[date] = []
            self.tasks[date].append(new_task)
            self.clear_entries()
            self.refresh_task_listbox(date)
            self.mark_calendar(start_date, end_date, self.selected_color)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def refresh_task_listbox(self, date):
        self.task_listbox.delete(0, tk.END)
        if date in self.tasks:
            for task in self.tasks[date]:
                self.task_listbox.insert(tk.END, task.get_name())

    def on_task_select(self, event):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task = self.tasks[self.calendar.get_date()][selected_task_index[0]]
            self.entries["Task Name:"].delete(0, tk.END)
            self.entries["Task Name:"].insert(0, selected_task.get_name())
            self.entries["Details:"].delete(0, tk.END)
            self.entries["Details:"].insert(0, selected_task.get_details())
            self.entries["Start Date (YYYY-MM-DD):"].delete(0, tk.END)
            self.entries["Start Date (YYYY-MM-DD):"].insert(0, selected_task.get_start_date())
            self.entries["End Date (YYYY-MM-DD):"].delete(0, tk.END)
            self.entries["End Date (YYYY-MM-DD):"].insert(0, selected_task.get_end_date())
            self.entries["Start Time (HH:MM):"].delete(0, tk.END)
            self.entries["Start Time (HH:MM):"].insert(0, selected_task.get_start_time())
            self.entries["End Time (HH:MM):"].delete(0, tk.END)
            self.entries["End Time (HH:MM):"].insert(0, selected_task.get_end_time())

    def update_task(self):
        date = self.calendar.get_date()
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[date][selected_task_index[0]]
            old_start_date, old_end_date = task.get_start_date(), task.get_end_date()
            task.set_name(self.entries["Task Name:"].get())
            task.set_details(self.entries["Details:"].get())
            task.set_start_date(self.entries["Start Date (YYYY-MM-DD):"].get())
            task.set_end_date(self.entries["End Date (YYYY-MM-DD):"].get())
            task.set_start_time(self.entries["Start Time (HH:MM):"].get())
            task.set_end_time(self.entries["End Time (HH:MM):"].get())
            task.set_color(self.selected_color)
            self.clear_entries()
            self.refresh_task_listbox(date)
            self.remove_calendar_marks(old_start_date, old_end_date)
            self.mark_calendar(task.get_start_date(), task.get_end_date(), task.get_color())

    def delete_task(self):
        date = self.calendar.get_date()
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.tasks[date][selected_task_index[0]]
            self.remove_calendar_marks(task.get_start_date(), task.get_end_date())
            del self.tasks[date][selected_task_index[0]]
            self.refresh_task_listbox(date)
            self.clear_entries()

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def mark_calendar(self, start_date, end_date, color):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        for n in range((end - start).days + 1):
            day = start + timedelta(n)
            event_id = self.calendar.calevent_create(day, "", tags=(color,))
            if day not in self.event_ids:
                self.event_ids[day] = []
            self.event_ids[day].append(event_id)
        self.calendar.tag_config(color, background=color)

    def remove_calendar_marks(self, start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        for n in range((end - start).days + 1):
            day = start + timedelta(n)
            if day in self.event_ids:
                for event_id in self.event_ids[day]:
                    self.calendar.calevent_remove(event_id=event_id)
                del self.event_ids[day]

# Main
root = tk.Tk()
app = CalendarApp(root)
root.mainloop()