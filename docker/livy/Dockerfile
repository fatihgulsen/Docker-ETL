FROM bitnami/spark:3.4.2

USER root
ENV LIVY_HOME /opt/bitnami/livy
WORKDIR /opt/bitnami/
RUN apt-get clean && apt-get update && apt-get install -y curl
RUN install_packages unzip \
    && curl "https://downloads.apache.org/incubator/livy/0.8.0-incubating/apache-livy-0.8.0-incubating_2.11-bin.zip" -O \
    && unzip "apache-livy-0.8.0-incubating_2.11-bin" \
    && rm -rf "apache-livy-0.8.0-incubating_2.11-bin.zip" \
    && mv "apache-livy-0.8.0-incubating_2.11-bin" $LIVY_HOME \
    && mkdir $LIVY_HOME/logs \
    && chown -R 1001:1001 $LIVY_HOME

USER 1001