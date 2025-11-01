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

# sagemath installer
if apt show sagemath 2>/dev/null | grep -q "Package: sagemath"; then
    echo "Installing sagemath via package manager"
    $PKG_INSTALL sagemath

elif ! command -v conda >/dev/null 2>&1; then
    echo "Installing sagemath via conda"
    curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda
    rm miniconda.sh
    export PATH="$HOME/miniconda/bin:$PATH"
    $HOME/miniconda/bin/conda init bash || true
    source ~/.bashrc || true
    eval "$(conda shell.bash hook)"
    # shell reloaded to make sure conda was initialised
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
    conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
    echo "Finished installing conda"
   conda config --add channels conda-forge || true
    conda config --add channels defaults || true
    conda config --set channel_priority flexible || true
    echo "Configuring sagemath"
    conda create -n sage-env -c conda-forge sage --yes --quiet
    eval "$(conda shell.bash hook)"
    conda activate sage-env
    echo "Configuration of sagemath complete"

elif command -v conda >/dev/null 2>&1; then
    echo "Installing sagemath via conda"
    conda config --add channels conda-forge || true
    conda config --add channels defaults || true
    conda config --set channel_priority flexible || true
    echo "Configuring sagemath"
    conda create -n sage-env -c conda-forge sage --yes --quiet
    echo "Configuration of sagemath complete"
    eval "$(conda shell.bash hook)"
    conda activate sage-env
fi

# pip3 install
echo "Running pip3 install..."
pip3 install --quiet --no-input -r requirements.txt
echo "Finished running pip3 install"

# the meat of the matter
clear
eval "$(conda shell.bash hook)"
conda activate sage-env
# now to run the line below on a machine that doesn't terminate the process due to lack of RAM
sage -python3 estimate.py
