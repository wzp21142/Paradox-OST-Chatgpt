import openai
import os
from utils.ymlFile import *
import re
import tiktoken
def translator(_messages):
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=_messages,
                #temperature=0.2,
            )
    return response.choices[0].message.content.strip()

def getAllymlFiles(path):
    ymlFiles = []
    for root, _, files in os.walk(path):
        for file in files:
            absolutePath=os.path.join(root, file)
            relPath=os.path.relpath(absolutePath,start=path)
            with open(absolutePath, 'r', encoding='UTF-8') as f:
                content = f.read()
            ymlFiles.append(ymlFile(content,relPath))
    return ymlFiles

def getKey_Value(content):
    content=content.split('\n')[1:]
    content=[s for s in content if len(s)>3]
    pattern = r':\d*\s"'
    key,value=[],[]
    for i in content:
        searcher=re.search(pattern,i)
        if searcher is None: continue
        start,end=searcher.start(),searcher.end()
        space=re.search(r'\s',i[start:end]).start()
        key.append(i[:start+space])
        value.append(i[end:-1])
    return [key,value]

def getPairs(key,value):
    pairs=[]
    for i in range(len(key)):
        pairs.append(key[i]+" \""+value[i]+"\""+"\n")
    return pairs

def getPromptLang(language):
    if language != ('braz_por' or 'simp_chinese'):
        return language
    else:
        return 'Portuguese' if language=='braz_por' else 'Chinese'

def saveFile(lang,path,files):
    savePath=os.path.join(path,files.filePath)
    if not os.path.exists(os.path.dirname(savePath)):
        os.makedirs(os.path.dirname(savePath))
    try:
        with open(savePath, 'w', encoding='UTF-8') as f:
            f.write("l_"+str(lang)+":\n")
            f.write(''.join(files.content))
            return True
    except:
        print("Error: "+savePath)
        return False

def tokensCount(messages):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    print("tokens:"+str(num_tokens))
    return num_tokens