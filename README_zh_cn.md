# Paradox-One-Step-Translator-Chatgpt

[![MIT licensed](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE)
本项目通过ChatGPT把P社定义的非标准YML本地化文本文件翻译成中文，一次运行可以翻译指定路径下的所有文件，享受完全本地化的mod和游戏！

**个人建议:如果想要发布用该工具生成的汉化mod，请尊重手工汉化和校对大佬的工作，标注mod是由chatgpt汉化的！**
## 使用指南

**1.** 在项目根目录下创建.env文件填入OpenAI的API KEY
```bash
OPENAI_API_KEY=<KEY>
```
**2.** 安装依赖
```bash
pip install -r requirements.txt
```

**2.5.** 删除假中文
mod原有的localization目录里可能已经有作者机翻过的中文，为了避免不必要的问题，可以[提前删除目录下的simp_chinese文件夹](https://steamcommunity.com/sharedfiles/filedetails/?id=2929724714)。

**3.** 运行脚本
```bash
python translate.py -i "输入路径" -l 语言 -o "输出路径"
```
注意输出路径不是必须的，如果不提供，默认输出路径会是输入路径/localization/LANGUAGE，其中LANGUAGE是用-l指定的语言。
例如，通过如下所示的方式运行脚本：
```bash
python translate.py -i "...\localization\english" -l simp_chinese
```
然后我们就可以在"...\localization\simp_chinese"这个路径下找到翻译后的YML文件。

**4.** 如果你没有指定输出路径，而且默认输出路径下没有假中文，理论上就可以直接开玩了！

## 注意

1. 当前的版本不支持超长的YML文件（受OpenAI 4096个tokens的限制），所以如果你十分需要翻译文本，请将这个文件拆分成多个YML文件，或者耐心等待我后续的更新，非常抱歉！如果你愿意写PR来修复这个问题，也非常欢迎和感谢！
2. 目前的脚本只是初版，可能还存在各种问题，发现bug欢迎及时提issue反馈！