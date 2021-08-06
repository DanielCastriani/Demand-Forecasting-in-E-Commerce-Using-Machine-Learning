# Install cuda 11.0

```sh
# Add NVIDIA package repositories
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"
sudo apt-get update

wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb

sudo apt install ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
sudo apt-get update

# Install NVIDIA driver
sudo apt install nvidia-utils-470
# Reboot. Check that GPUs are visible using the command: nvidia-smi

wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/libnvinfer7_7.1.3-1+cuda11.0_amd64.deb
sudo apt install ./libnvinfer7_7.1.3-1+cuda11.0_amd64.deb
sudo apt-get update

# Install development and runtime libraries (~4GB)
sudo apt-get install --no-install-recommends \
    cuda-11-0 \
    libcudnn8=8.0.4.30-1+cuda11.0  \
    libcudnn8-dev=8.0.4.30-1+cuda11.0


# Install TensorRT. Requires that libcudnn8 is installed above.
sudo apt-get install -y --no-install-recommends libnvinfer7=7.1.3-1+cuda11.0 \
    libnvinfer-dev=7.1.3-1+cuda11.0 \
    libnvinfer-plugin7=7.1.3-1+cuda11.0
```


Add in .bashrc
vim ~/.bashrc
```
# Cuda
export CUDA_HOME=/usr/local/cuda/cuda-11.0
export PATH=$PATH:$CUDA_HOME/bin
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

```




In python with tensorflow and tensorflow-gpu 2.5r, run the python code

```py
import tensorflow as tf
tf.test.is_gpu_available()
```

if show the folowing message, you will need to create a soft link to libcusolver.so.11

```
Could not load dynamic library 'libcusolver.so.11'; dlerror: libcusolver.so.11: cannot open shared object file: No such file or directory
...
False
```

## Fix libcusolver.so.11 Error

check if have libcusolver.so.10 and libcusolver.so.11
```
ll /usr/local/cuda-11.0/lib64/ | grep libcusolver.so
```

if have only libcusolver.so.10, run the script below
```sh
sudo ln -s /usr/local/cuda-11.0/lib64/libcusolver.so.10 /usr/local/cuda-11.0/lib64/libcusolver.so.11

ll /usr/local/cuda-11.0/lib64/ | grep libcusolver.so
```

## change default cuda to 11
```sh
ll /usr/local | grep cuda
ll /etc/alternatives/ | grep cuda


sudo ln -s /usr/local/cuda-11.0/ /etc/alternatives/cuda
sudo ln -s /usr/local/cuda-11.0  /usr/local/cuda 
```




