import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, timedelta

class Task:
    def __init__(self, name, details, start_date, end_date, start_time, end_time, color):
        self._name = name
        self._details = details
        self._start_date = start_date
        self._end_date = end_date
        self._start_time = start_time
        self._end_time = end_time
        self._color = color

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_details(self):
        return self._details

    def set_details(self, details):
        self._details = details

    def get_start_date(self):
        return self._start_date

    def set_start_date(self, start_date):
        self._start_date = start_date

    def get_end_date(self):
        return self._end_date

    def set_end_date(self, end_date):
        self._end_date = end_date

    def get_start_time(self):
        return self._start_time

    def set_start_time(self, start_time):
        self._start_time = start_time

    def get_end_time(self):
        return self._end_time

    def set_end_time(self, end_time):
        self._end_time = end_time

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management")

        self.calendar = Calendar(root, selectmode='day', command=self.show_tasks)
        self.calendar.pack(pady=20)

        self.event_ids = {}

        self.task_frame = tk.Frame(root)
        self.task_frame.pack(pady=10)

        self.task_label = tk.Label(self.task_frame, text="Task Name:")
        self.task_label.grid(row=0, column=0)

        self.task_entry = tk.Entry(self.task_frame, width=30)
        self.task_entry.grid(row=0, column=1)

        self.details_label = tk.Label(self.task_frame, text="Details:")
        self.details_label.grid(row=1, column=0)

        self.details_entry = tk.Entry(self.task_frame, width=30)
        self.details_entry.grid(row=1, column=1)

        self.start_date_label = tk.Label(self.task_frame, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.grid(row=2, column=0)

        self.start_date_entry = tk.Entry(self.task_frame, width=30)
        self.start_date_entry.grid(row=2, column=1)

        self.end_date_label = tk.Label(self.task_frame, text="End Date (YYYY-MM-DD):")
        self.end_date_label.grid(row=3, column=0)

        self.end_date_entry = tk.Entry(self.task_frame, width=30)
        self.end_date_entry.grid(row=3, column=1)

        self.start_time_label = tk.Label(self.task_frame, text="Start Time (HH:MM):")
        self.start_time_label.grid(row=4, column=0)

        self.start_time_entry = tk.Entry(self.task_frame, width=30)
        self.start_time_entry.grid(row=4, column=1)

        self.end_time_label = tk.Label(self.task_frame, text="End Time (HH:MM):")
        self.end_time_label.grid(row=5, column=0)

        self.end_time_entry = tk.Entry(self.task_frame, width=30)
        self.end_time_entry.grid(row=5, column=1)

        self.add_task_button = tk.Button(self.task_frame, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=7, column=0)

        self.update_button = tk.Button(self.task_frame, text="Update Task", command=self.update_task)
        self.update_button.grid(row=7, column=1)

        self.delete_button = tk.Button(self.task_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=7, column=2)

        self.tasks = {}
        self.task_listbox = tk.Listbox(root, width=50)
        self.task_listbox.pack(pady=10)

        self.task_listbox.bind("<<ListboxSelect>>", self.on_task_select)

    def show_tasks(self, event):
        date = self.calendar.get_date()
        self.refresh_task_listbox(date)

    def add_task(self):
        date = self.calendar.get_date()
        task_name = self.task_entry.get()
        details = self.details_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()

        if task_name:
            new_task = Task(task_name, details, start_date, end_date, start_time, end_time, "blue")  # Use a fixed color

            if date not in self.tasks:
                self.tasks[date] = []
            self.tasks[date].append(new_task)

            self.clear_entries()
            self.refresh_task_listbox(date)
            self.mark_calendar(start_date, end_date, "blue")  # Use a fixed color
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
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, selected_task.get_name())
            self.details_entry.delete(0, tk.END)
            self.details_entry.insert(0, selected_task.get_details())
            self.start_date_entry.delete(0, tk.END)
            self.start_date_entry.insert(0, selected_task.get_start_date())
            self.end_date_entry.delete(0, tk.END)
            self.end_date_entry.insert(0, selected_task.get_end_date())
            self.start_time_entry.delete(0, tk.END)
            self.start_time_entry.insert(0, selected_task.get_start_time())
            self.end_time_entry.delete(0, tk.END)
            self.end_time_entry.insert(0, selected_task.get_end_time())

    def update_task(self):
        date = self.calendar.get_date()
        selected_task_index = self.task_listbox.curselection()

        if selected_task_index:
            task_index = selected_task_index[0]
            task = self.tasks[date][task_index]

            task.set_name(self.task_entry.get())
            task.set_details(self.details_entry.get())
            task.set_start_date(self.start_date_entry.get())
            task.set_end_date(self.end_date_entry.get())
            task.set_start_time(self.start_time_entry.get())
            task.set_end_time(self.end_time_entry.get())
            task.set_color("blue")  # Use a fixed color

            self.refresh_task_listbox(date)
            self.clear_entries()

            self.remove_calendar_marks(task.get_start_date(), task.get_end_date())
            self.mark_calendar(task.get_start_date(), task.get_end_date(), "blue")  # Use a fixed color
        else:
            messagebox.showwarning("Warning", "Select a task to update.")

    def delete_task(self):
        date = self.calendar.get_date()
        selected_task_index = self.task_listbox.curselection()

        if selected_task_index:
            task_index = selected_task_index[0]
            task = self.tasks[date][task_index]
            self.remove_calendar_marks(task.get_start_date(), task.get_end_date())

            del self.tasks[date][task_index]
            self.refresh_task_listbox(date)
            self.redraw_calendar()
        else:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def clear_entries(self):
        self.task_entry.delete(0, tk.END)
        self.details_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.start_time_entry.delete(0, tk.END)
        self.end_time_entry.delete(0, tk.END)

    def mark_calendar(self, start_date, end_date, color):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        for n in range((end - start).days + 1):
            day = start + timedelta(n)
            event_id = self.calendar.calevent_create(day.date(), day.date(), {
                'color': color
            })
            if day.date() not in self.event_ids:
                self.event_ids[day.date()] = []
            self.event_ids[day.date()].append(event_id)

    def remove_calendar_marks(self, start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        for n in range((end - start).days + 1):
            day = start + timedelta(n)
            if day.date() in self.event_ids:
                for event_id in self.event_ids[day.date()]:
                    self.calendar.calevent_remove(event_id)
                del self.event_ids[day.date()]

    def redraw_calendar(self):
        for date in self.event_ids.keys():
            for event_id in self.event_ids[date]:
                self.calendar.calevent_remove(event_id)
        self.event_ids.clear()

        for date, tasks in self.tasks.items():
            for task in tasks:
                self.mark_calendar(task.get_start_date(), task.get_end_date(), "blue")  # Use a fixed color


if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
