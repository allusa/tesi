
hadoop dfs -copyFromLocal matriu0.csv /user/aleix/matriu0.csv



hadoop dfs -rmr /user/aleix/matriu

hadoop jar /usr/lib/hadoop/contrib/streaming/hadoop-streaming*.jar -file rrdoop.py -mapper 'rrdoop.py -map' -reducer 'rrdoop.py -reduce' -input /user/aleix/matriu0.csv -output /user/aleix/matriu



hadoop dfs -cat /user/aleix/matriu/part-00000

hadoop dfs -copyToLocal /user/aleix/matriu/part-00000 mtsdb0.csv
