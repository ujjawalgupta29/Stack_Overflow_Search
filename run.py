import sys
from subprocess import PIPE, Popen
import requests
import webbrowser
import shlex

cmd = "python hello.py"
args = shlex.split(cmd)
proc = Popen(args, stdout=PIPE, stderr=PIPE)
stdout, stderr = proc.communicate()
stderr = stderr.decode('utf-8') #std error in UTF format to convert it into string from bytes
# print(stderr)

if stderr == '':
    print("No errors found")

else:
    stderr_list = stderr.split('\n')
    #Extract error line
    error = stderr_list[-2]
    error_list = error.split(':')
    error_type = error_list[0]

    error_list = error_list[1:]
    error_msg = ''.join(error_list)
    # print(error_type)
    # print(error_msg)

    resp  = requests.get("https://api.stackexchange.com/2.2/search?order=desc&tagged=python&sort=activity&intitle={}&site=stackoverflow".format(error))
    data = resp.json()
    # print(type(data))
    # print(data["items"][0]["link"])
    
    counts = 0
    top_links = []

    for d in data["items"]:
        if d["is_answered"] == True:
            counts += 1
            top_links.append(d["link"])

        if counts == 5:
            break

    print(top_links)

    for i in range(len(top_links)):
        webbrowser.open(top_links[i])
