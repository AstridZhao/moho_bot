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
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project
This project is for the llama2 chatbot built specifically for Mount Holyoke College information. 

### Built With
* [![Python][python.org]][Python-url]
* [![JupyterLab][https://jupyterlab.readthedocs.io/en/latest/#]][JupyterLab-url]
* [![Llama.cpp][https://github.com/ggerganov/llama.cpp]][llamacpp-url]
* [![Streamlit][streamlit.io]][Streamlit-url]
* [![Next][Next.js]][Next-url]
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Prerequisite

### Python library packages

### Architecture
If you are using Apple Silicon (M1) Mac, make sure you have installed a version of Python that supports arm64 architecture; Otherwise, while installing it will build the llama.ccp x86 version which will be 10x slower on Apple Silicon (M1) Mac. To install arm64 architecture on your laptop, run the following code on your laptop:
```zsh
arm64path = "Miniforge3-MacOSX-arm64.sh"
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh
bash Miniforge3-MacOSX-arm64.sh
```
### Llama.cpp
The main goal of llama.cpp is to run the LLaMA model using 4-bit integer quantization on a MacBook. The instructions below are for Macs with an **M1 chip**.
For other operating systems, comment out those cells and get instructions [here](https://github.com/TrelisResearch/llamacpp-install-basics/blob/main/instructions.md).






