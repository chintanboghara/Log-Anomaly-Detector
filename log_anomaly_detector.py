import pandas as pd
from collections import Counter
import re
import argparse
import sys
from datetime import timedelta

def parse_log_line(line: str):
    """
    Parses a single log line into a tuple of (timestamp, level, message).
    Expected log format: YYYY-MM-DD HH:MM:SS LEVEL message
    """
    match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)", line.strip())
    if match:
        return match.groups()
    return None

def load_logs(log_file: str) -> pd.DataFrame:
    """
    Reads the log file and returns a DataFrame containing the timestamp, level, and message.
    """
    log_entries = []
    try:
        with open(log_file, "r") as file:
            for line in file:
                parsed = parse_log_line(line)
                if parsed:
                    log_entries.append(parsed)
    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    if not log_entries:
        print("Warning: No valid log entries found.", file=sys.stderr)
    
    df = pd.DataFrame(log_entries, columns=["timestamp", "level", "message"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    # Drop rows with invalid timestamps
    df = df.dropna(subset=["timestamp"])
    return df

def detect_anomalies(df: pd.DataFrame, level: str, threshold: int, interval_seconds: int):
    """
    Detects and prints anomalies where the count of log entries of a given level
    exceeds the specified threshold within a specified time interval.
    """
    # Floor the timestamps to the nearest interval (e.g., 30 seconds)
    interval = f"{interval_seconds}S"
    error_times = df[df["level"] == level]["timestamp"].dt.floor(interval)
    error_counts = Counter(error_times)
    
    anomalies = []
    for time, count in error_counts.items():
        if count > threshold:
            anomalies.append((time, count))
            print(f"🚨 Anomaly detected! {count} {level} logs in {interval_seconds} seconds at {time}")
    
    if not anomalies:
        print(f"No anomalies detected for {level} logs over a {interval_seconds}-second interval (threshold: {threshold}).")
    return anomalies

def main():
    parser = argparse.ArgumentParser(description="Log Analysis and Anomaly Detection Script")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("--level", default="ERROR", help="Log level to analyze (default: ERROR)")
    parser.add_argument("--threshold", type=int, default=3, help="Threshold for log count in the interval (default: 3)")
    parser.add_argument("--interval", type=int, default=30, help="Time interval in seconds for counting logs (default: 30)")
    
    args = parser.parse_args()
    
    df = load_logs(args.log_file)
    
    print("Full Log Analysis:")
    print(df)
    
    detect_anomalies(df, args.level, args.threshold, args.interval)

if __name__ == "__main__":
    main()
