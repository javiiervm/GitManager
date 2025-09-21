import os
import sys
import subprocess
import json
import platform
import base64
import getpass

try:
    import pyperclip
except Exception:
    pyperclip = None

from cryptography.fernet import Fernet

TOKEN_FILE = os.path.expanduser("~/.scripts/.safe/.gitmanager_tokens.json")
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"


def get_secret_key():
    key_b64 = os.getenv("GITMANAGER_KEY")
    if key_b64:
        try:
            key = base64.urlsafe_b64decode(key_b64)
            if len(key) != 32:
                raise ValueError("Invalid key length")
            return key_b64.encode()
        except Exception:
            print(f"{RED}Environment variable GITMANAGER_KEY is invalid. Must be base64 32 bytes.{RESET}")
            sys.exit(1)
    else:
        key_b64 = getpass.getpass("Enter your encryption key for GitManager tokens:\n>> ").strip()
        try:
            key = base64.urlsafe_b64decode(key_b64)
            if len(key) != 32:
                raise ValueError("Invalid key length")
            return key_b64.encode()
        except Exception:
            print(f"{RED}Invalid encryption key format. It must be base64 32 bytes.{RESET}")
            sys.exit(1)


SECRET_KEY = get_secret_key()
cipher = Fernet(SECRET_KEY)


def load_tokens_encrypted(path=TOKEN_FILE):
    if not os.path.exists(path):
        return {}
    with open(path, 'rb') as f:
        encrypted = f.read()
    try:
        decrypted = cipher.decrypt(encrypted)
        tokens = json.loads(decrypted.decode('utf-8'))
        return tokens
    except Exception as e:
        print(f"{RED}Error decrypting token file: {e}{RESET}")
        return {}


def save_tokens_encrypted(tokens, path=TOKEN_FILE):
    data = json.dumps(tokens).encode('utf-8')
    encrypted = cipher.encrypt(data)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(encrypted)


def get_repo_url():
    try:
        remote_url = subprocess.check_output(["git", "remote", "get-url", "origin"], encoding="utf-8").strip()
        if remote_url.endswith(".git"):
            remote_url = remote_url[:-4]
        return remote_url
    except Exception:
        return None


def get_token_for_repo(repo_url, tokens):
    if repo_url in tokens:
        return tokens[repo_url]
    token = input(f"{RED}No token found for {repo_url}.{RESET}\nEnter your GitHub token:\n>> ").strip()
    if not token:
        print(f"{RED}No token entered. Exiting program.{RESET}\n")
        sys.exit(1)
    tokens[repo_url] = token
    save_tokens_encrypted(tokens)
    print(f"{GREEN}Token saved for {repo_url}.{RESET}")
    print(f"{BOLD}You can now use this token for operations on {repo_url}.{RESET}\n")
    return token


def get_user_and_repo(repo_url):
    path = repo_url.split("github.com/", 1)[1]
    user, repo = path.split("/", 1)
    return user, repo


def copy_to_clipboard_windows(text):
    try:
        if not isinstance(text, str):
            text = str(text)
        cmd = f'echo {text.strip()}| clip'
        os.system(cmd)
        print(f"{GREEN}Copied to clipboard!{RESET}")
    except Exception:
        try:
            if pyperclip:
                pyperclip.copy(text)
                print(f"{GREEN}Copied to clipboard using pyperclip!{RESET}")
            else:
                print(f"{RED}Clipboard copy failed on Windows. Install pyperclip or use a compatible terminal.{RESET}")
        except Exception:
            print(f"{RED}Clipboard copy failed on Windows.{RESET}")


def copy_to_clipboard_linux(text):
    try:
        if os.system("which xclip > /dev/null 2>&1") == 0:
            os.system(f"echo '{text}' | xclip -selection clipboard")
            print(f"{GREEN}Copied to clipboard!{RESET}")
        elif os.system("which xsel > /dev/null 2>&1") == 0:
            os.system(f"echo '{text}' | xsel --clipboard --input")
            print(f"{GREEN}Copied to clipboard!{RESET}")
        else:
            if pyperclip:
                pyperclip.copy(text)
                print(f"{GREEN}Copied to clipboard using pyperclip!{RESET}")
            else:
                print(f"{RED}No clipboard utility found (install xclip, xsel, or pyperclip).{RESET}")
    except Exception:
        print(f"{RED}Clipboard copy failed on Linux.{RESET}")


