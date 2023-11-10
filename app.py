from langchain.vectorstores import Epsilla
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

# def generate_response(process):
    # output,error = process.communicate()
    #     # #reinitialize assistant_response each time
    #     # if process.poll() is not None and output == '':
    #     #     print("Subprocess has completed.")
    #     #     break 
    # if output:
    #     print("Subprocess has started.")
    #     assistant_response = f"{output.strip()}"
        
    #     # Ensure that `messages` is initialized in `st.session_state`
    #     if "messages" not in st.session_state:
    #         st.session_state["messages"] = []
            
    #     if assistant_response:
    #         msg = { 'role': 'assistant', 'content':assistant_response}
    #         st.session_state.messages.append(msg)
            
    #         # Ensure that Streamlit commands are only called in the main thread
    #         if threading.current_thread() == threading.main_thread():
    #             st.chat_message("assistant").write(msg['content'])
    #         print(f'{assistant_response}\n')
    # else:
    #     print(error)
        
    # process.stdout.close()

st.set_page_config(page_title="🦙💬 Llama 2 Chatbot with Streamlit")

#Create a Side bar
with st.sidebar:
    st.title("🦙💬 Llama 2 MohoBot")
    st.header("Settings")
    
# Clear the Chat Messages
def clear_chat_history():
    st.session_state.messages=[{"role":"assistant", "content": "How may I assist you today?"}]
    print_dialog()
# create Clear button
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Diplay the chat messages
def print_dialog(): 
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    
SYSTEM_PROMPT = '''You are a helpful question answer assistant. Answer the user question followed the rules:1. Do not copy the context in your answer. Try to understand the Context and rephrase them. 2. Please don't make things up or say things not mentioned in the Context. 3. You can trust the context. 4. Give a short response! Your answer should be in 200 words. The context is: '''
# template = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

#store message 
if "messages" not in st.session_state.keys():
    st.session_state.messages=[{"role": "assistant", "content": "You are a helpful question answer assistant. How can I help you?"}]
    # st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    st.chat_message("assistant").write("I am a helpful question answer assistant. How can I help you?")

if question := st.chat_input():
    question = question.strip()
    st.session_state.messages.append({"role": "user", "content": question})
    print_dialog()
    #vector_store.similarity_search
    context = ''.join(map(lambda doc: doc.page_content, vector_store.similarity_search(question, k = 2)))
    
    #Testing:
    prompt_template = f'''<s>[INST]<<SYS>>\n{SYSTEM_PROMPT}{context}\n<</SYS>>\n\n{question}[/INST]'''
    # prompt_template = f'''{SYSTEM_PROMPT}{context} The user question is: {question}'''

    # Start the subprocess and the threading to handle its output
    if (os.getcwd() != '/Users/astridz/Documents/llama.cpp'):
        os.chdir('/Users/astridz/Documents/llama.cpp')

    # prompt_template = f'''<s>[INST]<<SYS>>\n
    # {SYSTEM_PROMPT}{context}\n
    # <</SYS>>\n\n
    # {question}[/INST]'''
    
    # prompt_template = f'''./main -m llama-2-7b-chat.Q4_K_M.gguf -c 1024 --verbose-prompt --keep 0 -b 16 -ngl 48 --prompt '{SYSTEM_PROMPT}{context} USER: {question}' --in-suffix 'ASSISTANT:' '''
    
    # ./main -m llama-2-7b-chat.Q4_K_M.gguf -c 1024 --verbose-prompt --keep 0 -b 16 -ngl 48 -p
    pure_name = "llama-2-7b-chat.Q4_K_M.gguf"
    command = ['./main', '-m', pure_name, '-c', '2048', '--keep', '0', '-b', '1024', '-ngl', '48', '-p', prompt_template]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
    start_time = time.time()
    output = process.stdout.read()
    marker_index = output.find("[/INST]")
    prompt_tokens = []

    if marker_index != -1:
        assistant_response = output[marker_index + len("[/INST]"):] 
        st.session_state.messages.append([{"role":"assistant", "content": f'''{assistant_response}'''}] )
        st.chat_message("assistant").write(assistant_response)
    # else:
    #     st.session_state.messages.append([{"role":"assistant", "content": f'''{output}</s><s>[INST]'''}] )
    #     st.chat_message("assistant").write(output)
        
    # while True:
    #     output = process.stdout.readline()
        # print(output)
    #     if process.poll() is not None and output == '':
    #         print("Subprocess has completed.")
    #         break 
    #     if 'You are a helpful question answer' in output:
    #         continue
    # assistant_response = f"{output.strip()}"
    # st.session_state.messages.append([{"role":"assistant", "content": f'''{assistant_response}'''}] )
    # st.chat_message("assistant").write(assistant_response)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("total time :",  elapsed_time)

    # # Function to read from a stream and put the output in a queue
    # def enqueue_output(stream, queue):
    #     output = iter(stream.read, b'')
    #     queue.put(output)
    #     stream.close()
    
    # # Create queues to hold the output
    # stdout_queue = queue.Queue()
    # stdout_thread = threading.Thread(target=enqueue_output, args=(process.stdout, stdout_queue))
    # stdout_thread.start()
    
    # # Read from the queues
    # while True:
    #     try:
    #         # Try to get output from the queues
    #         stdout_line = stdout_queue.get_nowait()
    #         print(stdout_line)
    #         st.session_state.messages.append([{"role":"assistant", "content": stdout_line}])
    #         st.chat_message("assistant").write(stdout_line)
    #                 # output = process.stdout.read()
            
    #     except queue.Empty:
    #     # No output ready
    #         pass

    # # Process the output here

    #     # Check if the subprocess is still running
    #     if process.poll() is not None:
    #         break

    # # Make sure threads have finished
    # stdout_thread.join()

    # process.stdout.close()
        
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print("total time :",  elapsed_time)













    
    # # # Start the thread that will handle the subprocess output
    # output_thread = threading.Thread(target=generate_response, args=(process, output_log))
    # output_thread.start()
    # # Wait for the subprocess and thread to finish
    # process.wait()
    # output_thread.join()
    # os.chdir(local_directory)
    
    # placeholder=st.empty()
    # full_response=''
    
