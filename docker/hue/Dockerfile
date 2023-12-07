FROM gethue/hue:latest


USER root

RUN mv /etc/apt/sources.list.d/nodesource.list /etc/apt/sources.list.d/nodesource.list.disabled
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get  install -y \
    ca-certificates \
    libgnutls30 \
    netcat


RUN ./build/env/bin/pip install pyodbc 
RUN ./build/env/bin/pip install pymssql 

RUN mv /etc/apt/sources.list.d/nodesource.list.disabled /etc/apt/sources.list.d/nodesource.list

COPY ./entrypoint.sh .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]

CMD ["./startup.sh"]