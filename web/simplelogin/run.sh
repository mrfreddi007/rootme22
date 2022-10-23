#!/bin/bash

# Start all services
service mariadb start

# update root password to allow db usage
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'dec369de7fbce7b10e640d88315a1813'"

# Run sql init script
mysql -e "SOURCE /tmp/init.sql" -p'dec369de7fbce7b10e640d88315a1813';

node /var/app/app.js
tail -f /dev/null