# Log Analysis and Anomaly Detection Script

This Python script analyzes a log file to detect anomalies based on log level frequency within a specified time interval. The script reads the log file, processes the entries, and reports if an anomaly is detected (e.g., too many ERROR logs in a short period).

## Features

- **Dynamic Input:** Specify the log file path, log level, threshold, and time interval via command-line arguments.
- **Robust Parsing:** Uses regular expressions to parse log entries and gracefully handles errors.
- **Modularity:** Key functionalities are encapsulated in functions for easier maintenance and testing.
- **Timestamp Handling:** Converts log timestamps into Python datetime objects for efficient analysis.

## Requirements

- Python 3.6 or later
- The following Python libraries:
  - `pandas`
  - `argparse`

If these libraries are not already installed, install them using `pip`:

```bash
pip install pandas
```

## Installation

1. **Clone the Repository or Download the Script:**

   ```bash
   git clone https://github.com/chintanboghara/Log-Anomaly-Detector.git
   cd Log-Anomaly-Detector
   ```

   *Alternatively, download the script file directly.*

2. **Ensure you have the log file:**

   Place the log file (for example, `system_logs.txt`) in the same directory as the script or provide the full path when running the script.

## Log File Format

The script expects the log entries to be in the following format:

```
YYYY-MM-DD HH:MM:SS LEVEL message
```

Example:

```
2025-03-29 14:23:45 ERROR An unexpected error occurred
2025-03-29 14:23:50 INFO Service started successfully
```

## Usage

Run the script from the command line with the following syntax:

```bash
python script_name.py log_file_path [--level LEVEL] [--threshold THRESHOLD] [--interval INTERVAL]
```

- **`log_file_path`**: Path to your log file.
- **`--level`**: (Optional) Log level to analyze. Default is `ERROR`.
- **`--threshold`**: (Optional) The number of log entries that triggers an anomaly. Default is `3`.
- **`--interval`**: (Optional) The time interval in seconds over which to count log entries. Default is `30`.

### Example

To analyze a log file named `system_logs.txt` for `ERROR` logs, with a threshold of 3 errors per 30 seconds:

```bash
python log_anomaly_detector.py system_logs.txt --level ERROR --threshold 3 --interval 30
```

If the script detects more than 3 ERROR logs within any 30-second interval, it will print an anomaly message.

## Troubleshooting

- **File Not Found:**  
  If the specified log file does not exist, the script will output an error message and exit.
  
- **No Valid Log Entries:**  
  If the script does not find any log entries that match the expected format, it will display a warning message.
