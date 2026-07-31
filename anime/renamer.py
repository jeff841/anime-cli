from pathlib import Path

def rename(directory: Path):
    files = sorted(
            f for f in directory.iterdir()
            if f.is_file()
            )
    for count,file in enumerate(files,start=1):
        file.rename(directory/f"ep{count}-")

    
        

        

        
        
