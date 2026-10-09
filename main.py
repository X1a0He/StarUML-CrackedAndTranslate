import platform, os, shutil, subprocess, json, datetime, ctypes
from concurrent.futures import ThreadPoolExecutor
system = platform.system()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
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
    asar_file, asar_folder = get_asar_paths(base)
    subprocess.run(["asar", "extract", asar_file, asar_folder], check=True)

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

def translate_v7_file(file_path, replacements):
    original = read_text(file_path)
    content, missing = original, []
    if file_path.endswith('.json'):
        data = json.loads(content)
        changed = False
        fields = { field: { item['en']: item['cn'] for item in items }
                   for group in replacements for field, items in group.items() }
        seen = { field: set() for field in fields }

        def translate_values(value):
            nonlocal changed
            if isinstance(value, dict):
                for key, child in value.items():
                    if key in fields and isinstance(child, str):
                        seen[key].add(child)
                        translated = fields[key].get(child, child)
                        if translated != child:
                            value[key] = translated
                            changed = True
                    elif isinstance(child, (dict, list)):
                        translate_values(child)
            elif isinstance(value, list):
                for child in value:
                    translate_values(child)

        translate_values(data)
        for field, pairs in fields.items():
            missing.extend(field + ': ' + en for en, cn in pairs.items()
                           if en not in seen[field] and cn not in seen[field])
        if changed:
            content = json.dumps(data, ensure_ascii=False, indent=2)
            if original.endswith('\n'):
                content += '\n'
    else:
        for item in replacements:
            en, cn = item['en'], item['cn']
            count = item.get('count', 1)
            if cn and content.count(cn) >= count:
                continue
            if content.count(en) == count:
                content = content.replace(en, cn)
            else:
                missing.append(en.strip()[:120])
    return file_path, original, content, missing

def translate_v7_app(app_folder, language_file=None, workers=4):
    app_folder = os.path.realpath(app_folder)
    require_v7(app_folder)
    language_file = language_file or os.path.join(SCRIPT_DIR, 'StarUML_Language_v7.json')
    tasks = { }
    for relative, replacements in read_json(language_file).items():
        file_path = os.path.abspath(os.path.join(app_folder, relative))
        if (os.path.commonpath([app_folder, file_path]) != app_folder
                or os.path.realpath(file_path) != file_path):
            raise ValueError('汉化路径越界或含符号链接: ' + relative)
        tasks[file_path] = replacements
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda item: translate_v7_file(*item), sorted(tasks.items())))
    missing = [(os.path.relpath(path, app_folder), message)
               for path, _, _, messages in results for message in messages]
    if missing:
        details = '\n'.join(path + ': ' + message for path, message in missing[:10])
        raise RuntimeError('有 %d 条词条未命中，未写入汉化文件：\n%s' % (len(missing), details))
    changes = [(path, original, content) for path, original, content, _ in results if original != content]
    helper_path = os.path.join(app_folder, 'src', 'localization', 'zh-cn.js')
    if os.path.realpath(helper_path) != helper_path:
        raise ValueError('显示映射路径含符号链接')
    helper = read_text(os.path.join(SCRIPT_DIR, 'zh-cn.js'))
    existing_helper = read_text(helper_path) if os.path.exists(helper_path) else None
    if existing_helper != helper:
        changes.append((helper_path, existing_helper, helper))
    if not changes:
        log('v7 文件已汉化，无需重复写入')
        return 0
    for path, original, _ in changes:
        current = read_text(path) if os.path.exists(path) else None
        if current != original:
            raise RuntimeError('处理期间文件发生变化，已停止: ' + path)
    backup_folder = app_folder + '.zh-backup-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    for path, original, _ in changes:
        if original is not None:
            target = os.path.join(backup_folder, os.path.relpath(path, app_folder))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copyfile(path, target)
    if os.path.isdir(backup_folder):
        log('汉化前文件备份: ' + backup_folder)
    for path, _, content in changes:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        write_text(path, content)
    log('v7 汉化完成，共更新 %d 个文件' % len(changes))
    return len(changes)

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

