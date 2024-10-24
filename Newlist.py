import os
import sys
input_dir = sys.argv[1]


counter = 1

output2= input_dir + "/Newlist.txt"

for dir_name in sorted(os.listdir(input_dir)):
    full_path = os.path.join(input_dir, dir_name)
    
    if os.path.isdir(full_path):
        ID = f"{dir_name}_S"
        with open(output2, 'a') as f:
            f.write(f"{ID}\n")
        
        counter += 1


