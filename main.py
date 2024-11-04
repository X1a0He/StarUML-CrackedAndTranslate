import platform, os, shutil, subprocess, json, re, glob, datetime, ctypes
system = platform.system()

def extract(base):
    os.system(f"cd {base} && asar extract app.asar app")

def pack(base):
    os.system(f"cd {base} && asar pack app app.asar")

def backup(base):
    if not os.path.exists(convert_path(f"{base}/app.asar.original")):
        log("备份 app.asar -> app.asar.original")
        shutil.copyfile(convert_path(f"{base}/app.asar"), convert_path(f"{base}/app.asar.original"))
    else:
        log("备份文件已存在，无需再次备份")

def rollback(base):
    if os.path.exists(convert_path(f"{base}/app.asar.original")):
        log("还原 app.asar.original -> app.asar")
        shutil.copyfile(convert_path(f"{base}/app.asar.original"), convert_path(f"{base}/app.asar"))
    else:
        log("还原文件不存在，无法还原")

def isFirstInstall():
    home_dir = os.path.expanduser("~")
    user_path = os.path.join(home_dir, "Library", "Application Support", "StarUML")
    # 该文件夹不存在，则表示首次安装
    if not os.path.exists(rf"{user_path}"):
        log("请先打开一次 StarUML 再执行脚本")
        exit(0)
        # log("检测到为首次安装StarUML，正在创建用户目录...")
        # # 创建文件夹
        # os.makedirs(rf"{user_path}")
        # # chmod 777
        # os.chmod(rf"{user_path}", 0o777)
        # log("用户目录创建完毕")

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
                # elif option == 3:  # 还原
                #     content = content.replace(cn_text, en_text)
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
    # 这里他妈的app.asar都存在了，还你妈node解包出错的话，你不是傻逼谁是傻逼
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
    log("正在进行 StarUML 破解操作...")
    # 先把原来的license.key文件删掉
    home_dir = os.path.expanduser("~")
    try:
        if system == 'Darwin':
            user_path = os.path.join(home_dir, "Library", "Application Support", "StarUML")
            # 该文件夹不存在，则表示首次安装
            # if not os.path.exists(rf"{user_path}"):
            #     log("检测到为首次安装StarUML，正在创建用户目录...")
            #     # 创建文件夹
            #     os.makedirs(rf"{user_path}")
            #     # chmod 777
            #     os.chmod(rf"{user_path}", 0o777)
            #     log("用户目录创建完毕")
            if os.path.exists(rf"{user_path}/license.key"):
                log("移除已存在的 license.key 文件")
                os.remove(rf"{user_path}/license.key")

            # 2024.11.04 已采用 hook.js 进行 lib.so 写入
            # # StarUML 6.2.0 新增的评估lib.so处理
            # # 移除掉已经存在的lib.so
            # if os.path.exists(rf"{user_path}/lib.so"):
            #     log("移除已存在的 lib.so 文件")
            #     os.remove(rf"{user_path}/lib.so")
            # else:
            #     log("评估天数修改失败 lib.so 文件不存在，请先打开一次StarUML后再运行破解")
            #
            # # 写入到user_path下的lib.so，文件内容为309个9
            # with open(rf"{user_path}/lib.so", "w") as f:
            #     log("正在修改评估天数...")
            #     # 经过测试，写入309个9后，读取完计算后为Infinity天的评估市场剩余
            #     f.write('9' * 309)
            #     log("评估天数修改完毕")
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
    log("请输入StarUML关于页面要显示的用户名(回车即使用程序默认): ")
    username = input()
    if not username: username = "GitHub: X1a0He/StarUML-CrackedAndTranslate"
    # 1. 仅存在app.asar，只处理app.asar
    # 2. app.asar和app文件夹共存，优先处理app.asar
    if os.path.exists(convert_path(rf"{base}/app.asar")) or os.path.exists(convert_path(rf"{base}/app")):
        crack_asar(base, username, user_choice)
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif not os.path.exists(convert_path(rf"{base}/app.asar")) and os.path.exists(convert_path(rf"{base}/app")):
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
        shutil.rmtree(convert_path(f"{base}/app"))

def crack_app(base, username):
    destination_path = convert_path(f"{base}/app/src/")
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

        isFirstInstall()
        
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

        # macOS下检测是否安装了starUML，Windows下目录不确定，所以没写，拉倒吧
        if system == 'Darwin':
            if not os.path.exists("/Applications/StarUML.app"):
                log("未检测到 StarUML.app，结束执行")
                exit(0)

        user_choice = int(input("0 -> 仅破解\n1 -> 仅汉化\n2 -> 破解并汉化\n3 -> 还原所有\n-1 -> 退出运行\n请输入您的选择: \n"))
        if user_choice == -1:
            exit(0)

        # 还原功能已在 2024.11.04 改为还原为官方原包
        if user_choice in (0, 1, 2, 3):
            if system == 'Darwin':
                base = "/Applications/StarUML.app/Contents/Resources"
                handler(base, user_choice)
                log("如遇到打开 StarUML 提示已损坏，请手动在终端执行如下命令后，在 Application 右键打开 StarUML")
                log("sudo xattr -cr /Applications/StarUML.app")
                log("macOS 15 的用户如果一直遇到提示已损坏，建议先打开一遍 StarUML 后再运行")
                # os.system("open -a StarUML")
            elif system == 'Windows':
                base = r"C:\Program Files\StarUML\resources"
                handler(base, user_choice)
                # Windows的启动功不知道什么命令，拉倒吧
    except KeyboardInterrupt:
        print("\n用户中断了程序执行")

if __name__ == '__main__':
    main()
