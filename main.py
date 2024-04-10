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

# 为了nm的Windows，还要写一个方法来将路径的斜杠转换一下，Fuck u Windows!
def convert_path(path):
    if system == "Darwin":
        return path
    elif system == 'Windows':
        return path.replace('/', '\\')

def replace_in_file(file_path, replacements, option):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # log(f"正在替换文件: {file_path}")
    content = content.replace(r"\u2026", "...").replace(r"\"dev\"", "dev")
    for replacement in replacements:
        for key, value in replacement.items():
            if isinstance(value, list):  # 处理嵌套列表
                for item in value:
                    en_text = item['en']
                    cn_text = item['cn']
                    # log(f"正在替换 {en_text} -> {cn_text}")
                    if option == 1 or option == 2:  # 汉化
                        content = re.sub(f'"{key}": "{re.escape(en_text)}"', f'"{key}": "{re.escape(cn_text)}"'.replace('\\', ''), content)
                    elif option == 3:  # 还原
                        content = re.sub(f'"{key}": "{re.escape(cn_text)}"'.replace('\\', ''), f'"{key}": "{re.escape(en_text)}"', content)
            else:
                en_text = replacement['en']
                cn_text = replacement['cn']
                # log(f"正在替换 {en_text} -> {cn_text}")
                if option == 1 or option == 2:  # 汉化
                    content = content.replace(en_text, cn_text)
                elif option == 3:  # 还原
                    content = content.replace(cn_text, en_text)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

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
    language_file = "StarUML_Language.json"
    if user_choice == 0:
        crack(base, user_choice)

    if user_choice == 1 or user_choice == 3:
        translate(base, user_choice, language_file)

    if user_choice == 2:
        crack(base, user_choice)
        translate(base, user_choice, language_file)

def translate(base, user_choice, language_file):
    log("\n正在进行 StarUML 汉化操作...")
    # 1. 仅存在app.asar，只处理app.asar
    if os.path.exists(convert_path(f"{base}/app.asar")) and not os.path.exists(convert_path(f"{base}/app")):
        translate_asar(language_file, base, user_choice)
    # 2. app.asar和app文件夹共存，优先处理app.asar
    elif os.path.exists(convert_path(f"{base}/app.asar")) and os.path.exists(convert_path(f"{base}/app")):
        # 如果用户选择破解并汉化，就不需要解包了
        if user_choice != 2:
            log("检测到 app.asar 和 app 文件夹共存，优先处理 app.asar")
            translate_asar(language_file, base, user_choice)
        elif user_choice == 2:
            translate_app(language_file, base, user_choice)
            log("打包 app.asar")
            pack(base)
            log("删除 app 文件夹")
            shutil.rmtree(convert_path(f"{base}/app"))
            os.system(f"rm -rf {base}/app")
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif not os.path.exists(convert_path(f"{base}/app.asar")) and os.path.exists(convert_path(f"{base}/app")):
        log("检测到只存在 app 文件夹，本次操作仅对 app 文件夹进行处理")
        translate_app(language_file, base, user_choice)

    log("StarUML 汉化操作完成")

def translate_asar(language_file, base, user_choice):
    # 先对app.asar进行备份，备份文件名为app_backup.asar
    if not os.path.exists(convert_path(rf"{base}/app_backup.asar")):
        log("备份 app.asar -> app_backup.asar")
        shutil.copyfile(convert_path(rf"{base}/app.asar"), convert_path(rf"{base}/app_backup.asar"))

    # 备份完就对app.asar进行解包操作，这里他妈的app.asar都存在了，还你妈node解包出错的话，你不是傻逼谁是傻逼
    log("解包 app.asar")
    extract(base)
    translate_app(language_file, base, user_choice)
    # 汉化完成后，对app.asar进行打包操作，并删除app文件夹
    log("打包 app.asar")
    pack(base)
    log("删除 app 文件夹")
    shutil.rmtree(rf"{base}\app")

def translate_app(language_file, base, user_choice):
    log("正在汉化文件...")
    data = read_json(language_file)
    for path, replacements in data.items():
        files = get_file_list(base, path)
        for file_path in files:
            replace_in_file(file_path, replacements, user_choice)
    log("文件汉化完成")

