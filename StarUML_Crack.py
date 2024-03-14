import platform
import os
import shutil
system = platform.system()

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
    if system == "Darwin":
        macStarUML()
    elif system == "Windows":
        winStarUML()
    else:
        print("当前操作系统不支持")

if __name__ == "__main__":
    main()