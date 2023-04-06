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

## 已知问题

1. 目前程序用一种很蠢的方法切分开了过长的文本，并分段让ChatGPT进行翻译。但是，由于GPT-3.5模型本身对长文本的处理能力不是很理想，因此在大型mod上的翻译可能不尽如人意，还需要额外做大量校对工作。但个人认为这个问题是可以通过提供更好的prompt/更合理的超参数设置解决的。例如，目前脚本设置的是每1350个输入token切分一次，如果设置为400甚至300，翻译质量会更高，但带来的问题是每次请求的prompt约占100个token，这个数值设置得越低，就会发更多次翻译请求，在prompt上浪费越多的token，如果确实需要高质量翻译，请自行权衡。
2. 对于大文件可能存在等待时间较长的问题，这是因为程序99%的运行时间都是在等待ChatGPT的回复，除非OpenAI在API层面提高响应速度，否则只能并发式请求翻译，考虑到目前大面积封号的问题，暂时不实现这类可能对账号比较危险的功能。
3. 已知的bug：
   [1] ChatGPT有时会不按格式输出，导致key-value对无法配对，报错信息会是IndexError: list index out of range。目前的解决方案是用"↑"分割每个输入ChatGPT的value而不是用默认的引号和逗号（因为value文本中本身也存在这两种字符，在处理上下文关系时ChatGPT并不能完全理解分割关系，进而翻译出错），在测试中此类问题会减少很多，但仍然偶有发生。如果出现此类情况，可能是因为出错的文件中存在"↑"字符，可以换成其他字符，对照输出路径中已经翻译好的文件，暂时删除输入路径下对应的原文本文件，从上次中断的地方重新开始翻译，如果反复测试都在同一个文件上报错，再尝试改小每次分段的大小(见1)。由于GPT回答的随机性，目前没有更好的解决方法。
   [2] 在几行内有很多内容相似的文本时，ChatGPT会大概率遗漏掉其中的几条，导致key-value对无法匹配。这个问题在网页端是不存在的，但在API上几乎必定出现，可能仍然需要更精细的prompt设计，感兴趣的朋友可以尝试翻译V3本体的Victoria 3\game\localization\concepts_l_english.yml文件。
4. 目前的脚本只是初版，可能还存在其他各种问题，如果对以上任何问题有更好的建议、更好的配置方案或者发现bug，随时欢迎issue/PR！