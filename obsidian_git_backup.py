import os
import subprocess
import sys
import datetime

# path to remote repository
REMOTE_URL = "https://github.com/kshitij-r/obsidian.git"
# local path to Obsidian vault to push to remote repository
VAULT_PATH = "/Users/kshitijraj/Documents/Obsidian Vault"

# creates a subprocess to execute bash commands
def run_command(command, cwd=None, check=True):
    result = subprocess.run(command, shell=True, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

# creates a .gitignore file at VAULT_PATH
def git_ignore(path):
    gitignore_file = os.path.join(path, ".gitignore")
    if not os.path.exists(gitignore_file):
        with open(gitignore_file, "w") as f:
            f.write("""# Ignore log and temp files
                    *.log
                    *.tmp
                    """)

# initializes a git repository if needed and sets the remote url. Also adds all files (inside VAULT_PATH) to commit
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

# commits and pushes the staged changes
def git_commit_push(path, message):
    status = run_command("git status --porcelain", cwd=path, check=False)
    if not status:
        print("No changes to commit. Exiting.")
        return
    try:
        run_command(f'git commit -m "{message}"', cwd=path)
        run_command("git branch -M main", cwd=path)
        run_command("git push -u origin main", cwd=path)
        generate_log(path, message)
    except Exception as e:
        failMessage = "failed to commit and push changes on " + str(message)
        generate_log(path, failMessage)
        print(f'An error occured in commit and push stage : {e}')
         
# generates a log of all successful commits
def generate_log(path, message):
     LOG_FILE = "obsidian-git.md"
     logToWriteOn = os.path.join(path, LOG_FILE)
     try:
          with open(logToWriteOn, 'a') as logfile:
               logMessage = "\nlast commit on " + str(message)
               logfile.write(logMessage)
     except Exception as e:
          print(f'Unable to write daily git log, error occured {e}')

def main():
    currentDateTime = datetime.datetime.now()
    git_ignore(VAULT_PATH)
    git_init_add(VAULT_PATH)
    git_commit_push(VAULT_PATH, str(currentDateTime))

if __name__ == "__main__":
     main()
 





