#!/bin/bash
dirs=("ftp_client" "web_client" "web_server" "mysql_client" "mongo_client" "wp_client" "yt_client", "mqtt_client")
names=("tg_ftp_client" "tg_web_client" "tg_web_server" "tg_sql_client" "tg_mongo_client" "tg_wp_client" "tg_yt_client", "tg_mqtt_client")
for i in {0..5}; do
  docker build -t autofunbot/${names[$i]} ${dirs[$i]}
  docker push autofunbot/${names[$i]}
done