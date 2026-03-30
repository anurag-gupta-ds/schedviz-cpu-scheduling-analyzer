import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statistics


# ================================================================
#  SCHEDULING ALGORITHMS
# ================================================================

def fcfs(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    time = 0
    result = []
    for p in processes:
        start = max(time, p['arrival'])
        completion = start + p['burst']
        result.append({
            'id': p['id'], 'arrival': p['arrival'], 'burst': p['burst'],
            'start': start, 'completion': completion,
            'waiting': start - p['arrival'],
            'turnaround': completion - p['arrival']
        })
        time = completion
    return result


def sjf(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    time = 0
    ready = []
    result = []
    while processes or ready:
        while processes and processes[0]['arrival'] <= time:
            ready.append(processes.pop(0))
        if ready:
            ready.sort(key=lambda x: x['burst'])
            p = ready.pop(0)
            start = time
            completion = start + p['burst']
            result.append({
                'id': p['id'], 'arrival': p['arrival'], 'burst': p['burst'],
                'start': start, 'completion': completion,
                'waiting': start - p['arrival'],
                'turnaround': completion - p['arrival']
            })
            time = completion
        else:
            time += 1
    return result


def round_robin(processes, q):
    processes = sorted(processes, key=lambda x: x['arrival'])
    time = 0
    queue = []
    result = []
    gantt = []
    remaining = {p['id']: p['burst'] for p in processes}
    while processes or queue:
        while processes and processes[0]['arrival'] <= time:
            queue.append(processes.pop(0))
        if queue:
            p = queue.pop(0)
            start = time
            exec_time = min(q, remaining[p['id']])
            time += exec_time
            remaining[p['id']] -= exec_time
            gantt.append((p['id'], start, time))
            while processes and processes[0]['arrival'] <= time:
                queue.append(processes.pop(0))
            if remaining[p['id']] > 0:
                queue.append(p)
            else:
                completion = time
                result.append({
                    'id': p['id'], 'arrival': p['arrival'], 'burst': p['burst'],
                    'completion': completion,
                    'turnaround': completion - p['arrival'],
                    'waiting': completion - p['arrival'] - p['burst']
                })
        else:
            time += 1
    return result, gantt


def calculate_avg(result):
    avg_wt  = sum(p['waiting']    for p in result) / len(result)
    avg_tat = sum(p['turnaround'] for p in result) / len(result)
    return avg_wt, avg_tat


# ================================================================
#  MAIN WINDOW
# ================================================================

root = tk.Tk()
root.title("SchedViz — CPU Scheduling Analyzer")
root.geometry("1000x800")
root.configure(bg="#1e1e2e")
root.resizable(True, True)

COLORS = {
    'bg':      '#1e1e2e',
    'surface': '#313244',
    'surface2':'#45475a',
    'text':    '#cdd6f4',
    'subtext': '#6c7086',
    'blue':    '#89b4fa',
    'green':   '#a6e3a1',
    'red':     '#f38ba8',
    'yellow':  '#f9e2af',
    'mauve':   '#cba6f7',
    'teal':    '#94e2d5',
}

BAR_COLORS = ['#89b4fa', '#a6e3a1', '#f38ba8', '#f9e2af', '#cba6f7', '#94e2d5']

process_entries = []


# ================================================================
#  TITLE
# ================================================================

tk.Label(
    root,
    text="⚙   SchedViz — CPU Scheduling Analyzer",
    font=("Courier", 18, "bold"),
    bg=COLORS['bg'], fg=COLORS['blue']
).pack(pady=15)


# ================================================================
#  INPUT FRAME
# ================================================================

input_frame = tk.Frame(root, bg=COLORS['surface'], padx=20, pady=15)
input_frame.pack(pady=5, padx=40, fill="x")

tk.Label(
    input_frame, text="Number of Processes:",
    bg=COLORS['surface'], fg=COLORS['text'],
    font=("Courier", 11)
).grid(row=0, column=0, padx=10, pady=8, sticky="w")

num_entry = tk.Entry(
    input_frame, font=("Courier", 11), width=10,
    bg=COLORS['surface2'], fg=COLORS['text'],
    insertbackground="white"
)
num_entry.grid(row=0, column=1, padx=10, pady=8, sticky="w")

tk.Label(
    input_frame, text="Select Algorithm:",
    bg=COLORS['surface'], fg=COLORS['text'],
    font=("Courier", 11)
).grid(row=1, column=0, padx=10, pady=8, sticky="w")

algo_var = tk.StringVar(value="FCFS")
algo_menu = ttk.Combobox(
    input_frame, textvariable=algo_var,
    values=["FCFS", "SJF", "Round Robin", "Compare All", "Suggest Best"],
    font=("Courier", 11), width=15, state="readonly"
)
algo_menu.grid(row=1, column=1, padx=10, pady=8, sticky="w")

tk.Label(
    input_frame, text="Time Quantum (RR only):",
    bg=COLORS['surface'], fg=COLORS['text'],
    font=("Courier", 11)
).grid(row=2, column=0, padx=10, pady=8, sticky="w")

quantum_entry = tk.Entry(
    input_frame, font=("Courier", 11), width=10,
    bg=COLORS['surface2'], fg=COLORS['text'],
    insertbackground="white"
)
quantum_entry.grid(row=2, column=1, padx=10, pady=8, sticky="w")

btn_frame = tk.Frame(input_frame, bg=COLORS['surface'])
btn_frame.grid(row=3, column=0, columnspan=3, pady=12)

generate_btn = tk.Button(
    btn_frame, text="⚡  Generate Fields",
    font=("Courier", 11, "bold"),
    bg=COLORS['blue'], fg=COLORS['bg'],
    padx=12, pady=5, cursor="hand2", relief="flat"
)
generate_btn.pack(side="left", padx=8)

run_btn = tk.Button(
    btn_frame, text="▶  Run Algorithm",
    font=("Courier", 11, "bold"),
    bg=COLORS['green'], fg=COLORS['bg'],
    padx=12, pady=5, cursor="hand2", relief="flat"
)
run_btn.pack(side="left", padx=8)

clear_btn = tk.Button(
    btn_frame, text="✕  Clear",
    font=("Courier", 11, "bold"),
    bg=COLORS['red'], fg=COLORS['bg'],
    padx=12, pady=5, cursor="hand2", relief="flat"
)
clear_btn.pack(side="left", padx=8)


# ================================================================
#  SCROLLABLE AREA
# ================================================================

scroll_container = tk.Frame(root, bg=COLORS['bg'])
scroll_container.pack(fill="both", expand=True, padx=40, pady=5)

scroll_canvas = tk.Canvas(scroll_container, bg=COLORS['bg'], highlightthickness=0)
scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=scroll_canvas.yview)
scroll_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
scroll_canvas.pack(side="left", fill="both", expand=True)

inner_frame = tk.Frame(scroll_canvas, bg=COLORS['bg'])
inner_window = scroll_canvas.create_window((0, 0), window=inner_frame, anchor="nw")


def on_frame_configure(e):
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))


