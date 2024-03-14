import json
import os
import re
import platform
import shutil
system = platform.system()

def decompressAsar():
    os.system("cd /Applications/StarUML.app/Contents/Resources && asar extract app.asar app")

def pack2asar():
    os.system("cd /Applications/StarUML.app/Contents/Resources && asar pack app app.asar")

def load_replacements(file_path, direction):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    replacements = { }
    keys = ('strings', 'label', 'text', 'description')
    for key in keys:
        if key in data:
            if direction == 1:  # 汉化
                replacements.update({ item['en']: item['cn'] for item in data[key] })
            else:  # 还原
                replacements.update({ item['cn']: item['en'] for item in data[key] })
    return replacements

def replace_keys(obj, replacements, key_to_replace):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == key_to_replace and value in replacements:
                obj[key] = replacements[value]
                # print(f"替换 {obj[key]} -> {replacements[value]}")
            elif isinstance(value, (dict, list)):
                replace_keys(value, replacements, key_to_replace)
    elif isinstance(obj, list):
        for item in obj:
            replace_keys(item, replacements, key_to_replace)

def update_files(files_path, replacements):
    for file_info in files_path:
        for directory in file_info['path']:
            for key_to_replace in file_info['key_to_replace']:
                for root, dirs, files in os.walk(directory):
                    for file_name in files:
                        if file_name.endswith(file_info['file_pattern']):
                            file_path = os.path.join(root, file_name)
                            with open(file_path, 'r', encoding='utf-8') as file:
                                if file_path.endswith('.json'):
                                    print(f"正在替换文件: {file_path} 的 {key_to_replace} 字段")
                                    data = json.load(file)
                                    replace_keys(data, replacements, key_to_replace)
                                    with open(file_path, 'w', encoding='utf-8') as file:
                                        json.dump(data, file, indent=4, ensure_ascii=False)
                                elif file_path.endswith('.js'):
                                    print(f"正在替换文件: {file_path} 的 {key_to_replace} 字段")
                                    data = file.read()
                                    data = data.replace(r"\u2026", "...")
                                    data = data.replace(r"\"dev\"", "dev")
                                    matches = re.findall(r': \"(.*?)\"', data)
                                    for match in matches:
                                        if match in replacements:
                                            data = data.replace(f": \"{match}\"", f": \"{replacements[match]}\"")
                                            # print(f"替换 {match} -> {replacements[match]}")
                                    with open(file_path, 'w', encoding='utf-8') as file:
                                        file.write(data)

