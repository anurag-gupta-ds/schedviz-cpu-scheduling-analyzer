
# ⚡ Multilevel Queue CPU Scheduling System 

A Python-based Operating System project that demonstrates the working of the **Multilevel Queue (MLQ) CPU Scheduling Algorithm** using a graphical user interface built with Tkinter.

## 📌 Project Overview

This project simulates CPU scheduling by dividing processes into multiple queues based on their type and executing them according to predefined scheduling algorithms and priorities.

The scheduler classifies processes into:

- Queue 1 (System Processes) → FCFS
- Queue 2 (Interactive Processes) → Round Robin
- Queue 3 (Batch Processes) → FCFS

Queues are executed according to their priority:

**Q1 > Q2 > Q3**

---

## 🎯 Objectives

- Understand CPU Scheduling concepts.
- Implement Multilevel Queue Scheduling.
- Compare FCFS and Round Robin scheduling.
- Calculate Waiting Time and Turnaround Time.
- Visualize execution using a Gantt Chart.

---

## 🛠 Technologies Used

- Python
- Tkinter (GUI)
- Matplotlib (Gantt Chart Visualization)
- Collections (Deque)

---

## 📚 Operating System Concepts Used

- Process Management
- CPU Scheduling
- Multilevel Queue Scheduling
- Priority Scheduling
- FCFS Scheduling
- Round Robin Scheduling
- Process States
- Waiting Time
- Turnaround Time

---

## 🗂 Queue Structure

| Queue | Process Type | Algorithm |
|---------|------------|-----------|
| Q1 | System | FCFS |
| Q2 | Interactive | Round Robin |
| Q3 | Batch | FCFS |

Priority Order:

```text
Q1 → Highest Priority
Q2 → Medium Priority
Q3 → Lowest Priority
```

---

## 📊 Features

- Dynamic Process Input
- Process Classification
- FCFS Scheduling
- Round Robin Scheduling
- Waiting Time Calculation
- Turnaround Time Calculation
- Queue-wise Execution Display
- Process State Tracking
- Gantt Chart Visualization
- Average WT and TAT Calculation
- Modern Dark-Themed GUI

---

## 🧮 Performance Metrics

### Waiting Time (WT)

```text
WT = Turnaround Time - Burst Time
```

### Turnaround Time (TAT)

```text
TAT = Completion Time - Arrival Time
```

---

## 📈 Output

The system displays:

- Waiting Time of each process
- Turnaround Time of each process
- Process State
- Queue-wise Execution Order
- Average Waiting Time
- Average Turnaround Time
- Gantt Chart

---

## 🏗 Project Structure

### 1
- Process Class
- Process Attributes
- Queue Creation
- Process Assignment

### 2
- FCFS Scheduling Algorithm

### 3
- Round Robin Scheduling Algorithm

### 4
- GUI Development
- Result Display
- Gantt Chart Visualization

---

## 🚀 How to Run

1. Install Python 3.x
2. Install required libraries:

```bash
pip install matplotlib
```

3. Run the program:

```bash
python mlq_scheduler.py
```

---

## 📖 Sample Input

| PID | AT | BT | Type |
|-----|----|----|------|
| P1 | 0 | 5 | System |
| P2 | 1 | 4 | Interactive |
| P3 | 2 | 6 | Batch |

Time Quantum:

```text
2
```

---

---

## 👨‍💻 Author

Developed as an Operating System Mini Project demonstrating the implementation of the Multilevel Queue CPU Scheduling Algorithm.
