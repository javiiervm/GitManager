# Git Manager

### Description
This program has been developed to make git pull and git push operations more convenient for your projects, especially if you work with multiple repositories. 
> [!NOTE]
> This program was originally developed for Linux (Ubuntu), but it has also been tested succesfully on Windows.

### Available commands
This table shows the aliases I recommend to define for using the program, along with the parameter they will send to the program and the action this parameter performs (check the usage guide to know more about aliases and commands).
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
3. Save the .py file in a directory where you have a Python virtual environment (if you don't have one, create it by running `'python3 -m venv venv'` in the directory where you saved the .py, and then execute `'source venv/bin/activate'` to activate it).
> [!NOTE]
> This may not be necessary if you have allowed Python to run in your system without requiring a virtual environment, or if you are using Windows instead of Linux.
4. Add the repositories you want to use to the .py file. Remember that the token, username, and repository name must be in the same positions in the lists.
5. The usage for this script is `'python3 gitmanager.py command'`, but it's more convenient if you assign an alias to it in the terminal, so you can call it from anywhere on your PC.
6. To add an alias, go to the source file of your shell (bashrc, zshrc...) and add `'alias your_alias=python3 path/to/your/gitmanager.py command'`, for example `'alias push=python3 path/to/your/gitmanager.py push'`, 'push' being the parameter passed to the program when calling it.
> [!WARNING]
> Don't use as aliases existing commands, such as 'git push'.
7. From now on, you can call this script from any directory on your PC.

### Considerations
* This is a program to be used from the terminal.
* To exit the program and interrupt execution, use the command CTRL + C.
> [!IMPORTANT]
> **Always** check that the output in the terminal confirms that the operation has been performed successfully. This version of the gitmanager has a little issue, if for example you use an empty commit when using push, the operation is aborted but the final line of the output still says "Push performed successfully", this will be fixed in the next version of the program but from now make sure to check that the output doesn't say the operation was aborted.
