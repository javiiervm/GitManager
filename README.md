# Git Manager

### Description
This program has been developed to make git pull and git push operations more convenient for your projects, especially if you work with multiple repositories. Currently, this program only supports Linux, but I may extend it to other operating systems in the future.

### Available commands
| Alias   | Command  | Action   |
|------------|------------|------------|
| pull | pull | git pull |
| push | push | git add . && git push |
| psh | pushnoadd | git push |
| copytoken | token | Copies the token of the selected repo to the clipboard |
| copyuser | user | Copies the user of the selected repo to the clipboard |
| copyusertoken | usertoken | Copies both token and user of the selected repo to the clipboard |

### Usage
#### Python File
1. Download the .py file.
2. If you don't have Python installed on your PC, download it from [its official website](https://www.python.org/)).
3. Save the .py file in a directory where you have a Python virtual environment (if you don't have one, create it by running 'python3 -m venv venv' in the directory where you saved the .py, and then execute 'source venv/bin/activate' to activate it). This may not be necessary if you have allowed Python to run in your system without requiring a virtual environment.
4. Add the repositories you want to use to the .py file. Remember that the token, username, and repository name must be in the same positions in the lists.
5. The usage for this script is 'python3 gitmanager.py push/pull', but it's more convenient if you assign an alias to it in the terminal, so you can call it from anywhere on your PC.
6. To add an alias, go to the source file of your shell (bashrc, zshrc...) and add 'alias push/pull=python3 path/to/your/gitmanager.py push/pull' (remember that aliases for push and pull are defined separately).
7. From now on, you can call this script from any directory on your PC.

### Considerations
* This is a program to be used from the terminal.
* To exit the program and interrupt execution, use the command CTRL + C.
