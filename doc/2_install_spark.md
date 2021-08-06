
# Install Spark
```sh
wget https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
tar -xvf spark-3.1.2-bin-hadoop3.2.tgz 
sudo mv spark-3.1.2-bin-hadoop3.2 /opt/spark
```

vim ~/.bashrc
```bashrc

# Spark
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin
```


```sh
sudo cp /opt/spark/conf/spark-env.sh.template /opt/spark/conf/spark-env.sh

```

sudo vim /opt/spark/conf/spark-env.sh
```sh
SPARK_MASTER_HOST='192.168.2.100'
```
