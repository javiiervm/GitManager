import os
import sys
import subprocess
import json
import platform
import pyperclip

TOKEN_FILE = os.path.expanduser("~/.gitmanager_tokens.json")

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"

def get_repo_url():
    try:
        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], encoding="utf-8"
        ).strip()
        # Normalize the URL and remove possible .git at the end
        if remote_url.endswith(".git"):
            remote_url = remote_url[:-4]
        return remote_url
    except Exception:
        return None

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)

def get_token_for_repo(repo_url, tokens):
    if repo_url in tokens:
        return tokens[repo_url]
    token = input(f"{RED}No token found for {repo_url}.{RESET}\nEnter your GitHub token:\n>> ").strip()
    if not token:
        print(f"{RED}No token entered. Exiting program.{RESET}")
        sys.exit(1)
    tokens[repo_url] = token
    save_tokens(tokens)
    return token

def get_user_and_repo(repo_url):
    # repo_url format: https://github.com/user/repo
    path = repo_url.split("github.com/", 1)[1]
    user, repo = path.split("/", 1)
    return user, repo

def copy_to_clipboard_windows(text):
    try:
        import ctypes
        if not isinstance(text, str):
            text = str(text)
        cmd = f'echo {text.strip()}| clip'
        os.system(cmd)
        print(f"{GREEN}Copied to clipboard!{RESET}")
    except Exception:
        # Try pyperclip as fallback
        try:
            pyperclip.copy(text)
            print(f"{GREEN}Copied to clipboard using pyperclip!{RESET}")
        except Exception:
            print(f"{RED}Clipboard copy failed on Windows. Please install pyperclip or use a compatible terminal.{RESET}")

def copy_to_clipboard_linux(text):
    try:
        # Try xclip first
        if os.system("which xclip > /dev/null 2>&1") == 0:
            os.system(f"echo '{text}' | xclip -selection clipboard")
            print(f"{GREEN}Copied to clipboard!{RESET}")
        # Try xsel as fallback
        elif os.system("which xsel > /dev/null 2>&1") == 0:
            os.system(f"echo '{text}' | xsel --clipboard --input")
            print(f"{GREEN}Copied to clipboard!{RESET}")
        else:
            # Try pyperclip as last fallback
            try:
                pyperclip.copy(text)
                print(f"{GREEN}Copied to clipboard using pyperclip!{RESET}")
            except Exception:
                print(f"{RED}No clipboard utility found (install xclip, xsel, or pyperclip).{RESET}")
    except Exception:
        print(f"{RED}Clipboard copy failed on Linux.{RESET}")

def copy_to_clipboard_macos(text):
    try:
        os.system(f"echo '{text}' | pbcopy")
        print(f"{GREEN}Copied to clipboard!{RESET}")
    except Exception:
        # Try pyperclip as fallback
        try:
            pyperclip.copy(text)
            print(f"{GREEN}Copied to clipboard using pyperclip!{RESET}")
        except Exception:
            print(f"{RED}Clipboard copy failed on macOS. Please install pyperclip or use a compatible terminal.{RESET}")

def copy_to_clipboard(text):
    system = platform.system()
    if system == "Windows":
        copy_to_clipboard_windows(text)
    elif system == "Linux":
        copy_to_clipboard_linux(text)
    elif system == "Darwin":
        copy_to_clipboard_macos(text)
    else:
        # Try pyperclip as generic fallback
        try:
            pyperclip.copy(text)
            print(f"{GREEN}Copied to clipboard using pyperclip!{RESET}")
        except Exception:
            print(f"{RED}Clipboard copy not supported on this OS.{RESET}")

def make_pull(token, user, repo):
    remote_url = f"https://{user}:{token}@github.com/{user}/{repo}.git"
    os.system(f"git pull {remote_url}")

