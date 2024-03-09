# StarUML汉化效果
![display.png](images/display.png)
# X1a0He留
😁 作者暴脾气，但很温柔，素质很高，望周知

⚠️ 项目不更新不代表不能用，你不会自己看看吗

本项目来源由于自己大学要上UML必修课，书本上推荐的软件\
本项目汉化不完全，但如果你是一个大学生或工作的社畜，相信剩下那一点点b英文应该难不到你

如果你大学生看不懂那剩下没汉化的英文，你还上个集贸UML课，考试你必挂\
如果你社畜看不懂那些剩下没汉化的英文，那你赶紧上什么58同城，BOSS直聘赶紧找个b洗碗工洗洗盘子得了

而且最重要的一点，老子上传上来的初心是他妈给自己用的，老子2天时间完成了95%的汉化，剩下那5%的汉化你看不懂你他妈还用牛魔呢？

# 用前必读
1. 如果你有问题，请先确保自己的脑子🧠是清醒状态
2. 如果你在自己折腾途中，遇到还原出问题，或部分有问题，我可以告知你，你既然要汉化，你还要还原，你不是弱智谁是弱智？
3. 由于存在大量英文，本人为🇨🇳人，看不懂英文也很正常，所以翻译结果选择机翻，包含但不限于百度翻译，Google翻译，GPT翻译，搜索术语结果，所以如果出现有翻译错误，请你提issues，虽然我不一定会看
4. 由于脚本没有对原app.asar进行备份，请你决定使用前，先备份一遍原版的app.asar
5. 支持最新版本，从官网下的，别tm乱下跑过来问我为什么用不了
6. app.asar应该是Win和Mac通用的，如果有问题，可以通知我
7. 反馈方式: 提issues或者[@X1a0He](https://t.me/X1a0He)

# 目录
<!-- TOC -->
* [StarUML汉化效果](#staruml汉化效果)
* [X1a0He留](#x1a0he留)
* [用前必读](#用前必读)
* [目录](#目录)
* [支持状态](#支持状态)
* [更新日志](#更新日志)
* [使用方法](#使用方法)
  * [不想折腾无脑使用](#不想折腾无脑使用)
  * [想折腾又有耐心的使用](#想折腾又有耐心的使用)
    * [运行脚本的基本条件](#运行脚本的基本条件)
    * [NodeJS安装](#nodejs安装)
    * [asar安装](#asar安装)
    * [Python安装](#python安装)
    * [StarUML_Trans.py文件解析](#staruml_transpy文件解析)
    * [StarUML_Crack.py文件解析](#staruml_crackpy文件解析)
      * [Mac Crack运行说明](#mac-crack运行说明)
      * [Windows Crack运行说明](#windows-crack运行说明)
<!-- TOC -->

# 支持状态

|   App   |       版本       | 汉化程度 | Cracked | Mac | Windows |                    下载地址                    |
|:-------:|:--------------:|:----:|:-------:|:---:|:-------:|:------------------------------------------:|
| StarUML | 6.0.1 - Latest | 95%  |    ✅    |  ✅  |    ✅    | [https://staruml.io/](https://staruml.io/) |

# 更新日志
- [更新日志](Update-log.md)

# 使用方法
> 本项目使用最基本要求
> 1. 脑子正常，脑残人士请勿使用
> 2. Windows和Mac是nm通用的方法，别叫了
> 3. 如果你的机器上有Python，那么你可以自己跑一遍脚本，或者自己改
> 4. 按道理来说，汉化是通用的，除非StarUML不用Electron了，但是也够你大学生毕业或者社畜工作摸鱼用了

## 不想折腾无脑使用
- [Windows](Windows.md)
- [Mac](Mac.md)

## 想折腾又有耐心的使用
**因本人常用电脑为Mac💻，所以此处教程以Mac为重点，Windows大同小异，望周知✅**

**PS: ⚠️我是为了方便才写Python脚本全自动的，建议看过代码并研究完一遍才决定要不要自己运行**

----

既然你有耐心，且想折腾，那我就懒得跟你说遇到问题的解决方法了，你完全可以自己查 百度 or Google

> 本项目文件解释如下
> - StarUML_Trans.py 名如其意，负责全自动翻译的Python文件
> - StarUML_Crack.py 名如其意，负责全自动破解StarUML的Python文件
> - StarUML_Language.json 名如其意，负责存放中英双语的Json文件

### 运行脚本的基本条件
运行上述两个Python文件的前提条件如下
- 最好本机已安装好`NodeJS`, `asar`, `Python`\
Windows打开cmd，Mac打开终端，输入如下命令查看是否存在`NodeJS`和`asar`支持
```Bash
# 查看当前node和npm版本，建议为最新
node -v && npm -v

# 查看asar是否已安装
asar --version

# 查看Python是否已安装
# Python2
python --version

# Python3
python3 --version
```
若上述命令中，存在某个命令出现错误，则你需要提前进行安装，此处仅提供官方安装方法，其他方法(比如Mac的HomeBrew安装)请自行搜索

### NodeJS安装
NodeJS官方网址: [https://nodejs.org/](https://nodejs.org/)

NodeJS Current版本下载: [https://nodejs.org/en/download/current](https://nodejs.org/en/download/current)

**⚠️ NPM 会随着 NodeJS 一同安装**

**❗️❗️❗️建议下Current版本，也就是图中右边的版本**

![Nodejs.png](images/Nodejs.png)

但是！但是！但是！经过我的尝试，Windows上直接点右边下载，会给你下一个压缩包的，所以我的建议是点上面的[NodeJS Current版本](https://nodejs.org/en/download/current)下载

![Nodejs-current.png](images/Nodejs-current.png)

点击自己对应的系统图标下载即可，如果你还是不会，OK，you are a fucking genius!
### asar安装
当你完成了 NodeJS 和 NPM 的安装后，运行下列命令进行安装 `asar`
```Bash
npm -g i @electron/asar
```
该命令由 [@electron/asar](https://www.npmjs.com/package/@electron/asar) 提供，[官方Github地址](https://github.com/electron/asar)

![asar-website.png](images/asar-website.png)

其他安装方法请自行搜索，我不会🤡，嘿嘿😁

### Python安装
Python官方地址: [https://www.python.org/downloads/](https://www.python.org/downloads/)

![python-website.png](images/python-website.png)

该地址会默认检测当前操作系统并指引你下载对应安装包，安装过程自行领会

到此，你已经达到了运行脚本的条件了，接下来，我会给你解释每一个文件

### StarUML_Trans.py文件解析
⚠️ 由于要对目录进行解包操作，请确保运行该脚本前，Mac的运行命令前面加`sudo`，Windows下的 cmd 以管理员身份运行

- `decompressAsar()` \
负责对`asar.app`进行解包操作，需要用到`asar`命令，请再次确保你满足了[运行脚本的基本条件](#运行脚本的基本条件)
  - `app.asar`: StarUML 根目录下 resources 下的 app.asar 文件地址
  - `app`: 解包后的文件名，一般为app.asar文件路径删除后缀名即可

Mac使用说明举例如下，Windows类似
```python
def decompressAsar():
    os.system("asar extract /Applications/StarUML.app/Contents/Resources/app.asar /Applications/StarUML.app/Contents/Resources/app")
```

- `pack2asar()`\
负责对`app`文件夹进行打包操作，需要用到`asar`命令，请再次确保你满足了[运行脚本的基本条件](#运行脚本的基本条件)
  - `app`: 需要对已经修改过的`app`文件夹进行打包处理，该处为路径
  - `app.asar`: 打包后的文件，该处为路径

Mac使用说明举例如下，Windows类似
```python
def pack2asar():
    os.system("asar pack /Applications/StarUML.app/Contents/Resources/app /Applications/StarUML.app/Contents/Resources/app.asar")
```

- `load_replacements(file_path, direction)`\
负责读取汉化文件`StarUML_Language.json`并依据用户选择进行对应的汉化或还原
  - `file_path`: 汉化文件存放地址
  - `direction`: 汉化或还原，在main函数中可以看到，可自定义
  - `key`: 由于汉化是采用比对方式汉化，所以该处key的值可以在汉化文件中找到(html值已实现，但是我懒得上传了)


- `replace_keys(obj, replacements, key_to_replace)`\
负责对指定文件中的键值对进行翻译或还原，本函数采用了递归的方式，如果你不懂，无需修改
  - `obj`: 对应文本
  - `replacements`: 汉化规则，通过`load_replacements()`取得
  - `key_to_replace`: 处理方向，汉化或还原，main函数中可见


- `update_files(files_path, replacements)`\
负责对`app`文件夹中已指定的文件进行汉化或还原处理，该函数通过files_path规则进行智能匹配，如果你不懂，请你不要修改
  - `files_path`: main函数中指定的`files_path`规则
  - `replacements`: 汉化规则，通过`load_replacements()`取得


- `main()`\
主函数，支持让用户选择汉化或还原，并自动检测`app.asar`是否已被解包，若没被解包，则自动进行解包程序
  - `files_path`: 指定对应文件夹下的某个文件或某类文件需要被处理
  - `update_files()`: 执行处理函数

**files_path说明如下**\
拿`app/resources/default/menus/*.json`来举例子，若某个json文件新增了对应键值对需要被汉化处理，则填入规则如下\
```python
{
    'path': [
        'app/resources/default/menus/' # 填入该文件的所在目录，一个你也要给老子写成数组的形式
    ],
    'file_pattern': '.json',           # 如果你不知道要处理哪个json或要处理搜有json，你就只填 .json 就行，否则精确填写 xxx.json
    'key_to_replace': ['label']        # 该处的label意思是匹配"lebel": "xxxxx"的情况，注意，该处对js文件无效，js文件自己参考我的用正则匹配
}
```

### StarUML_Crack.py文件解析
⚠️ 由于要对目录进行解包操作，请确保运行该脚本前，Mac的运行命令前面加`sudo`，Windows下的 cmd 以管理员身份运行

刚才说了，由于我的主力常用机是Mac，所以该处的Mac处理非常友好

#### Mac Crack运行说明
感谢Mac的App只能默认安装在 Applications 文件夹，所以无论`StarUML_Crack.py`文件所处位置在哪里，你的都可以直接运行
```Bash
# 由于我是python3的版本
sudo python3 StarUML_Crack.py
```

#### Windows Crack运行说明
由于我没有Windows，有我也懒得测，所以随便写了个脚本，由`StarUML_Crack.py`文件可知，你需要准备的是
1. 你需要找到StarUML的根目录主程序并在有需要时填入
2. 如果你由更好的方法，请自行修改，我不需要，也不要提pr和issues

----