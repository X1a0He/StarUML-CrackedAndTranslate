import platform, os, shutil, subprocess, json, re, glob, datetime, ctypes
system = platform.system()

def is_admin():
    # 你他妈的，要修改文件都是要权限的，不用 sudo 或者 管理员 身份，你修改nm呢？
    if system == 'Darwin' or system == 'Linux':
        if not os.geteuid() == 0:
            log("请以「sudo」运行此脚本")
            exit(0)
    elif system == 'Windows':
        if not ctypes.windll.shell32.IsUserAnAdmin():
            log("请以「管理员」身份运行此脚本")
            exit(0)

def is_installed():
    # macOS下检测是否安装了starUML，Windows下目录不确定，所以没写，拉倒吧
    if system == 'Darwin':
        print(os.path.join("Applications", "StarUML.app"))
        if not os.path.exists(os.path.join("/Applications", "StarUML.app")):
            log("未检测到 StarUML.app，请先到官网下载安装")
            exit(0)
    elif system == 'Windows':
        if not os.path.exists(os.path.join("C:\\", "Program Files", "StarUML", "StarUML.exe")):
            log("未检测到 StarUML.exe 或非官网下载安装，请先到官网下载安装")
            exit(0)

# 没安装asar的能不能滚去先看教程怎么装，没有asar跑牛魔呢？
def detect_asar():
    if system == "Darwin":
        if os.system("command -v asar > /dev/null 2>&1") == 1:
            log("未检测到asar，请先安装asar")
            exit(0)
    elif system == "Windows":
        if os.system("where asar >nul 2>nul") != 0:
            log("未检测到asar，请先安装asar")
            exit(0)
    elif system == "Linux":
        pass

def extract(base):
    os.system(f"cd {base} && asar extract app.asar app")

def pack(base):
    os.system(f"cd {base} && asar pack app app.asar")

def backup(base):
    if not os.path.exists(os.path.join(base, "app.asar.original")):
        log("备份 app.asar -> app.asar.original")
        shutil.copyfile(os.path.join(base, "app.asar"), os.path.join(base, "app.asar.original"))
    else:
        log("备份文件已存在，无需再次备份")

def rollback(base):
    if os.path.exists(os.path.join(base, "app.asar.original")):
        log("还原 app.asar.original -> app.asar")
        shutil.copyfile(os.path.join(base, "app.asar.original"), os.path.join(base, "app.asar"))
    else:
        log("还原文件不存在，无法还原")

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
        log("不支持的操作系统")
        exit(0)

    # 该文件夹不存在，则表示首次安装
    if not os.path.exists(rf"{user_path}"):
        log("请先打开一次 StarUML 再执行脚本")
        exit(0)

def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"「{now}」 {msg}")

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_file_list(path):
    if '*' in path:
        full_path = path
        return glob.glob(full_path)
    else:
        return [path]

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
            else:
                en_text = replacement['en']
                cn_text = replacement['cn']
                # log(f"正在替换 {en_text} -> {cn_text}")
                if option == 1 or option == 2:  # 汉化
                    content = content.replace(en_text, cn_text)
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
    if user_choice in (0, 1, 2):
        backup(base)

    if user_choice == 0:
        crack(base, user_choice)

    if user_choice == 1:
        translate(base, user_choice, language_file)

    if user_choice == 2:
        crack(base, user_choice)
        translate(base, user_choice, language_file)

    # 还原所有操作 2024.11.04 增加
    if user_choice == 3:
        rollback(base)

def translate(base, user_choice, language_file):
    log("正在进行 StarUML 汉化操作...")
    # 1. 仅存在app.asar，只处理app.asar
    if os.path.exists(os.path.join(base, "app.asar")) and not os.path.exists(os.path.join(base, "app")):
        translate_asar(language_file, base, user_choice)
    # 2. app.asar和app文件夹共存，优先处理app.asar
    elif os.path.exists(os.path.join(base, "app.asar")) and os.path.exists(os.path.join(base, "app")):
        # 如果用户选择破解并汉化，就不需要解包了
        if user_choice != 2:
            log("检测到 app.asar 和 app 文件夹共存，优先处理 app.asar")
            translate_asar(language_file, base, user_choice)
        elif user_choice == 2:
            translate_app(language_file, base, user_choice)
            log("打包 app.asar")
            pack(base)
            log("删除 app 文件夹")
            shutil.rmtree(os.path.join(base, "app"))
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif not os.path.exists(os.path.join(base, "app.asar")) and os.path.exists(os.path.join(base, "app")):
        log("检测到只存在 app 文件夹，本次操作仅对 app 文件夹进行处理")
        translate_app(language_file, base, user_choice)

    log("StarUML 汉化操作完成")

def translate_asar(language_file, base, user_choice):
    # 这里他妈的app.asar都存在了，还你妈node解包出错的话，你不是傻逼谁是傻逼
    log("解包 app.asar")
    extract(base)
    translate_app(language_file, base, user_choice)
    # 汉化完成后，对app.asar进行打包操作，并删除app文件夹
    log("打包 app.asar")
    pack(base)
    log("删除 app 文件夹")
    shutil.rmtree(os.path.join(base, "app"))

