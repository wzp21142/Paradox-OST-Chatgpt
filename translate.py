from utils.utils import *
from dotenv.main import load_dotenv
import argparse

load_dotenv() 
openai.api_key = os.getenv("OPENAI_API_KEY")

parser = argparse.ArgumentParser()
parser.add_argument('-i','-input', type=str, required=True, help='The input path')
parser.add_argument('-l','-language', type=str, required=True, default='english', help="Target language (EXCEPTIONALLY, use 'braz_por' for Brazilian/Portuguese and 'simp_chinese' for Simplified Chinese)")
parser.add_argument('-o','-output', type=str, help='The output path, if not provided, the output will be saved in the same directory.')
args = parser.parse_args()

inputPath,language,outputPath=args.i,args.l,args.o
localeFiles=getAllymlFiles(inputPath)


count=0
for file in localeFiles:
    count+=1
    file.content=getKey_Value(file.content)
    origin=file.content[1]
    messages=[
    {"role": "system", "content": "You are a great translate bot. Translate a i18n locale array content to "+getPromptLang(language)+". It's a array structure, contains many strings, translate each of them and make a new array of translated strings. Consider all the string as a context to make better translation. Do not translate the text between [], $$ or @ and !.\n"},
    {"role": "user", "content": "".join(origin.__str__())},
]
    print(str(messages)+"\n")
    if tokensCount(messages)<=4095:
        file.content[1]=translator(messages)[2:-2].split("', '")
        print(file.content[1])
        if outputPath is None:
            outputPath=os.path.join(os.path.dirname(inputPath), language.lower())
        file.content=getPairs(file.content[0],file.content[1])
        saveFile(language,outputPath,file)
    else:
        print("Error: Too many tokens in "+file.filePath)
print("Done")