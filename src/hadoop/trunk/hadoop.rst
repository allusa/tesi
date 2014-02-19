======
Hadoop
======


http://cloudfront.blogspot.in/2012/07/how-to-configure-hadoop.html
http://digitallibraryworld.com/?p=256
https://beagle.whoi.edu/redmine/projects/ibt/wiki/Installing_Hadoop_on_Debian





Instal·lació
------------


Instal·lat des de cloudera. A **/etc/apt/sources.list**::

 deb http://archive.cloudera.com/debian/ squeeze-cdh3u6 contrib




* **hadoop version** mostra la versió


* **mkdir /home/hdfs**
* **/home/hdfs/{name,data,tmp}**
* **chown -R hdfs.hdfs /home/hdfs/**
* **chmod -R 755 /home/hdfs/**



* Adreça del NameNode (és el node principal que els altres han de
  conèixer) a **/etc/hadoop/conf/core-site.xml**::

   <configuration>
     <property>
       <name>fs.default.name</name>
       <value>hdfs://localhost:9000</value>
     </property>
     <property>
      <name>hadoop.tmp.dir</name>
      <value>/home/hadoop/hdfs/tmp</value>
     </property>
   </configuration>


* **/etc/hadoop/conf/hdfs-site.xml**::

   <configuration>
     <property>
      <name>dfs.name.dir</name>
      <value>/home/hadoop/hdfs/name</value>
     </property>
     <property>
      <name>dfs.data.dir</name>
      <value>/home/hadoop/hdfs/data</value>
     </property>
     <property>
      <name>dfs.replication</name>
      <value>1</value>
     </property>
   </configuration>

* **/etc/hadoop/conf/mapred-site.xml**::

   <configuration>
    <property>
      <name>mapred.job.tracker</name>
      <value>localhost:9001</value>
     </property>
   </configuration>



* **sudo -u hdfs hadoop namenode -format**

* **service hadoop-0.20-namenode start**
* log a */usr/lib/hadoop-0.20/logs/hadoop-hadoop-namenode-puput.log*

* **service hadoop-0.20-datanode start**


* Visitar http://localhost:50070/


* **mkdir /home/hadoop/hdfs/tmp/mapred**
* **chown mapred.hadoop  /home/hadoop/hdfs/tmp/mapred**
* **chmod g+w /home/hadoop/hdfs/tmp/mapred/**
* **service hadoop-0.20-jobtracker start** -> failed
* log *Failed to operate on mapred.system.dir (hdfs://localhost:9000/home/hadoop/hdfs/tmp/mapred/system) because of permissions.* 
* 
* **sudo -u hdfs hadoop fs -chmod 775 /**
* **sudo -u hdfs hadoop dfs -chown hdfs:hadoop /**
* **service hadoop-0.20-jobtracker start**

* Visitar http://localhost:50030/

* **service hadoop-0.20-tasktracker start**



Pels usuaris
------------

* **sudo -u hdfs hadoop dfs -ls /**

* **sudo -u hdfs hadoop dfs -chmod 777 /home/hadoop/hdfs/tmp/**
* **sudo -u hdfs hadoop dfs -mkdir /user/aleix**
* ** sudo -u hdfs hadoop dfs -chown aleix:aleix /user/aleix**
* **sudo chmod 777  /home/hadoop/hdfs/tmp/**
* **sudo -u hdfs hadoop dfs -chmod 777 /home/hadoop/hdfs/tmp/mapred/**


Com a aleix:

* **hadoop dfs -copyFromLocal cpl_svn/sistemes/ /user/aleix/prova**
* **hadoop jar /usr/lib/hadoop/hadoop-examples.jar wordcount /user/aleix/prova /user/aleix/prova-output**
* **hadoop dfs -ls /user/aleix/prova-output**
* **hadoop fs -cat /user/aleix/prova-output/part-r-00000**

Codi font de l'exemple a /usr/share/doc/hadoop-0.20/examples/src/


http://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/
http://www.michael-noll.com/tutorials/running-hadoop-on-ubuntu-linux-multi-node-cluster/




* hadoop jar /usr/lib/hadoop/contrib/streaming/hadoop-streaming*.jar -file hadoop/compta-map.py -mapper hadoop/compta-map.py -file hadoop/compta-reduce.py -reducer hadoop/compta-reduce.py -input /user/aleix/prova -output /user/aleix/prova-output2
