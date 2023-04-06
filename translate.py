from utils.utils import *
from dotenv.main import load_dotenv
import argparse
import tqdm
load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")

parser = argparse.ArgumentParser()
parser.add_argument('-i','-input', type=str, required=True, help='The input path')
parser.add_argument('-l','-language', type=str, required=True, default='english', help="Target language (EXCEPTIONALLY, use 'braz_por' for Brazilian/Portuguese and 'simp_chinese' for Simplified Chinese)")
parser.add_argument('-o','-output', type=str, help='The output path, if not provided, the output will be saved in the same directory.')
args = parser.parse_args()

inputPath,language,outputPath=args.i,args.l,args.o
localeFiles=getAllymlFiles(inputPath)
lang=getPromptLang(language)
if outputPath is None:
    outputPath=os.path.join(os.path.dirname(inputPath), language.lower())
tokensInTotal=0


for file in tqdm.tqdm(localeFiles):
    print(file.filePath)
    file.content=getKey_Value(file.content)
    origin=file.content[1]
    errorPath=os.path.join(outputPath,file.filePath+"_error.yml")
    # The total tokens counter is erroneous
    '''From OpenAI's documentation:
    Note that very long conversations are more likely to receive incomplete replies. 
    For example, a gpt-3.5-turbo conversation that is 4090 tokens long will have its reply cut off after just 6 tokens.
    A tested configuration that works well on Victoria 3 game is 1350 tokens per request. If you want to change this, DO REMEMBER TO CHANGE THE VALUE IN utils.splitContents.
    '''
    get_text = lambda _t: "[["+"".join(getSeparatedContent(_t)).__str__()+"]]"
    
    _text=get_text(origin)
    tokens=len(tiktoken.encoding_for_model('gpt-3.5-turbo-0301').encode(_text))
    tokensInTotal+=tokens
    if tokens<=1350:
        file.content=segmentTranslator(lang,_text,file.content[0],errorPath)
    else:
        splitLocation=splitContents(origin)
        translated=[]
        start=0
        for i in range(len(splitLocation)):
            if i==len(splitLocation)-1 and splitLocation[-1]==len(origin) and start!=0:
                start=len(origin)-1
            else:
                #print(len(tiktoken.encoding_for_model('gpt-3.5-turbo').encode("".join(origin[start:splitLocation[i]-1].__str__()))))
                _text=get_text(origin[start:(splitLocation[i]-1)])
                translated.append(segmentTranslator(lang,_text,file.content[0][start:splitLocation[i]-1],errorPath,i,translated))
                start=splitLocation[i]
        _text=get_text(origin[start:])
        translated.append(segmentTranslator(lang,_text,file.content[0][start:],errorPath,i,translated))
        file.content=translated
    saveFile(language,outputPath,file)


print("Done, total tokens used:"+str(tokensInTotal))