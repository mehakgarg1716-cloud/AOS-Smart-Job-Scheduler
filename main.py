
import tkinter as tk
from tkinter import ttk, messagebox

from job import Job
from scheduler import SmartScheduler
from charts import show_gantt_chart


# Store all jobs
jobs = []


# Main Window
root = tk.Tk()
root.title("Smart Job Scheduling Simulator")
root.geometry("900x650")
root.configure(bg="#f0f0f0")


# Heading
heading = tk.Label(
    root,
    text="Smart Job Scheduling Simulator",
    font=("Arial", 20, "bold"),
    bg="#f0f0f0"
)
heading.pack(pady=15)


# Input Frame
input_frame = tk.LabelFrame(
    root,
    text="Enter Job Details",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=15
)
input_frame.pack(pady=10)


# Input Fields
fields = [
    "Job ID",
    "Arrival Time",
    "Burst Time",
    "Priority",
    "Deadline"
]

entries = {}

for i, field in enumerate(fields):

    tk.Label(
        input_frame,
        text=field
    ).grid(row=i, column=0, padx=10, pady=5)

    entry = tk.Entry(input_frame)
    entry.grid(row=i, column=1, padx=10, pady=5)

    entries[field] = entry


# Job Table
table_frame = tk.LabelFrame(
    root,
    text="Job Details",
    font=("Arial", 12, "bold")
)
table_frame.pack(pady=10, padx=20, fill="x")

columns = (
    "Job ID",
    "Arrival Time",
    "Burst Time",
    "Priority",
    "Deadline"
)

job_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=6
)

for col in columns:
    job_table.heading(col, text=col)
    job_table.column(col, anchor="center", width=140)

job_table.pack(fill="x", padx=10, pady=10)


# Add Job Function
def add_job():

    try:
        job_id = entries["Job ID"].get().strip()
        arrival = int(entries["Arrival Time"].get())
        burst = int(entries["Burst Time"].get())
        priority = int(entries["Priority"].get())
        deadline = int(entries["Deadline"].get())

        if not job_id:
            messagebox.showerror("Error", "Enter Job ID")
            return

        if arrival < 0 or burst <= 0 or priority <= 0 or deadline < 0:
            messagebox.showerror(
                "Error",
                "Enter valid positive values"
            )
            return

        if any(job.job_id == job_id for job in jobs):
            messagebox.showerror(
                "Error",
                "Job ID already exists"
            )
            return

        job = Job(
            job_id,
            arrival,
            burst,
            priority,
            deadline
        )

        jobs.append(job)

        job_table.insert(
            "",
            "end",
            values=(
                job_id,
                arrival,
                burst,
                priority,
                deadline
            )
        )

        for entry in entries.values():
            entry.delete(0, tk.END)

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter valid numeric values"
        )


# Add Job Button
add_button = tk.Button(
    root,
    text="Add Job",
    command=add_job,
    bg="#2196F3",
    fg="white",
    width=15
)
add_button.pack(pady=10)


# Scheduler Function
def run_scheduler():

    if not jobs:
        messagebox.showwarning(
            "Warning",
            "Please add jobs first"
        )
        return

    # Run Smart Scheduler
    scheduler = SmartScheduler(jobs)

    result = scheduler.schedule_jobs()

    # Calculate Performance Metrics
    total_jobs = len(result)

    avg_waiting_time = sum(
        job.waiting_time for job in result
    ) / total_jobs

    avg_turnaround_time = sum(
        job.turnaround_time for job in result
    ) / total_jobs

    avg_response_time = sum(
        job.response_time for job in result
    ) / total_jobs

    total_burst_time = sum(
        job.burst_time for job in result
    )

    total_completion_time = max(
        job.completion_time for job in result
    )

    cpu_utilization = (
        total_burst_time / total_completion_time
    ) * 100 if total_completion_time > 0 else 0


    # Results Window
    result_window = tk.Toplevel(root)
    result_window.title("Scheduling Results")
    result_window.geometry("950x650")

    tk.Label(
        result_window,
        text="Scheduling Results",
        font=("Arial", 18, "bold")
    ).pack(pady=10)


    # Results Table
    result_columns = (
        "Job ID",
        "Start Time",
        "Completion Time",
        "Waiting Time",
        "Turnaround Time",
        "Response Time",
        "Deadline Status"
    )

    result_table = ttk.Treeview(
        result_window,
        columns=result_columns,
        show="headings",
        height=6
    )

    for col in result_columns:
        result_table.heading(col, text=col)
        result_table.column(
            col,
            anchor="center",
            width=125
        )

    result_table.pack(
        fill="x",
        padx=10,
        pady=10
    )


    # Display Job Results
    for job in result:

        result_table.insert(
            "",
            "end",
            values=(
                job.job_id,
                job.start_time,
                job.completion_time,
                job.waiting_time,
                job.turnaround_time,
                job.response_time,
                job.deadline_status
            )
        )


    # Performance Analysis
    metrics_frame = tk.LabelFrame(
        result_window,
        text="Performance Analysis",
        font=("Arial", 13, "bold"),
        padx=20,
        pady=15
    )

    metrics_frame.pack(
        fill="x",
        padx=20,
        pady=15
    )

    metrics_text = (
        f"Average Waiting Time: {avg_waiting_time:.2f}\n"
        f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
        f"Average Response Time: {avg_response_time:.2f}\n"
        f"CPU Utilization: {cpu_utilization:.2f}%"
    )

    tk.Label(
        metrics_frame,
        text=metrics_text,
        font=("Arial", 12, "bold"),
        justify="left",
        fg="blue"
    ).pack(anchor="w")


    # Gantt Chart Button
    gantt_button = tk.Button(
        result_window,
        text="SHOW GANTT CHART",
        command=lambda: show_gantt_chart(
            result_window,
            result
        ),
        bg="green",
        fg="white",
        font=("Arial", 12, "bold"),
        width=25,
        height=2
    )

    gantt_button.pack(pady=15)


# Run Scheduler Button
run_button = tk.Button(
    root,
    text="Run Scheduler",
    command=run_scheduler,
    bg="#FF9800",
    fg="white",
    width=20
)

run_button.pack(pady=15)


# Start GUI
root.mainloop()

