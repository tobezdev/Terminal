import datetime
import os
import random
import shutil
import string
import threading
import time

import psutil
from colorama import Fore, Style
from tabulate import tabulate

_version = "0.0.2*alpha"

def is_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


skiploading = False

if os.name in ["nt", "dos"]:
    USER = str(os.getlogin())
    CLEAR = str("cls")
elif os.name in ["posix"]:
    USER = str(os.environ.get("REPL_OWNER"))
else:
    USER = str(os.environ.get("USERNAME"))
    if USER == "None":
        USER = str(os.path.expanduser("~"))
        if USER == "None":
            USER = "Anonymous"


def show_loading_screen():
    term_name = "{Tobez: The Terminal}"
    print(Fore.GREEN + Style.BRIGHT +
          f"Welcome [ {Fore.MAGENTA}{USER}{Fore.GREEN} ] to {term_name}")
    width = 40
    total = 100
    interval = total / width
    for i in range(width + 1):
        progress = int(i * interval)
        bar = '█' * i
        stars = '=' * (width - i)
        loading_text = f"[{bar}{stars}] {progress}%"
        print(Fore.CYAN + loading_text, end='\r')
        time.sleep(0.1)
    print(Style.RESET_ALL)


if not skiploading:
    show_loading_screen()

current_datetime = datetime.datetime.now()
day = current_datetime.isoweekday()

if day == 1:
    day = "Monday"
elif day == 2:
    day = "Tuesday"
elif day == 3:
    day = "Wednesday"
elif day == 4:
    day = "Thursday"
elif day == 5:
    day = "Friday"
elif day == 6:
    day = "Saturday"
elif day == 7:
    day = "Sunday"

os.system('clear')
acv = os.getcwd()
id = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
current_datetime = datetime.datetime.now()
date_string = current_datetime.strftime("%d-%m-%Y")
print(f"{Fore.MAGENTA}Run_id: {Fore.CYAN}{id}{Fore.MAGENTA}  Version: {Fore.CYAN}{_version}  {Fore.MAGENTA}Date: {Fore.CYAN}{day} / {date_string}")

