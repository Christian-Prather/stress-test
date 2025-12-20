#!/bin/bash

# Script to detect NVIDIA GPU and determine the required compute capability

# Get GPU information from nvidia-smi
GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -1)

if [ -z "$GPU_INFO" ]; then
    echo "No NVIDIA GPU detected" >&2
    exit 1
fi

# Map GPU models to compute capabilities
case "$GPU_INFO" in
    *"GeForce GTX 1080"*|*"GeForce GTX 1070"*|*"GeForce GTX 1060"*|*"GeForce GTX 1050"*)
        COMPUTE_CAP="6.1"
        ;;
    *"GeForce GTX 1080 Ti"*|*"GeForce GTX 1070 Ti"*|*"GeForce GTX TITAN Xp"*)
        COMPUTE_CAP="6.1"
        ;;
    *"GeForce GTX 980"*|*"GeForce GTX 970"*|*"GeForce GTX 960"*|*"GeForce GTX 950"*)
        COMPUTE_CAP="5.2"
        ;;
    *"GeForce GTX 780"*|*"GeForce GTX 770"*|*"GeForce GTX 760"*|*"GeForce GTX 750 Ti"*)
        COMPUTE_CAP="3.0"
        ;;
    *"GeForce RTX 2080"*|*"GeForce RTX 2070"*|*"GeForce RTX 2060"*)
        COMPUTE_CAP="7.5"
        ;;
    *"GeForce RTX 2080 Ti"*)
        COMPUTE_CAP="7.5"
        ;;
    *"GeForce RTX 3090"*|*"GeForce RTX 3080"*|*"GeForce RTX 3070"*|*"GeForce RTX 3060"*)
        COMPUTE_CAP="8.6"
        ;;
    *"GeForce RTX 4090"*|*"GeForce RTX 4080"*|*"GeForce RTX 4070"*|*"GeForce RTX 4060"*)
        COMPUTE_CAP="8.9"
        ;;
    *"Tesla K80"*)
        COMPUTE_CAP="3.7"
        ;;
    *"Tesla P100"*)
        COMPUTE_CAP="6.0"
        ;;
    *"Tesla V100"*)
        COMPUTE_CAP="7.0"
        ;;
    *"Tesla T4"*)
        COMPUTE_CAP="7.5"
        ;;
    *"A100"*)
        COMPUTE_CAP="8.0"
        ;;
    *"H100"*)
        COMPUTE_CAP="9.0"
        ;;
    *)
        # Default to a common compute capability if model not recognized
        echo "Warning: GPU model '$GPU_INFO' not recognized. Using default compute capability 6.1." >&2
        COMPUTE_CAP="6.1"
        ;;
esac

echo "$COMPUTE_CAP"
echo "Detected GPU: $GPU_INFO" >&2
echo "Using compute capability: $COMPUTE_CAP" >&2
