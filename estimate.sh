pip install -r requirements.txt
conda init
conda create -n sage-env -c conda-forge sage
conda activate sage-env
sage -python3 estimate.py