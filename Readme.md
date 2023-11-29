<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
This project is for the llama2 chatbot built specifically for Mount Holyoke College information. 

### Built With
* ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
* ![JupyterLab](https://img.shields.io/badge/JupyterLab-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white)
* ![Llama.cpp](https://img.shields.io/badge/Llama.cpp-002b36?style=for-the-badge)
* ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
  
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Prerequisite

### Install Architecture
If you are using Apple Silicon (M1) Mac, make sure you have installed a version of Python that supports arm64 architecture; Otherwise, while installing it will build the llama.ccp x86 version which will be 10x slower on Apple Silicon (M1) Mac. To install arm64 architecture on your laptop, run the following code on your laptop terminal:
```zsh
arm64path = "Miniforge3-MacOSX-arm64.sh"
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
```

## Installation
### Clone the repo
```zsh
git clone [https://github.com/](https://github.com/AstridZhao/moho_bot.git)
```
### Install essential packages
To have all the packages needed to run the code, you can run the below code in the **terminal** with the main program directory:
```zsh
pip install -r requirements.txt
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Install Llama.cpp
The main goal of llama.cpp is to run the LLaMA model using 4-bit integer quantization on a MacBook. The instructions below are for Macs with an **M1 chip**.
For other operating systems, you can find instructions [here](https://github.com/TrelisResearch/llamacpp-install-basics/blob/main/instructions.md).

Run the below code in **terminal**. Make sure the current directory should be the main program directory.
```zsh
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
LLAMA_METAL=1 make
cd ..
```
Then, after installing llama.cpp, we can require the specific llama model from huggingface. In this project, we chose to use  "llama-2-7b-chat.Q4_K_M.gguf". Run the below code in the **terminal**.
```zsh
cd llama.cpp
wget https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
cd ..
```

Now you have the llama model available to run on your laptop. 
To test if your installation is successful, you can do it with the below code in the **terminal**:
```zsh
cd llama.cpp
./main -m llama-2-7b-chat.Q4_K_M.gguf -c 1024 -ngl 8 -p "Where is new york?"
```

### Install Docker Desktop

In this project, we need to use the vector database (epsilla/vectordb), which could be pulled by docker.

Docker Desktop is a one-click-install application for your Mac, Linux, or Windows environment that lets you build, share, and run containerized applications and microservices. Docker packages software into standardized units called containers that have everything the software needs to run including libraries, system tools, code, and runtime.

You find the more detailed install instructions of docker [here](https://docs.docker.com/desktop/install/mac-install/).
I suggest you install the docker in the "/Users/{your username}" directory.

After installing successfully, you need to run the below code in **terminal** before initiating the program code each time.

```zsh
cd /Users/{your username}
open -a Docker
docker pull epsilla/vectordb
docker run --pull=always -d -p 8888:8888 epsilla/vectordb
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->

## Program function

To run this program project, you need to do FOUR steps: 

* 1. Initiate Docker with the command
     
     ```zsh
      cd /Users/{your username}
      open -a Docker
      docker pull epsilla/vectordb
      docker run --pull=always -d -p 8888:8888 epsilla/vectordb
    ```
and then return back to the program directory.
  
* 2. To extract text from the Mount Holyoke College website, run [collect.py].
     You can find or edit the website link in "URL.txt" file in the folder.

      ```zsh
     python3 collect.py
     ```
     
* 3. To train the dataset, run [learn.py] by using command
     
     ```zsh
     python3 learn.py
     ```
  
* 4. To run the chatbot, run [app.py] by using command

     ```zsh
     streamlit run app.py
     ```

**I suggest you run the program following the above sequence to avoid unexpected errors.**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->

## Chatbot Interface

After running the app.py, the streamlit will bring you to the chatbot interface.



https://github.com/AstridZhao/moho_bot/assets/79214456/5bde6326-8039-458f-9949-a4c0ad573064