def make_push(token, user, repo, commit_msg):
    remote_url = f"https://{user}:{token}@github.com/{user}/{repo}.git"
    os.system("git add .")
    os.system(f'git commit -m "{commit_msg}"')
    os.system(f"git push {remote_url}")

def make_push_no_add(token, user, repo, commit_msg):
    remote_url = f"https://{user}:{token}@github.com/{user}/{repo}.git"
    os.system(f'git commit -m "{commit_msg}"')
    os.system(f"git push {remote_url}")

def make_commit_only(commit_msg):
    os.system(f'git commit -m "{commit_msg}"')

def interactive_git_add():
    status = subprocess.check_output(["git", "status", "--short"], encoding="utf-8")
    files = [line[3:] for line in status.splitlines() if line]
    if not files:
        print(f"{GREEN}No files to add.{RESET}")
        return
    print("Select files to add (comma separated numbers):")
    for idx, fname in enumerate(files, 1):
        print(f"{idx}. {fname}")
    choices = input(">> ").strip()
    if not choices:
        print(f"{RED}No files selected.{RESET}")
        return
    try:
        selected = [files[int(i)-1] for i in choices.split(",") if i.strip().isdigit() and 0 < int(i) <= len(files)]
        for f in selected:
            os.system(f'git add "{f}"')
        print(f"{GREEN}Added selected files.{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")

def show_git_status():
    status = subprocess.check_output(["git", "status"], encoding="utf-8")
    print(f"{BOLD}{status}{RESET}")

def show_current_branch():
    branch = subprocess.check_output(["git", "branch", "--show-current"], encoding="utf-8").strip()
    print(f"{GREEN}Current branch: {branch}{RESET}")

def manage_branches():
    while True:
        print("\nBranch Management:")
        print("1. List branches")
        print("2. Create branch")
        print("3. Delete branch")
        print("4. Switch branch")
        print("5. Merge branch")
        print("6. Back")
        op = input("Select an option:\n>> ").strip()
        if op == "1":
            branches = subprocess.check_output(["git", "branch"], encoding="utf-8")
            print(branches)
        elif op == "2":
            name = input("Enter new branch name:\n>> ").strip()
            os.system(f"git branch {name}")
        elif op == "3":
            name = input("Enter branch name to delete:\n>> ").strip()
            os.system(f"git branch -d {name}")
        elif op == "4":
            name = input("Enter branch name to switch to:\n>> ").strip()
            os.system(f"git checkout {name}")
        elif op == "5":
            name = input("Enter branch name to merge into current:\n>> ").strip()
            os.system(f"git merge {name}")
        elif op == "6":
            break
        else:
            print(f"{RED}Unrecognized option.{RESET}")

def revert_last_commit():
    os.system("git revert HEAD")

def revert_last_push(token, user, repo):
    remote_url = f"https://{user}:{token}@github.com/{user}/{repo}.git"
    os.system("git reset --hard HEAD~1")
    os.system(f"git push {remote_url} --force")

def revert_last_add():
    os.system("git reset")

def revert_last_merge():
    os.system("git merge --abort")

def remove_token_for_repo(repo_url, tokens):
    if repo_url in tokens:
        del tokens[repo_url]
        save_tokens(tokens)
        print(f"{GREEN}Token for {repo_url} removed.{RESET}")
    else:
        print(f"{RED}No token found for {repo_url}.{RESET}")

