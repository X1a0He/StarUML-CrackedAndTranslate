import json, os, re, glob

def decompressAsar(base):
    os.system(f"cd {base} && asar extract app.asar app")

def pack2asar(base):
    os.system(f"cd {base} && asar pack app app.asar")

def handle_crack_asar(base, username, user_choice):
    # 先对app.asar进行备份，备份文件名为app_backup.asar
    if not os.path.exists(f"{base}/app_backup.asar"):
        print("备份 app.asar -> app_backup.asar")
        os.system(f"cp -f {base}/app.asar {base}/app_backup.asar")

    # 备份完就对app.asar进行解包操作，这里他妈的app.asar都存在了，还你妈node解包出错的话，你不是傻逼谁是傻逼
    print("解包 app.asar")
    decompressAsar(base)
    handle_crack_app(base, username)
    # 如果用户选择破解并汉化的话，就不需要重新打包了，做完再打包
    if user_choice != 2:
        # 再次对app.asar进行打包操作
        print("打包 app.asar")
        pack2asar(base)
        print("删除 app 文件夹")
        os.system(f"rm -rf {base}/app")

    # 修复已损坏
    print("正在修复已损坏")
    os.system("sudo xattr -r -d com.apple.quarantine /Applications/StarUML.app")
    print("修复完毕")
    print("StarUML 破解操作完成")

def handle_crack_app(base, username):
    # 写入破解hook文件，复制hook.js到 app/src/ 目录下
    destination_path = f"{base}/app/src/"
    os.system(f"cp -f hook.js {destination_path}")
    # 将破解文件中的字符串进行替换处理
    with open(f"{destination_path}hook.js", "r") as file:
        js_content = file.read()
    new_js_content = js_content.replace("Cracked by X1a0He", username)

    # 将替换后的内容写回到js文件
    with open(f"{destination_path}hook.js", "w") as file:
        file.write(new_js_content)
    # 对同目录下的app-context.js进行改写处理
    # 读入app-context.js文件
    with open(f"{destination_path}app-context.js", "r") as file:
        js_content = file.read()
        # 查找字符串require("./hook");
        if js_content.find('require("./hook");') != -1:
            # 存在字符串require("./hook"); 则证明已被修改过
            print("文本已被修改过，无需再次修改")
        else:
            # 不存在字符串require("./hook"); 则进行修改
            new_js_content = js_content.replace('const _ = require("lodash");', 'require("./hook");\nconst _ = require("lodash");')
            # 将替换后的内容写回到js文件
            with open(f"{destination_path}app-context.js", "w") as file2:
                file2.write(new_js_content)
                print("hook写入完毕")

def handle_crack_mac_staruml(user_choice):
    print("正在进行 macOS StarUML 破解操作...")

    # 先把从阿猫阿狗那里获取到的license.key文件删掉，防止影响我
    os.system("rm -rf ~/Library/Application\ Support/StarUML/license.key")

    if os.system("command -v asar > /dev/null 2>&1") == 1:
        print("未检测到asar，请先安装asar")
        exit(0)
    username = input("请输入StarUML关于页面要显示的用户名: ")
    if not username: username = "Cracked by X1a0He"
    base = "/Applications/StarUML.app/Contents/Resources"

    # 1. 仅存在app.asar，只处理app.asar
    if os.path.exists(f"{base}/app.asar") and not os.path.exists(f"{base}/app"):
        handle_crack_asar(base, username, user_choice)
    # 2. app.asar和app文件夹共存，优先处理app.asar
    elif os.path.exists(f"{base}/app.asar") and os.path.exists(f"{base}/app"):
        print("检测到 app.asar 和 app 文件夹共存，优先处理 app.asar")
        handle_crack_asar(base, username, user_choice)
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif not os.path.exists(f"{base}/app.asar") and os.path.exists(f"{base}/app"):
        print("检测到只存在 app 文件夹，本次操作仅对 app 文件夹进行处理")
        handle_crack_app(base, username)

    print("Mac StarUML 处理完毕，请按照下列步骤进行操作")
    print("1. 运行StarUML，选择菜单栏的Help - Enter License Key")
    print("2. 弹出窗口后，直接点击OK即可")

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_file_list(base, path_pattern):
    base_path = f"{base}/app/"
    if '*' in path_pattern:
        full_path = os.path.join(base_path, path_pattern)
        return glob.glob(full_path)
    else:
        return [os.path.join(base_path, path_pattern)]

