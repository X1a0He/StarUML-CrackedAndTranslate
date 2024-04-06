import os
"""
    X1a0He留
    这个Python文件是留给Mac自己单独破解的！！！！！！，你不需要汉化你就只运行这个Python脚本就行了
    同样类似于StarUML_Trans.py一样，分三种情况进行处理
    1. 仅存在app.asar，则程序默认处理app.asar，处理完app.asar后，会将解包后的app文件夹删除
    2. app.asar和app文件夹共存，因优先级的原因，StarUML启动会依赖app.asar，所以二者共存时候，程序会默认优先处理app.asar
    3. 不存在app.asar，只存在app文件夹，则程序默认处理app文件夹，但并不会对app文件夹进行打包
"""

def decompressAsar(base):
    os.system(f"cd {base} && asar extract app.asar app")

def pack2asar(base):
    os.system(f"cd {base} && asar pack app app.asar")

def handleASAR(base, username):
    # 先对app.asar进行备份，备份文件名为app_backup.asar
    print("备份 app.asar -> app_backup.asar")
    os.system(f"cp -f {base}/app.asar {base}/app_backup.asar")
    # 备份完就对app.asar进行解包操作，这里他妈的app.asar都存在了，还你妈node解包出错的话，你不是傻逼谁是傻逼
    print("解包 app.asar")
    decompressAsar(base)
    handleAPP(base, username)
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

def handleAPP(base, username):
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
            # 不存在字符串require("./hook");则进行修改
            new_js_content = js_content.replace('const _ = require("lodash");', 'require("./hook");\nconst _ = require("lodash");')
            # 将替换后的内容写回到js文件
            with open(f"{destination_path}app-context.js", "w") as file2:
                file2.write(new_js_content)
                print("hook写入完毕")

def macStarUML():
    print("「操作系统」macOS")
    if os.system("command -v asar > /dev/null 2>&1") == 1:
        print("未检测到asar，请先安装asar")
        exit(1)
    username = input("请输入StarUML关于页面要显示的用户名: ")
    if not username: username = "Cracked by X1a0He"
    base = "/Applications/StarUML.app/Contents/Resources"

    # 1. 仅存在app.asar，只处理app.asar
    if os.path.exists(f"{base}/app.asar") and not os.path.exists(f"{base}/app"):
        handleASAR(base, username)
    # 2. app.asar和app文件夹共存，优先处理app.asar
    elif os.path.exists(f"{base}/app.asar") and os.path.exists(f"{base}/app"):
        print("检测到 app.asar 和 app 文件夹共存，优先处理 app.asar")
        handleASAR(base, username)
    # 3. 不存在app.asar，只存在app文件夹，则只处理app文件夹
    elif not os.path.exists(f"{base}/app.asar") and os.path.exists(f"{base}/app"):
        print("检测到只存在 app 文件夹，本次操作仅对 app 文件夹进行处理")
        handleAPP(base, username)

    print("Mac StarUML 处理完毕，请按照下列步骤进行操作")
    print("1. 运行StarUML，选择菜单栏的Help - Enter License Key")
    print("2. 弹出窗口后，直接点击OK即可")

def main():
    macStarUML()

if __name__ == "__main__":
    main()
