
hadoop dfs -copyFromLocal matriu0.csv /user/aleix/matriu0.csv



hadoop dfs -rmr /user/aleix/matriu

hadoop jar /usr/lib/hadoop/contrib/streaming/hadoop-streaming*.jar -file rrdoop.py -mapper 'rrdoop.py -map' -reducer 'rrdoop.py -reduce' -input /user/aleix/matriu0.csv -output /user/aleix/matriu



hadoop dfs -cat /user/aleix/matriu/part-00000

hadoop dfs -copyToLocal /user/aleix/matriu/part-00000 mtsdb0.csv







experiment amb matriu0.csv
--------------------------

* python

time cat matriu0.csv | ./rrdoop.py -map | sort -k1,1 | ./rrdoop.py -reduce > provant.csv::

 real	0m21.639s
 user	0m21.513s
 sys	0m0.864s


* hadoop

time hadoop jar /usr/lib/hadoop/contrib/streaming/hadoop-streaming*.jar -file rrdoop.py -mapper 'rrdoop.py -map' -reducer 'rrdoop.py -reduce' -input /user/aleix/matriu0.csv -output /user/aleix/matriu::

 real	0m28.314s
 user	0m1.640s
 sys	0m0.152s
