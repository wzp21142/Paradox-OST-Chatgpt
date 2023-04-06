import openai
import os
from utils.ymlFile import *
import re
import tiktoken
def translator(lang,content):
    messages=[
        {"role": "system", "content": "You are a great translate bot. Translate a locale array content to "+lang+". It's an array structure which is related to politics and history, contains many strings that separated by UP arrow ↑, translate each of them and make a new array of translated strings separated by UP arrow ↑. Do make sure that translate every element between two ↑ and do not miss any of them. Do not translate the text between [], $$ or @ and !.\n"},
        {"role": "user", "content": content},
    ]
    try:
        response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    #The hyperparameters may be optimizable to keep the stability of the text form
                )
    except openai.error.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass
    return response.choices[0].message.content.strip()[2:-2].split("', '")

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
    annoPattern = r'^\s*#'
    key,value=[],[]
    for i in content:
        searcher=re.search(pattern,i)
        annoSearcher=re.search(annoPattern,i)
        if (searcher is None) or (annoSearcher is not None):
            continue
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

def splitContents(content):
    # return the position where exceed 4096 tokens
    start=0
    ans=[]
    for pos in range(len(content)):
        if len(tiktoken.encoding_for_model('gpt-3.5-turbo-0301').encode("[["+"".join(getSeparatedContent(content[start:pos])).__str__()+"]]"))>1350:
            ans.append(pos)
            start=pos
    return ans

def getSeparatedContent(content):
    ans=""
    for pos in range(len(content)):
        ans+=content[pos]
        if pos != len(content)-1:
            ans+='↑'
    return ans

def segmentTranslator(lang,_text,_keys,errorPath,segmentNum=0,translatedList=[]):
    translated=translator(lang, _text)
    translated="".join(translated).split("↑")
    try:
        ans=getPairs(_keys,translated)
    except:
        errorPath=os.path.join(errorPath+"_"+str(segmentNum))
        if not os.path.exists(os.path.dirname(errorPath)):
            os.makedirs(os.path.dirname(errorPath))
        with open(errorPath, 'w', encoding='UTF-8') as f:
            if len(translatedList)==0:
                for i in range(len(translated)):
                    translated[i]+='\n'
                f.write(''.join(translated))
            else:
                f.write(''.join(translatedList))
                f.write(''.join(translated))
        exit("Error, the half-translated file is saved to "+errorPath)
    return ans