def handle_input():
    while True:
        user_input = input(
            f"{Fore.MAGENTA}@{USER}{os.getcwd()}:{Fore.GREEN}~$ ")
        if not user_input:
            continue
        X, *args = user_input.split()
        if X == 'kill':
            if args:
                if is_int(args[0]):
                    id = args[0]
                    print(Fore.RED +
                          f'The process with PID {id} has been terminated.' + Style.RESET_ALL)
                else:
                    p_name = args[0]
                    print(Fore.RED +
                          f'The process "{p_name}" has has terminated.')
                if args[0].lower() == "terminal" or int(args[0]) == 0:
                    raise Exception(
                        Style.BRIGHT + "A program requied by the system was shut down, or was not started correctly." + Style.RESET_ALL + Fore.RED
                    )
            else:
                print(Fore.RED + "Usage: kill [(pID|name)]")

        elif X in ['clear', 'cls']:
            os.system("clear")
            current_datetime = datetime.datetime.now()
            date_string = current_datetime.strftime("%d/%m/%Y")
            print(
                f"{Fore.MAGENTA}Run_id: {Fore.CYAN}{id}{Fore.MAGENTA}  //  Version: {Fore.CYAN}{_version}  //  {Fore.MAGENTA}Date: {Fore.CYAN}{day} / {date_string}"
            )
        elif X in ['help']:
            print("""
Help Menu:
    - kill [(pID|name)]: Terminates the process with the pID or name provided.
    - clear/cls: Clears the terminal screen
    - help: Displays a help message with a list of available commands
    - cd [directory]: Changes the current directory to the specified director
    - ls: Lists the files and directories in the current directory
    - edit [filename]: Opens the specified file in the default editor for editing
    - write [filename]: Appends text to the specified file and allows you to create multiple lines and create text files (type 'exit' to stop)
    - run [filetype][filename]: Executes the specified file with support of (python)
    - cat [filename]: Displays the contents of the specified file
    - timer [seconds]: Sets a timer for the specified number of seconds
    - cp [source] [destination]: Copies a file from the source location to the destination location
    - mv [source] [destination]: Moves or renames a file from the source location to the destination location
    - rm [filename]: Deletes a file
    - mkdir [directory]: Creates a new directory
    - rmdir [directory]: Removes a directory (if it's empty)
    - howdoi [query]: Assists with coding, and provides snippets of code
    - disk: Displays information about the disk usage
    - cpu: Displays information about the CPU usage
    - restart: Restart the terminal (appplies any new code) [dev only]
         """)
        elif X in ['cd', '..']:
            if X == 'cd':
                if not args:
                    print(Fore.RED + "Error: Missing directory name" +
                          Style.RESET_ALL)
                    continue
                try:
                    res = os.chdir(args[0])
                    print(f"Changed directory to {res}")

                except FileNotFoundError:
                    print(Fore.RED +
                          f"Error: Directory '{args[0]}' not found" +
                          Style.RESET_ALL)
            elif X == '..':
                res = os.chdir('..')
                print(f"Changed directory to {res}")

        elif X == 'write':
            if not args:
                print(Fore.RED + "Error: Missing file name" + Style.RESET_ALL)
                continue
            filename = args[0]
            try:
                with open(filename, 'a') as file:
                    while True:
                        line = input()
                        if line == 'exit':
                            break
                        file.write(line + '\n')
                    file.close()
            except FileNotFoundError:
                print(Fore.RED + f"Error: File '{filename}' not found" +
                      Style.RESET_ALL)

        elif X == 'run':
            if len(args) < 2:
                print(Fore.RED + "Error: Missing file type and/or file name" + Style.RESET_ALL)
                continue

            file_type = args[0]
            filename = args[1]

            try:
                if os.path.isfile(filename):
                    if file_type == 'python' or file_type == 'py':
                        os.system(f"python {filename}")
                    elif file_type == 'cpp' or file_type == 'c++':
                        os.system(f"g++ {filename} -o {filename}.out && ./{filename}.out")
                    elif file_type == "js" or file_type == "javascript":
                        os.system(f"node {filename}")
                    else:
                        print(Fore.RED + "Error: Unsupported file type" +
                              Style.RESET_ALL)
                else:
                    print(Fore.RED + f"Error: File '{filename}' not found" +
                          Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)

        elif X.startswith("edit"):
            if not args:
                print(Fore.RED + "Error: Missing file name" + Style.RESET_ALL)
                continue
            filename = args[0]
            try:
                with open(filename, 'r') as file:
                    contents = file.read()
                    if filename.endswith(".txt"):
                        contents = (Fore.WHITE + contents + Style.RESET_ALL +  Fore.GREEN)
                    elif filename.endswith(".py"):
                        pass
                    elif filename.endswith(".js"):
                        pass
                    elif filename.endswith(".cpp"):
                        pass

                print(f"Editing file: {filename}")
                print("===FILE CONTENTS===")
                print(contents)
                print("===================")

                print("Enter new content: Type 'help' for file controls:\n")
                edited_contents = []
                while True:
                    line = input()
                    if line == 'exit':
                        break
                    if line == "help":
                        print("""
File Controls:
'exit' - Stop editing file
'help' - Displays this help message
'del' - Delete the selected line number
                        """)
                    if line == 'del':
                        ln_no = input(
                            "Enter the line number to delete. Type 'cancel' to cancel: "
                        )
                        if ln_no == 'cancel':
                            pass
                        else:
                            with open(filename, 'rw+') as file:
                                line = file.readline(int(ln_no))
                                line = ""
                    edited_contents.append(line)

                contents = '\n'.join(edited_contents)

                with open(filename, 'w') as file:
                    file.write(contents)
                    print(f"File '{filename}' saved successfully.")

            except FileNotFoundError:
                print(Fore.RED + f"Error: File '{filename}' not found" +
                      Style.RESET_ALL)

        elif X.startswith("cat"):
            if not args:
                print(Fore.RED + "Error: Missing file name" + Style.RESET_ALL)
                continue
            filename = args[0]
            if os.path.isdir(filename):
                print(Fore.RED + f"Error: '{filename}' is a directory." +
                      Style.RESET_ALL)
            else:
                try:
                    with open(filename, 'r') as file:
                        contents = file.read()

                    print(f"Reading file: {filename}")
                    print("===FILE CONTENTS===")
                    print(Fore.WHITE + contents + Style.RESET_ALL + Fore.GREEN)
                    print("===================")

                except FileNotFoundError:
                    print(Fore.RED + f"Error: File '{filename}' not found" +
                          Style.RESET_ALL)

        elif X.startswith("timer"):
            if not args:
                print(Fore.RED + "Error: Missing timer duration" +
                      Style.RESET_ALL)
                continue
            duration = args[0]
            try:
                duration = int(duration)
                threading.Timer(duration, times_up).start()
                handle_input()
            except ValueError:
                print(Fore.RED +
                      f"Error: Invalid timer duration: '{duration}'" +
                      Style.RESET_ALL)

        elif X == 'cp':
            if len(args) != 2:
                print(Fore.RED + "Usage: cp [source] [destination]" +
                      Style.RESET_ALL)
            else:
                source, destination = args
                try:
                    shutil.copy(source, destination)
                    print(f"File '{source}' copied to '{destination}'")
                except FileNotFoundError:
                    print(Fore.RED + f"Error: File '{source}' not found" +
                          Style.RESET_ALL)

        elif X == 'mv':
            if len(args) != 2:
                print(Fore.RED + "Usage: mv [source] [destination]" +
                      Style.RESET_ALL)
            else:
                source, destination = args
                try:
                    shutil.move(source, destination)
                    print(f"File '{source}' moved to '{destination}'")
                except FileNotFoundError:
                    print(Fore.RED + f"Error: File '{source}' not found" +
                          Style.RESET_ALL)

        elif X == 'rm':
            if not args:
                print(Fore.RED + "Error: Missing file name" + Style.RESET_ALL)
            else:
                filename = args[0]
                try:
                    os.remove(filename)
                    print(f"File '{filename}' deleted")
                except FileNotFoundError:
                    print(Fore.RED + f"Error: File '{filename}' not found" +
                          Style.RESET_ALL)

        elif X == 'mkdir':
            if not args:
                print(Fore.RED + "Error: Missing directory name" +
                      Style.RESET_ALL)
            else:
                directory = args[0]
                try:
                    os.mkdir(directory)
                    print(f"Directory '{directory}' created")
                except FileExistsError:
                    print(Fore.RED +
                          f"Error: Directory '{directory}' already exists" +
                          Style.RESET_ALL)

        elif X == 'dir':
            directory = '/' if args and args[0] == '/s' else '../' if not args else args[0]
            try:
                print(Fore.LIGHTGREEN_EX +
                      f"Showing contents of directory: [{directory}]")
                for i in os.listdir(directory):
                    try:
                        print(Fore.LIGHTGREEN_EX +
                              f"[{os.path.getsize(i)} MiB] {i}" +
                              Style.RESET_ALL)
                    except (Exception, FileNotFoundError):
                        print(
                            Fore.RED +
                            f"Hidden or locked files cannot be displayed in this directory."
                            + Style.RESET_ALL)
            except (Exception, FileNotFoundError):
                print(
                    Fore.RED +
                    f"Hidden or locked files cannot be displayed in this directory."
                    + Style.RESET_ALL)

        elif X == 'rmdir' or X == 'deldir':
            if not args:
                print(Fore.RED + "Error: Missing directory name" +
                      Style.RESET_ALL)
            else:
                directory = args[0]
                try:

                    os.rmdir(directory)
                    print(f"Directory '{directory}' removed")
                except FileNotFoundError:
                    print(Fore.RED +
                          f"Error: Directory '{directory}' not found" +
                          Style.RESET_ALL)
                except OSError as e:
                    print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        elif X == 'howdoi':
            asking = input('> ')
            os.system("howdoi " + asking)
        elif X == 'disk':
            try:
                df = psutil.disk_usage('/')
                print(f"Total space: {df.total / (2**30)} GB")
                print(f"Used space: {df.used / (2**30)} GB")
                print(f"Free space: {df.free / (2**30)} GB")
            except Exception as e:
                print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        elif X == 'cpu':
            try:
                print(f"CPU Usage: {psutil.cpu_percent()}%")
            except Exception as e:
                print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
        elif X == 'ls':
            try:
                directory = os.getcwd()
                items = os.listdir(directory)

                file_list = []
                folder_list = []

                for item in items:
                    if os.path.isfile(item):
                        file_list.append(('📝', item))
                else:
                    folder_list.append(('📁', item))

                sorted_items = sorted(folder_list) + sorted(file_list)

                print(Fore.GREEN + Style.BRIGHT + f"Contents of Directory: {directory}")
                table = tabulate(sorted_items, ['Type', 'Name'], tablefmt="fancy_grid")
                print(Fore.CYAN + table + Style.RESET_ALL)
            except NotADirectoryError:
                print(Fore.RED + Style.BRIGHT + "Directory {} does not exist." + Style.RESET_ALL)
        elif X == "restart":
            if USER == "TobezEdu" or USER == "TobezDev":
                print(Style.BRIGHT + Fore.CYAN + f"Identity confirmed: {USER}")
                print(Fore.RED + "Restarting the system..." + Style.RESET_ALL)
                os.system("python main.py")
            else:
                print(
                    Fore.RED +
                    "You do not have sufficient permissions to restart the terminal. This command is reserved for the development team only."
                    + Style.RESET_ALL)

        else:
            print(
                Fore.RED +
                f"Command '{X}'' not recognised. Try 'help' for a list of commands."
            )


def times_up():
    print(Fore.YELLOW + 'Time is up! ⏰' + Style.RESET_ALL)


threading.Thread(target=handle_input).start()
