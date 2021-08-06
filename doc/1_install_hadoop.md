# Install Hadoop
if you are in your user, change to hadoop user.

```sh
su hadoop
```

```sh
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz

tar -xvf hadoop-3.3.0.tar.gz
sudo mv hadoop-3.3.0 /opt/hadoop

sudo mkdir /opt/hadoop/dfs
sudo mkdir /opt/hadoop/dfs/data
sudo mkdir /opt/hadoop/dfs/namespace_logs

sudo chmod 777 -R /opt/hadoop/dfs/
sudo chown hadoop:hadoop -R /opt/hadoop
```

# Config

vim /opt/hadoop/etc/hadoop/core-site.xml
```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://0.0.0.0:9000</value>
  </property>
</configuration>
```

vim /opt/hadoop/etc/hadoop/hdfs-site.xml
```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
  <property>
    <name>dfs.namenode.name.dir</name>
    <value>/opt/hadoop/dfs/namespace_logs</value>
  </property>
  <property>
    <name>dfs.datanode.data.dir</name>
    <value>/opt/hadoop/dfs/data</value>
  </property>
</configuration>
```


vim /opt/hadoop/etc/hadoop/hadoop-env.sh
```sh
export JAVA_HOME=/opt/jdk
```

vim ~/.bashrc

```bashrc
# Hadoop
export HADOOP_HOME=/opt/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_COMMOM_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

source ~/.bashrc


# Format HDFS
```sh
hdfs namenode -format

start-dfs.sh

hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/hadoop

# Is not recommended to allow rwx for everyone, only for didatical proposals
sudo chmod -R 777 /opt/hadoop/dfs/

hdfs dfs -mkdir /user/[you user]
hdfs dfs -chown [you user] /user/[you user]

hdfs dfs -mkdir /user/[you user]/dataset
hdfs dfs -chown [you user] /user/[you user]/dataset
```


http://localhost:9870/

check if have datanote in Datanode usage histogram


# Config Yarn (Optional)


vim /opt/hadoop/etc/hadoop/mapred-site.xml
```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>mapreduce.application.classpath</name>
    <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
  </property>
</configuration>
```

vim /opt/hadoop/etc/hadoop/yarn-site.xml
```xml
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.env-whitelist</name>
    <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
  </property>
</configuration>
```

```
su hadoop

start-dfs.sh
start-yarn.sh

```

http://localhost:8088/


# Install Spark

* [2 - Install Spark](./2_install_spark.md)
