import time
import matplotlib.pyplot as plt
import seaborn as sns

print("SMART TRAFFIC SIGNAL SIMULATION")
print("--------------------------------")

# Roads at intersection
roads = ["Road A", "Road B", "Road C", "Road D"]

traffic = {}
emergency = {}

# -------- INPUT (Simulating sensors) --------
for road in roads:
    traffic[road] = int(input(f"Enter number of vehicles on {road}: "))
    emergency_input = input(f"Is there an emergency vehicle on {road}? (yes/no): ")
    emergency[road] = emergency_input.lower() == "yes"


# --------  1 GREEN TIME CALCULATION --------
def calculate_green_time(vehicle_count):
    green_time = vehicle_count * 2
    if green_time < 15:
        return 15
    elif green_time > 60:
        return 60
    else:
        return green_time


# -------- 2 TRAFFIC LEVEL CLASSIFICATION --------
def traffic_level(count):
    if count < 50:
        return "Low"
    elif count < 200:
        return "Medium"
    else:
        return "High"


# -------- 3 COUNTDOWN TIMER --------
def countdown(seconds):
    for i in range(seconds, 0, -5):
        print(f"   ⏳ {i} seconds remaining")
        time.sleep(1)


# -------- DETECT EMERGENCY ROADS --------
emergency_roads = []
for road in roads:
    if emergency[road]:
        emergency_roads.append(road)


# -------- CALCULATE GREEN TIMES --------
green_times = {}
for road in roads:
    green_times[road] = calculate_green_time(traffic[road])


# -------- 4 HIGHEST TRAFFIC ALERT --------
max_road = max(traffic, key=traffic.get)
print(f"\n⚠️ Highest traffic detected on {max_road} ({traffic[max_road]} vehicles)")



# ---- 5 QUEUE SPILLBACK PREVENTION ----


# Simulated downstream road capacity (vehicles that can exit)
downstream_capacity = {
    "Road A": 30,
    "Road B": 10,   # narrow exit
    "Road C": 50,
    "Road D": 15
}

spillback_risk = {}

for road in roads:
    spillback_risk[road] = traffic[road] > downstream_capacity[road]
    if spillback_risk[road]:
        print(f"⚠️ Spillback risk on {road} (downstream congested)")


# -------- SORT ROADS BY PRIORITY --------
# Priority order:
# 1. Emergency roads
# 2. No spillback risk
# 3. Higher green time

sorted_roads = sorted(
    green_times.items(),
    key=lambda x: (
        not emergency[x[0]],       # emergency first
        spillback_risk[x[0]],      # deprioritize spillback
        -x[1]                      # higher green time
    )
)


# -------- SIGNAL SIMULATION --------
print("\n--- SIGNAL OPERATION STARTED ---\n")

# -------- FEATURE 5: EMERGENCY OVERRIDE --------
if emergency_roads:
    print("🚨 EMERGENCY OVERRIDE ACTIVE 🚨\n")
    for road in emergency_roads:
        print(f"{road} → GREEN SIGNAL OVERRIDE (60 seconds)")
        countdown(60)


# -------- NORMAL TRAFFIC CYCLE --------
print("\nNORMAL TRAFFIC SIGNAL CYCLE\n")
for road, time_sec in sorted_roads:
    if spillback_risk[road]:
        print(f"\n{road} GREEN LIMITED (spillback prevention)")
        countdown(15)
    else:
        print(f"\n{road} GREEN for {time_sec} seconds")
        countdown(time_sec)

print("\n--- SIGNAL CYCLE COMPLETE ---")


# -------- SUMMARY --------
print("\n--- TRAFFIC SUMMARY ---")
for road in roads:
    level = traffic_level(traffic[road])
    spill = "YES" if spillback_risk[road] else "NO"
    print(
        f"{road} | Vehicles: {traffic[road]} | "
        f"Traffic Level: {level} | Emergency: {emergency[road]} | "
        f"Spillback Risk: {spill}"
    )


# -------- GRAPH --------
vehicle_counts = list(traffic.values())


# Colors: emergency = red, spillback = orange, normal = blue
colors = []
for road in roads:
    if emergency[road]:
        colors.append('#d62728')
    elif spillback_risk[road]:
        colors.append('#ff7f0e')
    else:
        colors.append('#1f77b4')

sns.set_theme(style="darkgrid")

fig, ax = plt.subplots(figsize=(8,6))
bars = ax.bar(roads, vehicle_counts, color=colors,
              edgecolor='black', linewidth=1.2)

# -------- SHOW VEHICLES + GREEN TIME ON GRAPH --------
for i, bar in enumerate(bars):
    vehicles = bar.get_height()
    green_time = green_times[roads[i]]
    label = f"{vehicles} vehicles\n{green_time} sec"
    if spillback_risk[roads[i]]:
        label += "\n(spillback)"

    ax.text(
        bar.get_x() + bar.get_width()/2,
        vehicles + 5,
        label,
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold'
    )

ax.set_title("Traffic Density with Spillback Prevention", fontsize=16, fontweight='bold')
ax.set_xlabel("Roads", fontsize=13)
ax.set_ylabel("Vehicle Count", fontsize=13)

plt.tight_layout()
plt.show()
