import os
import subprocess
import sys
import datetime

REMOTE_URL = "https://github.com/kshitij-r/obsidian.git"
VAULT_PATH = "/Users/kshitijraj/Documents/Obsidian Vault"

def run_command(command, cwd=None, check=True):
    result = subprocess.run(command, shell=True, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def git_ignore(path):
    gitignore_file = os.path.join(path, ".gitignore")
    if not os.path.exists(gitignore_file):
        with open(gitignore_file, "w") as f:
            f.write("""# Ignore log and temp files
                    *.log
                    *.tmp
                    # Also ignore the daily commit log update
                    obdisian-git.md
                    """)
     
def git_init_add(path):
    if not os.path.isdir(path):
        print(f"Folder {path} does not exist.")
        sys.exit(1)

    if not os.path.isdir(os.path.join(path, ".git")):
            print("Initializing new Git repository...")
            run_command("git init", cwd=path)
            run_command(f"git remote add origin {REMOTE_URL}", cwd=path)
    
    run_command(f"git remote set-url origin {REMOTE_URL}", cwd=path)
    run_command("git add .", cwd=path)

def git_commit_push(path, message):
    status = run_command("git status --porcelain", cwd=path, check=False)
    if not status:
        print("No changes to commit. Exiting.")
        return
    try:
        run_command(f'git commit -m "{message}"', cwd=path)
        run_command("git branch -M main", cwd=path)
        run_command("git push -u origin main", cwd=path)
        generate_daily_log(path, message)
    except Exception as e:
         print(f'An error occured in commit and push stage : {e}')

def generate_daily_log(path, message):
     LOG_FILE = "obdisian-git.md"
     logToWriteOn = os.path.join(path, LOG_FILE)
     try:
          with open(logToWriteOn, 'a') as logfile:
               logMessage = "last commit -> " + str(message)
               logfile.write(logMessage)
               logfile.write('\n')
     except Exception as e:
          print(f'Unable to write daily git log, error occured {e}')

if __name__ == "__main__":
    currentDateTime = datetime.datetime.now()
    commit_messsage = "commit-" + str(currentDateTime)
    git_ignore(VAULT_PATH)
    git_init_add(VAULT_PATH)
    git_commit_push(VAULT_PATH, commit_messsage)





