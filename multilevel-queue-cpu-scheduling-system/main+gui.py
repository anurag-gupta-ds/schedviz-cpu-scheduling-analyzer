import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ================================================================
# 🔧 MAIN LOGIC (100% MATCH WITH MAM STEPS)
# ================================================================

class Process:
    def __init__(self, pid, at, bt, ptype):
        self.pid = pid
        self.arrival = at
        self.burst = bt
        self.remaining = bt
        self.type = ptype

        self.start = -1
        self.completion = 0
        self.waiting = 0
        self.turnaround = 0
        self.state = "Ready" 
        
      # ✅ Step 8


# ---------------- FCFS ----------------
def fcfs(queue, time, gantt, exec_list):
    while queue:
        p = queue.popleft()

        if time < p.arrival:
            time = p.arrival

        p.state = "Running"
        p.start = time

        gantt.append((p.pid, time, time + p.burst))
        exec_list.append(p.pid)

        time += p.burst

        p.completion = time
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst
        p.state = "Completed"

    return time


# ---------------- Round Robin ----------------
def round_robin(queue, quantum, time, gantt, exec_list):
    q = deque(queue)

    while q:
        p = q.popleft()

        if time < p.arrival:
            time = p.arrival

        if p.start == -1:
            p.start = time

        p.state = "Running"

        exec_time = min(p.remaining, quantum)
        gantt.append((p.pid, time, time + exec_time))
        exec_list.append(p.pid)

        time += exec_time
        p.remaining -= exec_time

        if p.remaining > 0:
            p.state = "Waiting"
            q.append(p)
        else:
            p.completion = time
            p.turnaround = p.completion - p.arrival
            p.waiting = p.turnaround - p.burst
            p.state = "Completed"

    return time


# ---------------- Scheduler ----------------
def scheduler(processes, quantum):

    # Step 1 & 3: Define + Assign Queues
    q1, q2, q3 = deque(), deque(), deque()

    for p in processes:
        if p.type == "System":
            q1.append(p)
        elif p.type == "Interactive":
            q2.append(p)
        else:
            q3.append(p)

    # Sort by arrival
    q1 = deque(sorted(q1, key=lambda x: x.arrival))
    q2 = deque(sorted(q2, key=lambda x: x.arrival))
    q3 = deque(sorted(q3, key=lambda x: x.arrival))

    gantt = []
    time = 0

    # For queue-wise execution display
    exec_q1, exec_q2, exec_q3 = [], [], []

    # Step 5 & 6: Priority Execution
    time = fcfs(q1, time, gantt, exec_q1)
    time = round_robin(q2, quantum, time, gantt, exec_q2)
    time = fcfs(q3, time, gantt, exec_q3)

    return processes, gantt, exec_q1, exec_q2, exec_q3


# ================================================================
# 🎨 GUI (same as your code)
# ================================================================

COLORS = {
    "bg": "#0f172a",
    "card": "#1e293b",
    "accent": "#38bdf8",
    "text": "#e2e8f0",
    "green": "#22c55e",
    "red": "#ef4444",
    "yellow": "#facc15"
}

root = tk.Tk()
root.title("⚙ Multilevel Queue Scheduler")
root.geometry("1100x820")
root.configure(bg=COLORS["bg"])

tk.Label(root, text="⚡ Multilevel Queue CPU Scheduling System ⚡",
         font=("Segoe UI", 18, "bold"),
         bg=COLORS["bg"],
         fg=COLORS["accent"]).pack(pady=15)

frame = tk.Frame(root, bg=COLORS["card"], padx=20, pady=15)
frame.pack(padx=40, fill="x")

tk.Label(frame, text="Processes:", bg=COLORS["card"], fg=COLORS["text"]).grid(row=0, column=0)
num_entry = tk.Entry(frame)
num_entry.grid(row=0, column=1)

tk.Label(frame, text="Time Quantum:", bg=COLORS["card"], fg=COLORS["text"]).grid(row=1, column=0)
quantum_entry = tk.Entry(frame)
quantum_entry.grid(row=1, column=1)

btn_frame = tk.Frame(frame, bg=COLORS["card"])
btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

