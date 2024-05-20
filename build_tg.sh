#!/bin/bash
dirs=("ftp_client" "web_client" "web_server" "mysql_client" "mongo_client", "wp_client")
names=("tg_ftp_client" "tg_web_client" "tg_web_server" "tg_sql_client" "tg_mongo_client", "tg_wp_client")
for i in {0..3}; do
  docker build -t autofunbot/${names[$i]} ${dirs[$i]}
  docker push autofunbot/${names[$i]}
done