def on_canvas_configure(e):
    scroll_canvas.itemconfig(inner_window, width=e.width)


inner_frame.bind("<Configure>", on_frame_configure)
scroll_canvas.bind("<Configure>", on_canvas_configure)


def on_mousewheel(e):
    scroll_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")


scroll_canvas.bind_all("<MouseWheel>", on_mousewheel)

fields_frame = tk.Frame(inner_frame, bg=COLORS['bg'])
fields_frame.pack(fill="x", pady=5)

result_frame = tk.Frame(inner_frame, bg=COLORS['bg'])
result_frame.pack(fill="x", pady=5)

chart_frame = tk.Frame(inner_frame, bg=COLORS['bg'])
chart_frame.pack(fill="x", pady=5)


# ================================================================
#  STATUS BAR
# ================================================================

status_var = tk.StringVar(value="Ready — Enter number of processes and click Generate")
tk.Label(
    root, textvariable=status_var,
    font=("Courier", 9),
    bg="#181825", fg=COLORS['subtext'],
    anchor="w", padx=10
).pack(side="bottom", fill="x")


# ================================================================
#  GENERATE FIELDS
# ================================================================

def generate_fields():
    global process_entries

    for w in fields_frame.winfo_children():
        w.destroy()
    for w in result_frame.winfo_children():
        w.destroy()
    for w in chart_frame.winfo_children():
        w.destroy()
    process_entries = []

    try:
        n = int(num_entry.get())
        if n <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid number of processes (minimum 1)")
        return

    header = tk.Frame(fields_frame, bg=COLORS['surface'])
    header.pack(fill="x", pady=(0, 3))

    for col, text in enumerate(["Process", "Arrival Time", "Burst Time"]):
        tk.Label(
            header, text=text,
            font=("Courier", 11, "bold"),
            bg=COLORS['surface'], fg=COLORS['blue'],
            width=18, anchor="center", pady=6
        ).grid(row=0, column=col, padx=4)

    for i in range(n):
        row_color = COLORS['surface'] if i % 2 == 0 else COLORS['surface2']
        row = tk.Frame(fields_frame, bg=row_color)
        row.pack(fill="x", pady=1)

        tk.Label(
            row, text=f"P{i+1}",
            font=("Courier", 11, "bold"),
            bg=row_color, fg=COLORS['mauve'],
            width=18, anchor="center", pady=5
        ).grid(row=0, column=0, padx=4)

        at_e = tk.Entry(
            row, font=("Courier", 11), width=18,
            bg=COLORS['surface2'], fg=COLORS['text'],
            insertbackground="white", justify="center"
        )
        at_e.grid(row=0, column=1, padx=4, pady=4)

        bt_e = tk.Entry(
            row, font=("Courier", 11), width=18,
            bg=COLORS['surface2'], fg=COLORS['text'],
            insertbackground="white", justify="center"
        )
        bt_e.grid(row=0, column=2, padx=4, pady=4)

        process_entries.append((at_e, bt_e))

    status_var.set(f"✅  {n} process fields ready — fill AT and BT then click Run")


