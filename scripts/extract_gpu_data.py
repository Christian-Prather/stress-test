#!/usr/bin/env python3
import os
import re
import sys


def extract_gpu_data(log_file):
    """
    Extract GPU performance data from gpu_burn log for plotting
    """
    if not os.path.exists(log_file):
        print(f"Error: Log file '{log_file}' not found", file=sys.stderr)
        return None, None

    data = []
    with open(log_file, "r") as f:
        for line in f:
            if "proc'd:" in line:
                # Extract percentage, Gflops, and temperature
                match = re.search(
                    r"([\d.]+)%.*proc.d:.*\(([\d]+) Gflop/s\).*temps: ([\d]+) C", line
                )
                if match:
                    percent = float(match.group(1))
                    gflops = float(match.group(2))
                    temp = float(match.group(3))
                    data.append((percent, gflops, temp))

    # Check test result
    result = "UNKNOWN"
    with open(log_file, "r") as f:
        content = f.read()
        if "OK" in content:
            result = "PASS"
        elif any(word in content for word in ["FAILED", "ERROR", "DIED"]):
            result = "FAIL"

    return data, result


def save_csv_data(data, result, output_file):
    """
    Save extracted data to CSV format for easier plotting
    """
    with open(output_file, "w") as f:
        f.write("percentage,gflops,temperature\n")
        for percent, gflops, temp in data:
            f.write(f"{percent},{gflops},{temp}\n")
        f.write(f"result,{result}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_gpu_data.py <gpu_burn_log_file>", file=sys.stderr)
        sys.exit(1)

    log_file = sys.argv[1]
    data, result = extract_gpu_data(log_file)

    if data is None:
        sys.exit(1)

    # Save CSV data
    output_csv = log_file.replace(".log", "_data.csv")
    save_csv_data(data, result, output_csv)

    print(f"Extracted {len(data)} data points to {output_csv}")
    print(f"Test result: {result}")