generate_btn = tk.Button(btn_frame, text="Generate", bg=COLORS["accent"])
generate_btn.pack(side="left", padx=10)

run_btn = tk.Button(btn_frame, text="Run", bg=COLORS["green"])
run_btn.pack(side="left", padx=10)

fields_frame = tk.Frame(root, bg=COLORS["bg"])
fields_frame.pack(pady=10)

result_frame = tk.Frame(root, bg=COLORS["bg"])
result_frame.pack()

chart_frame = tk.Frame(root, bg=COLORS["bg"])
chart_frame.pack(fill="both", expand=True)

process_entries = []


def generate_fields():
    process_entries.clear()
    for w in fields_frame.winfo_children():
        w.destroy()

    n = int(num_entry.get())

    for i, h in enumerate(["PID", "AT", "BT", "Type"]):
        tk.Label(fields_frame, text=h, fg=COLORS["accent"], bg=COLORS["bg"]).grid(row=0, column=i)

    for i in range(n):
        row = {}
        tk.Label(fields_frame, text=f"P{i+1}", fg=COLORS["yellow"], bg=COLORS["bg"]).grid(row=i+1, column=0)

        at = tk.Entry(fields_frame, width=8)
        at.grid(row=i+1, column=1)

        bt = tk.Entry(fields_frame, width=8)
        bt.grid(row=i+1, column=2)

        t = ttk.Combobox(fields_frame, values=["System", "Interactive", "Batch"], state="readonly")
        t.current(0)
        t.grid(row=i+1, column=3)

        row.update({"pid": f"P{i+1}", "at": at, "bt": bt, "type": t})
        process_entries.append(row)

generate_btn.config(command=generate_fields)


def run():
    for w in result_frame.winfo_children(): w.destroy()
    for w in chart_frame.winfo_children(): w.destroy()

    processes = []
    q = int(quantum_entry.get())

    for r in process_entries:
        processes.append(Process(r["pid"], int(r["at"].get()), int(r["bt"].get()), r["type"].get()))

    processes, gantt, q1_exec, q2_exec, q3_exec = scheduler(processes, q)

    # TABLE
    for i, h in enumerate(["PID", "WT", "TAT", "State"]):
        tk.Label(result_frame, text=h, fg=COLORS["accent"], bg=COLORS["bg"]).grid(row=0, column=i)

    total_wt = total_tat = 0

    for i, p in enumerate(processes):
        tk.Label(result_frame, text=p.pid, bg=COLORS["bg"], fg="white").grid(row=i+1, column=0)
        tk.Label(result_frame, text=p.waiting, bg=COLORS["bg"], fg="white").grid(row=i+1, column=1)
        tk.Label(result_frame, text=p.turnaround, bg=COLORS["bg"], fg="white").grid(row=i+1, column=2)
        tk.Label(result_frame, text=p.state, bg=COLORS["bg"], fg="white").grid(row=i+1, column=3)

        total_wt += p.waiting
        total_tat += p.turnaround

    n = len(processes)
    tk.Label(result_frame, text=f"Avg WT: {total_wt/n:.2f}", fg=COLORS["green"], bg=COLORS["bg"]).grid(row=n+2, column=0)
    tk.Label(result_frame, text=f"Avg TAT: {total_tat/n:.2f}", fg=COLORS["green"], bg=COLORS["bg"]).grid(row=n+2, column=1)

    # Queue-wise Execution
    tk.Label(result_frame, text=f"Q1: {q1_exec}", fg="white", bg=COLORS["bg"]).grid(row=n+3, column=0, columnspan=2)
    tk.Label(result_frame, text=f"Q2: {q2_exec}", fg="white", bg=COLORS["bg"]).grid(row=n+4, column=0, columnspan=2)
    tk.Label(result_frame, text=f"Q3: {q3_exec}", fg="white", bg=COLORS["bg"]).grid(row=n+5, column=0, columnspan=2)

    # Gantt Chart
    fig, ax = plt.subplots()
    for pid, start, end in gantt:
        ax.barh(pid, end - start, left=start)

    canvas = FigureCanvasTkAgg(fig, chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


run_btn.config(command=run)

root.mainloop()