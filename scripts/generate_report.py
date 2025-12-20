#!/usr/bin/env python3
import os
import sys
from datetime import datetime


def create_summary_md(results_dir, src_dir):
    """Create the test summary chapter in markdown format"""
    summary_md = "# Test Summary\n"
    summary_md += "| Test Name | Result | Details |\n"
    summary_md += "|-----------|--------|---------|\n"

    # Check CPU Single Core test
    if os.path.exists(f"{results_dir}/cpu_single.yaml"):
        with open(f"{results_dir}/cpu_single.yaml", "r") as f:
            content = f.read()
            if "metrics:" in content:
                summary_md += "| CPU Single Core | ✅ | Completed successfully |\n"
            else:
                summary_md += "| CPU Single Core | ❌ | Failed or incomplete |\n"
    else:
        summary_md += "| CPU Single Core | ❌ | No test results found |\n"

    # Check CPU Multi Core test
    if os.path.exists(f"{results_dir}/cpu_multi.yaml"):
        with open(f"{results_dir}/cpu_multi.yaml", "r") as f:
            content = f.read()
            if "metrics:" in content:
                summary_md += "| CPU Multi Core | ✅ | Completed successfully |\n"
            else:
                summary_md += "| CPU Multi Core | ❌ | Failed or incomplete |\n"
    else:
        summary_md += "| CPU Multi Core | ❌ | No test results found |\n"

    # Check CPU All Cores test
    if os.path.exists(f"{results_dir}/cpu_all.yaml"):
        with open(f"{results_dir}/cpu_all.yaml", "r") as f:
            content = f.read()
            if "metrics:" in content:
                summary_md += "| CPU All Cores | ✅ | Completed successfully |\n"
            else:
                summary_md += "| CPU All Cores | ❌ | Failed or incomplete |\n"
    else:
        summary_md += "| CPU All Cores | ❌ | No test results found |\n"

    # Check Memory Single test
    if os.path.exists(f"{results_dir}/mem_single.yaml"):
        with open(f"{results_dir}/mem_single.yaml", "r") as f:
            content = f.read()
            if "metrics:" in content:
                summary_md += "| Memory Single | ✅ | Completed successfully |\n"
            else:
                summary_md += "| Memory Single | ❌ | Failed or incomplete |\n"
    else:
        summary_md += "| Memory Single | ❌ | No test results found |\n"

    # Check Memory Multi test
    if os.path.exists(f"{results_dir}/mem_multi.yaml"):
        with open(f"{results_dir}/mem_multi.yaml", "r") as f:
            content = f.read()
            if "metrics:" in content:
                summary_md += "| Memory Multi | ✅ | Completed successfully |\n"
            else:
                summary_md += "| Memory Multi | ❌ | Failed or incomplete |\n"
    else:
        summary_md += "| Memory Multi | ❌ | No test results found |\n"

    # Check Disk IO Write test
    if os.path.exists(f"{results_dir}/disk_write_test.yaml"):
        with open(f"{results_dir}/disk_write_test.yaml", "r") as f:
            content = f.read()
            if "metrics:" in content:
                summary_md += "| Disk IO Write | ✅ | Completed successfully |\n"
            else:
                summary_md += "| Disk IO Write | ❌ | Failed or incomplete |\n"
    else:
        summary_md += "| Disk IO Write | ❌ | No test results found |\n"

    # Check Disk IO Mix test
    if os.path.exists(f"{results_dir}/disk_io_test.yaml"):
        with open(f"{results_dir}/disk_io_test.yaml", "r") as f:
            content = f.read()
            if "metrics:" in content:
                summary_md += "| Disk IO Mix | ✅ | Completed successfully |\n"
            else:
                summary_md += "| Disk IO Mix | ❌ | Failed or incomplete |\n"
    else:
        summary_md += "| Disk IO Mix | ❌ | No test results found |\n"

    # Check Disk Fallocate test
    if os.path.exists(f"{results_dir}/disk_fallocate_test.yaml"):
        with open(f"{results_dir}/disk_fallocate_test.yaml", "r") as f:
            content = f.read()
            if "metrics:" in content:
                summary_md += "| Disk Fallocate | ✅ | Completed successfully |\n"
            else:
                summary_md += "| Disk Fallocate | ❌ | Failed or incomplete |\n"
    else:
        summary_md += "| Disk Fallocate | ❌ | No test results found |\n"

    # Check GPU test
    if os.path.exists(f"{results_dir}/gpu_burn.log"):
        with open(f"{results_dir}/gpu_burn.log", "r") as f:
            content = f.read()
            if "OK" in content:
                summary_md += "| GPU Burn Test | ✅ | Completed successfully |\n"
            elif "(DIED!)" in content or "ERROR" in content or "Failed" in content:
                summary_md += "| GPU Burn Test | ❌ | Test failed with errors |\n"
            elif os.path.getsize(f"{results_dir}/gpu_burn.log") > 0:
                summary_md += "| GPU Burn Test | ⚠️ | Completed with warnings |\n"
            else:
                summary_md += "| GPU Burn Test | ❌ | Test output empty |\n"
    else:
        summary_md += "| GPU Burn Test | ❌ | No test results found |\n"

    with open(f"{src_dir}/chapter_summary.md", "w") as f:
        f.write(summary_md)


