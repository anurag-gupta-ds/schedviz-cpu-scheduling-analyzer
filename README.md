⚙️ SchedViz — CPU Scheduling Analyzer
A Python-based desktop application that simulates and visualizes CPU Scheduling algorithms used in Operating Systems. Built with Python, Tkinter and Matplotlib.

📸 Screenshots
Main Window
FCFS Result + Gantt Chart
Algorithm Comparison
Smart Algorithm Suggestion

📌 Description
SchedViz simulates how an Operating System decides which process runs on the CPU and in what order. It implements three scheduling algorithms, visualizes results as a Gantt chart, compares all algorithms on the same input and intelligently recommends the best algorithm based on actual performance scores.

✅ Features

FCFS — First Come First Serve scheduling
SJF — Shortest Job First scheduling
Round Robin — Time quantum based scheduling
Result Table — Shows ID, AT, BT, ST, CT, WT, TAT with averages
Gantt Chart — Embedded inside the app with time labels
Compare All — Runs all 3 algorithms and shows dual bar graphs
Suggest Best — Smart recommendation based on actual performance scores
Dark Theme GUI — Built with Tkinter
Input Validation — Error popups for invalid input
Clear / Reset — One click to reset everything
Scrollable Window — Scroll to see results and charts


🛠️ Tech Stack
ToolPurposePython 3.10Core languageTkinterGUI window and widgetsMatplotlibGantt charts and bar graphsStatisticsVariance calculation for smart suggestion

⚙️ Algorithms
1. FCFS — First Come First Serve
Executes processes in the order they arrive. Simple and easy to implement but can cause convoy effect.
2. SJF — Shortest Job First
Picks the process with the shortest burst time from the ready queue. Minimizes average waiting time but can cause starvation.
3. Round Robin
Each process gets a fixed time quantum. Ensures fairness but too small quantum causes excessive context switching.

🤖 Smart Suggestion Logic
1. Run all 3 algorithms on the given input
2. Calculate Score = Avg WT + Avg TAT for each
3. Find the minimum score
4. If clear winner → recommend directly
5. If tie:
   - Variance < 3       → FCFS  (similar burst times)
   - Variance >= 3, n≤5 → SJF   (varied burst times)
   - n > 5              → RR    (many processes, fairness)

📐 OS Concepts Covered

Arrival Time, Burst Time, Start Time
Completion Time, Waiting Time, Turnaround Time
Ready Queue, Context Switching
CPU Idle Handling, Starvation, Convoy Effect


🚀 How to Run
1. Clone the repository
bashgit clone https://github.com/anurag-gupta-ds/schedviz-cpu-scheduling-analyzer.git
cd schedviz-cpu-scheduling-analyzer
2. Install dependencies
bashpip install matplotlib
3. Run the GUI version
bashpy -3.14 gui.py

📁 Project Structure
schedviz-cpu-scheduling-analyzer/
│                       # Terminal version
├── gui.py              # GUI version with Tkinter                                  
├── README.md           # Project documentation
└── screenshots/        # App screenshots
    ├── main_window.png
    ├── fcfs_gantt.png
    ├── compare_all.png
    └── suggest_best.png

📊 How to Use

Enter number of processes and click Generate Fields
Fill Arrival Time and Burst Time for each process
Select algorithm from dropdown
For Round Robin, enter Time Quantum
Click Run Algorithm
Scroll down to see results and Gantt chart

👨‍💻 Author
Anurag Gupta

🏷️ Tags
python tkinter matplotlib cpu-scheduling operating-systems gantt-chart gui data-visualization
