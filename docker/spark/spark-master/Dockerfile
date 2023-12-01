FROM spark-base:latest

ENV SPARK_MASTER_PORT=7077
ENV SPARK_MASTER_UI_PORT=4040
ENV SPARK_MASTER_LOG_DIR=/var/logs/spark

COPY start-master.sh .

RUN chmod +x start-master.sh

EXPOSE 4040 
EXPOSE 7077 
EXPOSE 6066

CMD [ "./start-master.sh" ]