def create_system_md(results_dir, src_dir):
    """Create the system information chapter in markdown format"""
    sys_md = "# System Information\n```\n"

    if os.path.exists(f"{results_dir}/system_info.txt"):
        # Filter out identifying information from system info
        if os.path.exists(f"{results_dir}/system_info.txt"):
            with open(f"{results_dir}/system_info.txt", "r") as f:
                content = f.read()
                # Remove identifying information
                lines = content.split("\n")
                for i, line in enumerate(lines):
                    # Filter hostname, user, and other identifying info
                    if "hostname:" in line.lower():
                        lines[i] = "hostname: [REDACTED]"
                    elif "run-by:" in line.lower():
                        lines[i] = "run-by: [REDACTED]"
                    elif "user" in line.lower() and "@" in line:
                        lines[i] = line.split("@")[0] + "@[REDACTED]"
                    elif "/home/" in line:
                        lines[i] = line.replace("/home/christian", "/home/[USER]")

                sys_md += "\n".join(lines)
    else:
        sys_md += "No system information available\n"

    sys_md += "```\n"

    with open(f"{src_dir}/chapter_sys.md", "w") as f:
        f.write(sys_md)


def create_cpu_md(results_dir, src_dir):
    """Create the CPU test results chapter in markdown format"""
    cpu_md = "# CPU Stress Test Results\n"

    # Single Core Test
    cpu_md += "\n## Single Core Test\n```yaml\n"
    if os.path.exists(f"{results_dir}/cpu_single.yaml"):
        with open(f"{results_dir}/cpu_single.yaml", "r") as f:
            cpu_md += f.read()
    else:
        cpu_md += "No results available\n"
    cpu_md += "```\n"

    # Multi-Core Test
    cpu_md += "\n## Multi-Core Test (4 cores)\n```yaml\n"
    if os.path.exists(f"{results_dir}/cpu_multi.yaml"):
        with open(f"{results_dir}/cpu_multi.yaml", "r") as f:
            cpu_md += f.read()
    else:
        cpu_md += "No results available\n"
    cpu_md += "```\n"

    # All Cores Test
    cpu_md += "\n## All Cores Test\n```yaml\n"
    if os.path.exists(f"{results_dir}/cpu_all.yaml"):
        with open(f"{results_dir}/cpu_all.yaml", "r") as f:
            cpu_md += f.read()
    else:
        cpu_md += "No results available\n"
    cpu_md += "```\n"

    with open(f"{src_dir}/chapter_cpu.md", "w") as f:
        f.write(cpu_md)


def create_mem_md(results_dir, src_dir):
    """Create the memory test results chapter in markdown format"""
    mem_md = "# Memory Stress Test Results\n"

    # Single Memory Test
    mem_md += "\n## Single Memory Test\n```yaml\n"
    if os.path.exists(f"{results_dir}/mem_single.yaml"):
        with open(f"{results_dir}/mem_single.yaml", "r") as f:
            mem_md += f.read()
    else:
        mem_md += "No results available\n"
    mem_md += "```\n"

    # Multiple Memory Test
    mem_md += "\n## Multiple Memory Test (4 instances)\n```yaml\n"
    if os.path.exists(f"{results_dir}/mem_multi.yaml"):
        with open(f"{results_dir}/mem_multi.yaml", "r") as f:
            mem_md += f.read()
    else:
        mem_md += "No results available\n"
    mem_md += "```\n"

    with open(f"{src_dir}/chapter_mem.md", "w") as f:
        f.write(mem_md)


def create_disk_md(results_dir, src_dir):
    """Create the disk IO test results chapter in markdown format"""
    disk_md = "# Disk IO Stress Test Results\n"

    # Disk IO Write Test
    disk_md += "\n## Disk IO Write Test\n```yaml\n"
    if os.path.exists(f"{results_dir}/disk_write_test.yaml"):
        with open(f"{results_dir}/disk_write_test.yaml", "r") as f:
            disk_md += f.read()
    else:
        disk_md += "No results available\n"
    disk_md += "```\n"

    # Disk IO Mix Test
    disk_md += "\n## Disk IO Mix Test\n```yaml\n"
    if os.path.exists(f"{results_dir}/disk_io_test.yaml"):
        with open(f"{results_dir}/disk_io_test.yaml", "r") as f:
            disk_md += f.read()
    else:
        disk_md += "No results available\n"
    disk_md += "```\n"

    # Disk Fallocate Test
    disk_md += "\n## Disk Fallocate Test\n```yaml\n"
    if os.path.exists(f"{results_dir}/disk_fallocate_test.yaml"):
        with open(f"{results_dir}/disk_fallocate_test.yaml", "r") as f:
            disk_md += f.read()
    else:
        disk_md += "No results available\n"
    disk_md += "```\n"

    with open(f"{src_dir}/chapter_disk.md", "w") as f:
        f.write(disk_md)


