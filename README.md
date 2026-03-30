# ⚙️ SchedViz — CPU Scheduling Analyzer

> A modern desktop application built with Python that simulates and visualizes core CPU Scheduling algorithms used in Operating Systems.
> It combines interactive GUI, performance analysis, and data visualization to help understand scheduling behavior intuitively.

---

## 📌 Overview

SchedViz demonstrates how an Operating System schedules processes on the CPU.

In this project, you can:

- Simulate multiple scheduling algorithms
- Visualize execution using Gantt Charts
- Compare performance metrics
- Get an intelligent recommendation for the best algorithm

---

## ✨ Features

- ⚡ FCFS (First Come First Serve)
- ⚡ SJF (Shortest Job First)
- ⚡ Round Robin Scheduling

### 📊 Result Table
- AT, BT, ST, CT, WT, TAT
- Average Waiting Time & Turnaround Time

### 📈 Visualization
- Gantt Chart embedded inside the GUI

### 🔍 Analysis
- Compare all algorithms side-by-side
- Smart algorithm recommendation

### 🎨 Interface
- Dark themed UI (Tkinter)
- Scrollable layout

### ✅ Additional Features
- Input validation & error handling
- One-click reset

---

## 🛠️ Tech Stack

- Python 3.x
- Tkinter
- Matplotlib
- Statistics Module

---

## ⚙️ Implemented Algorithms

### 🔹 FCFS — First Come First Serve
- Executes processes in arrival order
- Simple and easy to implement
- ❌ Can cause convoy effect

### 🔹 SJF — Shortest Job First
- Selects process with smallest burst time
- ✅ Minimizes average waiting time
- ❌ May cause starvation

### 🔹 Round Robin
- Uses fixed time quantum
- ✅ Ensures fairness
- ❌ Small quantum → high context switching

---

## 🤖 Smart Recommendation Logic

SchedViz doesn't just simulate — it analyzes and recommends:

- Run all three algorithms
- Compute:
Score = Average Waiting Time + Average Turnaround Time

- Select the algorithm with the minimum score

### 🧠 Tie-breaking Strategy
- Low variance → FCFS
- Moderate variance & small input → SJF
- Large number of processes → Round Robin

---

## 📐 OS Concepts Covered

- Arrival Time (AT), Burst Time (BT)
- Start Time (ST), Completion Time (CT)
- Waiting Time (WT), Turnaround Time (TAT)
- Ready Queue & Scheduling
- CPU Idle Handling
- Context Switching
- Starvation & Convoy Effect

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/anurag-gupta-ds/schedviz-cpu-scheduling-analyzer.git
cd schedviz-cpu-scheduling-analyzer
```

### 2. Install dependencies
```bash
pip install matplotlib
```

### 3. Run the application
```bash
python gui.py
```

---

## 📂 Project Structure
schedviz-cpu-scheduling-analyzer/
│
├── gui.py              # Main GUI application
├── README.md           # Documentation
└── screenshots/        # UI previews
├── main_window.png
├── fcfs_gantt.png
├── compare_all.png
└── suggest_best.png

---

## 📊 Usage Guide

- Enter number of processes
- Click Generate Fields
- Input Arrival Time & Burst Time
- Select algorithm
- (Optional) Enter Time Quantum for Round Robin
- Click Run Algorithm
- Scroll to view results and charts

---

## 📸 Screenshots

- Main Interface
- FCFS with Gantt Chart
- Algorithm Comparison
- Smart Suggestion

(Add images inside `/screenshots` folder)

---

## 👨‍💻 Author

Anurag Gupta

---

## 🏷️ Tags

`python` `tkinter` `matplotlib` `cpu-scheduling` `operating-systems` `gantt-chart` `gui` `data-visualization`

---

## ⭐ Final Note

> SchedViz is not just a simulator — it's a learning tool + analyzer that helps you understand how scheduling decisions impact system performance.
