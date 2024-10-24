import sys
import os

folder_path = str(sys.argv[1])  # Specify the folder path
out = "outputPop.txt"
filenames = []
loci = []
n = []

perc = float(sys.argv[2])  # Threshold percentage for valid data

# Iterate over all files in the folder
for file in os.listdir(folder_path):
    # Check if the file has the '.genepop' extension
    if file.endswith('.genepop'):
        filenames.append(os.path.join(folder_path, file))
        t = file.split('.')[0]
        loci.append(file.split('.')[0])  # Take the part before the dot in the file name
        n.append(int(t.split('L')[1]))   # Extract the numeric part after 'L'

# Sort the loci based on the numeric part of the name
sor = sorted(n)
lista = []
for i in range(0, len(sor)):
    b = 'L' + str(sor[i]) + '.genepop'
    lista.append(b)

# Function to calculate the percentage of valid data (not '000000') for a locus
def calculate_valid_data_percentage(locus_data):
    total_count = len(locus_data)
    valid_count = sum(1 for value in locus_data if value != '000000')  # Count valid values different from '000000'
    return valid_count / total_count

# List to keep track of valid loci
valid_loci = []
valid_data_per_locus = []

# Iterate over all files and filter loci with valid data
for filename in lista:
    with open(os.path.join(folder_path, filename)) as file:
        lines = [line.strip() for line in file.readlines()]  # Read the locus data line by line
        
        # Calculate the percentage of valid data for the file (locus)
        valid_data_percentage = calculate_valid_data_percentage(lines)
        
        # Keep the locus only if at least the specified percentage of the data is valid
        if valid_data_percentage >= perc:
            valid_loci.append(filename.split('/')[-1].split('.')[0])  # Add the name of the valid locus
            valid_data_per_locus.append(lines)  # Add the data of the valid locus

# If there are no valid loci, terminate the script
if len(valid_loci) == 0:
    print("No valid loci found.")
    sys.exit()

# Transpose the data so that valid loci are adjacent (like columns)
merged_data = list(zip(*valid_data_per_locus))

# Open the output file for writing
with open(out, 'w') as writer:
    print("Insert title", file=writer)  # Write the title of the output file
    
    # Write the header only for valid loci
    print(','.join(valid_loci), file=writer)
    
    print('Pop', file=writer)  # Write 'Pop' to indicate the end of the header

    # Write the data of valid loci (now in columns)
    for row in merged_data:
        print(' '.join(row), file=writer)

print("Merging completed. Output saved to", out)