def update_html_files(json_path, html_dirs):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for html_dir in html_dirs:
        for html_file, replacements in data['html'][0].items():
            html_file_path = os.path.join(html_dir, f"{html_file}.html")

            print(f"正在替换文件: {html_file_path}")
            if os.path.isfile(html_file_path):
                with open(html_file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                for item in replacements:
                    en_text = item['en']
                    cn_text = item['cn']
                    if en_text in html_content:
                        html_content = html_content.replace(en_text, cn_text)
                        # print(f"{html_file}.html: 修改 {en_text} -> {cn_text}")

                with open(html_file_path, 'w', encoding='utf-8') as file:
                    file.write(html_content)
            else:
                pass
                # print(f"文件 {html_file_path} 不存在。")

def macStarUML():
    print("当前操作系统为 macOS")
    if os.system("command -v asar > /dev/null 2>&1") == 1:
        print("未检测到asar，请先安装asar")
        exit(1)
    username = input("请输入StarUML关于页面要显示的用户名: ")
    if not username: username = "X1a0He"
    bash_extract = """
    cd /Applications/StarUML.app/Contents/Resources && asar extract app.asar app
    """
    os.system(bash_extract)
    # 复制license-manager.js文件到目标位置
    destination_path = "/Applications/StarUML.app/Contents/Resources/app/src/engine/"
    os.system("cp -f license-manager.js {}".format(destination_path))

    # 将字符串中的"X1a0He"替换为用户输入的文本
    with open(destination_path + "license-manager.js", 'r') as file:
        js_content = file.read()
    new_js_content = js_content.replace('Cracked by X1a0He', username)

    # 将替换后的内容写回到js文件
    with open(destination_path + "license-manager.js", 'w') as file:
        file.write(new_js_content)

    # 修复已损坏提示
    print("需要修复app，稍后请输入电脑密码")
    bash_pack = """
    cd /Applications/StarUML.app/Contents/Resources &&
    asar pack app app.asar &&
    rm -rf app && sudo xattr -r -d com.apple.quarantine /Applications/StarUML.app
    """
    os.system(bash_pack)
    print("Mac StarUML 处理完毕，请按照下列步骤进行操作")
    print("1. 运行StarUML，选择菜单栏的Help - Enter License Key")
    print("2. 弹出窗口后，直接点击OK即可")

def winStarUML():
    print("当前操作系统为 Windows")
    if os.system("where asar >nul 2>nul") != 0:
        print("未检测到asar，请先安装asar")
        exit(1)
    username = input("请输入StarUML关于页面要显示的用户名: ")
    if not username: username = "X1a0He"
    root_dir = input("请找到StarUML的根目录主程序并填入此处: ")
    # 如果root_dir有引号，则把引号去掉，否则直接下一步
    if root_dir.startswith('"') and root_dir.endswith('"'):
        root_dir = root_dir[1:-1]
    directory = root_dir.rsplit("\\", 1)[0]
    # 查找根目录下是否存在resource文件夹
    if not os.path.exists(directory + "\\resources"):
        print("未找到resource文件夹")
        exit(1)
    print("正在解包...")
    bash_extract = "cd {} && asar extract app.asar app".format(directory + "\\resources")
    os.system(bash_extract)
    # 复制license-manager.js文件到目标位置
    destination_path = directory + "\\resources\\app\\src\\engine\\"
    print("正在替换文件...")
    shutil.copyfile("license-manager.js", os.path.join(destination_path, "license-manager.js"))

    # 将字符串中的"X1a0He"替换为用户输入的文本
    with open(destination_path + "license-manager.js", 'r') as file:
        js_content = file.read()
    new_js_content = js_content.replace('Cracked by X1a0He', username)

    # 将替换后的内容写回到js文件
    with open(destination_path + "license-manager.js", 'w') as file:
        file.write(new_js_content)

    print("正在重新打包...")
    bash_pack = "cd {} && asar pack app app.asar && rd /s /q app".format(directory + "\\resources")
    os.system(bash_pack)
    print("\nWindows StarUML 处理完毕，请按照下列步骤进行操作")
    print("1. 运行StarUML，选择菜单栏的Help - Enter License Key")
    print("2. 弹出窗口后，直接点击OK即可")
def main():
    try:
        # 用户选择
        print("__  ___        ___  _   _")
        print("\\ \\/ / | __ _ / _ \\| | | | ___")
        print(" \\  /| |/ _` | | | | |_| |/ _ \\")
        print(" /\\/\\| | (_| | |_| |  _  | ___/")
        print("/_/\\_\\_|\\__,_|\\___/|_| |_|\\___|")
        print("StarUML一键破解汉化脚本")
        user_choice = int(input("0 -> 破解\n1 -> 汉化\n2 -> 还原\n请输入您的选择: \n"))

        if user_choice == 2:
            print("由于我不知道还原会不会有问题，虽然代码里面是支持的，但是我还是不建议")
            print("那既然你都跑代码了，如果你要还原，你自己注释这里")
            exit(1)

        if user_choice == 0:
            if system == "Darwin":
                macStarUML()
            elif system == "Windows":
                winStarUML()
            else:
                print("当前操作系统不支持")
            exit(1)

        # 如果app_backup.asar不存在，则复制一份app.asar为app_backup.asar
        if not os.path.exists("/Applications/StarUML.app/Contents/Resources/app_backup.asar"):
            print("正在备份app.asar")
            os.system(
                "cp -f /Applications/StarUML.app/Contents/Resources/app.asar /Applications/StarUML.app/Contents/Resources/app_backup.asar")

        if not os.path.exists("cd /Applications/StarUML.app/Contents/Resources/app"):
            print("正在解包app.asar")
            decompressAsar()

        # 加载汉化文件
        replacements = load_replacements('StarUML_Language.json', user_choice)

        files_path = [
            {
                'path': [
                    '/Applications/StarUML.app/Contents/Resources/app/resources/default/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/uml/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/aws/menus',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/bpmn/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/c4/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/gcp/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/erd/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/wireframe/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/staruml-v1/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/html-export/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/sysml/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/alignment/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/diagram-layout/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/mindmap/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/flowchart/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/find/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/diagram-generator/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/minimap/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/diagram-thumbnails/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/relationship-view/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/markdown/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/debug/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/dfd/menus/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/c4/toolbox/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/bpmn/preferences/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/uml/toolbox/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/common/toolbox',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/default/robustness/toolbox/'
                ],
                'file_pattern': '.json',
                'key_to_replace': ['label']
            },
            {
                'path': [
                    # 'app/resources/default/preferences/',
                    # 'app/extensions/essential/aws/preferences/',
                    # 'app/extensions/essential/bpmn/preferences/',
                    # 'app/extensions/essential/c4/preferences/',
                    # 'app/extensions/essential/dfd/preferences/',
                    # 'app/extensions/essential/erd/preferences/',
                    # 'app/extensions/essential/flowchart/preferences/',
                    # 'app/extensions/essential/gcp/preferences/',
                    # 'app/extensions/essential/mindmap/preferences/',
                    # 'app/extensions/essential/sysml/preferences/',
                    # 'app/extensions/essential/uml/preferences/',
                    '/Applications/StarUML.app/Contents/Resources/app/extensions/essential/',
                    '/Applications/StarUML.app/Contents/Resources/app/resources/default/',
                ],
                'file_pattern': '.json',
                'key_to_replace': ['text', 'description', 'name']
            },
            {
                'path': [
                    '/Applications/StarUML.app/Contents/Resources/app/src/'
                ],
                'file_pattern': 'strings.js',
                'key_to_replace': ['strings']
            }
        ]
        update_files(files_path, replacements)
        update_html_files('StarUML_Language.json', [
            '/Applications/StarUML.app/Contents/Resources/app/src/static/html-contents/',
            '/Applications/StarUML.app/Contents/Resources/app/extensions/default/markdown/',
            '/Applications/StarUML.app/Contents/Resources/app/extensions/default/diagram-thumbnails/',
            '/Applications/StarUML.app/Contents/Resources/app/extensions/default/relationship-view/'
        ])
        print("正在打包app.asar")
        pack2asar()
    except KeyboardInterrupt:
        print("\n用户中断了程序执行")

if __name__ == "__main__":
    main()