generate_btn.config(command=generate_fields)


# ================================================================
#  CLEAR
# ================================================================

def clear_all():
    for w in fields_frame.winfo_children():
        w.destroy()
    for w in result_frame.winfo_children():
        w.destroy()
    for w in chart_frame.winfo_children():
        w.destroy()
    process_entries.clear()
    num_entry.delete(0, tk.END)
    quantum_entry.delete(0, tk.END)
    algo_var.set("FCFS")
    status_var.set("✅  Cleared — Ready for new input")


clear_btn.config(command=clear_all)


# ================================================================
#  GET PROCESS DATA
# ================================================================

def get_process_data():
    processes = []
    for i, (at_e, bt_e) in enumerate(process_entries):
        try:
            at = int(at_e.get())
            bt = int(bt_e.get())
            if at < 0 or bt <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                f"P{i+1}: Enter valid Arrival Time (≥ 0) and Burst Time (> 0)"
            )
            return None
        processes.append({'id': f'P{i+1}', 'arrival': at, 'burst': bt})
    return processes


# ================================================================
#  RESULT TABLE (INSIDE MAIN WINDOW)
# ================================================================

def show_result_table(result, title):
    for w in result_frame.winfo_children():
        w.destroy()

    tk.Label(
        result_frame, text=title,
        font=("Courier", 13, "bold"),
        bg=COLORS['bg'], fg=COLORS['yellow']
    ).pack(pady=(10, 4))

    table = tk.Frame(result_frame, bg=COLORS['surface'])
    table.pack(fill="x")

    headers = ["ID", "AT", "BT", "ST", "CT", "WT", "TAT"]
    for j, h in enumerate(headers):
        tk.Label(
            table, text=h,
            font=("Courier", 11, "bold"),
            bg=COLORS['surface'], fg=COLORS['blue'],
            width=11, anchor="center", pady=6
        ).grid(row=0, column=j, padx=2, pady=2)

    for i, p in enumerate(result):
        bg = COLORS['surface'] if i % 2 == 0 else COLORS['surface2']
        vals = [
            p['id'], p['arrival'], p['burst'],
            p.get('start', '-'), p['completion'],
            p['waiting'], p['turnaround']
        ]
        for j, v in enumerate(vals):
            tk.Label(
                table, text=str(v),
                font=("Courier", 11),
                bg=bg, fg=COLORS['text'],
                width=11, anchor="center", pady=5
            ).grid(row=i+1, column=j, padx=2, pady=1)

    avg_wt, avg_tat = calculate_avg(result)
    tk.Label(
        result_frame,
        text=f"Average Waiting Time: {avg_wt:.2f}     |     Average Turnaround Time: {avg_tat:.2f}",
        font=("Courier", 11, "bold"),
        bg=COLORS['bg'], fg=COLORS['green']
    ).pack(pady=8)


