#!/bin/bash

echo "Enter wordpress password: "
read password

yum install -y httpd
service sshd start
yum install -y mysql mysql-server
chkconfig mysqld on
service mysqld start

# Make sure that NOBODY can access the server without a password
mysql -e "UPDATE mysql.user SET Password = PASSWORD('$password') WHERE User = 'root'"
# Kill the anonymous users
mysql -e "DROP USER ''@'localhost'"
# Because our hostname varies we'll use some Bash magic here.
mysql -e "DROP USER ''@'$(hostname)'"
# Kill off the demo database
mysql -e "DROP DATABASE test"
# Make our changes take effect
mysql -e "FLUSH PRIVILEGES"
# Any subsequent tries to run queries this way will get access denied because lack of usr/pwd param

yum install -y php php-mysql php-gd php-pear php-pgsql
yum -y install automake php-devel libtool openssl-devel gcc php-mysql php-gd php-imap php-ldap php-odbc php-pear php-xml php-xmlprc gcc php-devel php-pear php-common php-mbstring
service httpd restart

mysql -u root -p$password <<MY_QUERY
CREATE DATABASE wordpress;
CREATE USER wordpressuse@localhost IDENTIFIED BY '$password';
GRANT ALL PRIVILEGES ON wordpress.* to wordpressuse@localhost identified by '$password';
FLUSH PRIVILEGES;
MY_QUERY


cd /var/www/html/
yum install -y wget
wget http://wordpress.org/latest.tar.gz
tar -xzvf latest.tar.gz
mv wordpress/* .
chown -R apache:apache /var/www/html/

service iptables stop;
