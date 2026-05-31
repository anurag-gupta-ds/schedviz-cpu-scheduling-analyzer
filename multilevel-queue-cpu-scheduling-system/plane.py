from collections import deque

# ================================================================
# 🔧 PROCESS CLASS
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


# ================================================================
# 🔧 FCFS (Queue 1 & Queue 3)
# ================================================================
def fcfs(queue, time, gantt):
    while queue:
        p = queue.popleft()

        if time < p.arrival:
            time = p.arrival

        p.start = time
        gantt.append((p.pid, time, time + p.burst))

        time += p.burst

        p.completion = time
        p.turnaround = p.completion - p.arrival
        p.waiting = p.turnaround - p.burst

    return time


# ================================================================
# 🔧 ROUND ROBIN (Queue 2)
# ================================================================
def round_robin(queue, quantum, time, gantt):
    q = deque(queue)

    while q:
        p = q.popleft()

        if time < p.arrival:
            time = p.arrival

        if p.start == -1:
            p.start = time

        exec_time = min(p.remaining, quantum)
        gantt.append((p.pid, time, time + exec_time))

        time += exec_time
        p.remaining -= exec_time

        if p.remaining > 0:
            q.append(p)
        else:
            p.completion = time
            p.turnaround = p.completion - p.arrival
            p.waiting = p.turnaround - p.burst

    return time


# ================================================================
# 🔧 MULTILEVEL QUEUE SCHEDULER
# ================================================================
def scheduler(processes, quantum):

    # Step 1: Create Queues
    q1, q2, q3 = deque(), deque(), deque()

    # Step 2 & 3: Assign to Queues
    for p in processes:
        if p.type == "System":
            q1.append(p)
        elif p.type == "Interactive":
            q2.append(p)
        else:
            q3.append(p)

    # Sort by arrival time
    q1 = deque(sorted(q1, key=lambda x: x.arrival))
    q2 = deque(sorted(q2, key=lambda x: x.arrival))
    q3 = deque(sorted(q3, key=lambda x: x.arrival))

    gantt = []
    time = 0

    # Step 5: Priority execution
    time = fcfs(q1, time, gantt)
    time = round_robin(q2, quantum, time, gantt)
    time = fcfs(q3, time, gantt)

    return processes, gantt


# ================================================================
# 🔧 INPUT
# ================================================================
n = int(input("Enter number of processes: "))
quantum = int(input("Enter Time Quantum (for RR): "))

processes = []

for i in range(n):
    print(f"\nProcess P{i+1}:")
    at = int(input("Arrival Time: "))
    bt = int(input("Burst Time: "))
    ptype = input("Type (System / Interactive / Batch): ")

    processes.append(Process(f"P{i+1}", at, bt, ptype))


# ================================================================
# 🔧 RUN SCHEDULER
# ================================================================
processes, gantt = scheduler(processes, quantum)


# ================================================================
# 🔧 OUTPUT
# ================================================================
print("\nProcess Table:")
print("PID\tAT\tBT\tWT\tTAT")

total_wt = 0
total_tat = 0

for p in processes:
    print(f"{p.pid}\t{p.arrival}\t{p.burst}\t{p.waiting}\t{p.turnaround}")
    total_wt += p.waiting
    total_tat += p.turnaround

# Averages
avg_wt = total_wt / n
avg_tat = total_tat / n

print(f"\nAverage Waiting Time = {avg_wt:.2f}")
print(f"Average Turnaround Time = {avg_tat:.2f}")


# ================================================================
# 🔧 GANTT CHART (TEXT)
# ================================================================
print("\nGantt Chart:")
for pid, start, end in gantt:
    print(f"| {pid} ({start}-{end}) ", end="")
print("|")