# ================================================================
#  GANTT CHART (INSIDE MAIN WINDOW)
# ================================================================

def plot_gantt(gantt, title):
    for w in chart_frame.winfo_children():
        w.destroy()

    tk.Label(
        chart_frame, text="Gantt Chart",
        font=("Courier", 13, "bold"),
        bg=COLORS['bg'], fg=COLORS['yellow']
    ).pack(pady=(10, 4))

    fig, ax = plt.subplots(figsize=(9, 3))
    fig.patch.set_facecolor('#1e1e2e')
    ax.set_facecolor('#313244')

    pids = list(dict.fromkeys([pid for pid, _, _ in gantt]))

    for pid, start, end in gantt:
        color = BAR_COLORS[pids.index(pid) % len(BAR_COLORS)]
        ax.barh(pid, end - start, left=start, color=color,
                edgecolor='#1e1e2e', height=0.5)
        ax.text((start + end) / 2, pid, f"{start}-{end}",
                ha='center', va='center', fontsize=8,
                color='#1e1e2e', fontweight='bold')

    ax.set_xlabel("Time", color='#cdd6f4')
    ax.set_ylabel("Processes", color='#cdd6f4')
    ax.set_title(title, color='#cdd6f4')
    ax.tick_params(colors='#cdd6f4')
    for spine in ax.spines.values():
        spine.set_edgecolor('#45475a')

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="x", pady=5)
    plt.close(fig)


# ================================================================
#  COMPARE ALL (INSIDE MAIN WINDOW)
# ================================================================

