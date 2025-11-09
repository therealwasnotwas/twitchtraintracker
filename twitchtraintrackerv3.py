# === Twitch Train Tracker  ===
# === Version 0.3alpha
# === Python CLI Version
# === (©)opyright 2025 - wasnotwas - Ross Leak - wasnotwas@duck.com


import re
import os
import glob
from datetime import datetime, timedelta

# === Here are the precompiled regex patterns to optimise speed and memory ===
def build_patterns(user):
    return {
        "join": re.compile(
            rf"^(\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}})\s+-->\s+{re.escape(user)} \({re.escape(user)}@{re.escape(user)}\.tmi\.twitch\.tv\) has joined (#[\w\d_]+)"
        ),
        "leave": re.compile(
            rf"^(\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}})\s+<--\s+{re.escape(user)} \({re.escape(user)}@{re.escape(user)}\.tmi\.twitch\.tv\) has left (#[\w\d_]+)"
        )
    }

# === Funcion: Define the Stream Lines from File List to save memory ===
def stream_lines(file_list):
    for path in file_list:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                yield from f
        except Exception as e:
            print(f"⚠️ Skipping unreadable file: {path} ({e})")

# === Function: Parse the Sessions in One Pass to save resources ===
def parse_sessions(lines, user):
    patterns = build_patterns(user)
    joins, leaves = [], []

    for line in lines:
        line = line.strip()
        if m := patterns["join"].search(line):
            timestamp = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
            channel = m.group(2)
            joins.append((timestamp, channel))
        elif m := patterns["leave"].search(line):
            timestamp = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
            channel = m.group(2)
            leaves.append((timestamp, channel))

    joins.sort()
    leaves.sort()

    sessions = []
    j, l = 0, 0
    while j < len(joins) and l < len(leaves):
        join_time, join_chan = joins[j]
        leave_time, leave_chan = leaves[l]
        if join_time <= leave_time and join_chan == leave_chan:
            sessions.append((join_chan, join_time, leave_time))
            j += 1
            l += 1
        elif join_time > leave_time:
            l += 1
        else:
            j += 1
    return sessions

# === Function: Summarise Sessions ===
def summarize_sessions(sessions, user):
    total = timedelta()
    print(f"\n⏱ Time summary for twitch user: \033[1;36m{user}\033[0m\n")
    print(f"{'Channel':<20} {'Joined':<20} {'Left':<20} {'Duration'}")
    print("-" * 80)
    for channel, join, leave in sessions:
        duration = leave - join
        total += duration
        print(f"{channel:<20} {join} {leave} {str(duration)}")
    print(f"\nTotal time \033[1;36m{user}\033[0m spent: {str(total)}")

# === Function: File Discovery and Filtering ===
def discover_files(directory, use_filter=False, start=None, end=None):
    extensions = ("*.txt", "*.log", "*.weechatlog")
    files = []
    for ext in extensions:
        for path in glob.glob(os.path.join(directory, ext)):
            if not use_filter or (start <= datetime.fromtimestamp(os.path.getmtime(path)) <= end):
                files.append(path)
    return files

# === Confirm File List ===
def confirm_files(files):
    print("\n📂 Files to be processed are the following (Please check they are correct):")
    for f in files:
        print(f" - {f}")
    return input("\nProceed with these files? (yes/no): ").strip().lower() == "yes"

# === Main Interface ===
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("🎧 Twitch Train Tracker (version 0.3alpha - (©) wasnotwas 2025)")
    print("Latest version: https://github.com/therealwasnotwas/twitchtraintracker\n")

    print("note: file extensions read by the program are .txt, .log, or .weechatlog")
    mode = input("Would you like to analyse a single log file, or a directory full of log files? (file/dir): ").strip().lower()
    user = input("Please enter the Twitch username you wish to query against the log file(s): ").strip()

    try:
        if mode == "dir":
            path = input("Please enter full directory path for the logs (such as /home/oldgit/logs):  ").strip()
            use_filter = input("Would you like to filter the log files processed by a date range? (yes/no): ").strip().lower() == "yes"
            if use_filter:
                start = datetime.strptime(input("Start date (YYYY-MM-DD): ").strip(), "%Y-%m-%d")
                end = datetime.strptime(input("End date (YYYY-MM-DD): ").strip(), "%Y-%m-%d")
                files = discover_files(path, True, start, end)
            else:
                files = discover_files(path)

            if not files:
                print("❌ Oops. Sorry there are matching files found.")
                return
            if not confirm_files(files):
                print("❌ Oh no. You have cancelled the operation. Please re-run the app if you made a mistake and wish to start again.")
                return

        else:
            path = input("Enter full file path: ").strip()
            if not os.path.exists(path):
                print("❌ Oops. Guru Meditation. That file not found. Please try again")
                return
            files = [path]

        lines = stream_lines(files)
        sessions = parse_sessions(lines, user)
        summarize_sessions(sessions, user)

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
