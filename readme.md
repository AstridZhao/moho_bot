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
* [![JupyterLab][https://jupyterlab.readthedocs.io/en/latest/#][Jupyter-url]
* [![Llama.cpp][https://python.langchain.com/docs/integrations/llms/llamacpp]][llamacpp-url]
* [![Streamlit][streamlit.io][streamlit-url]
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started
If you are using Apple Silicon (M1) Mac, make sure you have installed a version of Python that supports arm64 architecture; Otherwise, while installing it will build the llama.ccp x86 version which will be 10x slower on Apple Silicon (M1) Mac. For example:
```sh
arm64path = "Miniforge3-MacOSX-arm64.sh"
if os.path.exists(arm64path):
    print("Version of Python that supports arm64 architecture already exists!")
else:
    print("Uncomment the next block of code and install python.")
```
