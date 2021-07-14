
# Install Java

https://www.oracle.com/br/java/technologies/javase/javase-jdk8-downloads.html

```sh
tar -xzf jdk-8u291-linux-x64.tar.gz
sudo mv jdk1.8.0_291/ /opt/jdk
```

# Install SSH Server
```sh
sudo apt install openssh-server
sudo systemctl enable sshd
sudo systemctl start sshd
sudo systemctl status sshd

ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
sudo chmod 0600 ~/.ssh/authorized_keys

```

code vim /etc/ssh/sshd_config
```txt
Port 22
AddressFamily any
ListenAddress 0.0.0.0
```

```sh
sudo systemctl restart sshd
sudo systemctl status sshd
```


sudo code ~/.bashrc
```bashrc
# Java
export JAVA_HOME=/opt/jdk
export PATH=$PATH:$JAVA_HOME/bin
```

# Create Hadoop user

```sh
sudo adduser hadoop
sudo usermod -aG sudo hadoop
sudo usermod -aG [your user group] hadoop
su hadoop
cd ~/Downloads

su hadoop
```

# Install Hadoop

[1 - Install Hadoop](./1_install_hadoop.md)