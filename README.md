<div align="center">
  <img width="80" height="80" alt="Git-Icon-1788C" src="https://github.com/user-attachments/assets/a0385a6f-6304-40c2-af95-3c76da4b5cee" />
  <h1 align="center">Git Manager</h1>
</div>
<br /><br />

**Git Manager** is a Python command-line tool for easily managing GitHub repositories and personal access tokens. It provides a user-friendly interactive menu to perform common git operations, manage authentication tokens, and handle branches, commits, and clipboard operations across Linux, Windows, and macOS.
> [!WARNING]
> This program has originally been developed for Linux (successfully tested in Ubuntu), but it has also been tested successfully on Windows. It should also be compatible with macOS, but it **hasn't been tested in this environment**.

> [!WARNING]
> All routes specified in this code must follow **UNIX format** for the script to work properly.

(MENCIONAR LO DE GIT BASH CONSOLE EN WINDOWS)

## Features
* **Token Management**: Securely store, retrieve, copy, and delete GitHub personal access tokens per repository using a json file (doesn't change any GitHub data!).
* **Git Operations**: Pull, push (with or without commit), commit, and add files interactively.
* **Branch Management**: List, create, delete, switch, and merge branches.
* **Revert Actions**: Revert last commit, push, add, or merge.
* **Clipboard Support**: Copy tokens to the clipboard with cross-platform support.
* **Interactive Menus**: Easy-to-use text-based interface for all operations.
* **Token Management Mode**: Manage tokens even when not inside a git repository.

## Security
Tokens are stored in a JSON file in your home directory under `.scripts/.safe/` (you can change this route to what you want), and they are only used for authenticated git operations and are not shared elsewhere.

## Requirements
* Python 3.10 or newer (for match statement support)
* pyperclip Python package
* Git installed and available in your system PATH

## Installation

## Usage
Navigate to your git repository directory and run:
```bash
gitmanager    # (or the alias you have defined).
```
If not inside a git repository, GitManager will start in **token management mode**.

## Example
```bash
$ python gitmanager.py
Repository URL detected: https://github.com/youruser/yourrepo
=============== GIT MANAGER ===============
1. pull
2. push (add all + commit)
...
Select an option:
>> 2
Enter the commit message (optional):
>> Update README
```

### Main menu
When inside a git repository, you will see a screen like this:
```bash
=============== GIT MANAGER ===============
1. pull
2. push (add all + commit)
3. push (existing commit only)
4. commit only
5. interactive add
6. git status
7. show current branch
8. manage branches
9. copy token
10. revert last commit
11. revert last push
12. revert last add
13. revert last merge
14. remove this repo from git manager
0. exit
```
Menu options:
1. **pull**: Pull from remote using your stored token.
2. **push (add all + commit)**: Add all changes, commit, and push.
3. **push (existing commit only)**: Push existing commits without adding/committing.
4. **commit only**: Commit changes without adding or pushing.
5. **interactive add**: Selectively add files to staging.
6. **git status**: Show current git status.
7. **show current branch**: Display the current branch name.
8. **manage branches**: List, create, delete, switch, or merge branches.
9. **copy token**: Copy the stored token for this repo to clipboard.
10. **revert last commit**: Revert the most recent commit.
11. **revert last push**: Undo the last push (force push).
12. **revert last add**: Unstage all staged files.
13. **revert last merge**: Abort the last merge operation.
14. **remove this repo from git manager**: Delete the stored token for this repo.
0. **exit**: Exit the program.

### Token management mode
If not in a git repository, you can:
* List tokens
* Copy token
* Add token
* Delete token
* Delete all tokens
* Exit

> [!IMPORTANT]
> Tokens are stored by default in the route:
> ```bash
> ~/.scripts/.safe/.gitmanager_tokens.json
> ```
> Make sure to create all this folders or change the route to an existing one!

## Troubleshooting
* **Clipboard not working?**
  * On Linux, install `xclip` or `xsel`.
  * On Windows/macOS, ensure `pyperclip` is installed.
* **Token not accepted?**
  * Ensure your GitHub token has the correct scopes (typically repo).

<br /><br />
For any issues or suggestions, please open an issue or contact the author.
