<div align="center">
  <img width="80" height="80" alt="Git-Icon-1788C" src="https://github.com/user-attachments/assets/a0385a6f-6304-40c2-af95-3c76da4b5cee" />
  <h1 align="center">Git Manager</h1>
</div>
<br /><br />

**Git Manager** is a Python command-line tool for easily managing GitHub repositories and personal access tokens. It provides a user-friendly interactive menu to perform common git operations, manage authentication tokens, and handle branches, commits, and clipboard operations across Linux, Windows, and macOS.
> [!NOTE]
> This program has originally been developed for **Linux** and successfully tested in *Ubuntu*.

> [!WARNING]
> This program has also been tested successfully on **Windows**, using the **Git Bash terminal**, (NOT WORKING WITH POWERSHELL).
>
> It should also be compatible with macOS, but it **hasn't been tested in this environment**.

> [!CAUTION]
> All routes specified in this code must follow **UNIX format** for the script to work properly.

## Features
* **Token Management**: Securely store, retrieve, copy, and delete GitHub personal access tokens per repository using a json file (doesn't change any GitHub data!).
* **Git Operations**: Pull, push (with or without commit), commit, and add files interactively.
* **Branch Management**: List, create, delete, switch, and merge branches.
* **Revert Actions**: Revert last commit, push, add, or merge.
* **Clipboard Support**: Copy tokens to the clipboard with cross-platform support.
* **Interactive Menus**: Easy-to-use text-based interface for all operations.
* **Token Management Mode**: Manage tokens even when not inside a git repository.

## Security
Tokens are stored in a JSON file for authenticated git operations and are not shared elsewhere.

> [!IMPORTANT]
> Tokens are stored by default in the route:
> ```bash
> ~/.scripts/.safe/.gitmanager_tokens.json
> ```
> Make sure to create all this folders or change the route to an existing one!

## Requirements
* Python 3.10 or newer *(Program has been tested with Python 3.13)*
* pyperclip Python package
* Git installed and available in your system PATH

## Installation
> [!TIP]
> The idea is that you have the script somewhere you can access to from anywhere in the computer, and assign an alias to execute the script automatically. This example is made with the route `~/.scripts/` but you can choose what you want as soon as it is a valid path.

The installation is done inside the selected path, `~/.scripts/` in our case. Please move to your desired installation folder before beginning the process.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/javiiervm/python-gitmanager.git
   cd python-gitmanager
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

 > [!CAUTION]
 > I recommend not creating a virtual environment for this project, or the script may not work properly from any directory. However, if you want to create a virtual environment to install the dependencies there, you can do so with the command:
 >
 > ```bash
 > python3 -m venv venv
 > source venv/bin/activate  # On Windows use: venv\Scripts\activate
 > ```

3. **Define an alias for the script:**
   Open your shell script in your favourite editor, for example in a bash terminal with nano editor:
   ```bash
   nano ~/.bashrc
   ```
   > For zsh you should execute `nano ~/.zshrc` or maybe you prefer to use `vim` instead of `nano`, make sure to match your system configuration in this step.
   
   Once you have opened the shell script in your text editor, add the following line at the bottom:
   ```bash
   alias gitmanager="python3 ~/.scripts/gitmanager.py"
   # You may have defined another route or may need to execute 'python' instead of 'python3', depending on your installation and OS
   ```

You are all set!

## Usage
Navigate to your git repository directory and run:
```bash
gitmanager    # (or the alias you have defined).
```
If not inside a git repository, GitManager will start in **token management mode**.

### Main menu (inside a repository)
|  | Action                            | Description                                                        |
|-----|-----------------------------------|--------------------------------------------------------------------|
| 1   | **pull**                          | Pull from remote using your stored token.                          |
| 2   | **push (add all + commit)**       | Add all changes, commit, and push.                                 |
| 3   | **push (existing commit only)**   | Push existing commits without adding/committing.                   |
| 4   | **commit only**                   | Commit changes without adding or pushing.                          |
| 5   | **interactive add**               | Selectively add files to staging.                                  |
| 6   | **git status**                    | Show current git status.                                           |
| 7   | **show current branch**           | Display the current branch name.                                   |
| 8   | **manage branches**               | List, create, delete, switch, or merge branches.                   |
| 9   | **copy token**                    | Copy the stored token for this repo to clipboard.                  |
| 10  | **revert last commit**            | Revert the most recent commit.                                     |
| 11  | **revert last push**              | Undo the last push (force push).                                   |
| 12  | **revert last add**               | Unstage all staged files.                                          |
| 13  | **revert last merge**             | Abort the last merge operation.                                    |
| 14  | **remove this repo from git manager** | Delete the stored token for this repo.                        |
| 0   | **exit**                          | Exit the program.                                                  |

### Token management mode (outside a repository)
|  | Action                            | Description                                                        |
|-----|-----------------------------------|--------------------------------------------------------------------|
| 1   | **List tokens**                          | Shows a list with the name of the repositories that have a stored token in the JSON file.                        |
| 2   | **Copy token**       | Copies to the clipboard the token assigned to the repository the user selects.                               |
| 3   | **Add token**   | Asks for a GitHub repository link and its token, and adds it to the JSON file.                 |
| 4   | **Delete token**                   | Deletes from the JSON file the information about the selected repository.                        |
| 5   | **Delete all tokens**               | Clears all the content in the JSON file.                               
| 0   | **Exit**                          | Exit the program.                                                  |

## Troubleshooting
* **Clipboard not working?**
  * On Linux, install `xclip` or `xsel`.
  * On Windows/macOS, ensure `pyperclip` is installed.
* **Token not accepted?**
  * Ensure your GitHub token has the correct scopes (typically repo).

<br /><br />
For any issues or suggestions, please open an issue or contact the author.
