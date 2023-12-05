FROM gethue/hue:latest


USER root

RUN mv /etc/apt/sources.list.d/nodesource.list /etc/apt/sources.list.d/nodesource.list.disabled
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get  install -y \
    ca-certificates \
    libgnutls30 \
    netcat

RUN pip3 install --upgrade cython && \
    pip3 install pyodbc && \
    pip3 install pymssql && \
    pip install pyodbc && \
    pip install pymssql

RUN mv /etc/apt/sources.list.d/nodesource.list.disabled /etc/apt/sources.list.d/nodesource.list

COPY ./entrypoint.sh .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

CMD ["./startup.sh"]