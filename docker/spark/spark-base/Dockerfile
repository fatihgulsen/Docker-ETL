FROM hive-base:latest
LABEL maintainer="FatihGulsen"

# Defining useful environment variables
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3.3.6
ENV SCALA_VERSION=2.12.18
ENV SCALA_HOME=/usr/share/scala
ENV SPARK_HOME=/usr/local/spark
ENV SBT_VERSION=1.9.7
ENV PYTHONHASHSEED=1
ENV SPARK_EXECUTOR_MEMORY=8g
ENV SPARK_DRIVER_MEMORY=8g
ENV SPARK_WORKER_MEMORY=8g
ENV SPARK_DAEMON_MEMORY=8g
ENV PATH $SPARK_HOME/bin/:$PATH
ENV TZ=Europe/Istanbul
RUN date
# Upgrade and install some tools and dependencies
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq \
    netcat \
    apt-utils \
    curl \
    vim \
    ssh \
    net-tools \
    ca-certificates \
    jq \
    wget \
    software-properties-common

# Installing Scala
WORKDIR /tmp

RUN wget --no-verbose "https://downloads.typesafe.com/scala/${SCALA_VERSION}/scala-${SCALA_VERSION}.tgz" && \
    tar zxf scala-${SCALA_VERSION}.tgz && \
    mkdir ${SCALA_HOME} && \
    rm "scala-${SCALA_VERSION}/bin/"*.bat && \
    mv "scala-${SCALA_VERSION}/bin" "scala-${SCALA_VERSION}/lib" "${SCALA_HOME}" && \
    ln -s "${SCALA_HOME}/bin/*" "/usr/bin/" && \
    rm -rf *

# Installing SBT
RUN export PATH="/usr/local/sbt/bin:$PATH" && \ 
    apt-get update && \
    apt-get install ca-certificates wget tar && \
    mkdir -p "/usr/local/sbt" && \
    wget -qO - --no-check-certificate "https://github.com/sbt/sbt/releases/download/v${SBT_VERSION}/sbt-${SBT_VERSION}.tgz" | tar xz -C /usr/local/sbt --strip-components=1 && \
    sbt sbtVersion

# Adding dependencies for PySpark
RUN apt-get install -y curl python3.7 python3.7-dev python3.7-distutils
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
RUN update-alternatives --set python /usr/bin/python3.7
RUN curl https://bootstrap.pypa.io/get-pip.py | python3
RUN pip install --upgrade "pip==20.2.4"
RUN apt-get install -yqq python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy

#RUN apt-get install -yqq python3 python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy && \
#    update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1 && \
#    curl https://bootstrap.pypa.io/get-pip.py | python3

# Installing Spark
WORKDIR ${SPARK_HOME}

RUN wget --no-verbose https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar zxf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \ 
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/* . && \
    rm -rf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    rm -rf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}

# Use Spark with Hive
RUN cp ${HIVE_HOME}/conf/hive-site.xml $SPARK_HOME/conf

RUN apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /tmp/* /var/tmp/*

RUN curl -o hadoop-aws-3.3.6.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-3.3.6.jar && \
    curl -o aws-java-sdk-bundle-1.12.99.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.99/aws-java-sdk-bundle-1.12.99.jar && \
    curl -o postgresql-42.3.5.jar https://jdbc.postgresql.org/download/postgresql-42.3.5.jar && \
    curl -o mssql-jdbc-12.4.2.jre11.jar https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/12.4.2.jre11/mssql-jdbc-12.4.2.jre11.jar && \
    curl -o mssql-jdbc-12.4.2.jre8.jar https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/12.4.2.jre8/mssql-jdbc-12.4.2.jre8.jar && \
    curl -o delta-core_2.12-2.4.0.jar https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar && \
    mv aws-java-sdk-bundle-1.12.99.jar hadoop-aws-3.3.6.jar postgresql-42.3.5.jar mssql-jdbc-12.4.2.jre11.jar mssql-jdbc-12.4.2.jre8.jar delta-core_2.12-2.4.0.jar ${SPARK_HOME}/jars/ && \
    apt-get clean
RUN mkdir -p ${SPARK_HOME}/history

WORKDIR /

COPY ./entrypoint.sh .
COPY ./spark-defaults.conf ${SPARK_HOME}/conf/spark-defaults.conf

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]