def copy_to_clipboard_macos(text):
    try:
        os.system(f"echo '{text}' | pbcopy")
        print(f"{GREEN}Copied to clipboard!{RESET}")
    except Exception:
        try:
            if pyperclip:
                pyperclip.copy(text)
                print(f"{GREEN}Copied to clipboard using pyperclip!{RESET}")
            else:
                print(f"{RED}Clipboard copy failed on macOS. Install pyperclip or use a compatible terminal.{RESET}")
        except Exception:
            print(f"{RED}Clipboard copy failed on macOS.{RESET}")


def copy_to_clipboard(text):
    system = platform.system()
    if system == "Windows":
        copy_to_clipboard_windows(text)
    elif system == "Linux":
        copy_to_clipboard_linux(text)
    elif system == "Darwin":
        copy_to_clipboard_macos(text)
    else:
        try:
            if pyperclip:
                pyperclip.copy(text)
                print(f"{GREEN}Copied to clipboard using pyperclip!{RESET}")
            else:
                print(f"{RED}Clipboard copy not supported on this OS.{RESET}")
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


def make_push_no_add(token, user, repo):
    remote_url = f"https://{user}:{token}@github.com/{user}/{repo}.git"
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
    print(f"{GREEN}Current branch: {BOLD}{branch}{RESET}")


def manage_branches():
    while True:
        print(f"\n{BOLD}Branch Management:{RESET}")
        print("1. List branches")
        print("2. Create branch")
        print("3. Delete branch")
        print("4. Switch branch")
        print("5. Merge branch")
        print("0. Back")
        while True:
            op = input("\nSelect an option:\n>> ").strip()
            match op:
                case "1":
                    branches = subprocess.check_output(["git", "branch"], encoding="utf-8")
                    print(branches)
                case "2":
                    name = input("Enter new branch name:\n>> ").strip()
                    os.system(f"git branch {name}")
                case "3":
                    name = input("Enter branch name to delete:\n>> ").strip()
                    os.system(f"git branch -d {name}")
                case "4":
                    name = input("Enter branch name to switch to:\n>> ").strip()
                    os.system(f"git checkout {name}")
                case "5":
                    name = input("Enter branch name to merge into current:\n>> ").strip()
                    os.system(f"git merge {name}")
                case "0":
                    return
                case _:
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
        save_tokens_encrypted(tokens)
        print(f"{GREEN}Token for {repo_url} removed.{RESET}")
    else:
        print(f"{RED}No token found for {repo_url}.{RESET}")


def list_all_files():
    try:
        output = subprocess.check_output(["git", "ls-files"], encoding="utf-8")
        files = output.strip().split("\n")
        return [f for f in files if f]
    except subprocess.CalledProcessError:
        print(f"{RED}Error listing files.{RESET}")
        return []


def list_sparse_files():
    try:
        output = subprocess.check_output(["git", "sparse-checkout", "list"], encoding="utf-8")
        files = output.strip().split("\n")
        return [f for f in files if f]
    except Exception:
        return []


def untrack_files():
    all_files = list_all_files()
    if not all_files:
        print(f"{RED}No tracked files found.{RESET}")
        return
    current_included = list_sparse_files()
    if not current_included:
        current_included = all_files
    candidates = [f for f in all_files if f in current_included]
    if not candidates:
        print(f"{GREEN}No files to untrack.{RESET}")
        return
    print("Select files to untrack (comma separated numbers):")
    for idx, fname in enumerate(candidates, 1):
        print(f"{idx}. {fname}")
    choices = input(">> ").strip()
    if not choices:
        print(f"{RED}No files selected.{RESET}")
        return
    try:
        selected = [candidates[int(i) - 1] for i in choices.split(",") if i.strip().isdigit() and 0 < int(i) <= len(candidates)]
        if not selected:
            print(f"{RED}Invalid selection.{RESET}")
            return
        new_included = [f for f in current_included if f not in selected]
        subprocess.run(["git", "sparse-checkout", "init", "--no-cone"], check=False)
        if new_included:
            subprocess.run(["git", "sparse-checkout", "set"] + new_included, check=True)
        else:
            subprocess.run(["git", "sparse-checkout", "set"], check=True)
        subprocess.run(["git", "checkout"], check=True)
        print(f"{GREEN}Files untracked: {', '.join(selected)}{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")