def compare_all(processes):
    for w in result_frame.winfo_children():
        w.destroy()
    for w in chart_frame.winfo_children():
        w.destroy()

    try:
        q = int(quantum_entry.get())
        if q <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid Time Quantum (> 0) for comparison")
        return

    fcfs_res  = fcfs(processes.copy())
    sjf_res   = sjf(processes.copy())
    rr_res, _ = round_robin(processes.copy(), q)

    fcfs_wt, fcfs_tat = calculate_avg(fcfs_res)
    sjf_wt,  sjf_tat  = calculate_avg(sjf_res)
    rr_wt,   rr_tat   = calculate_avg(rr_res)

    # Summary table
    tk.Label(
        result_frame, text="Algorithm Comparison — Summary",
        font=("Courier", 13, "bold"),
        bg=COLORS['bg'], fg=COLORS['yellow']
    ).pack(pady=(10, 4))

    table = tk.Frame(result_frame, bg=COLORS['surface'])
    table.pack(fill="x")

    for j, h in enumerate(["Algorithm", "Avg WT", "Avg TAT", "Score (WT+TAT)"]):
        tk.Label(
            table, text=h,
            font=("Courier", 11, "bold"),
            bg=COLORS['surface'], fg=COLORS['blue'],
            width=16, anchor="center", pady=6
        ).grid(row=0, column=j, padx=2, pady=2)

    data = [
        ("FCFS",        fcfs_wt, fcfs_tat),
        ("SJF",         sjf_wt,  sjf_tat),
        ("Round Robin", rr_wt,   rr_tat),
    ]
    best_score = min(wt + tat for _, wt, tat in data)

    for i, (algo, wt, tat) in enumerate(data):
        score = wt + tat
        bg = COLORS['surface'] if i % 2 == 0 else COLORS['surface2']
        fg = COLORS['green'] if abs(score - best_score) < 0.01 else COLORS['text']
        for j, v in enumerate([algo, f"{wt:.2f}", f"{tat:.2f}", f"{score:.2f}"]):
            tk.Label(
                table, text=v,
                font=("Courier", 11, "bold" if fg == COLORS['green'] else "normal"),
                bg=bg, fg=fg,
                width=16, anchor="center", pady=5
            ).grid(row=i+1, column=j, padx=2, pady=1)

    # Graphs
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    fig.patch.set_facecolor('#1e1e2e')
    algos  = ['FCFS', 'SJF', 'RR']
    colors = [COLORS['blue'], COLORS['green'], COLORS['mauve']]

    for ax in axes:
        ax.set_facecolor('#313244')
        ax.tick_params(colors='#cdd6f4')
        for spine in ax.spines.values():
            spine.set_edgecolor('#45475a')

    bars1 = axes[0].bar(algos, [fcfs_wt, sjf_wt, rr_wt],
                        color=colors, edgecolor='#1e1e2e')
    axes[0].set_title("Average Waiting Time",    color='#cdd6f4')
    axes[0].set_xlabel("Algorithm",              color='#cdd6f4')
    axes[0].set_ylabel("Time",                   color='#cdd6f4')
    for bar, v in zip(bars1, [fcfs_wt, sjf_wt, rr_wt]):
        axes[0].text(bar.get_x() + bar.get_width() / 2,
                     v + 0.1, f"{v:.2f}", ha='center',
                     fontweight='bold', color='#cdd6f4')

    bars2 = axes[1].bar(algos, [fcfs_tat, sjf_tat, rr_tat],
                        color=colors, edgecolor='#1e1e2e')
    axes[1].set_title("Average Turnaround Time", color='#cdd6f4')
    axes[1].set_xlabel("Algorithm",              color='#cdd6f4')
    axes[1].set_ylabel("Time",                   color='#cdd6f4')
    for bar, v in zip(bars2, [fcfs_tat, sjf_tat, rr_tat]):
        axes[1].text(bar.get_x() + bar.get_width() / 2,
                     v + 0.1, f"{v:.2f}", ha='center',
                     fontweight='bold', color='#cdd6f4')

    plt.suptitle("CPU Scheduling — Algorithm Comparison",
                 fontsize=12, fontweight='bold', color='#cdd6f4')
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="x", pady=5)
    plt.close(fig)


# ================================================================
#  SUGGEST BEST (POPUP) — FIXED
# ================================================================

