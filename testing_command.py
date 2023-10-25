import shlex, subprocess, os
os.chdir('/Users/astridz/Documents/llama.cpp')
command_line = input()
# ./main -m llama-2-7b-chat.Q4_K_M.gguf -c 2048 -c N 2048 -ngl 48 -p
# ./main -m llama-2-7b-chat.Q4_K_M.gguf -c 2048 -ngl 48 -p
# command = ['./main', '-m', pure_name, '-c', '2048', '-ngl', '48', '-n N', '5',  '-e', '-p', prompt]
# ./main -m llama-2-7b-chat.Q4_K_M.gguf -c 2048 -ngl 48 -p "You are a helpful question answer assistant. Based on given Context: comsc150 followed comsc161 combination two equivalent comsc151for student curious computer science comsc151ds comsc151hc 2 comsc150 plus comsc121 substitute comsc151 3 comsc205py plus comsc122 COMSC-161 serves as an alternate prerequisite route for COMSC-205 Data Structures.COMSC-205  Data computer science study, COMSC-150 should be followed by COMSC-161; the combination of the two is comsc161 serves alternate prerequisite route comsc205 data structurescomsc205 data structuresfall, answer question what is COMSC151?""

"""
        You are a helpful question answer assistant. Based on given Context: comsc150 followed comsc161 combination two equivalent comsc151for student curious computer science comsc151ds comsc151hc 2 comsc150 plus comsc121 substitute comsc151 3 comsc205py plus comsc122 COMSC-161 serves as an alternate prerequisite route for COMSC-205 Data Structures.COMSC-205  Data computer science study, COMSC-150 should be followed by COMSC-161; the combination of the two is comsc161 serves alternate prerequisite route comsc205 data structurescomsc205 data structuresfall, answer question what is COMSC151?. 
        
        Do not copy the context in your answer.
        Try to understand the Context and rephrase them.
        Please don't make things up or say things not mentioned in the Context. 
        
"""
args = shlex.split(command_line)
print(args)

p = subprocess.Popen(args,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output = p.stdout.readlines()
# try:
#     # print("communicated")
#     outs, errs = p.communicate(timeout=15)
#     print("communicated")
# except subprocess.TimeoutExpired:
#     p.kill()
#     outs, errs = p.communicate()

print("Answer: \n " )
print(output)

os.chdir('/Users/astridz/Documents/Moho_Bot')