def restore_untracked_files():
    all_files = list_all_files()
    if not all_files:
        print(f"{RED}No tracked files found.{RESET}")
        return
    current_included = list_sparse_files()
    if not current_included:
        print(f"{GREEN}No files currently untracked.{RESET}")
        return
    excluded = [f for f in all_files if f not in current_included]
    if not excluded:
        print(f"{GREEN}No files currently untracked.{RESET}")
        return
    print("Select files to restore:")
    print("0. Back")
    for idx, fname in enumerate(excluded, 1):
        print(f"{idx}. {fname}")
    print(f"{len(excluded) + 1}. Restore all")
    choice = input(">> ").strip()
    if choice == "0" or choice.lower() == "back":
        print(f"{GREEN}Returning to main menu.{RESET}")
        return
    try:
        if choice == str(len(excluded) + 1):
            new_included = current_included + [f for f in excluded if f not in current_included]
            subprocess.run(["git", "sparse-checkout", "init", "--no-cone"], check=False)
            subprocess.run(["git", "sparse-checkout", "set"] + new_included, check=True)
            subprocess.run(["git", "checkout"], check=True)
            print(f"{GREEN}All files restored.{RESET}")
        else:
            selected = [excluded[int(i) - 1] for i in choice.split(",") if i.strip().isdigit() and 0 < int(i) <= len(excluded)]
            if not selected:
                print(f"{RED}Invalid selection.{RESET}")
                return
            new_included = current_included + [s for s in selected if s not in current_included]
            subprocess.run(["git", "sparse-checkout", "init", "--no-cone"], check=False)
            subprocess.run(["git", "sparse-checkout", "set"] + new_included, check=True)
            subprocess.run(["git", "checkout"], check=True)
            print(f"{GREEN}Files restored: {', '.join(selected)}{RESET}")
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}")
        return
    current_included = list_sparse_files()
    excluded = [f for f in all_files if f not in current_included]
    if not excluded:
        try:
            subprocess.run(["git", "sparse-checkout", "disable"], check=True)
            print(f"{GREEN}sparse-checkout disabled (no more untracked files).{RESET}")
        except Exception as e:
            print(f"{RED}Failed to disable sparse-checkout: {e}{RESET}")

