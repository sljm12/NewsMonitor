---
name: changelog-manager
description: Manage and update the project's CHANGELOG.md based on Git commit history. Use this skill when you need to create a new changelog or sync an existing one with recent commits before merging or finishing a phase of work.
---

# Changelog Manager

This skill helps maintain a consistent `CHANGELOG.md` file in the project root by grouping Git commits by date.

## Usage

When the user asks to "update the changelog" or "create a changelog," follow these steps:

1.  **Locate**: Ensure you are in the project root.
2.  **Run Script**: Execute the `scripts/update_changelog.py` script.
3.  **Verify**: Check that `CHANGELOG.md` exists and contains the latest commits grouped under the correct date headings.

### Workflow
- **Creation**: If `CHANGELOG.md` is missing, the script will create it from the entire Git history.
- **Maintenance**: Before merging or finishing a significant task, run this skill to ensure the changelog reflects all changes since the last update.
- **Grouping**: The script automatically groups multiple commits from the same day under a single date heading (`## YYYY-MM-DD`).