def crack(base, user_choice):
    log("\n正在进行 StarUML 破解操作...")
    # 先把原来的license.key文件删掉
    home_dir = os.path.expanduser("~")
    try:
        if system == 'Darwin':
            user_path = os.path.join(home_dir, "Library", "Application Support", "StarUML")
            os.remove(rf"{user_path}/license.key")
            if os.system("command -v asar > /dev/null 2>&1") == 1:
                log("未检测到asar，请先安装asar")
                exit(0)

        elif system == 'Windows':
            user_path = os.path.join(home_dir, "AppData", "Roaming", "StarUML")
            os.remove(rf"{user_path}\license.key")
            os.remove(rf"{base}\app\license.key")
            # 没安装asar的能不能滚去先看教程怎么装，没有asar跑牛魔呢？
            if os.system("where asar >nul 2>nul") != 0:
                log("未检测到asar，请先安装asar")
                exit(0)
    except FileNotFoundError:
        pass
    except KeyboardInterrupt:
        pass

    username = input("请输入StarUML关于页面要显示的用户名: ")
    if not username: username = "Cracked by X1a0He"

    # 1. 仅存在app.asar，只处理app.asar
    if os.path.exists(convert_path(rf"{base}/app.asar")) and not os.path.exists(convert_path(rf"{base}/app")):
        crack_asar(base, username, user_choice)
    # 2. app.asar和app文件夹共存，优先处理app.asar
    elif os.path.exists(convert_path(rf"{base}/app.asar")) and os.path.exists(convert_path(rf"{base}/app")):
        crack_asar(base, username, user_choice)
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif not os.path.exists(convert_path(rf"{base}/app.asar")) and os.path.exists(convert_path(rf"{base}/app")):
        crack_app(base, username)

    log("StarUML 破解处理完毕，请按照下列步骤进行操作")
    log("1. 运行StarUML，选择菜单栏的Help - Enter License Key")
    log("2. 弹出窗口后，直接点击OK即可")

def crack_asar(base, username, user_choice):
    if not os.path.exists(convert_path(f"{base}/app_backup.asar")):
        log("备份 app.asar -> app_backup.asar")
        shutil.copyfile(convert_path(f"{base}/app.asar"), convert_path(f"{base}/app_backup.asar"))

    log("解包 app.asar")
    extract(base)
    crack_app(base, username)

    # 如果用户选择破解并汉化的话，就不需要重新打包了，做完再打包
    if user_choice != 2:
        log("打包 app.asar")
        pack(base)
        log("删除 app 文件夹")
        shutil.rmtree(convert_path(f"{base}/app"))

    if system == 'Darwin':
        log("正在修复已损坏")
        os.system("sudo xattr -r -d com.apple.quarantine /Applications/StarUML.app")
        log("修复完毕")

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
        if 'require("./hook);' not in js_content:
            log("hook写入中...")
            new_js_content = js_content.replace('const _ = require("lodash");', 'require("./hook");\nconst _ = require("lodash");')

            with open(app_context_file_path, "w", encoding="utf-8") as file2:
                file2.write(new_js_content)
                log("hook写入完毕")
        else:
            log("文本已被修改过，无需再次修改")

def main():
    try:
        # 用户选择
        print("__  ___        ___  _   _        ____  _             _   _ __  __ _")
        print("\\ \\/ / | __ _ / _ \\| | | | ___  / ___|| |_ __ _ _ __| | | |  \\/  | |")
        print(" \\  /| |/ _` | | | | |_| |/ _ \\ \\___ \\| __/ _` | '__| | | | |\\/| | |")
        print(" /  \\| | (_| | |_| |  _  |  __/  ___) | || (_| | |  | |_| | |  | | |___")
        print("/_/\\_\\_|\\__,_|\\___/|_| |_|\\___| |____/ \\__\\__,_|_|   \\___/|_|  |_|_____|")
        print("StarUML「Mac & Win」一键破解汉化脚本")
        print("Github: https://github.com/X1a0He/StarUML-CrackedAndTranslate\n")

        is_staruml_running()

        # 你他妈的，要修改文件都是要权限的，不用 sudo 或者 管理员 身份，你修改nm呢？
        if system == 'Darwin':
            if not os.geteuid() == 0:
                log("请以「sudo」运行此脚本")
                exit(0)
        elif system == 'Windows':
            if ctypes.windll.shell32.IsUserAnAdmin():
                log("请以「管理员」身份运行此脚本")
                exit(0)

        user_choice = int(input("0 -> 仅破解\n1 -> 仅汉化\n2 -> 破解并汉化\n3 -> 还原语言\n-1 -> 退出运行\n请输入您的选择: \n"))
        if user_choice == -1:
            exit(0)

        # 还原功能我测试过了，但是不保证有什么问题，既然你要汉化，那你还原干什么呢？找骂？
        if user_choice in (0, 1, 2, 3):
            if system == 'Darwin':
                base = "/Applications/StarUML.app/Contents/Resources"
                handler(base, user_choice)
                os.system("open -a StarUML")
            elif system == 'Windows':
                base = r"C:\Program Files\StarUML\resources"
                handler(base, user_choice)
                # Windows的启动功不知道什么命令，拉倒吧
    except KeyboardInterrupt:
        print("\n用户中断了程序执行")

if __name__ == '__main__':
    main()