def create_gpu_md(results_dir, src_dir):
    """Create the GPU test results chapter in markdown format"""
    gpu_md = "# GPU Stress Test Results\n"

    # GPU Burn Test
    gpu_md += "\n## GPU Burn Test\n```\n"
    if os.path.exists(f"{results_dir}/gpu_burn.log"):
        with open(f"{results_dir}/gpu_burn.log", "r") as f:
            gpu_md += f.read()
    else:
        gpu_md += "No results available\n"
    gpu_md += "```\n"

    with open(f"{src_dir}/chapter_gpu.md", "w") as f:
        f.write(gpu_md)


def create_plots_md(plots_dir, src_dir):
    """Create the performance plots chapter in markdown format"""
    plots_md = "# Performance Plots\n"

    # CPU Performance
    plots_md += "\n## CPU Performance\n"
    plots_md += (
        "The following chart shows the relative performance of CPU stress tests:\n"
    )
    plots_md += "![CPU Performance](plots/cpu_performance.png)\n"

    # Memory Performance
    plots_md += "\n## Memory Performance\n"
    plots_md += (
        "The following chart shows the relative performance of memory stress tests:\n"
    )
    plots_md += "![Memory Performance](plots/memory_performance.png)\n"

    # Disk IO Performance (if available)
    if os.path.exists(f"{plots_dir}/disk_io_performance.png"):
        plots_md += "\n## Disk IO Performance\n"
        plots_md += (
            "The following chart shows disk IO performance during the stress test:\n"
        )
        plots_md += "![Disk IO Performance](plots/disk_io_performance.png)\n"

    # GPU Performance (if available)
    if os.path.exists(f"{plots_dir}/gpu_performance.png"):
        plots_md += "\n## GPU Performance\n"
        plots_md += (
            "The following chart shows GPU performance during the stress test:\n"
        )
        plots_md += "![GPU Performance](plots/gpu_performance.png)\n"

    # GPU Temperature (if available)
    if os.path.exists(f"{plots_dir}/gpu_temperature.png"):
        plots_md += "\n## GPU Temperature\n"
        plots_md += (
            "The following chart shows GPU temperature during the stress test:\n"
        )
        plots_md += "![GPU Temperature](plots/gpu_temperature.png)\n"

    # GPU Combined Metrics (if available)
    if os.path.exists(f"{plots_dir}/gpu_combined.png"):
        plots_md += "\n## GPU Combined Metrics\n"
        plots_md += "The following chart shows both GPU performance and temperature:\n"
        plots_md += "![GPU Combined Metrics](plots/gpu_combined.png)\n"

    plots_md += "\n### Note\n"
    plots_md += "If the PNG images are not rendering correctly, the SVG versions can be found in the same directory with .svg extension.\n"

    with open(f"{src_dir}/chapter_plots.md", "w") as f:
        f.write(plots_md)


def generate_report(report_dir="report"):
    """Generate the complete stress test report"""
    results_dir = f"{report_dir}/results"
    src_dir = f"{report_dir}/src"
    plots_dir = f"{report_dir}/plots"

    # Create directories if they don't exist
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(plots_dir, exist_ok=True)

    # Create SUMMARY.md
    summary_md = "# Stress Test Report\n"
    summary_md += "- [Introduction](chapter_1.md)\n"
    summary_md += "- [Test Summary](chapter_summary.md)\n"
    summary_md += "- [System Information](chapter_sys.md)\n"
    summary_md += "- [CPU Test Results](chapter_cpu.md)\n"
    summary_md += "- [Memory Test Results](chapter_mem.md)\n"
    summary_md += "- [Disk IO Test Results](chapter_disk.md)\n"
    summary_md += "- [GPU Test Results](chapter_gpu.md)\n"
    summary_md += "- [Performance Plots](chapter_plots.md)\n"

    with open(f"{src_dir}/SUMMARY.md", "w") as f:
        f.write(summary_md)

    # Create chapter_1.md (Introduction)
    intro_md = "# Stress Test Report\n"
    intro_md += f"Test completed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    intro_md += "\nThis report contains the results of stress tests performed on this system to evaluate its performance under various workloads.\n"
    intro_md += "\nTest results auto generated by the stress test suite https://github.com/Christian-Prather/stress-test"

    with open(f"{src_dir}/chapter_1.md", "w") as f:
        f.write(intro_md)

    # Create all other chapters
    create_summary_md(results_dir, src_dir)
    create_system_md(results_dir, src_dir)
    create_cpu_md(results_dir, src_dir)
    create_mem_md(results_dir, src_dir)
    create_disk_md(results_dir, src_dir)
    create_gpu_md(results_dir, src_dir)
    create_plots_md(plots_dir, src_dir)

    print(f"Report generated in {report_dir}/src/")


if __name__ == "__main__":
    report_dir = sys.argv[1] if len(sys.argv) > 1 else "report"
    generate_report(report_dir)
