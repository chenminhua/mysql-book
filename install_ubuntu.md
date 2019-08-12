https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04

```
apt update
apt install mysql-server
sudo mysql_secure_installation

# 即使你已经设置了root用户的password，你也不能从命令行用root pass登录
sudo mysql

> SELECT user,authentication_string,plugin,host FROM mysql.user;
> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '1234qwer';
# 1234qwer是密码

> FLUSH PRIVILEGES;
> SELECT user,authentication_string,plugin,host FROM mysql.user;
> exit;

现在就可以用密码1234qwer来登录root用户了。
```

## create a user

```
> CREATE USER 'minhua'@'localhost' IDENTIFIED BY '1234qwer';
> GRANT ALL PRIVILEGES ON *.* TO 'minhua'@'localhost'  WITH GRANT OPTION;

> exit

mysql -u minhua -p
```
