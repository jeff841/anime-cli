from os import walk
from os.path import join
from subprocess import run
from pathlib import Path

directory = Path(input("Enter the directory where your episode files are: "))
for folder,sub_folders,files in walk(directory):
    sor = []
    for file in files:
        sor.append(file)
    sor.sort()
    count = 1
    for i in sor:
        run(['mv',join(directory,i),join(directory,f'ep{count}-')])
        count+=1

    
        

        

        
        
