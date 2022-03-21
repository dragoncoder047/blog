#! /bin/bash
cd /tmp
wget https://www.python.org/ftp/python/$1/Python-$1.tar.xz
tar xf Python-$1.tar.xz
cd Python-$1
./configure
make
sudo make install
cd ..
sudo rm -r Python-$1
rm Python-$1.tar.xz
. ~/.bashrc
python3 --version