def suggest_best(processes):
    bursts = [p['burst'] for p in processes]
    n      = len(processes)
    variance = statistics.variance(bursts) if len(bursts) > 1 else 0

    try:
        q = int(quantum_entry.get())
        if q <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid Time Quantum (> 0) for suggestion")
        return

    fcfs_res  = fcfs(processes.copy())
    sjf_res   = sjf(processes.copy())
    rr_res, _ = round_robin(processes.copy(), q)

    fcfs_wt, fcfs_tat = calculate_avg(fcfs_res)
    sjf_wt,  sjf_tat  = calculate_avg(sjf_res)
    rr_wt,   rr_tat   = calculate_avg(rr_res)

    scores = {
        "FCFS":        round(fcfs_wt + fcfs_tat, 4),
        "SJF":         round(sjf_wt  + sjf_tat,  4),
        "Round Robin": round(rr_wt   + rr_tat,   4),
    }

    # Step 1 — find actual minimum score
    min_score = min(scores.values())

    # Step 2 — find all algos within 5% of best score
    threshold = min_score * 0.05 if min_score > 0 else 0.5
    best_algos = [k for k, v in scores.items() if abs(v - min_score) <= threshold]

    # Step 3 — clear winner
    if len(best_algos) == 1:
        best   = best_algos[0]
        reason = f"Lowest combined WT + TAT score ({min_score:.2f}) among all algorithms."

    # Step 4 — tie: break using input characteristics
    else:
        if variance < 3:
            best   = "FCFS"
            reason = "Tied — burst times are very similar, FCFS is simplest and equally efficient."
        elif variance >= 3 and n <= 5:
            best   = "SJF"
            reason = "Tied — burst variance is high, SJF minimizes waiting time for short jobs."
        elif n > 5:
            best   = "Round Robin"
            reason = "Tied — many processes detected, RR ensures fair CPU distribution."
        else:
            best   = "SJF"
            reason = "Tied — SJF is theoretically optimal for minimizing average waiting time."

    # Popup
    win = tk.Toplevel(root)
    win.title("Algorithm Suggestion")
    win.configure(bg=COLORS['bg'])
    win.geometry("520x420")

    tk.Label(
        win, text="🤖  Algorithm Suggestion",
        font=("Courier", 15, "bold"),
        bg=COLORS['bg'], fg=COLORS['blue']
    ).pack(pady=15)

    table = tk.Frame(win, bg=COLORS['surface'], padx=15, pady=10)
    table.pack(padx=20, fill="x")

    for j, h in enumerate(["Algorithm", "Avg WT", "Avg TAT", "Score"]):
        tk.Label(
            table, text=h,
            font=("Courier", 11, "bold"),
            bg=COLORS['surface'], fg=COLORS['blue'],
            width=13, anchor="center", pady=5
        ).grid(row=0, column=j, padx=2)

    rows = [
        ("FCFS",        fcfs_wt, fcfs_tat),
        ("SJF",         sjf_wt,  sjf_tat),
        ("Round Robin", rr_wt,   rr_tat),
    ]

    for i, (algo, wt, tat) in enumerate(rows):
        score = scores[algo]
        bg    = COLORS['surface'] if i % 2 == 0 else COLORS['surface2']
        fg    = COLORS['green'] if algo == best else COLORS['text']
        for j, v in enumerate([algo, f"{wt:.2f}", f"{tat:.2f}", f"{score:.2f}"]):
            tk.Label(
                table, text=v,
                font=("Courier", 11, "bold" if fg == COLORS['green'] else "normal"),
                bg=bg, fg=fg,
                width=13, anchor="center", pady=4
            ).grid(row=i+1, column=j, padx=2, pady=1)

    tk.Label(
        win, text=f"✅  BEST ALGORITHM:  {best}",
        font=("Courier", 13, "bold"),
        bg=COLORS['bg'], fg=COLORS['green']
    ).pack(pady=(15, 4))

    tk.Label(
        win, text=f"Reason: {reason}",
        font=("Courier", 10),
        bg=COLORS['bg'], fg=COLORS['subtext'],
        wraplength=460
    ).pack()

    tk.Label(
        win,
        text=f"Processes: {n}     Avg Burst: {sum(bursts)/n:.2f}     Variance: {variance:.2f}",
        font=("Courier", 10),
        bg=COLORS['bg'], fg=COLORS['subtext']
    ).pack(pady=8)


# ================================================================
#  RUN ALGORITHM
# ================================================================

def run_algorithm():
    if not process_entries:
        messagebox.showerror("No Input", "Click Generate Fields first")
        return

    processes = get_process_data()
    if processes is None:
        return

    algo = algo_var.get()

    if algo == "FCFS":
        result = fcfs(processes)
        gantt  = [(p['id'], p['start'], p['completion']) for p in result]
        show_result_table(result, "Results — FCFS")
        plot_gantt(gantt, "Gantt Chart — FCFS")

    elif algo == "SJF":
        result = sjf(processes)
        gantt  = [(p['id'], p['start'], p['completion']) for p in result]
        show_result_table(result, "Results — SJF")
        plot_gantt(gantt, "Gantt Chart — SJF")

    elif algo == "Round Robin":
        try:
            q = int(quantum_entry.get())
            if q <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a valid Time Quantum (> 0)")
            return
        result, gantt = round_robin(processes, q)
        show_result_table(result, "Results — Round Robin")
        plot_gantt(gantt, "Gantt Chart — Round Robin")

    elif algo == "Compare All":
        compare_all(processes)

    elif algo == "Suggest Best":
        suggest_best(processes)

    status_var.set(f"✅  {algo} executed successfully")


run_btn.config(command=run_algorithm)


# ================================================================
#  START
# ================================================================

root.mainloop()
