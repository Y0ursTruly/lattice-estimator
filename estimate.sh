# package manager selection
if command -v apt-get >/dev/null 2>&1; then
    PKG_INSTALL="sudo apt-get install -y"
    PKG_UPDATE="sudo apt-get update -y"
elif command -v yum >/dev/null 2>&1; then
    PKG_INSTALL="sudo yum install -y"
    PKG_UPDATE="sudo yum makecache"
elif command -v dnf >/dev/null 2>&1; then
    PKG_INSTALL="sudo dnf install -y"
    PKG_UPDATE="sudo dnf makecache"
elif command -v brew >/dev/null 2>&1; then
    PKG_INSTALL="brew install"
    PKG_UPDATE="brew update"
else
    echo "No supported package manager BRUH!" >&2
    exit 1
fi

# python3 installer
if ! command -v python3 >/dev/null 2>&1; then
    echo "Installing python3"
    $PKG_UPDATE
    $PKG_INSTALL python3 python3-pip
    echo "Finished installing python3"
fi

# conda installer
if ! command -v conda >/dev/null 2>&1; then
    echo "Installing conda"
    curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda
    rm miniconda.sh
    export PATH="$HOME/miniconda/bin:$PATH"
    $HOME/miniconda/bin/conda init bash || true
    source ~/.bashrc || true
    # shell reloaded to make sure conda was initialised
    echo "Finished installing conda"
fi

# conda config
conda config --add channels conda-forge || true
conda config --add channels defaults || true
conda config --set channel_priority flexible || true

# sage env
if ! conda env list | grep -q '^sage-env '; then
    echo "Configuring sagemath"
    conda create -n sage-env -c conda-forge sage -y
    echo "Configuration of sagemath complete"
fi

# pip3 install
echo "Running pip3 install..."
pip3 install --quiet --no-input -r requirements.txt
echo "Finished running pip3 install"

# random line that needs to run inside a script but not needed in a live shell
eval "$(conda shell.bash hook)"


# the meat of the matter
conda activate sage-env
clear
# now to run the line below on a machine that doesn't terminate the process due to lack of RAM
sage -python3 estimate.py
