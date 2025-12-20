#!/usr/bin/env python3
import csv
import os
import sys

import matplotlib
import yaml

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def get_bogo_ops(file_path):
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        # Handle the YAML structure from stress-ng
        if "metrics" in data:
            for item in data["metrics"]:
                if "stressor" in item and item["stressor"] in [
                    "cpu",
                    "vm",
                    "hdd",
                    "iomix",
                    "fallocate",
                ]:
                    if "bogo-ops" in item:
                        return item["bogo-ops"]
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        pass
    return 0


# Create plots directory if it doesn't exist
os.makedirs("report/plots", exist_ok=True)

# Extract data from YAML files
cpu_single = get_bogo_ops("report/results/cpu_single.yaml")
cpu_multi = get_bogo_ops("report/results/cpu_multi.yaml")
cpu_all = get_bogo_ops("report/results/cpu_all.yaml")
mem_single = get_bogo_ops("report/results/mem_single.yaml")
mem_multi = get_bogo_ops("report/results/mem_multi.yaml")

# Extract disk IO test data
disk_write_test = get_bogo_ops("report/results/disk_write_test.yaml")
disk_io_test = get_bogo_ops("report/results/disk_io_test.yaml")
disk_fallocate_test = get_bogo_ops("report/results/disk_fallocate_test.yaml")

# Plot CPU performance
plt.figure(figsize=(10, 6))
bars = plt.bar(
    ["Single Core", "Multi Core", "All Cores"], [cpu_single, cpu_multi, cpu_all]
)
plt.bar_label(bars)
plt.title("CPU Stress Test Performance")
plt.ylabel("Bogo Operations")
plt.savefig("report/plots/cpu_performance.png")
plt.close()

# Plot Memory performance
plt.figure(figsize=(10, 6))
bars = plt.bar(["Single VM", "Multi VM"], [mem_single, mem_multi])
plt.bar_label(bars)
plt.title("Memory Stress Test Performance")
plt.ylabel("Bogo Operations")
plt.savefig("report/plots/memory_performance.png")
plt.close()

# Plot Disk IO performance
plt.figure(figsize=(10, 6))
bars = plt.bar(
    ["HDD Write", "IO Mix", "Fallocate"],
    [disk_write_test, disk_io_test, disk_fallocate_test],
)
plt.bar_label(bars)
plt.title("Disk IO Stress Test Performance")
plt.ylabel("Bogo Operations")
plt.savefig("report/plots/disk_io_performance.png")
plt.close()

# Plot GPU performance if requested and data is available
if "--with-gpu" in sys.argv:
    gpu_data = []
    csv_file = "report/results/gpu_burn_data.csv"

    if os.path.exists(csv_file):
        try:
            with open(csv_file, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 3 and row[0] != "result":
                        percent = float(row[0])
                        gflops = float(row[1])
                        temp = float(row[2])
                        gpu_data.append((percent, gflops, temp))
        except Exception as e:
            print(f"Error reading GPU data: {e}")

    if gpu_data:
        # Sort by percentage to ensure proper order
        gpu_data.sort(key=lambda x: x[0])

        # Extract separate arrays for plotting
        percents = [x[0] for x in gpu_data]
        gflops = [x[1] for x in gpu_data]
        temps = [x[2] for x in gpu_data]

        # Create GPU performance plot
        plt.figure(figsize=(10, 6))
        plt.plot(percents, gflops, "b-", marker="o")
        plt.title("GPU Performance During Stress Test")
        plt.xlabel("Test Completion (%)")
        plt.ylabel("Performance (Gflop/s)")
        plt.grid(True)
        plt.savefig("report/plots/gpu_performance.png")
        plt.close()

        # Create GPU temperature plot
        plt.figure(figsize=(10, 6))
        plt.plot(percents, temps, "r-", marker="s")
        plt.title("GPU Temperature During Stress Test")
        plt.xlabel("Test Completion (%)")
        plt.ylabel("Temperature (°C)")
        plt.grid(True)
        plt.savefig("report/plots/gpu_temperature.png")
        plt.close()

        # Create combined GPU metrics plot
        fig, ax1 = plt.subplots(figsize=(10, 6))
        color = "tab:blue"
        ax1.set_xlabel("Test Completion (%)")
        ax1.set_ylabel("Performance (Gflop/s)", color=color)
        ax1.plot(percents, gflops, color=color, marker="o", label="Performance")
        ax1.tick_params(axis="y", labelcolor=color)

        ax2 = ax1.twinx()
        color = "tab:red"
        ax2.set_ylabel("Temperature (°C)", color=color)
        ax2.plot(percents, temps, color=color, marker="s", label="Temperature")
        ax2.tick_params(axis="y", labelcolor=color)

        plt.title("GPU Performance and Temperature During Stress Test")
        fig.tight_layout()
        plt.savefig("report/plots/gpu_combined.png")
        plt.close()

        print("GPU plots generated in report/plots/")
    else:
        print("No GPU data available for plotting")

print("Plots generated in report/plots/")
