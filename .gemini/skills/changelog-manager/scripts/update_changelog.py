import subprocess
import os
from datetime import datetime
from collections import defaultdict

def get_git_commits():
    try:
        # Get commits in format: YYYY-MM-DD|Subject
        output = subprocess.check_output(
            ["git", "log", "--pretty=format:%ad|%s", "--date=short"],
            universal_newlines=True
        )
        return output.splitlines()
    except Exception as e:
        print(f"Error fetching git commits: {e}")
        return []

def update_changelog(file_path="CHANGELOG.md"):
    commits = get_git_commits()
    if not commits:
        print("No commits found.")
        return

    # Group by date
    daily_commits = defaultdict(list)
    for line in commits:
        if "|" in line:
            date, subject = line.split("|", 1)
            daily_commits[date].append(subject)

    # Sort dates descending
    sorted_dates = sorted(daily_commits.keys(), reverse=True)

    with open(file_path, "w") as f:
        f.write("# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n")
        for date in sorted_dates:
            f.write(f"## {date}\n")
            for subject in daily_commits[date]:
                f.write(f"- {subject}\n")
            f.write("\n")

    print(f"Successfully updated {file_path}")

if __name__ == "__main__":
    update_changelog()
