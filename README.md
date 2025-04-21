# Log Anomaly Detector

A Python script designed to analyze log files and detect anomalies based on the frequency of specific log levels within configurable time intervals. It helps identify potential issues, such as a surge of errors, by monitoring log patterns.

## Overview

This script reads a log file line by line, parses each entry to extract the timestamp, log level, and message. It then aggregates log entries based on the specified log level and time interval. If the count of entries for the target level exceeds a defined threshold within any given interval, an anomaly is reported.

## Key Features

-   **Command-Line Interface:** Easily configure the analysis using command-line arguments for the log file path, target log level, anomaly threshold, and time window.
-   **Flexible Log Parsing:** Uses regular expressions to parse common log formats (`YYYY-MM-DD HH:MM:SS LEVEL message`). Gracefully skips lines that don't match the expected format.
-   **Time-Based Analysis:** Aggregates log entries into time windows (e.g., 30 seconds) for frequency analysis.
-   **Configurable Anomaly Conditions:** Define what constitutes an anomaly by setting the log level (`ERROR`, `WARN`, etc.), the threshold count, and the time interval.
-   **Error Handling:** Provides informative messages for common issues like file not found or parsing problems.
-   **Modular Design:** Core logic is separated into functions for better readability, maintainability, and potential extension.

## Prerequisites

-   **Python:** Version 3.6 or later.
-   **pip:** Python package installer (usually comes with Python).
-   **Required Libraries:**
    -   `pandas`

## Installation

1.  **Clone the Repository or Download the Script:**
    ```bash
    git clone https://github.com/chintanboghara/Log-Anomaly-Detector.git
    cd Log-Anomaly-Detector
    ```
    *Alternatively, download the `log_anomaly_detector.py` (or your script's name) file directly.*

2.  **Install Dependencies:**
    Navigate to the script's directory in your terminal and install the required libraries using pip:
    ```bash
    pip install pandas
    ```
    *(Consider using a virtual environment for better dependency management: `python -m venv venv`, `source venv/bin/activate` or `venv\Scripts\activate`, then `pip install ...`)*

3.  **Prepare Your Log File:**
    Ensure you have a log file ready. The script expects a format like the one described below. Note the path to this file.

## Log File Format

The script anticipates log entries following this structure:

```
YYYY-MM-DD HH:MM:SS LEVEL message
```

-   **Timestamp:** `YYYY-MM-DD HH:MM:SS` (e.g., `2025-03-29 14:23:45`)
-   **Log Level:** A single word indicating the severity (e.g., `ERROR`, `INFO`, `WARN`, `DEBUG`). Case-sensitive by default in the script's logic, but the parsing aims to capture it.
-   **Message:** The rest of the line is considered the log message.

**Example Log Entries:**

```
2025-03-29 14:23:45 ERROR An unexpected error occurred during data processing.
2025-03-29 14:23:50 INFO Service started successfully on port 8080.
2025-03-29 14:24:05 ERROR Database connection failed: timeout expired.
2025-03-29 14:24:08 ERROR Failed to write to cache.
2025-03-29 14:24:12 WARN Disk space nearing threshold.
2025-03-29 14:24:15 ERROR Another critical error event.
```

*Note: Lines deviating significantly from this format might be skipped during parsing.*

## Usage

Execute the script from your terminal using the following command structure:

```bash
python <script_name.py> <log_file_path> [options]
```

**Arguments:**

-   **`log_file_path`** (Required): The path to the log file you want to analyze (e.g., `data/system_logs.txt`, `/var/log/app.log`).

**Options:**

-   **`--level LEVEL`**:
    -   The log level to monitor for anomalies.
    -   Default: `ERROR`
    -   Example: `--level WARN`
-   **`--threshold THRESHOLD`**:
    -   The maximum number of log entries of the specified `LEVEL` allowed within the `INTERVAL` before triggering an anomaly alert.
    -   Type: integer
    -   Default: `3`
    -   Example: `--threshold 10`
-   **`--interval INTERVAL`**:
    -   The time window (in seconds) over which to count log entries for anomaly detection.
    -   Type: integer
    -   Default: `30`
    -   Example: `--interval 60` (analyze per minute)

### Examples

1.  **Analyze `system.log` for ERRORs using defaults (3 errors in 30 seconds):**
    ```bash
    python log_anomaly_detector.py system.log
    ```

2.  **Analyze `app.log` for `WARN` level logs, triggering if more than 5 occur within a 60-second window:**
    ```bash
    python log_anomaly_detector.py app.log --level WARN --threshold 5 --interval 60
    ```

3.  **Analyze `/var/log/webserver.log` for `CRITICAL` logs, triggering on just 1 occurrence within a 10-second window:**
    ```bash
    python log_anomaly_detector.py /var/log/webserver.log --level CRITICAL --threshold 1 --interval 10
    ```

## Output

The script will print messages to the console indicating its progress and findings.

-   If an anomaly is detected (threshold exceeded within an interval), it will print a message similar to:
    ```
    Anomaly detected! 4 ERROR logs found between YYYY-MM-DD HH:MM:SS and YYYY-MM-DD HH:MM:SS (threshold: 3)
    ```
-   If the script completes without finding anomalies based on the criteria, it might print a summary message or simply finish silently (depending on implementation details).
-   Error messages will be printed for issues like file not found or parsing problems.

## Troubleshooting

-   **`FileNotFoundError`:** The script could not find the log file at the specified `log_file_path`. Double-check the path and ensure the file exists and the script has permission to read it.
-   **`Permission Denied`:** The script does not have the necessary permissions to read the log file. Adjust file permissions (`chmod`) or run the script with appropriate privileges (use `sudo` cautiously if necessary).
-   **`No Valid Log Entries Found` / Few Entries Processed:** The script might not be parsing lines correctly. Verify that your log file format matches the expected `YYYY-MM-DD HH:MM:SS LEVEL message` structure. Check for inconsistencies or leading/trailing whitespace.
-   **Incorrect Dependencies:** Ensure `pandas` is installed correctly in the Python environment you are using to run the script. Try reinstalling: `pip install --force-reinstall pandas`.
-   **Unexpected Behavior:** Review the command-line arguments (`--level`, `--threshold`, `--interval`) to ensure they are set as intended.
