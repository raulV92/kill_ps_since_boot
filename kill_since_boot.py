## kill every process created after initial boot:
# Note:
# Print statements commented in this script were used to debug during the making of this
# You can uncomment them to have a better undestanding of what this is doing

import os
from typing import List
import subprocess
import re
import pwd

   
def get_ps(ps_output:List)->List:   
    ps_name_re=re.compile(r':\d\d:\d\d\s.*$')
    ps_id_re=re.compile(r'^\s*\d*')
    useless=7 ## hardcoded into regular expression
    ps_names=[]
    ps_data={} # {name:id}
    for line in ps_output:
        ps_name= re.search(ps_name_re,line)
        ps_id= re.search(ps_id_re,line)
        #print(line)
        if ps_name and ps_id:
            #print(ps_line.group()[useless:])
            ps_data[ps_name.group()[useless:]]=ps_id.group().strip()
            
        else:
            # this should not fail, but just in case...
            # note: it actually fails on the headers and of the file has a blank line, but its fine...
            print(line+" >match failed") 
            
    return ps_data

def get_boot_process():
    """
    It expects you to have the "ps -u $USER > boot_ps.txt" output file in the same directory
    """
    with open('./boot_ps.txt','r') as f:
        ps_output=f.readlines()
        boot_ps=get_ps(ps_output)
    return boot_ps

def get_current_process():
    user=pwd.getpwuid(os.getuid())[0]
    result = subprocess.run(['ps','-u',user], stdout=subprocess.PIPE)
    result=result.stdout.decode('utf-8')
    
    return get_ps(result.split('\n'))

def kill_ps(ps_to_kill):
    for i in ps_to_kill:
        try:
            subprocess.run(["kill", "-9",str(ps_to_kill[i])]) 
            print(i,' killed')
        except:
            print('cannot kill ',i)

if __name__=='__main__':
    boot_data=get_boot_process()
    #print(boot_data.keys())
    #print(len(boot_data))
    current_ps=get_current_process()
    ps_to_kill={}
    for ps in current_ps.keys():
        if (ps not in boot_data and( ps!='python3' and ps != 'python')):# avoid killing itself 
            ps_to_kill[ps]=current_ps[ps]
    #print('\nPS TO KILL:')
    #print(ps_to_kill)
    
    kill_ps(ps_to_kill)