def reduced_menu(tokens):
    while True:
        print("======= GIT MANAGER (No repo detected) =======")
        print("1. List tokens")
        print("2. Copy token")
        print("3. Add token")
        print("4. Delete token")
        print("5. Delete all tokens")
        print("0. Exit")
        op = input("Select an option:\n>> ").strip()
        if op == "1":
            if not tokens:
                print(f"{RED}No tokens registered.{RESET}")
            else:
                print("Registered repositories:")
                for idx, repo_url in enumerate(tokens, 1):
                    print(f"{idx}. {repo_url}")
        elif op == "2":
            if not tokens:
                print(f"{RED}No tokens registered.{RESET}")
                continue
            print("Select a repository to copy its token:")
            repo_list = list(tokens.keys())
            for idx, repo_url in enumerate(repo_list, 1):
                print(f"{idx}. {repo_url}")
            sel = input(">> ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(repo_list):
                copy_to_clipboard(tokens[repo_list[int(sel)-1]])
            else:
                print(f"{RED}Invalid selection.{RESET}")
        elif op == "3":
            repo_url = input("Enter repository URL (e.g. https://github.com/user/repo):\n>> ").strip()
            token = input("Enter GitHub token for this repo:\n>> ").strip()
            tokens[repo_url] = token
            save_tokens(tokens)
            print(f"{GREEN}Token added for {repo_url}.{RESET}")
        elif op == "4":
            if not tokens:
                print(f"{RED}No tokens registered.{RESET}")
                continue
            print("Select a repository to delete its token:")
            repo_list = list(tokens.keys())
            for idx, repo_url in enumerate(repo_list, 1):
                print(f"{idx}. {repo_url}")
            sel = input(">> ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(repo_list):
                del tokens[repo_list[int(sel)-1]]
                save_tokens(tokens)
                print(f"{GREEN}Token deleted.{RESET}")
            else:
                print(f"{RED}Invalid selection.{RESET}")
        elif op == "5":
            confirm = input(f"{RED}Are you sure you want to delete ALL tokens? (yes/no):{RESET}\n>> ").strip().lower()
            if confirm == "yes":
                tokens.clear()
                save_tokens(tokens)
                print(f"{GREEN}All tokens deleted.{RESET}")
        elif op == "0":
            break
        else:
            print(f"{RED}Unrecognized option.{RESET}")

def menu():
    print("=============== GIT MANAGER ===============")
    print("1. pull")
    print("2. push (add all)")
    print("3. push (no add)")
    print("4. commit only")
    print("5. interactive add")
    print("6. git status")
    print("7. show current branch")
    print("8. manage branches")
    print("9. copytoken")
    print("10. revert last commit")
    print("11. revert last push")
    print("12. revert last add")
    print("13. revert last merge")
    print("14. remove token for this repo")
    print("0. exit")

if __name__ == "__main__":
    repo_url = get_repo_url()
    tokens = load_tokens()
    if not repo_url:
        reduced_menu(tokens)
        sys.exit(0)
    token = get_token_for_repo(repo_url, tokens)
    user, repo = get_user_and_repo(repo_url)
    menu()

    while True:
        op = input("Select an option:\n>> ").strip()
        if op == "1" or op.lower() == "pull":
            make_pull(token, user, repo)
        elif op == "2":
            commit_msg = input("Enter the commit message (optional):\n>> ")
            if not commit_msg.strip():
                commit_msg = "Updated repository"
            make_push(token, user, repo, commit_msg)
        elif op == "3":
            commit_msg = input("Enter the commit message (optional):\n>> ")
            if not commit_msg.strip():
                commit_msg = "Updated repository"
            make_push_no_add(token, user, repo, commit_msg)
        elif op == "4":
            commit_msg = input("Enter the commit message (optional):\n>> ")
            if not commit_msg.strip():
                commit_msg = "Updated repository"
            make_commit_only(commit_msg)
        elif op == "5":
            interactive_git_add()
        elif op == "6":
            show_git_status()
        elif op == "7":
            show_current_branch()
        elif op == "8":
            manage_branches()
        elif op == "9" or op.lower() == "copytoken":
            copy_to_clipboard(token)
        elif op == "10":
            revert_last_commit()
        elif op == "11":
            revert_last_push(token, user, repo)
        elif op == "12":
            revert_last_add()
        elif op == "13":
            revert_last_merge()
        elif op == "14":
            remove_token_for_repo(repo_url, tokens)
        elif op == "0" or op.lower() == "exit":
            break
        else:
            print(f"{RED}Unrecognized option.{RESET}")