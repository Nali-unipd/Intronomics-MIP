import os
import sys
import re

input_dir = sys.argv[1]

counter = 1


output_file = "NameInd-ID.txt"

def natural_key(string):
    """Funzione che permette di ordinare in modo naturale."""
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', string)]

for dir_name in sorted(os.listdir(input_dir), key=natural_key):
    full_path = os.path.join(input_dir, dir_name)
    
    if os.path.isdir(full_path):

        new_name = f"Ind{counter}"
        new_full_path = os.path.join(input_dir, new_name)
        

        os.rename(full_path, new_full_path)
        

        with open(os.path.join(input_dir, output_file), 'a') as f:
            f.write(f"{dir_name} -> {new_name}\n")
        

        counter += 1

path = os.path.join(input_dir, "Log_rename.txt")
with open(path, 'a') as log_file:
    log_file.write(f"The correspondence between the old and new names has been saved in {output_file}\n")
