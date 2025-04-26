This script lets users automatically backup their Obsidian notes to a Git repository as the free version of the application does not allow syncs. It will backup your entire Obsidian vault (you can fine-tune on your own if needed).

### Setting up the script
 - Create your remote repository and add specify the URL in the `REMOTE_URL` field
 - Specify the path of your Obsidian vault in the `VAULT_PATH` field
 - If you want git to not track some files or folders, you can add them to the `git_ignore()` in the script

### Setting up CRON (MacOS/Linux)
To make sure your system runs this script and commits changes (if there are any), we have to setup CRON to schedule this job. Steps are:
 - Open the Crontab editor
    ```bash
    crontab -e
    ```
- Add this line at the bottom (modify as per need based on the information given in the table below):
    ```bash
    0 21 * * * /usr/bin/python3 /path/to/your/obsidian_git_backup.py
    ```

    | Field         | Value | Meaning             |
    |---------------|-------|---------------------|
    | Minute        | 0     | at minute 0          |
    | Hour          | 21    | 9 PM (24-hour clock) |
    | Day of month  | *     | every day            |
    | Month         | *     | every month          |
    | Day of week   | *     | any day              |
- Save and exit vim

This CRON routine will also keep a log of all your commits in a file `obdisian-git.md`, which is created and maintained in your Obsidian vault at `VAULT_PATH`