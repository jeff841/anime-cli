from os import walk
from os.path import join
from subprocess import run

directory = '/home/jeff/anime_list/nisekoi/'
for folder,sub_folders,files in walk(directory):
    sor = []
    for file in files:
        sor.append(file)
    sor.sort()
    count = 1
    for i in sor:
        run(['mv',join(directory,i),join(directory,f'ep{count}-')])
        count+=1

    
        

        

        
        
