# Pixi environment setup
setup:
    pixi install
    pixi run cargo install mdbook-pdf
    pixi run sudo apt install glmark2-x11

    mkdir -p report/results

# Test single CPU
[group('CPU')]
cpu_single duration:
    mkdir -p report/results
    pixi run stress-ng --cpu 1 --timeout {{ duration }}s --metrics-brief --verbose --yaml report/results/cpu_single.yaml

# Test 4 CPUs
[group('CPU')]
cpu_multi duration:
    mkdir -p report/results
    pixi run stress-ng --cpu 4 --timeout {{ duration }}s --metrics-brief --verbose --yaml report/results/cpu_multi.yaml

# Test all CPUs
[group('CPU')]
cpu_all duration:
    mkdir -p report/results
    pixi run stress-ng --cpu 0 --timeout {{ duration }}s  --metrics-brief --verbose --yaml report/results/cpu_all.yaml

# Test single memory writes
[group('Memory')]
mem_single duration:
    mkdir -p report/results
    pixi run stress-ng --vm 1 --vm-bytes 10G --timeout {{ duration }}s  --metrics-brief --verbose --yaml report/results/mem_single.yaml

# Test parallel memory writes
[group('Memory')]
mem_multi duration:
    mkdir -p report/results
    pixi run stress-ng --vm 4 --vm-bytes 10G --timeout {{ duration }}s --metrics-brief --verbose --yaml report/results/mem_multi.yaml

# GPU stress testing (requires NVIDIA GPU and gpu-burn)
[group('GPU')]
gpu_stress duration:
    mkdir -p report/results
    # Build gpu-burn in the pixi environment
    rm -rf gpu-burn
    pixi run git clone https://github.com/wilicc/gpu-burn
    # Auto-detect compute capability for the GPU
    pixi run bash -c 'COMPUTE_CAP=$(bash scripts/detect_gpu.sh); echo "Building gpu-burn with compute capability: $COMPUTE_CAP"; cd gpu-burn && pixi run make clean && pixi run make COMPUTE=$COMPUTE_CAP'
    echo "Starting GPU burn test for {{ duration }} seconds..."
    cd gpu-burn && pixi run ./gpu_burn {{ duration }} | tee ../report/results/gpu_burn.log && cd ..
    # Extract GPU performance data for plotting
    pixi run python3 scripts/extract_gpu_data.py report/results/gpu_burn.log
    echo "GPU burn test completed."

# GPU benchmark testing with glmark2
[group('GPU')]
gpu_benchmark:
    mkdir -p report/results
    echo "Starting GPU benchmark test with glmark2..."
    pixi run glmark2 | tee report/results/glmark2.log
    # Extract glmark2 performance data for plotting
    pixi run python3 scripts/extract_glmark2_data.py report/results/glmark2.log --output report/results/glmark2_data.json --plot-data report/results/glmark2_plot_data.json
    echo "GPU benchmark test completed."

# Disk IO stress test with write operations
[group('Disk')]
disk_write_test duration:
    mkdir -p report/results
    pixi run stress-ng --hdd 4 --hdd-bytes 2G --timeout {{ duration }}s --metrics-brief --verbose --yaml report/results/disk_write_test.yaml

# Disk IO stress test with read/write operations
[group('Disk')]
disk_io_test duration:
    mkdir -p report/results
    pixi run stress-ng --iomix 4 --iomix-bytes 2G --timeout {{ duration }}s --metrics-brief --verbose --yaml report/results/disk_io_test.yaml

# File allocation stress test
[group('Disk')]
disk_fallocate_test duration:
    mkdir -p report/results
    pixi run stress-ng --fallocate 4 --fallocate-bytes 2G --timeout {{ duration }}s --metrics-brief --verbose --yaml report/results/disk_fallocate_test.yaml

# Collect system information for reporting
collect_sysinfo:
    mkdir -p report/results
    echo "=== System Information ===" > report/results/system_info.txt
    pixi run date >> report/results/system_info.txt
    echo "" >> report/results/system_info.txt
    echo "CPU Info:" >> report/results/system_info.txt
    pixi run lscpu | sed 's/hostname: .*/hostname: [REDACTED]/' >> report/results/system_info.txt
    echo "" >> report/results/system_info.txt
    echo "Memory Info:" >> report/results/system_info.txt
    pixi run free -h >> report/results/system_info.txt
    echo "" >> report/results/system_info.txt
    echo "GPU Info:" >> report/results/system_info.txt
    pixi run nvidia-smi >> report/results/system_info.txt
    echo "" >> report/results/system_info.txt
    echo "Disk Usage:" >> report/results/system_info.txt
    pixi run df -h | sed 's/\(\/dev\/\S*\)\s*\S*\s*\S*\s*\S*\s*\/home\/\S*/\1 [REDACTED] [REDACTED] [REDACTED] [REDACTED] \/home\/[USER]/' >> report/results/system_info.txt
    echo "" >> report/results/system_info.txt
    echo "OS Info:" >> report/results/system_info.txt
    pixi run uname -a >> report/results/system_info.txt

# Generate plots from stress test data
generate_plots:
    mkdir -p report/plots
    pixi run python3 scripts/plot_data.py --with-gpu

# Generate markdown report using Python script
generate_report:
    mkdir -p report/src
    pixi run python3 scripts/generate_report.py report
    mkdir -p report/src/plots
    cp report/plots/* report/src/plots/
    cp book.toml report/
    pixi run mdbook build report

# Full test with optional duration parameter (defaults to 60s)
full_test duration="60":
    just collect_sysinfo
    just cpu_single {{ duration }}
    just cpu_multi {{ duration }}
    just cpu_all {{ duration }}
    just mem_single {{ duration }}
    just mem_multi {{ duration }}
    # just gpu_stress {{ duration }}
    just gpu_benchmark
    just disk_write_test {{ duration }}
    just disk_io_test {{ duration }}
    just disk_fallocate_test {{ duration }}
    just generate_plots
    just generate_report
