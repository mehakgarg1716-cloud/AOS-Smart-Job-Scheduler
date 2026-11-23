
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_gantt_chart(parent, jobs):

    chart_window = tk.Toplevel(parent)
    chart_window.title("Gantt Chart")
    chart_window.geometry("900x450")

    fig, ax = plt.subplots(figsize=(9, 3))

    for i, job in enumerate(jobs):

        ax.barh(
            0,
            job.burst_time,
            left=job.start_time,
            height=0.5,
            label=f"Job {job.job_id}"
        )

        ax.text(
            job.start_time + job.burst_time / 2,
            0,
            f"J{job.job_id}",
            ha='center',
            va='center'
        )

    ax.set_xlabel("Time")
    ax.set_title("Smart Job Scheduling - Gantt Chart")
    ax.set_yticks([])
    ax.grid(axis='x')

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