def translate_app(language_file, base, user_choice):
    log("正在汉化文件...")
    data = read_json(language_file)
    for path, replacements in data.items():
        files = get_file_list(os.path.join(base, "app", path))
        for file_path in files:
            replace_in_file(file_path, replacements, user_choice)
    log("文件汉化完成")

def crack(base, user_choice):
    log("正在进行 StarUML 破解操作...")
    # 先把原来的license.key文件删掉
    if system == "Linux":
        home_dir = os.path.expanduser(f"~{os.environ['SUDO_USER']}")
    else:
        home_dir = os.path.expanduser("~")
    try:
        if system == 'Darwin':
            user_path = os.path.join(home_dir, "Library", "Application Support", "StarUML")
            if os.path.exists(os.path.join(user_path, "license.key")):
                log("移除已存在的 license.key 文件")
                os.remove(os.path.join(user_path, "license.key"))
        elif system == 'Windows':
            user_path = os.path.join(home_dir, "AppData", "Roaming", "StarUML")
            if os.path.exists(os.path.join(user_path, "license.key")):
                log("移除已存在的 license.key 文件")
                os.remove(os.path.join(user_path, "license.key"))
                os.remove(os.path.join(base, "app", "license.key"))
        elif system == 'Linux':
            user_path = os.path.join(home_dir, ".config", "StarUML")
            if os.path.exists(os.path.join(user_path, "license.key")):
                log("移除已存在的 license.key 文件")
                os.remove(os.path.join(user_path, "license.key"))
                os.remove(os.path.join(user_path, "app", "license.key"))
    except FileNotFoundError:
        pass
    except KeyboardInterrupt:
        pass

    log("请输入StarUML关于页面要显示的用户名(回车即使用程序默认): ")
    username = input()
    if not username: username = "GitHub: X1a0He/StarUML-CrackedAndTranslate"
    # 1. 仅存在app.asar，只处理app.asar
    # 2. app.asar和app文件夹共存，优先处理app.asar
    if os.path.exists(os.path.join(base, "app.asar")) or os.path.exists(os.path.join(base, "app")):
        crack_asar(base, username, user_choice)
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif not os.path.exists(os.path.join(base, "app.asar")) and os.path.exists(os.path.join(base, "app")):
        crack_app(base, username)

    log("StarUML 破解处理完毕，请按照下列步骤进行操作")
    log("1. 运行StarUML，选择菜单栏的Help - Enter License Key")
    log("2. 弹出窗口后，直接点击OK即可")

def crack_asar(base, username, user_choice):
    log("解包 app.asar")
    extract(base)
    crack_app(base, username)
    # 如果用户选择破解并汉化的话，就不需要重新打包了，做完再打包
    if user_choice != 2:
        log("打包 app.asar")
        pack(base)
        log("删除 app 文件夹")
        shutil.rmtree(os.path.join(base, "app"))

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
            log("hook写入中...")
            new_js_content = js_content.replace('const _ = require("lodash");', 'require("./hook");\nconst _ = require("lodash");')

            with open(app_context_file_path, "w", encoding="utf-8") as file2:
                file2.write(new_js_content)
                log("hook写入完毕")
        else:
            log("文本已被修改过，无需再次修改")

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
        print("StarUML「Mac & Win」一键破解汉化脚本")
        print("Github: https://github.com/X1a0He/StarUML-CrackedAndTranslate")
        print()

        is_admin()
        detect_asar()
        is_installed()
        is_first_install()
        is_staruml_running()

        user_choice = int(input("0 -> 仅破解\n1 -> 仅汉化\n2 -> 破解并汉化\n3 -> 还原所有\n-1 -> 退出运行\n请输入您的选择: \n"))
        if user_choice == -1:
            exit(0)

        if user_choice in (0, 1, 2, 3):
            if system == 'Darwin':
                base = os.path.join("/Applications", "StarUML.app", "Contents", "Resources")
                handler(base, user_choice)
                log("如遇到打开 StarUML 提示已损坏，请手动在终端执行如下命令后，在 Application 右键打开 StarUML")
                log("sudo xattr -cr /Applications/StarUML.app")
                log("macOS 15 的用户如果一直遇到提示已损坏，建议先打开一遍 StarUML 后再运行")
                # os.system("open -a StarUML")
            elif system == 'Windows':
                base = os.path.join("C:\\", "Program Files", "StarUML", "resources")
                handler(base, user_choice)
                # Windows的启动功不知道什么命令，拉倒吧
            elif system == 'Linux':
                # Linux 系统未经证实，请谨慎运行
                base = "/opt/StarUML/resources"
                handler(base, user_choice)
    except KeyboardInterrupt:
        print("\n用户中断了程序执行")

if __name__ == '__main__':
    main()
