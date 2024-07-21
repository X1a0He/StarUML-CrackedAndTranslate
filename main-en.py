import platform, os, shutil, subprocess, json, re, glob, datetime, ctypes
system = platform.system()

def extract(base):
    os.system(f"cd {base} && asar extract app.asar app")

def pack(base):
    os.system(f"cd {base} && asar pack app app.asar")

def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"「{now}」 {msg}")

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_file_list(base, path_pattern):
    base_path = convert_path(f"{base}/app/")

    if '*' in convert_path(path_pattern):
        full_path = os.path.join(base_path, convert_path(path_pattern))
        return glob.glob(full_path)
    else:
        return [os.path.join(base_path, convert_path(path_pattern))]

# Convert the slashes in the path under Windows，Fuck u Windows!
def convert_path(path):
    if system == "Darwin":
        return path
    elif system == 'Windows':
        return path.replace('/', '\\')

def is_staruml_running():
    # 这里本来要kill掉的，一想到肯定有傻逼会有未保存的图表，kill掉就丢失了，所以仁慈一下
    if system == 'Darwin':
        if os.system("pgrep -x StarUML > /dev/null 2>&1") == 0:
            log("检测到 StarUML 进程正在运行，请先关闭 StarUML 进程")
            # os.system("killall -9 StarUML") # macOS
            exit(0)
    elif system == 'Windows':
        if 'StarUML.exe' in subprocess.run(['tasklist', '/FI', 'IMAGENAME eq StarUML.exe'], capture_output=True, text=True).stdout:
            log("检测到 StarUML 进程正在运行，请先关闭 StarUML 进程")
            # os.system("taskkill /f /t /im StarUML.exe") # Windows
            exit(0)

def handler(base, user_choice):
    if user_choice == 0:
        crack(base, user_choice)

def crack(base, user_choice):
    log("StarUML cracking operation in progress...")
    home_dir = os.path.expanduser("~")
    try:
        if system == 'Darwin':
            user_path = os.path.join(home_dir, "Library", "Application Support", "StarUML")
            if not os.path.exists(rf"{user_path}"):
                log("Detected that this is the first time to install StarUML, creating user directory...")
                os.makedirs(rf"{user_path}")
                # chmod 777
                os.chmod(rf"{user_path}", 0o777)
                log("User directory created.")

            if os.path.exists(rf"{user_path}/license.key"):
                log("Remove the existing license.key file")
                os.remove(rf"{user_path}/license.key")

            # StarUML 6.2.0
            if os.path.exists(rf"{user_path}/lib.so"):
                log("Remove the existing lib.so file")
                os.remove(rf"{user_path}/lib.so")
            else:
                log("Failed to modify the evaluation days. The lib.so file does not exist. Please open StarUML once before running the crack.")

            with open(rf"{user_path}/lib.so", "w") as f:
                log("Modifying evaluation days...")
                f.write('9' * 309)
                log("Evaluation days modified")

            if os.system("command -v asar > /dev/null 2>&1") == 1:
                log("asar not detected, please install asar first")
                exit(0)

        elif system == 'Windows':
            user_path = os.path.join(home_dir, "AppData", "Roaming", "StarUML")
            os.remove(rf"{user_path}\license.key")
            os.remove(rf"{base}\app\license.key")
            if os.system("where asar >nul 2>nul") != 0:
                log("asar not detected, please install asar first")
                exit(0)
    except FileNotFoundError:
        pass
    except KeyboardInterrupt:
        pass

    username = input("Please enter the username to be displayed on the StarUML about dialog:")
    if not username: username = "Cracked by X1a0He"

    # 1. Only app.asar exists, only app.asar is processed
    if os.path.exists(convert_path(rf"{base}/app.asar")) and not os.path.exists(convert_path(rf"{base}/app")):
        crack_asar(base, username, user_choice)
    # 2. app.asar and app folder coexist, app.asar is processed first
    elif os.path.exists(convert_path(rf"{base}/app.asar")) and os.path.exists(convert_path(rf"{base}/app")):
        crack_asar(base, username, user_choice)
    # 3. If app.asar does not exist and only the app folder exists, only the app folder will be processed.
    elif not os.path.exists(convert_path(rf"{base}/app.asar")) and os.path.exists(convert_path(rf"{base}/app")):
        crack_app(base, username)

    log("StarUML cracking is complete, please follow the steps below")
    log("1. Run StarUML and select Help - Enter License Key from the menu bar.")
    log("2. When the window pops up, just click OK")

