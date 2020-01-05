#Instll Python3 - makes working with Ukrainian letters easier than w/Python2
sudo yum install gcc openssl-devel bzip2-devel libffi-devel;
cd /opt;
sudo wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz;
tar xzf Python-3.8.0.tgz;
cd Python-3.8.0;
sudo ./configure --enable-optimizations;
sudo make altinstall;
sudo rm /opt/Python-3.8.0.tgz;

