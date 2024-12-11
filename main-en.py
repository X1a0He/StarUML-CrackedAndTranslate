import platform, os, shutil, subprocess, json, datetime, ctypes
system = platform.system()

def is_admin():
    if system == 'Darwin' or system == 'Linux':
        if not os.geteuid() == 0:
            log("Please run this script with 「sudo」")
            exit(0)
    elif system == 'Windows':
        if not ctypes.windll.shell32.IsUserAnAdmin():
            log("Please run this script with 「Administrator」")
            exit(0)

def is_installed():
    if system == 'Darwin':
        if not os.path.exists(os.path.join("/Applications", "StarUML.app")):
            log("StarUML.app is not detected, please download and install it from the official website first")
            exit(0)
    elif system == 'Windows':
        if not os.path.exists(os.path.join("C:\\", "Program Files", "StarUML", "StarUML.exe")):
            log("StarUML.exe is not detected or the installation is not from the official website. Please download and install from the official website first.")
            exit(0)

def detect_asar():
    if system == "Darwin":
        if os.system("command -v asar > /dev/null 2>&1") == 1:
            log("asar not detected, please install asar first")
            exit(0)
    elif system == "Windows":
        if os.system("where asar >nul 2>nul") != 0:
            log("asar not detected, please install asar first")
            exit(0)
    elif system == "Linux":
        pass

def extract(base):
    asar_file = os.path.join(base, "app.asar")
    asar_folder = os.path.join(base, "app")
    os.system(f"asar extract \"{asar_file}\" \"{asar_folder}\"")

def pack(base):
    asar_file = os.path.join(base, "app.asar")
    asar_folder = os.path.join(base, "app")
    os.system(f"asar pack \"{asar_folder}\" \"{asar_file}\"")

def backup(base):
    if not os.path.exists(os.path.join(base, "app.asar.original")):
        log("backup app.asar -> app.asar.original")
        shutil.copyfile(os.path.join(base, "app.asar"), os.path.join(base, "app.asar.original"))
    else:
        log("The backup file already exists, no need to back it up again")

def rollback(base):
    if os.path.exists(os.path.join(base, "app.asar.original")):
        log("restored app.asar.original -> app.asar")
        shutil.copyfile(os.path.join(base, "app.asar.original"), os.path.join(base, "app.asar"))
    else:
        log("The original file does not exist and cannot be restored.")

def is_first_install():
    if system == "Darwin":
        home_dir = os.path.expanduser("~")
        user_path = os.path.join(home_dir, "Library", "Application Support", "StarUML")
    elif system == "Windows":
        home_dir = os.path.expanduser("~")
        user_path = os.path.join(home_dir, "AppData", "Roaming", "StarUML")
    elif system == "Linux":
        home_dir = os.path.expanduser(f"~{os.environ['SUDO_USER']}")
        user_path = os.path.join(home_dir, ".config", "StarUML")
    else:
        log("Unsupported system")
        exit(0)

    # 该文件夹不存在，则表示首次安装
    if not os.path.exists(rf"{user_path}"):
        log("Please open StarUML first and then execute the script")
        exit(0)

def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"「{now}」 {msg}")

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def is_staruml_running():
    if system == 'Darwin':
        if os.system("pgrep -x StarUML > /dev/null 2>&1") == 0:
            log("It is detected that the StarUML process is running, please close the StarUML process first")
            # os.system("killall -9 StarUML") # macOS
            exit(0)
    elif system == 'Windows':
        if 'StarUML.exe' in subprocess.run(['tasklist', '/FI', 'IMAGENAME eq StarUML.exe'], capture_output=True, text=True).stdout:
            log("It is detected that the StarUML process is running, please close the StarUML process first")
            # os.system("taskkill /f /t /im StarUML.exe") # Windows
            exit(0)

def handler(base, user_choice):
    if user_choice == 0:
        backup(base)
        crack(base, user_choice)

