FROM bitnami/spark:3.5
USER root
RUN apt-get clean && apt-get update && apt-get install -y curl wget vim nano
RUN curl -o hadoop-aws-3.3.6.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-3.3.6.jar && \
    curl -o aws-java-sdk-bundle-1.12.99.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.99/aws-java-sdk-bundle-1.12.99.jar && \
    curl -o postgresql-42.3.5.jar https://jdbc.postgresql.org/download/postgresql-42.3.5.jar && \
    curl -o mssql-jdbc-12.4.2.jre11.jar https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/12.4.2.jre11/mssql-jdbc-12.4.2.jre11.jar && \
    curl -o mssql-jdbc-12.4.2.jre8.jar https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/12.4.2.jre8/mssql-jdbc-12.4.2.jre8.jar && \
    curl -o delta-core_2.12-2.4.0.jar https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar && \
    mv aws-java-sdk-bundle-1.12.99.jar hadoop-aws-3.3.6.jar postgresql-42.3.5.jar mssql-jdbc-12.4.2.jre11.jar mssql-jdbc-12.4.2.jre8.jar delta-core_2.12-2.4.0.jar /opt/bitnami/spark/jars/ && \
    apt-get clean
RUN mkdir -p /opt/bitnami/spark/history
ENV TZ=Europe/Istanbul
RUN date
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
USER 1001