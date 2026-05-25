import platform, os, shutil, subprocess, json, re, glob, datetime, ctypes
system = platform.system()
staruml_version = None
DEFAULT_USERNAME = "GitHub: X1a0He/StarUML-CrackedAndTranslate"
AUTHOR_MENU_ITEM = {
    "label": "By GitHub: X1a0He/StarUML-CrackedAndTranslate",
    "id": "",
    "command": "help:cracked"
}
HELP_CRACKED_COMMAND = 'app.commands.register("help:cracked", () => shell.openExternal("https://github.com/X1a0He/StarUML-CrackedAndTranslate"), "Help: Cracked");'
BANNER = """ -----------------------------------------------
|                                               |
| ██╗  ██╗ ██╗ █████╗  ██████╗ ██╗  ██╗███████╗ |
| ╚██╗██╔╝███║██╔══██╗██╔═████╗██║  ██║██╔════╝ |
|  ╚███╔╝ ╚██║███████║██║██╔██║███████║█████╗   |
|  ██╔██╗  ██║██╔══██║████╔╝██║██╔══██║██╔══╝   |
| ██╔╝ ██╗ ██║██║  ██║╚██████╔╝██║  ██║███████╗ |
| ╚═╝  ╚═╝ ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ |
|                StarUML Cracker                |
 -----------------------------------------------"""

def log(msg):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"「{now}」 {msg}")

def get_asar_paths(base):
    return os.path.join(base, "app.asar"), os.path.join(base, "app")

def get_home_dir():
    if system == "Linux":
        sudo_user = os.environ.get("SUDO_USER")
        if sudo_user:
            return os.path.expanduser(f"~{sudo_user}")
    return os.path.expanduser("~")

def get_user_data_path():
    home_dir = get_home_dir()
    if system == "Darwin":
        return os.path.join(home_dir, "Library", "Application Support", "StarUML")
    elif system == "Windows":
        return os.path.join(home_dir, "AppData", "Roaming", "StarUML")
    elif system == "Linux":
        return os.path.join(home_dir, ".config", "StarUML")
    log("不支持的操作系统")
    exit(0)

def get_base_path():
    if system == 'Darwin':
        return os.path.join("/Applications", "StarUML.app", "Contents", "Resources")
    elif system == 'Windows':
        return os.path.join("C:\\", "Program Files", "StarUML", "resources")
    elif system == 'Linux':
        return "/opt/StarUML/resources"
    log("不支持的操作系统")
    exit(0)