def crack(base, user_choice):
    log("StarUML cracking operation in progress...")
    if system == "Linux":
        home_dir = os.path.expanduser(f"~{os.environ['SUDO_USER']}")
    else:
        home_dir = os.path.expanduser("~")
    try:
        if system == 'Darwin':
            user_path = os.path.join(home_dir, "Library", "Application Support", "StarUML")
            if os.path.exists(os.path.join(user_path, "license.key")):
                log("Remove the existing license.key file")
                os.remove(os.path.join(user_path, "license.key"))
        elif system == 'Windows':
            user_path = os.path.join(home_dir, "AppData", "Roaming", "StarUML")
            if os.path.exists(os.path.join(user_path, "license.key")):
                log("Remove the existing license.key file")
                os.remove(os.path.join(user_path, "license.key"))
                os.remove(os.path.join(base, "app", "license.key"))
        elif system == 'Linux':
            user_path = os.path.join(home_dir, ".config", "StarUML")
            if os.path.exists(os.path.join(user_path, "license.key")):
                log("Remove the existing license.key file")
                os.remove(os.path.join(user_path, "license.key"))
                os.remove(os.path.join(user_path, "app", "license.key"))
    except FileNotFoundError:
        pass
    except KeyboardInterrupt:
        pass

    username = input("Please enter the username to be displayed on the StarUML about dialog:")
    if not username: username = "GitHub: X1a0He/StarUML-CrackedAndTranslate"

    # 1. Only app.asar exists, only app.asar is processed
    # 2. app.asar and app folder coexist, app.asar is processed first
    if os.path.exists(os.path.join(base, "app.asar")) or os.path.exists(os.path.join(base, "app")):
        crack_asar(base, username, user_choice)
    # 3. If app.asar does not exist and only the app folder exists, only the app folder will be processed.
    elif not os.path.exists(os.path.join(base, "app.asar")) and os.path.exists(os.path.join(base, "app")):
        crack_app(base, username)

    log("StarUML cracking is complete, please follow the steps below")
    log("1. Run StarUML and select Help - Enter License Key from the menu bar.")
    log("2. When the window pops up, just click OK")

def crack_asar(base, username, user_choice):
    log("extract app.asar")
    extract(base)
    crack_app(base, username)

def add_member_after_label(obj, target_label, new_member):
    if isinstance(obj, list):
        for index, item in enumerate(obj):
            if isinstance(item, dict) and item.get("label") == target_label:
                obj.insert(index + 1, new_member)
                return True
            result = add_member_after_label(item, target_label, new_member)
            if result:
                return result
    elif isinstance(obj, dict):
        for key in obj:
            if isinstance(obj[key], (dict, list)):
                result = add_member_after_label(obj[key], target_label, new_member)
                if result:
                    return result
    return None

def write_author_info(base):
    app_folder = os.path.join(base, "app")
    src_folder = os.path.join(app_folder, "src")
    # 修改关于弹窗部分
    static_folder = os.path.join(src_folder, "static")
    html_contents_folder = os.path.join(static_folder, "html-contents")
    about_dialog = os.path.join(html_contents_folder, "about-dialog.html")
    with open(about_dialog, "r", encoding="utf-8") as file:
        html_content = file.read()
    new_html_content = html_content.replace("<span class=\"license\" style=\"font-weight: 600;\"></span>",
                                            "<a href=\"https://github.com/X1a0He/StarUML-CrackedAndTranslate\"><span class=\"license\" style=\"font-weight: 600;\"></span></a>")
    with open(about_dialog, "w", encoding="utf-8") as file:
        file.write(new_html_content)
    # 修改标题部分
    titlebar_view = os.path.join(src_folder, "views", "titlebar-view.js")
    with open(titlebar_view, "r", encoding="utf-8") as file:
        js_content = file.read()
    new_js_content = js_content.replace("""title += "(EVALUATION MODE)";
    }""",
                                        """title += "(EVALUATION MODE)";
    } else { title += '【By GitHub: X1a0He/StarUML-CrackedAndTranslate】'}""")
    with open(titlebar_view, "w", encoding="utf-8") as file:
        file.write(new_js_content)
    # 修改菜单栏部分
    resources_folder = os.path.join(app_folder, "resources")
    darwin_json = os.path.join(resources_folder, "default", "menus", "darwin.json")
    win32_json = os.path.join(resources_folder, "default", "menus", "win32.json")
    linux_json = os.path.join(resources_folder, "default", "menus", "linux.json")
    darwin_data = read_json(darwin_json)
    win32_data = read_json(win32_json)
    linux_data = read_json(linux_json)
    add_member_after_label(darwin_data, "About StarUML", {
        "label": "By GitHub: X1a0He/StarUML-CrackedAndTranslate",
        "id": "",
        "command": "help:cracked"
    })
    add_member_after_label(win32_data, "About StarUML", {
        "label": "By GitHub: X1a0He/StarUML-CrackedAndTranslate",
        "id": "",
        "command": "help:cracked"
    })
    add_member_after_label(linux_data, "About StarUML", {
        "label": "By GitHub: X1a0He/StarUML-CrackedAndTranslate",
        "id": "",
        "command": "help:cracked"
    })
    write_json(darwin_json, darwin_data)
    write_json(win32_json, win32_data)
    write_json(linux_json, linux_data)
    engine_folder = os.path.join(src_folder, "engine")
    default_commands = os.path.join(engine_folder, "default-commands.js")
    with open(default_commands, "r", encoding="utf-8") as file:
        js_content = file.read()

    if 'app.commands.register("help:cracked", () => shell.openExternal("https://github.com/X1a0He/StarUML-CrackedAndTranslate"), "Help: Cracked");' not in js_content:
        js_content += "\n" + 'app.commands.register("help:cracked", () => shell.openExternal("https://github.com/X1a0He/StarUML-CrackedAndTranslate"), "Help: Cracked");'

    with open(default_commands, "w", encoding="utf-8") as file:
        file.write(js_content)