def require_v7(app_folder):
    version = str(read_json(os.path.join(app_folder, "package.json")).get("version", "")).strip()
    if not version.startswith("7."):
        raise ValueError("仅支持 StarUML v7，检测到版本: " + (version or "未知"))

def prepare_app(base):
    asar_file, app_folder = get_asar_paths(base)
    needs_pack = os.path.exists(asar_file)
    if needs_pack:
        detect_asar()
        extract(base)
    elif not os.path.isdir(app_folder):
        log("未检测到 app.asar 或 app 文件夹")
        exit(0)
    require_v7(app_folder)
    if needs_pack:
        backup(base)
    return needs_pack

def handler(base, user_choice):
    # 还原所有操作 2024.11.04 增加
    if user_choice == 3:
        rollback(base)
        return
    if user_choice not in (0, 1, 2):
        return

    needs_pack = prepare_app(base)
    if user_choice in (0, 2):
        crack(base)
    if user_choice in (1, 2):
        log("正在进行 StarUML 汉化操作...")
        translate_v7_app(os.path.join(base, "app"))
        log("StarUML 汉化操作完成")
    if needs_pack:
        pack_and_remove_app(base)

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

def crack(base):
    log("正在进行 StarUML 破解操作...")
    clear_license_files(base)
    log("请输入StarUML关于页面要显示的用户名(回车即使用程序默认): ")
    username = input() or DEFAULT_USERNAME
    crack_app(base, username)

    log("StarUML 破解处理完毕，请按照下列步骤进行操作")
    log("1. 运行StarUML，选择菜单栏的Help - Enter License Key")
    log("2. 弹出窗口后，直接点击OK即可")

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
    app_folder = os.path.join(base, "app")
    src_folder = os.path.join(app_folder, "src")

    # 修改关于弹窗部分
    static_folder = os.path.join(src_folder, "static")
    html_contents_folder = os.path.join(static_folder, "html-contents")
    about_dialog = os.path.join(html_contents_folder, "about-dialog.html")

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
    main_process_file_path = os.path.join(destination_path, 'main-process', 'main.js')
    main_original = read_text(main_process_file_path)
    main_content = main_original
    ready = '  app.on("ready", () => {\n'
    ready_with_hook = (
        '  app.on("ready", async () => {\n'
        '    try {\n'
        '      await require("../hook");\n'
        '    } catch (error) {\n'
        '      console.error("[X1a0He StarUML Cracker] 初始化失败:", error);\n'
        '    }\n'
    )
    activate = '    if (!hasVisibleWindows) {'
    if ready_with_hook not in main_content:
        if main_content.count(ready) != 1 or main_content.count(activate) != 1:
            raise RuntimeError("无法识别 v7 主进程启动结构，未写入 hook")
        main_content = ''.join(line for line in main_content.splitlines(keepends=True)
                               if line.strip() != 'require("../hook");')
        main_content = main_content.replace(ready, ready_with_hook, 1)
        main_content = main_content.replace(
            activate, '    if (!hasVisibleWindows && global.application) {', 1)

    shutil.copy(os.path.join(SCRIPT_DIR, "hook.js"), destination_path)
    shutil.copy(os.path.join(SCRIPT_DIR, "dialog.js"), destination_path)
    hook_file_path = os.path.join(destination_path, "hook.js")
    replace_file_text(hook_file_path, DEFAULT_USERNAME, username)
    app_context_file_path = os.path.join(destination_path, "app-context.js")

    patch_if_missing(app_context_file_path, 'require("./dialog");',
                     'this.appReady();', 'require("./dialog");\nthis.appReady();')
    if read_text(main_process_file_path) != main_original:
        raise RuntimeError("处理期间主进程文件发生变化，已停止")
    if main_content != main_original:
        write_text(main_process_file_path, main_content)
        log("hook 启动等待已写入")

    write_author_info(base)

def main():
    try:
        print(BANNER)
        print("StarUML v7「Mac & Win」一键破解汉化脚本")
        print("Github: https://github.com/X1a0He/StarUML-CrackedAndTranslate")
        print()

        is_admin()
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
