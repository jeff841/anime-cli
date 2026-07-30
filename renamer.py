from os import walk
from os.path import join
from subprocess import run
from pathlib import Path

def rename(directory):
    for folder,subfolders,files in walk(directory):
        sor = []
        for file in files:
            sor.append(file)
        sor.sort()
        count = 1
        for i in sor:
            run(['mv',directory/i,str(directory/f'ep{count}-')])
            count+=1

    
        

        

        
        