def crack_app(base, username):
    destination_path = os.path.join(base, "app", "src")
    shutil.copy("hook.js", destination_path)

    hook_file_path = os.path.join(destination_path, "hook.js")
    app_context_file_path = os.path.join(destination_path, "app-context.js")

    with open(hook_file_path, "r", encoding="utf-8") as file:
        js_content = file.read()
    new_js_content = js_content.replace("GitHub: X1a0He/StarUML-CrackedAndTranslate", username)

    with open(hook_file_path, "w", encoding="utf-8") as file:
        file.write(new_js_content)

    with open(app_context_file_path, "r", encoding="utf-8") as file:
        js_content = file.read()
        if 'require("./hook");' not in js_content:
            log("Hook writing...")
            new_js_content = js_content.replace('this.appReady();', 'require("./hook");\nthis.appReady();')

            with open(app_context_file_path, "w", encoding="utf-8") as file2:
                file2.write(new_js_content)
                log("Hook written")
        else:
            log("The hook has been written and does not need to be modified again")
    write_author_info(base)

def main():
    try:
        print(" -----------------------------------------------")
        print("|                                               |")
        print("| ██╗  ██╗ ██╗ █████╗  ██████╗ ██╗  ██╗███████╗ |")
        print("| ╚██╗██╔╝███║██╔══██╗██╔═████╗██║  ██║██╔════╝ |")
        print("|  ╚███╔╝ ╚██║███████║██║██╔██║███████║█████╗   |")
        print("|  ██╔██╗  ██║██╔══██║████╔╝██║██╔══██║██╔══╝   |")
        print("| ██╔╝ ██╗ ██║██║  ██║╚██████╔╝██║  ██║███████╗ |")
        print("| ╚═╝  ╚═╝ ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ |")
        print("|                StarUML Cracker                |")
        print(" -----------------------------------------------")
        print("StarUML「Mac & Win」Crack script")
        print("Github: https://github.com/X1a0He/StarUML-CrackedAndTranslate")
        print()

        is_admin()
        detect_asar()
        is_installed()
        is_first_install()
        is_staruml_running()

        log("macOS 15 users, please make sure to manually open StarUML once after updating StarUML and then execute the script")
        user_choice = int(input("0 -> Crack the StarUML\n-1 -> Exit\nPlease enter your selection: \n"))
        if user_choice == -1:
            exit(0)

        if user_choice == 0:
            if system == 'Darwin':
                base = os.path.join("/Applications", "StarUML.app", "Contents", "Resources")
                handler(base, user_choice)
                log("If you encounter a message that StarUML is damaged when you open it, please manually execute the following command in the terminal, right-click Application to open StarUML")
                log("sudo xattr -cr /Applications/StarUML.app")
                log("If macOS 15 users keep getting the damaged message , it is recommended to open StarUML first and then run this script again.")
                # os.system("open -a StarUML")
            elif system == 'Windows':
                base = os.path.join("C:\\", "Program Files", "StarUML", "resources")
                handler(base, user_choice)
                # I don't know what command to use to start StarUML
            elif system == 'Linux':
                # Linux system is unverified, please run with caution
                base = "/opt/StarUML/resources"
                handler(base, user_choice)
    except KeyboardInterrupt:
        print("\nThe user interrupted the program execution")

if __name__ == '__main__':
    main()