def read_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def write_text(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

def patch_file(file_path, transform):
    write_text(file_path, transform(read_text(file_path)))

def replace_file_text(file_path, old, new):
    patch_file(file_path, lambda content: content.replace(old, new))

def patch_if_missing(file_path, marker, old, new, log_hook=False, log_exists=False):
    content = read_text(file_path)
    if marker not in content:
        if log_hook:
            log("hook写入中...")
        write_text(file_path, content.replace(old, new))
        if log_hook:
            log("hook写入完毕")
    elif log_exists:
        log("文本已被修改过，无需再次修改")

def remove_file_if_exists(file_path, message):
    if os.path.exists(file_path):
        log(message)
        os.remove(file_path)

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
        if not os.path.exists(os.path.join("/Applications", "StarUML.app")):
            log("未检测到 StarUML.app，请先到官网下载安装")
            exit(0)
    elif system == 'Windows':
        if not os.path.exists(os.path.join("C:\\", "Program Files", "StarUML", "StarUML.exe")):
            log("未检测到 StarUML.exe 或非官网下载安装，请先到官网下载安装")
            exit(0)

# 没安装asar的能不能滚去先看教程怎么装，没有asar跑牛魔呢？
def detect_asar():
    if system in ("Darwin", "Windows", "Linux") and shutil.which("asar") is None:
        log("未检测到asar，请先安装asar")
        exit(0)

def extract(base):
    global staruml_version
    asar_file, asar_folder = get_asar_paths(base)
    subprocess.run(["asar", "extract", asar_file, asar_folder], check=True)
    staruml_version = get_version_from_app_package(base)

def pack(base):
    asar_file, asar_folder = get_asar_paths(base)
    subprocess.run(["asar", "pack", asar_folder, asar_file], check=True)

def pack_and_remove_app(base):
    _, asar_folder = get_asar_paths(base)
    log("打包 app.asar")
    pack(base)
    log("删除 app 文件夹")
    shutil.rmtree(asar_folder)

def backup(base):
    asar_file, _ = get_asar_paths(base)
    original_file = os.path.join(base, "app.asar.original")
    if not os.path.exists(original_file):
        log("备份 app.asar -> app.asar.original")
        shutil.copyfile(asar_file, original_file)
    else:
        log("备份文件已存在，无需再次备份")

def rollback(base):
    asar_file, _ = get_asar_paths(base)
    original_file = os.path.join(base, "app.asar.original")
    if os.path.exists(original_file):
        log("还原 app.asar.original -> app.asar")
        shutil.copyfile(original_file, asar_file)
        os.remove(original_file)
    else:
        log("还原文件不存在，无法还原")

def is_first_install():
    # 该文件夹不存在，则表示首次安装
    if not os.path.exists(get_user_data_path()):
        log("请先打开一次 StarUML 再执行脚本")
        exit(0)

def read_json(file_path):
    return json.loads(read_text(file_path))

def write_json(file_path, data):
    write_text(file_path, json.dumps(data, ensure_ascii=False, indent=2))

def get_file_list(path):
    return glob.glob(path) if '*' in path else [path]

def replace_in_file(file_path, replacements, option):
    content = read_text(file_path)
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
    write_text(file_path, content)

def is_staruml_running():
    # 这里本来要kill掉的，一想到肯定有傻逼会有未保存的图表，kill掉就丢失了，所以仁慈一下
    if system == 'Darwin':
        if subprocess.run(["pgrep", "-x", "StarUML"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            log("检测到 StarUML 进程正在运行，请先关闭 StarUML 进程")
            # os.system("killall -9 StarUML") # macOS
            exit(0)
    elif system == 'Windows':
        if 'StarUML.exe' in subprocess.run(['tasklist', '/FI', 'IMAGENAME eq StarUML.exe'], capture_output=True, text=True).stdout:
            log("检测到 StarUML 进程正在运行，请先关闭 StarUML 进程")
            # os.system("taskkill /f /t /im StarUML.exe") # Windows
            exit(0)

def get_version_from_app_package(base):
    pkg = os.path.join(base, "app", "package.json")
    if os.path.exists(pkg):
        data = read_json(pkg)
        version = str(data.get("version", "")).strip()
        return version or None
    return None

def get_major_version(version_str):
    match = re.match(r"(\d+)", version_str)
    if match:
        return int(match.group(1))
    else:
        raise ValueError("无效的版本格式")

def prepare_app(base):
    global staruml_version
    asar_file, asar_folder = get_asar_paths(base)
    if os.path.exists(asar_file):
        extract(base)
        backup(base)
    elif os.path.exists(asar_folder):
        staruml_version = get_version_from_app_package(base)
    else:
        log("未检测到 app.asar 或 app 文件夹")
        exit(0)

def get_language_file():
    major_version = get_major_version(staruml_version)
    if major_version == 6:
        return "StarUML_Language_v6.json"
    if major_version == 7:
        return "StarUML_Language_v7.json"
    return None

def handler(base, user_choice):
    if user_choice in (0, 1, 2):
        prepare_app(base)
        language_file = get_language_file()
        if user_choice in (0, 2):
            crack(base, user_choice)
        if user_choice in (1, 2):
            translate(base, user_choice, language_file)

    # 还原所有操作 2024.11.04 增加
    if user_choice == 3:
        rollback(base)

def translate(base, user_choice, language_file):
    log("正在进行 StarUML 汉化操作...")
    asar_file, asar_folder = get_asar_paths(base)
    # 1. 仅存在app.asar，只处理app.asar
    if os.path.exists(asar_file) and not os.path.exists(asar_folder):
        translate_asar(language_file, base, user_choice)
    # 2. app.asar和app文件夹共存，优先处理app.asar
    elif os.path.exists(asar_file) and os.path.exists(asar_folder):
        # 如果用户选择破解并汉化，就不需要解包了
        if user_choice != 2:
            log("检测到 app.asar 和 app 文件夹共存，优先处理 app.asar")
            translate_asar(language_file, base, user_choice)
        elif user_choice == 2:
            translate_app(language_file, base, user_choice)
            pack_and_remove_app(base)
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif not os.path.exists(asar_file) and os.path.exists(asar_folder):
        log("检测到只存在 app 文件夹，本次操作仅对 app 文件夹进行处理")
        translate_app(language_file, base, user_choice)

    log("StarUML 汉化操作完成")

def translate_asar(language_file, base, user_choice):
    # 这里他妈的app.asar都存在了，还你妈node解包出错的话，你不是傻逼谁是傻逼
    log("解包 app.asar")
    translate_app(language_file, base, user_choice)
    # 汉化完成后，对app.asar进行打包操作，并删除app文件夹
    pack_and_remove_app(base)

def translate_app(language_file, base, user_choice):
    log("正在汉化文件...")
    data = read_json(language_file)
    for path, replacements in data.items():
        files = get_file_list(os.path.join(base, "app", path))
        for file_path in files:
            replace_in_file(file_path, replacements, user_choice)
    log("文件汉化完成")

def clear_license_files(base):
    # 先把原来的license.key和v7的activation.key文件删掉
    user_path = get_user_data_path()
    try:
        remove_file_if_exists(os.path.join(user_path, "license.key"), "移除已存在的 license.key 文件")
        remove_file_if_exists(os.path.join(base, "app", "license.key"), "移除已存在的 license.key 文件")
        remove_file_if_exists(os.path.join(user_path, "activation.key"), "移除已存在的 activation.key 文件")
    except FileNotFoundError:
        pass
    except KeyboardInterrupt:
        pass

def crack(base, user_choice):
    log("正在进行 StarUML 破解操作...")
    clear_license_files(base)
    log("请输入StarUML关于页面要显示的用户名(回车即使用程序默认): ")
    username = input()
    if not username: username = DEFAULT_USERNAME
    asar_file, asar_folder = get_asar_paths(base)
    # 1. 仅存在app.asar，只处理app.asar
    # 2. app.asar和app文件夹共存，优先处理app.asar
    if os.path.exists(asar_file):
        crack_asar(base, username, user_choice)
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif os.path.exists(asar_folder):
        crack_app(base, username)

    log("StarUML 破解处理完毕，请按照下列步骤进行操作")
    log("1. 运行StarUML，选择菜单栏的Help - Enter License Key")
    log("2. 弹出窗口后，直接点击OK即可")

def crack_asar(base, username, user_choice):
    log("解包 app.asar")
    crack_app(base, username)
    # 如果用户选择破解并汉化的话，就不需要重新打包了，做完再打包
    if user_choice != 2:
        pack_and_remove_app(base)

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
        if obj.get("label") == target_label and isinstance(obj.get("submenu"), list):
            obj["submenu"].insert(0, new_member)
            return True
        for value in obj.values():
            if isinstance(value, (dict, list)):
                result = add_member_after_label(value, target_label, new_member)
                if result:
                    return result
    return None

def write_author_info(base):
    major_version = get_major_version(staruml_version)
    app_folder = os.path.join(base, "app")
    src_folder = os.path.join(app_folder, "src")

    # 修改关于弹窗部分
    static_folder = os.path.join(src_folder, "static")
    html_contents_folder = os.path.join(static_folder, "html-contents")
    about_dialog = os.path.join(html_contents_folder, "about-dialog.html")

    if major_version == 6:
        replace_file_text(about_dialog,
                          "<span class=\"license\" style=\"font-weight: 600;\"></span>",
                          "<a href=\"https://github.com/X1a0He/StarUML-CrackedAndTranslate\"><span class=\"license\" style=\"font-weight: 600;\"></span></a>")
        # 修改标题部分
        titlebar_view = os.path.join(src_folder, "views", "titlebar-view.js")
        replace_file_text(titlebar_view, """title += "(EVALUATION MODE)";
        }""",
                          """title += "(EVALUATION MODE)";
        } else { title += '【By GitHub: X1a0He/StarUML-CrackedAndTranslate】'}""")

    if major_version == 7:
        replace_file_text(about_dialog,
                          "<div><a href=\"#\" class=\"thirdparty\">Thirdparty softwares</a></div>",
                          "<div><a href=\"#\" class=\"thirdparty\">Thirdparty softwares</a><br/><br/><a href=\"https://github.com/X1a0He/StarUML-CrackedAndTranslate\">GitHub: X1a0He/StarUML-CrackedAndTranslate</a></div>")

    # 修改菜单栏部分
    menus_folder = os.path.join(app_folder, "resources", "default", "menus")
    for menu_file in ("darwin.json", "win32.json", "linux.json"):
        menu_path = os.path.join(menus_folder, menu_file)
        menu_data = read_json(menu_path)
        add_member_after_label(menu_data, "About StarUML", AUTHOR_MENU_ITEM)
        write_json(menu_path, menu_data)

    engine_folder = os.path.join(src_folder, "engine")
    default_commands = os.path.join(engine_folder, "default-commands.js")
    js_content = read_text(default_commands)

    if HELP_CRACKED_COMMAND not in js_content:
        js_content += "\n" + HELP_CRACKED_COMMAND

    write_text(default_commands, js_content)

def crack_app(base, username):
    destination_path = os.path.join(base, "app", "src")
    shutil.copy("hook.js", destination_path)
    shutil.copy("dialog.js", destination_path)
    major_version = get_major_version(staruml_version)
    hook_file_path = os.path.join(destination_path, "hook.js")
    replace_file_text(hook_file_path, DEFAULT_USERNAME, username)
    app_context_file_path = os.path.join(destination_path, "app-context.js")

    if major_version == 6:
        patch_if_missing(app_context_file_path, 'require("./hook");\nrequire("./dialog");',
                         'this.appReady();', 'require("./hook");\nrequire("./dialog");\nthis.appReady();',
                         log_hook=True, log_exists=True)

    if major_version == 7:
        main_process_file_path = os.path.join(destination_path, 'main-process', 'main.js')
        patch_if_missing(app_context_file_path, 'require("./dialog");',
                         'this.appReady();', 'require("./dialog");\nthis.appReady();')
        patch_if_missing(main_process_file_path, 'require("./hook");',
                         'global.application = new Application();',
                         'global.application = new Application();\nrequire("../hook");',
                         log_hook=True, log_exists=True)

    write_author_info(base)

def main():
    try:
        print(BANNER)
        print("StarUML「Mac & Win」一键破解汉化脚本")
        print("Github: https://github.com/X1a0He/StarUML-CrackedAndTranslate")
        print()

        is_admin()
        detect_asar()
        is_installed()
        is_first_install()
        is_staruml_running()

        log("macOS 15+ 用户请确保在更新完 StarUML 后手动打开一次 StarUML 再执行脚本")
        user_choice = int(input("0 -> 仅破解\n1 -> 仅汉化\n2 -> 破解并汉化\n3 -> 还原所有\n-1 -> 退出运行\n请输入您的选择: \n"))
        if user_choice == -1:
            exit(0)

        if user_choice in (0, 1, 2, 3):
            base = get_base_path()
            handler(base, user_choice)
            if system == 'Darwin':
                log("如遇到打开 StarUML 提示已损坏，请手动在终端执行如下命令后，在 Application 右键打开 StarUML")
                log("sudo xattr -cr /Applications/StarUML.app")
                log("macOS 15+ 的用户如果一直遇到提示已损坏，建议先打开一遍 StarUML 后再运行")
                # os.system("open -a StarUML")
            elif system == 'Windows':
                # Windows的启动功不知道什么命令，拉倒吧
                pass
            elif system == 'Linux':
                # Linux 系统未经证实，请谨慎运行
                pass
    except KeyboardInterrupt:
        print("\n用户中断了程序执行")

if __name__ == '__main__':
    main()
