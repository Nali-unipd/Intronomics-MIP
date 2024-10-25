#!/bin/bash

# Error handling function
handle_error() {
    echo "Error: $1"
    exit 1
}

# Check if Miniconda is installed
if ! command -v conda &> /dev/null; then
    echo "Miniconda not found. Installing Miniconda..."
    mkdir -p ~/miniconda3 || handle_error "Failed to create the Miniconda directory."
    
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh || handle_error "Failed to download Miniconda."
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 || handle_error "Miniconda installation failed."
    
    rm -rf ~/miniconda3/miniconda.sh || handle_error "Failed to remove the installation file."
    echo "export PATH=~/miniconda3/bin/:$PATH" >> ~/.bash_profile || handle_error "Failed to modify ~/.bash_profile."
    echo "Miniconda installed successfully."

else
    echo "Miniconda is already installed."
fi

# Create the Conda environment if it doesn't exist already
if ! conda env list | grep -q "MIPS"; then
    conda create --name MIPS python=3.8 pandas bioconda::bbmap bioconda::snakemake bioconda::flash2 bioconda::cutadapt -y || handle_error "Failed to create the MIPS environment."
else
    echo "The MIPS environment already exists."
fi

# Check if SeekDeep is installed
if ! command -v SeekDeep &> /dev/null; then
    echo "SeekDeep not found. Installing SeekDeep..."
    sudo apt-get update && sudo apt-get dist-upgrade -y || handle_error "System update failed."
    sudo apt-get -y autoremove || handle_error "Failed to remove unnecessary packages."
    
    sudo apt-get install -y build-essential software-properties-common libcurl4-openssl-dev git make || handle_error "Failed to install base packages."

    sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y || handle_error "Failed to add the PPA."
    sudo apt-get update && sudo apt-get install -y g++-10 || handle_error "Failed to install g++-10."
    
    cd ~ || handle_error "Failed to access the home directory."
    git clone https://github.com/bailey-lab/SeekDeep || handle_error "Failed to clone SeekDeep."
    cd SeekDeep || handle_error "Failed to access the SeekDeep directory."

    ./setup.py --libs cmake:3.7.2 --symlinkBin || handle_error "SeekDeep setup failed."
    echo "" >> ~/.profile 
    echo "# Add SeekDeep bin to your path" >> ~/.profile 
    echo "export PATH=\"$(pwd)/bin:\$PATH\"" >> ~/.profile || handle_error "Failed to modify ~/.profile."
    
    . ~/.profile || handle_error "Failed to reload ~/.profile."
    ./setup.py --addBashCompletion || handle_error "Bash completion setup failed."
    ./install.sh 7 || handle_error "SeekDeep installation failed."
else
    echo "SeekDeep is already installed."
fi

echo "Installation complete. Please run 'source ~/.bash_profile' to apply the changes to your PATH."
