import os
import shutil
"""
    X1a0He留
    这个Python文件不维护了，有问题也不会修复，因为我没有Windows，也不想为Windows做自动化处理，有能力的自己写吧
    破解方式也改成优雅的hook了，过程也不用那么麻烦了，自己看看教程应该能动手处理
"""

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
    winStarUML()

if __name__ == "__main__":
    main()
