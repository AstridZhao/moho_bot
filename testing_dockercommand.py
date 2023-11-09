import subprocess, os
from langchain.vectorstores import Epsilla

if (os.getcwd() != "/Users/astridz"):
    os.chdir('/Users/astridz')
# Pull the Docker image

start_command = "open -a Docker"
start_process = subprocess.Popen(start_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = start_process.communicate()
if start_process.returncode != 0:
    print(f"Error start Docker: {err}")
else:
    print("start success! \n")
    print(f"Output: {out} \n")

pull_command = "docker pull epsilla/vectordb"
pull_process = subprocess.Popen(pull_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = pull_process.communicate()
if pull_process.returncode != 0:
    print(f"Error pulling Docker image: {err}")
else:
    print("pull success! \n")
    print(f"Output: {out} \n")

# Run the Docker container
run_command = "docker run --pull=always -d -p 8888:8888 epsilla/vectordb"
run_process = subprocess.Popen(run_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = run_process.communicate()
if run_process.returncode != 0:
    print(f"Error running Docker container: {err}")
else:
    print("r! success! \n")
    print(f"Output: {out} \n")
    
os.chdir('/Users/astridz/Documents/moho_bot')