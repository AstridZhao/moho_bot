
from pyepsilla import vectordb
from sentence_transformers import SentenceTransformer
import streamlit as st
import os
import subprocess, threading
from typing import List
from transformers import AutoTokenizer
import requests
import json
import time, queue

import subprocess, os
from langchain.vectorstores import Epsilla
from langchain.prompts import PromptTemplate
# start docker ->---------------->---------------->---------------
# if (os.getcwd() != "/Users/astridz"):
#     os.chdir('/Users/astridz')
# # Pull the Docker image

# start_command = "open -a Docker"
# subprocess.run(start_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# # out, err = start_process.communicate()
# # if start_process.returncode != 0:
# #     print(f"Error start Docker: {err}")
# # else:
# #     print("start success! \n")
# #     print(f"Output: {out} \n")

# pull_command = "docker pull epsilla/vectordb"
# subprocess.run(pull_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# # out, err = pull_process.communicate()
# # if pull_process.returncode != 0:
# #     print(f"Error pulling Docker image: {err}")
# # else:
# #     print("pull success! \n")
# #     print(f"Output: {out} \n")

# # # Run the Docker container
# run_command = "docker run --pull=always -d -p 8888:8888 epsilla/vectordb"
# subprocess.run(run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# # out, err = run_process.communicate()
# # if run_process.returncode != 0:
# #     print(f"Error running Docker container: {err}")
# # else:
# #     print("r! success! \n")
# #     print(f"Output: {out} \n")
    
# os.chdir('/Users/astridz/Documents/moho_bot')

# ->---------------->---------------->---------------

local_directory = "/Users/astridz/Documents/moho_bot"
# Local embedding model for embedding the question.
model = SentenceTransformer('all-MiniLM-L6-v2')
class LocalEmbeddings():
    def embed_query(self, text: str) -> List[float]:
        return model.encode(text).tolist()
    
embeddings = LocalEmbeddings()
# Connect to Epsilla as knowledge base.
client = vectordb.Client()
vector_store = Epsilla(
    client,
    embeddings,
    db_path="/tmp/localchatdb",
    db_name="LocalChatDB"
)

vector_store.use_collection("LocalChatCollection")

model_name = 'TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf'
pure_name = model_name.split('/')[-1]

st.set_page_config(page_title="🦙💬 Llama 2 Chatbot with Streamlit")

#Create a Side bar
with st.sidebar:
    st.title("🦙💬 Llama 2 MohoBot")
    st.header("Settings")
    
# Clear the Chat Messages
def clear_chat_history():
    st.session_state.messages=[{"role":"assistant", "content": "As a helpful question answer assistant, how can I help you today?"}]
    print_dialog()
# create Clear button
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Diplay the chat messages
def print_dialog(): 
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    
#store message 
if "messages" not in st.session_state.keys():
    st.session_state.messages=[{"role": "assistant", "content": "As a helpful question answer assistant, how can I help you today?"}]
    # st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    st.chat_message("assistant").write("As a helpful question answer assistant, how can I help you today?")


if question := st.chat_input():
    question = question.strip()
    st.session_state.messages.append({"role": "user", "content": question})
    print_dialog()
    #vector_store.similarity_search
    context = ''.join(map(lambda doc: doc.page_content, vector_store.similarity_search(question, k = 2)))
    # Split into lines, strip whitespace, filter out empty lines, and join back into a single string
    clean_context = '\n'.join([line.strip() for line in context.splitlines() if line.strip()])
    
    SYSTEM_PROMPT =f'''As a helpful question answer assistant, answer the user question by giving response and follow the rules: \
    1. Do not copy the context in your answer. Try to understand the context and rephrase them. \
    2. Please don't make things up or say things not mentioned in the Context. \
    3. You can trust the context. \
    The context is: {clean_context}'''
    # prompt_template = f'''[INST]<<SYS>>\n{SYSTEM_PROMPT}{context}\n<</SYS>>\n\n{question}[/INST]'''
    # prompt_template = f'''[INST]<<SYS>>\n{SYSTEM_PROMPT}{context}\n<</SYS>>\n\n{question}[/INST]'''
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    SYSTEM_PROMPT = B_SYS + SYSTEM_PROMPT + E_SYS
    prompt_template = B_INST + SYSTEM_PROMPT + question + E_INST

    # Start the subprocess and the threading to handle its output
    if (os.getcwd() != '/Users/astridz/Documents/llama.cpp'):
        os.chdir('/Users/astridz/Documents/llama.cpp')
    
    # prompt_template = f'''./main -m llama-2-7b-chat.Q4_K_M.gguf -c 1024 --verbose-prompt --keep 0 -b 16 -ngl 48 --prompt '{SYSTEM_PROMPT}{context} USER: {question}' --in-suffix 'ASSISTANT:' '''
    
    # ./main -m llama-2-7b-chat.Q4_K_M.gguf -c 1024 --verbose-prompt --keep 0 -b 16 -ngl 48 -p
    pure_name = "llama-2-7b-chat.Q4_K_M.gguf"
    print(prompt_template)
    command = ['./main', '-m', pure_name, '-c', '1024', '--multiline-input', '-ngl', '8', '-p', prompt_template]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    start_time = time.time()
    while True:
        if process.poll() is not None:
            break  # Break the loop if the subprocess has finished
        
        output = process.stdout.readline()
        assistant_response = ""
        if output:
            if '[/INST]' in output:
                inst_index = output.find('[/INST]')
                # Check if [/INST] is found in the text
                if inst_index != -1:
                    # Print everything after [/INST]
                    assistant_response = output[inst_index + len('[/INST]'):].strip()
                    st.session_state.messages.append({"role" : "assistant", "content": f'''{assistant_response}</s><s>[INST]'''})
                    st.chat_message("assistant").write(assistant_response)
            elif '<</SYS>>' in output or '[INST]' in output:
                continue
            elif  'As a helpful question answer assistant, ' in output:
                st.chat_message("assistant").write("processing...")
            else:
                assistant_response = output.strip()
                if assistant_response == "":
                    continue
                else:
                    st.session_state.messages.append({"role":"assistant", "content": f'''{assistant_response}</s><s>[INST]'''})
                    st.chat_message("assistant").write(assistant_response)
    
        # end_time = time.time()
        # elapsed_time = end_time - start_time
        # print("total time :",  elapsed_time)
        
        # process.stdout.close()

