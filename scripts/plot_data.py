#!/usr/bin/env python3
import csv
import json
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
    # First, try to plot GPU burn test data
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

        print("GPU burn test plots generated in report/plots/")
    else:
        print("No GPU burn test data available for plotting")

    # Now, try to plot glmark2 benchmark data
    glmark2_plot_file = "report/results/glmark2_plot_data.json"
    if os.path.exists(glmark2_plot_file):
        try:
            import json

            with open(glmark2_plot_file, "r") as f:
                plot_data = json.load(f)

            # Create a horizontal bar chart for glmark2 test results
            plt.figure(figsize=(12, 10))
            test_names = plot_data.get("test_names", [])
            fps_values = plot_data.get("fps_values", [])

            # Create the plot
            y_pos = range(len(test_names))
            bars = plt.barh(y_pos, fps_values, align="center")
            plt.yticks(y_pos, test_names)
            plt.xlabel("FPS (Frames Per Second)")
            plt.title("glmark2 Benchmark Results")

            # Add value labels to bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                plt.text(
                    width + max(fps_values) * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"{fps_values[i]}",
                    ha="left",
                    va="center",
                )

            plt.tight_layout()
            plt.savefig("report/plots/glmark2_benchmark.png")
            plt.close()

            # Also create a summary plot if overall score is available
            glmark2_data_file = "report/results/glmark2_data.json"
            if os.path.exists(glmark2_data_file):
                with open(glmark2_data_file, "r") as f:
                    glmark2_data = json.load(f)

                if "overall_score" in glmark2_data and "opengl_info" in glmark2_data:
                    score = glmark2_data["overall_score"]
                    renderer = glmark2_data["opengl_info"].get("renderer", "Unknown")

                    plt.figure(figsize=(8, 6))
                    plt.bar(["glmark2 Score"], [score], color="green")
                    plt.title(f"GPU Benchmark Score\n{renderer}")
                    plt.ylabel("Score")

                    # Add score value as text
                    plt.text(
                        0, score + score * 0.02, str(score), ha="center", fontsize=14
                    )

                    plt.ylim(0, score + score * 0.2)  # Add space above for text
                    plt.tight_layout()
                    plt.savefig("report/plots/glmark2_score.png")
                    plt.close()

            print("glmark2 benchmark plots generated in report/plots/")
        except Exception as e:
            print(f"Error generating glmark2 plots: {e}")
    else:
        print("No glmark2 data available for plotting")

print("Plots generated in report/plots/")
