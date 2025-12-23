#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import datetime


def parse_glmark2_output(log_file):
    """
    Parse glmark2 output to extract performance data

    Args:
        log_file (str): Path to the glmark2 output log file

    Returns:
        dict: Parsed data including OpenGL info, test results, and overall score
    """
    data = {
        "timestamp": datetime.now().isoformat(),
        "opengl_info": {},
        "test_results": [],
        "overall_score": None,
        "summary": {
            "total_tests": 0,
            "min_fps": None,
            "max_fps": None,
            "avg_fps": None,
        },
    }

    try:
        with open(log_file, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return data

    # Extract OpenGL information with flexible whitespace handling
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if "GL_VENDOR:" in line:
            parts = line.split("GL_VENDOR:", 1)
            if len(parts) > 1:
                data["opengl_info"]["vendor"] = parts[1].strip()
        elif "GL_RENDERER:" in line:
            parts = line.split("GL_RENDERER:", 1)
            if len(parts) > 1:
                data["opengl_info"]["renderer"] = parts[1].strip()
        elif "GL_VERSION:" in line:
            parts = line.split("GL_VERSION:", 1)
            if len(parts) > 1:
                data["opengl_info"]["version"] = parts[1].strip()
        elif "Surface Config:" in line:
            parts = line.split("Surface Config:", 1)
            if len(parts) > 1:
                data["opengl_info"]["surface_config"] = parts[1].strip()
        elif "Surface Size:" in line:
            parts = line.split("Surface Size:", 1)
            if len(parts) > 1:
                data["opengl_info"]["surface_size"] = parts[1].strip()

    # Extract test results - using pattern that handles variable spacing
    test_pattern = r"\[(.+?)\][^:]*:\s*FPS:\s+(\d+)\s+FrameTime:\s+([\d.]+)\s+ms"
    test_matches = re.findall(test_pattern, content)

    fps_values = []
    for match in test_matches:
        test_name = match[0]
        fps = int(match[1])
        frame_time = float(match[2])

        data["test_results"].append(
            {"test_name": test_name, "fps": fps, "frame_time_ms": frame_time}
        )
        fps_values.append(fps)

    # Extract overall score
    score_pattern = r"glmark2 Score:\s+(\d+)"
    score_match = re.search(score_pattern, content)
    if score_match:
        data["overall_score"] = int(score_match.group(1))

    # Calculate summary statistics
    if fps_values:
        data["summary"]["total_tests"] = len(fps_values)
        data["summary"]["min_fps"] = min(fps_values)
        data["summary"]["max_fps"] = max(fps_values)
        data["summary"]["avg_fps"] = sum(fps_values) / len(fps_values)

    return data


def extract_plot_data(glmark2_data):
    """
    Extract data suitable for plotting

    Args:
        glmark2_data (dict): Parsed glmark2 data

    Returns:
        dict: Data formatted for plotting
    """
    plot_data = {"test_names": [], "fps_values": [], "frame_times": []}

    for result in glmark2_data["test_results"]:
        # Truncate long test names for better plotting
        test_name = result["test_name"]
        if len(test_name) > 20:
            test_name = test_name[:17] + "..."

        plot_data["test_names"].append(test_name)
        plot_data["fps_values"].append(result["fps"])
        plot_data["frame_times"].append(result["frame_time_ms"])

    return plot_data


def save_data(glmark2_data, output_file):
    """
    Save the extracted data to a JSON file

    Args:
        glmark2_data (dict): Parsed glmark2 data
        output_file (str): Path to the output JSON file
    """
    try:
        with open(output_file, "w") as f:
            json.dump(glmark2_data, f, indent=2)
        print(f"Data saved to {output_file}")
    except Exception as e:
        print(f"Error saving data: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Extract performance data from glmark2 output"
    )
    parser.add_argument("log_file", help="Path to the glmark2 output log file")
    parser.add_argument(
        "--output",
        "-o",
        default="glmark2_data.json",
        help="Output JSON file (default: glmark2_data.json)",
    )
    parser.add_argument(
        "--plot-data", help="Save additional data for plotting in a separate file"
    )

    args = parser.parse_args()

    # Parse the glmark2 output
    glmark2_data = parse_glmark2_output(args.log_file)

    # Save the main data
    save_data(glmark2_data, args.output)

    # Save plot data if requested
    if args.plot_data:
        plot_data = extract_plot_data(glmark2_data)
        try:
            with open(args.plot_data, "w") as f:
                json.dump(plot_data, f, indent=2)
            print(f"Plot data saved to {args.plot_data}")
        except Exception as e:
            print(f"Error saving plot data: {e}", file=sys.stderr)

    # Print summary to console
    print("\n=== glmark2 Test Summary ===")
    if glmark2_data["opengl_info"]:
        print(f"GPU: {glmark2_data['opengl_info']['renderer']}")
        print(f"OpenGL Version: {glmark2_data['opengl_info']['version']}")
    if glmark2_data["overall_score"]:
        print(f"Overall Score: {glmark2_data['overall_score']}")
    if glmark2_data["summary"]["total_tests"] > 0:
        print(f"Tests Completed: {glmark2_data['summary']['total_tests']}")
        print(f"Average FPS: {glmark2_data['summary']['avg_fps']:.2f}")
        print(f"Min FPS: {glmark2_data['summary']['min_fps']}")
        print(f"Max FPS: {glmark2_data['summary']['max_fps']}")


if __name__ == "__main__":
    main()