def crack_asar(base, username, user_choice):
    if not os.path.exists(convert_path(f"{base}/app_backup.asar")):
        log("backup app.asar -> app_backup.asar")
        shutil.copyfile(convert_path(f"{base}/app.asar"), convert_path(f"{base}/app_backup.asar"))

    log("extract app.asar")
    extract(base)
    crack_app(base, username)

    if user_choice != 2:
        log("pack app.asar")
        pack(base)
        log("delete app folder")
        shutil.rmtree(convert_path(f"{base}/app"))

    if system == 'Darwin':
        log("Repairing damaged")
        os.system("sudo xattr -cr /Applications/StarUML.app")
        log("Repair completed")

def crack_app(base, username):
    destination_path = convert_path(f"{base}/app/src/")
    shutil.copy("hook.js", destination_path)

    hook_file_path = os.path.join(destination_path, "hook.js")
    app_context_file_path = os.path.join(destination_path, "app-context.js")

    with open(hook_file_path, "r", encoding="utf-8") as file:
        js_content = file.read()
    new_js_content = js_content.replace("Cracked by X1a0He", username)

    with open(hook_file_path, "w", encoding="utf-8") as file:
        file.write(new_js_content)

    with open(app_context_file_path, "r", encoding="utf-8") as file:
        js_content = file.read()
        if 'require("./hook");' not in js_content:
            log("Hook writing...")
            new_js_content = js_content.replace('const _ = require("lodash");', 'require("./hook");\nconst _ = require("lodash");')

            with open(app_context_file_path, "w", encoding="utf-8") as file2:
                file2.write(new_js_content)
                log("Hook written")
        else:
            log("The hook has been written and does not need to be modified again")

def main():
    try:
        print("__  ___        ___  _   _        ____  _             _   _ __  __ _")
        print("\\ \\/ / | __ _ / _ \\| | | | ___  / ___|| |_ __ _ _ __| | | |  \\/  | |")
        print(" \\  /| |/ _` | | | | |_| |/ _ \\ \\___ \\| __/ _` | '__| | | | |\\/| | |")
        print(" /  \\| | (_| | |_| |  _  |  __/  ___) | || (_| | |  | |_| | |  | | |___")
        print("/_/\\_\\_|\\__,_|\\___/|_| |_|\\___| |____/ \\__\\__,_|_|   \\___/|_|  |_|_____|")
        print("StarUML「Mac & Win」Crack script")
        print("Github: https://github.com/X1a0He/StarUML-CrackedAndTranslate\n")

        is_staruml_running()

        if system == 'Darwin':
            if not os.geteuid() == 0:
                log("Please run this script with 「sudo」")
                exit(0)
        elif system == 'Windows':
            if ctypes.windll.shell32.IsUserAnAdmin():
                log("Please run this script with 「Administrator」")
                exit(0)

        # Check whether starUML is installed under macOS
        if system == 'Darwin':
            if not os.path.exists("/Applications/StarUML.app"):
                log("StarUML.app not detected, ending execution")
                exit(0)

        user_choice = int(input("0 -> Crack the StarUML\n-1 -> Exit\nPlease enter your selection: \n"))
        if user_choice == -1:
            exit(0)

        if user_choice == 0:
            if system == 'Darwin':
                base = "/Applications/StarUML.app/Contents/Resources"
                handler(base, user_choice)
                os.system("open -a StarUML")
            elif system == 'Windows':
                base = r"C:\Program Files\StarUML\resources"
                handler(base, user_choice)
                # I don't know what command to use to start StarUML
    except KeyboardInterrupt:
        print("\nThe user interrupted the program execution")

if __name__ == '__main__':
    main()
