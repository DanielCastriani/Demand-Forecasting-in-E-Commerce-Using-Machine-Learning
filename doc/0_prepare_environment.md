# Install Java

https://www.oracle.com/br/java/technologies/javase/javase-jdk8-downloads.html

```sh
tar -xzf jdk-8u301-linux-x64.tar.gz
sudo mv jdk1.8.0_301/ /opt/jdk
```

# Create Hadoop user

```sh
sudo adduser hadoop
sudo usermod -aG sudo hadoop
sudo usermod -aG [your user group] hadoop

su hadoop
mkdir ~/Downloads
cd ~/Downloads
```

# Install SSH Server
```sh
sudo apt install openssh-server
sudo systemctl enable sshd
sudo systemctl start sshd
sudo systemctl status sshd

ssh-keygen -t rsa # password need to be blank
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
sudo chmod 0600 ~/.ssh/authorized_keys

```

sudo vim /etc/ssh/sshd_config
```txt
Port 22
AddressFamily any
ListenAddress 0.0.0.0
```

```sh
sudo systemctl restart sshd
sudo systemctl status sshd
```


sudo vim ~/.bashrc
```bashrc
# Java
export JAVA_HOME=/opt/jdk
export PATH=$PATH:$JAVA_HOME/bin
```


# Hosts

sudo vim /etc/hosts

```txt
# add
192.168.2.[machine ip]   hadoop
``` 


# Install Hadoop

[1 - Install Hadoop](./1_install_hadoop.md)


After install all tools, you need to add the paths to the .bashrc file of your main user

```bashrc
# Java
export JAVA_HOME=/opt/jdk
export PATH=$PATH:$JAVA_HOME/bin

# Hadoop
export HADOOP_HOME=/opt/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_COMMOM_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Spark
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin
```