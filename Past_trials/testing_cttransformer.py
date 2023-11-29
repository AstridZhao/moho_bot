from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import CTransformers
import os

model_name = 'TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf'
pure_name = model_name.split('/')[-1]

llamacpp_directory = '/Users/astridz/Documents/llama.cpp'
local_directory = '/Users/astridz/Documents/moho_bot'
docker_directory = '/Users/astridz'


DEFAULT_PROMPT = "You are a helpful, respectful and honest assistant."
instruction = "Convert the following text from English to Chinese: {text}."
text = "you are beautiful."
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
DEFAULT_PROMPT = B_SYS + DEFAULT_PROMPT  + E_SYS
template = B_INST + DEFAULT_PROMPT + instruction + E_INST
# template = B_INST + DEFAULT_PROMPT + instruction + E_INST

prompt = PromptTemplate(template=template,input_variables= ["text"])

os.chdir(llamacpp_directory)
llm = CTransformers(model=pure_name,
                model_type='llama',
                config={'max_new_tokens': 128,
                        'temperature': 0.01}
                )

LLM_Chain=LLMChain(prompt=prompt, llm=llm)
print(LLM_Chain.run("How are you"))