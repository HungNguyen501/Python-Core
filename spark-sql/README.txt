===> Set header for query result
    Add the following line to the file "spark-3.1.2-bin-hadoop3.2\conf\spark-defaults.conf":
    spark.hadoop.hive.cli.print.header true

===> Create table using CSV

    Table t1:
    CREATE TEMPORARY VIEW t1 USING csv  OPTIONS ( path 'tables/t1.csv', header true );
    CREATE TEMPORARY VIEW t1(name STRING, age INT, gender INT) USING csv  OPTIONS ( path 'tables/t1.csv', header true );

    Table t2:
    CREATE TEMPORARY VIEW t2 USING csv  OPTIONS ( path 'tables/t2.csv', header true );
    CREATE TEMPORARY VIEW t2(id string, time date, temperature int, humidity int, led int) USING csv  OPTIONS ( path 'tables/t2.csv', header true );