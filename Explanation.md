# Explanation of the Log Analysis and Anomaly Detection Script

This document provides a detailed explanation of each part of the Python script, which analyzes a log file to detect anomalies in log frequency based on a given threshold and time interval.

## Overview

The script processes a log file where each log entry follows the format:

```
YYYY-MM-DD HH:MM:SS LEVEL message
```

It then performs the following key tasks:
- **Parsing the Log File:** Reads each log line and extracts the timestamp, log level, and message.
- **Data Conversion:** Converts extracted log entries into a Pandas DataFrame, parsing timestamps into datetime objects.
- **Anomaly Detection:** Groups log entries by a specified time interval (e.g., 30 seconds) and counts occurrences of a specified log level (e.g., ERROR). An anomaly is flagged if the count exceeds a threshold.
- **Command-Line Interface:** The script accepts parameters for the log file, log level, threshold, and time interval using command-line arguments.

## Detailed Code Breakdown

### 1. Import Statements

```python
import pandas as pd
from collections import Counter
import re
import argparse
import sys
from datetime import timedelta
```

- **`pandas`:** Used for creating and manipulating DataFrames.
- **`Counter`:** A convenient way to count occurrences of items.
- **`re`:** For parsing log lines with regular expressions.
- **`argparse`:** Facilitates command-line argument parsing.
- **`sys`:** Provides system-specific functions; here, it is used for error messages and exiting.
- **`timedelta`:** (Imported but not explicitly used in the current version; it can be helpful for time interval manipulation if needed in the future.)

### 2. Function: `parse_log_line`

```python
def parse_log_line(line: str):
    """
    Parses a single log line into a tuple of (timestamp, level, message).
    Expected log format: YYYY-MM-DD HH:MM:SS LEVEL message
    """
    match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)", line.strip())
    if match:
        return match.groups()
    return None
```

- **Purpose:**  
  To extract the timestamp, log level, and message from each log entry.
  
- **How it works:**  
  - Uses a regular expression to match the expected format.
  - Returns a tuple `(timestamp, level, message)` if the line is correctly formatted.
  - Returns `None` if the line does not match the expected pattern.

### 3. Function: `load_logs`

```python
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
```

- **Purpose:**  
  To read and parse the log file, creating a Pandas DataFrame of log entries.
  
- **Key Components:**
  - **Error Handling:**  
    - If the file is not found, prints an error message and exits the script.
    - Issues a warning if no valid log entries are found.
  
  - **Data Processing:**  
    - Iterates over each line in the log file.
    - Uses `parse_log_line` to parse each line.
    - Constructs a DataFrame with columns: `timestamp`, `level`, and `message`.
    - Converts the `timestamp` column to datetime objects for proper time-based operations.
    - Drops any rows with invalid timestamps to maintain data integrity.

### 4. Function: `detect_anomalies`

```python
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
```

- **Purpose:**  
  To identify intervals where the frequency of a specific log level exceeds a given threshold.
  
- **How it works:**  
  - Filters the DataFrame to only include logs of the specified level.
  - Rounds down each timestamp to the nearest interval (using `dt.floor`).
  - Counts the number of logs within each interval using `Counter`.
  - Iterates over these counts to check against the threshold.
  - Prints a message and collects anomaly data for intervals that exceed the threshold.

### 5. Function: `main`

```python
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
```

- **Purpose:**  
  Serves as the entry point for the script.
  
- **Command-Line Arguments:**  
  - **`log_file`:** Required argument specifying the path to the log file.
  - **`--level`:** Optional argument to specify which log level to analyze (default is `ERROR`).
  - **`--threshold`:** Optional argument to set the anomaly threshold (default is `3`).
  - **`--interval`:** Optional argument to set the time interval in seconds for analysis (default is `30`).
  
- **Flow:**  
  - Parses command-line arguments.
  - Calls `load_logs` to read and process the log file.
  - Displays the full log DataFrame.
  - Calls `detect_anomalies` to identify and print any detected anomalies.

## Summary

- **Modularity:**  
  Each function is designed to handle a specific part of the log analysis process, making the script easier to maintain and extend.
  
- **Error Handling:**  
  The script handles missing files and invalid log entries gracefully, providing meaningful feedback to the user.
  
- **Flexibility:**  
  Command-line arguments allow for easy adjustment of parameters such as log level, threshold, and interval, making the tool versatile for different log formats and analysis requirements.
