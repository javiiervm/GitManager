import os
import platform
import base64
from cryptography.fernet import Fernet

try:
    import pyperclip
except ImportError:
    pyperclip = None

def copy_to_clipboard_windows(text):
    try:
        if not isinstance(text, str):
            text = str(text)
        cmd = f'echo {text.strip()}| clip'
        os.system(cmd)
        print("Copied to clipboard!")
    except Exception:
        try:
            if pyperclip:
                pyperclip.copy(text)
                print("Copied to clipboard using pyperclip!")
            else:
                print("Clipboard copy failed on Windows. Install pyperclip or use a compatible terminal.")
        except Exception:
            print("Clipboard copy failed on Windows.")

def copy_to_clipboard_linux(text):
    try:
        if os.system("which xclip > /dev/null 2>&1") == 0:
            os.system(f"echo '{text}' | xclip -selection clipboard")
            print("Copied to clipboard!")
        elif os.system("which xsel > /dev/null 2>&1") == 0:
            os.system(f"echo '{text}' | xsel --clipboard --input")
            print("Copied to clipboard!")
        else:
            if pyperclip:
                pyperclip.copy(text)
                print("Copied to clipboard using pyperclip!")
            else:
                print("No clipboard utility found (install xclip, xsel, or pyperclip).")
    except Exception:
        print("Clipboard copy failed on Linux.")

def copy_to_clipboard_macos(text):
    try:
        os.system(f"echo '{text}' | pbcopy")
        print("Copied to clipboard!")
    except Exception:
        try:
            if pyperclip:
                pyperclip.copy(text)
                print("Copied to clipboard using pyperclip!")
            else:
                print("Clipboard copy failed on macOS. Install pyperclip or use a compatible terminal.")
        except Exception:
            print("Clipboard copy failed on macOS.")

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
                print("Copied to clipboard using pyperclip!")
            else:
                print("Clipboard copy not supported on this OS.")
        except Exception:
            print("Clipboard copy not supported on this OS.")

def generate_key():
    key = Fernet.generate_key()
    key_str = key.decode()
    print("\nYour new encryption key (base64 32 bytes) is:\n")
    print(key_str)
    print("\nSave this key carefully! You will need it to decrypt your tokens.\n")
    copy_to_clipboard(key_str)
    print("The key has been copied to your clipboard.\n")

    export_cmd = f'export GITMANAGER_KEY="{key_str}"'
    print(f"To set this key as an environment variable, you can run:\n\n{export_cmd}\n")

    save_env = input("Do you want to print the command to save it in your shell profile? (y/n): ").strip().lower()
    if save_env == "y":
        shell = os.getenv("SHELL", "")
        profile_file = None
        if "bash" in shell:
            profile_file = "~/.bashrc"
        elif "zsh" in shell:
            profile_file = "~/.zshrc"
        elif "fish" in shell:
            profile_file = "~/.config/fish/config.fish"
        else:
            profile_file = "~/.profile"

        print(f"\nAdd the following line to your shell profile ({profile_file}):\n")
        print(export_cmd)
        print("\nYou can add it manually or run:")
        print(f'echo \'{export_cmd}\' >> {profile_file}')
        print("Then reload your shell or source the profile file.\n")



if __name__ == "__main__":
    generate_key()
