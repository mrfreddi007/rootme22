FROM debian:latest

# Init
RUN apt -y -qq update \
    && apt install -y -qq nodejs npm mariadb-server;

# Copy necessary files
COPY web/ /var/app/
COPY ./run.sh /run.sh
COPY ./config /tmp

# Install dependencies
WORKDIR /var/app/
RUN npm i;

# Start
CMD [ "/bin/bash", "/run.sh" ]