In this lab, you will interact with a small web application that generates log
entries at different levels. You will use these logs as evidence to understand
what happened on the system and where that information is recorded.

## Lab Goals

- Generate predictable application log entries
- Identify different log levels
- Distinguish between application logs and nginx logs
- Practice reading logs as evidence

## What You Will Practice

- Application logging vs web server logging
- Log levels: debug, info, warning, error, critical
- Finding log files on a Linux system
- Answering questions using log evidence

## Prerequisites

- An Ubuntu virtual machine
- nginx installed and running
- A GitHub account

## Command Formatting Note

**Course convention:**  
If something appears in a command block, you are expected to run it.  
If it does not appear in a command block, you are not expected to type it.

### Lab
## Quick Task View
1. Verify Python 3 is installed.
1. Clone the lab repository and change into the project directory.
1. Create a virtual environment, activate it, and install dependencies.
1. Start the application and open it in a browser.
1. Click each log level button once.
1. For each click, locate the corresponding entry in `logs/app.log`.
1. Answer the following for each entry:
 - What happened?
 - When did it happen?
 - What log level was used?
 - What URL path was accessed?
1. Trigger the “Server Error” button.
1. Compare what appears in:
 - The application log
 - The nginx access log
 - The nginx error log

## Task Details
# Step 1: Verify Python 3 Is Installed
This lab uses Python 3. Before continuing, verify that Python 3 is available on your system.
```bash
python3 --version
```
If Python 3 is not installed, install it using:
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```
# Step 2: Get the Application code
Clone the lab repository from GitHub into your virtual machine.
```bash
git clone https://github.com/CryptoRAT/cit215.git
cd cit215
```
# Step 3: Set Up the Application
Create a virtual environment and install the required Python packages.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
# Step 4: Run the Application
```bash
python3 app.py
```
The application listens on:
```text
http://127.0.0.1:5000
```
# Step 5: Using the Application
Open the application in a browser. You will see buttons for different log levels.
Each button generates a log entry at the corresponding level.
  - Debug
  - Info
  - Warning
  - Error
  - Critical
  - Trigger Server Error
# Step 6: Viewing Application Logs
The application writes logs to a file inside the project directory at `logs/app.log`.
View the most recent log entries:
```bash
tail -n 25 logs/app.log
```
Watch logs update in real time while clicking buttons:
```bash
tail -f logs/app.log
```
press `ctrl+c` to end the stream

# Step 8: Viewing nginx Logs
nginx maintains separate logs for access and errors.
View the access log:
```bash
sudo tail -f /var/log/nginx/access.log
```
View the error log:
```bash
sudo tail -f /var/log/nginx/error.log
```

## Reflection Questions
1. Which logs told you that something happened?
1. Which logs showed how the web server responded?
1. What information was missing that you might want in a real system?

## Key Takeaway

Logs are not explanations. They are evidence. Understanding a system means learning how to read and interpret that evidence across multiple sources.