def reduced_menu(tokens):
    while True:
        print("\n======= GIT MANAGER (No repo detected) =======")
        print("1. List tokens")
        print("2. Copy token")
        print("3. Add token")
        print("4. Delete token")
        print("5. Delete all tokens")
        print("0. Exit")
        while True:
            op = input("\nSelect an option:\n>> ").strip()
            match op:
                case "1":
                    if not tokens:
                        print(f"{RED}No tokens registered.{RESET}")
                    else:
                        print("Registered repositories:")
                        for idx, repo_url in enumerate(tokens, 1):
                            print(f"{idx}. {repo_url}")
                case "2":
                    if not tokens:
                        print(f"{RED}No tokens registered.{RESET}")
                        continue
                    print("Select a repository to copy its token:")
                    repo_list = list(tokens.keys())
                    for idx, repo_url in enumerate(repo_list, 1):
                        print(f"{idx}. {repo_url}")
                    sel = input(">> ").strip()
                    if sel.isdigit() and 1 <= int(sel) <= len(repo_list):
                        copy_to_clipboard(tokens[repo_list[int(sel) - 1]])
                    else:
                        print(f"{RED}Invalid selection.{RESET}")
                case "3":
                    repo_url = input("Enter repository URL (e.g. https://github.com/user/repo):\n>> ").strip()
                    if not repo_url:
                        print(f"{RED}Repository URL cannot be empty.{RESET}")
                        continue
                    token = input("Enter GitHub token for this repo:\n>> ").strip()
                    if not token:
                        print(f"{RED}Token cannot be empty.{RESET}")
                        continue
                    tokens[repo_url] = token
                    save_tokens_encrypted(tokens)
                    print(f"{GREEN}Token added for {repo_url}.{RESET}")
                case "4":
                    if not tokens:
                        print(f"{RED}No tokens registered.{RESET}")
                        continue
                    print("Select a repository to delete its token:")
                    repo_list = list(tokens.keys())
                    for idx, repo_url in enumerate(repo_list, 1):
                        print(f"{idx}. {repo_url}")
                    sel = input(">> ").strip()
                    if sel.isdigit() and 1 <= int(sel) <= len(repo_list):
                        del tokens[repo_list[int(sel) - 1]]
                        save_tokens_encrypted(tokens)
                        print(f"{GREEN}Token deleted.{RESET}")
                    else:
                        print(f"{RED}Invalid selection.{RESET}")
                case "5":
                    confirm = input(f"{RED}Are you sure you want to delete ALL tokens? (Y/N):{RESET}\n>> ").strip().lower()
                    if confirm == "y":
                        tokens.clear()
                        save_tokens_encrypted(tokens)
                        print(f"{GREEN}All tokens deleted.{RESET}")
                case "0":
                    return
                case _:
                    print(f"{RED}Unrecognized option.{RESET}")


def menu():
    print("\n=============== GIT MANAGER ===============")
    print("1. pull")
    print("2. push (add all + commit)")
    print("3. push (existing commit only)")
    print("4. commit only")
    print("5. interactive add")
    print("6. git status")
    print("7. show current branch")
    print("8. manage branches")
    print("9. copy token")
    print("10. revert last commit")
    print("11. revert last push")
    print("12. revert last add")
    print("13. revert last merge")
    print("14. remove this repo from git manager")
    print("15. untrack files (sparse-checkout)")
    print("16. restore untracked files")
    print("0. exit")


if __name__ == "__main__":
    repo_url = get_repo_url()
    tokens = load_tokens_encrypted()
    if not repo_url:
        reduced_menu(tokens)
        sys.exit(0)
    print(f"{GREEN}Repository URL detected: {BOLD}{repo_url}{RESET}")
    token = get_token_for_repo(repo_url, tokens)
    user, repo = get_user_and_repo(repo_url)
    if '--push' in sys.argv:
        make_push_no_add(token, user, repo)
        exit(0)
    if '--pull' in sys.argv:
        make_pull(token, user, repo)
        exit(0)
    while True:
        menu()
        op = input("\nSelect an option:\n>> ").strip()
        match op.lower():
            case "1":
                make_pull(token, user, repo)
            case "2":
                commit_msg = input("Enter the commit message (optional):\n>> ").strip()
                if not commit_msg:
                    commit_msg = "Updated repository"
                make_push(token, user, repo, commit_msg)
            case "3":
                make_push_no_add(token, user, repo)
            case "4":
                commit_msg = input("Enter the commit message (optional):\n>> ").strip()
                if not commit_msg:
                    commit_msg = "Updated repository"
                make_commit_only(commit_msg)
            case "5":
                interactive_git_add()
            case "6":
                show_git_status()
            case "7":
                show_current_branch()
            case "8":
                manage_branches()
            case "9":
                copy_to_clipboard(token)
            case "10":
                revert_last_commit()
            case "11":
                revert_last_push(token, user, repo)
            case "12":
                revert_last_add()
            case "13":
                revert_last_merge()
            case "14":
                remove_token_for_repo(repo_url, tokens)
                break
            case "15":
                untrack_files()
            case "16":
                restore_untracked_files()
            case "0" | "exit":
                break
            case _:
                print(f"{RED}Unrecognized option.{RESET}")