def replace_in_file(file_path, replacements, option):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # print(f"正在替换文件: {file_path}")
    content = content.replace(r"\u2026", "...").replace(r"\"dev\"", "dev")
    for replacement in replacements:
        for key, value in replacement.items():
            if isinstance(value, list):  # 处理嵌套列表
                for item in value:
                    en_text = item['en']
                    cn_text = item['cn']
                    # print(f"正在替换 {en_text} -> {cn_text}")
                    if option == 1 or option == 2:  # 汉化
                        content = re.sub(f'"{key}": "{re.escape(en_text)}"', f'"{key}": "{re.escape(cn_text)}"'.replace('\\', ''), content)
                    elif option == 3:  # 还原
                        content = re.sub(f'"{key}": "{re.escape(cn_text)}"'.replace('\\', ''), f'"{key}": "{re.escape(en_text)}"', content)
            else:
                en_text = replacement['en']
                cn_text = replacement['cn']
                # print(f"正在替换 {en_text} -> {cn_text}")
                if option == 1 or option == 2:  # 汉化
                    content = content.replace(en_text, cn_text)
                elif option == 3:  # 还原
                    content = content.replace(cn_text, en_text)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def handle_translate_asar(language_file, base, user_choice):
    # 先对app.asar进行备份，备份文件名为app_backup.asar
    if not os.path.exists(f"{base}/app_backup.asar"):
        print("备份 app.asar -> app_backup.asar")
        os.system(f"cp -f {base}/app.asar {base}/app_backup.asar")

    os.system(f"cp -f {base}/app.asar {base}/app_backup.asar")
    # 备份完就对app.asar进行解包操作，这里他妈的app.asar都存在了，还你妈node解包出错的话，你不是傻逼谁是傻逼
    print("解包 app.asar")
    decompressAsar(base)
    # 解包完就开始对文件进行汉化操作
    handle_translate_app(language_file, base, user_choice)
    # 汉化操作完成后，对app.asar进行打包操作，并删除app文件夹
    print("打包 app.asar")
    pack2asar(base)
    print("删除 app 文件夹")
    os.system(f"rm -rf {base}/app")

def handle_translate_app(language_file, base, user_choice):
    print("正在汉化文件...")
    data = read_json(language_file)
    for path, replacements in data.items():
        files = get_file_list(base, path)
        for file_path in files:
            replace_in_file(file_path, replacements, user_choice)
    print("文件汉化完成")

def translate(user_choice):
    print("正在进行 macOS StarUML 汉化操作...")
    base = "/Applications/StarUML.app/Contents/Resources"
    language_file = "StarUML_Language.json"
    # 1. 仅存在app.asar，只处理app.asar
    if os.path.exists(f"{base}/app.asar") and not os.path.exists(f"{base}/app"):
        handle_translate_asar(language_file, base, user_choice)
    # 2. app.asar和app文件夹共存，优先处理app.asar
    elif os.path.exists(f"{base}/app.asar") and os.path.exists(f"{base}/app"):
        # 如果用户选择破解并汉化，就不需要解包了
        if user_choice != 2:
            print("检测到 app.asar 和 app 文件夹共存，优先处理 app.asar")
            handle_translate_asar(language_file, base, user_choice)
        elif user_choice == 2:
            handle_translate_app(language_file, base, user_choice)
            print("打包 app.asar")
            pack2asar(base)
            print("删除 app 文件夹")
            os.system(f"rm -rf {base}/app")
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif not os.path.exists(f"{base}/app.asar") and os.path.exists(f"{base}/app"):
        print("检测到只存在 app 文件夹，本次操作仅对 app 文件夹进行处理")
        handle_translate_app(language_file, base, user_choice)

    print("StarUML 汉化操作完成")

def main():
    try:
        # 用户选择
        print("__  ___        ___  _   _")
        print("\\ \\/ / | __ _ / _ \\| | | | ___")
        print(" \\  /| |/ _` | | | | |_| |/ _ \\")
        print(" /\\/\\| | (_| | |_| |  _  | ___/")
        print("/_/\\_\\_|\\__,_|\\___/|_| |_|\\___|")
        print("Mac StarUML一键破解汉化脚本")
        if os.system("pgrep -x StarUML > /dev/null 2>&1") == 0:
            print("检测到 StarUML 进程正在运行，请先关闭 StarUML 进程")
            # 这里本来要kill掉的，一想到肯定有傻逼会有未保存的图表，kill掉就丢失了，所以仁慈一下
            # os.system("killall -9 StarUML")
            exit(0)

        user_choice = int(input("0 -> 仅破解\n1 -> 仅汉化\n2 -> 破解并汉化\n3 -> 还原语言\n-1 -> 退出运行\n请输入您的选择: \n"))
        if user_choice == -1:
            exit(0)

        if user_choice == 0:
            handle_crack_mac_staruml(user_choice)
            # 运行StarUML
            os.system("open -a StarUML")
            exit(0)

        if user_choice == 1:
            translate(user_choice)
            os.system("open -a StarUML")
            exit(0)

        if user_choice == 2:
            handle_crack_mac_staruml(user_choice)
            translate(user_choice)
            os.system("open -a StarUML")
            exit(0)

        if user_choice == 3:
            print("由于我不知道还原会不会有问题，虽然代码里面是支持的，但是我还是不建议")
            print("那既然你都跑代码了，如果你要还原，你自己注释这里")
            exit(0)

    except KeyboardInterrupt:
        print("\n用户中断了程序执行")

if __name__ == "__main__":
    main()
