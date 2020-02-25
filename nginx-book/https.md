配置 HTTPS 要用到私钥 example.key 文件和 example.crt 证书文件，申请证书文件的时候要用到 example.csr 文件，OpenSSL 命令可以生成 example.key 文件和 example.csr 证书文件。

- CSR：Cerificate Signing Request，证书签署请求文件，里面包含申请者的 DN（Distinguished Name，标识名）和公钥信息，在第三方证书颁发机构签署证书的时候需要提供。证书颁发机构拿到 CSR 后使用其根证书私钥对证书进行加密并生成 CRT 证书文件，里面包含证书加密信息以及申请者的 DN 及公钥信息
- Key：证书申请者私钥文件，和证书里面的公钥配对使用，在 HTTPS 『握手』通讯过程需要使用私钥去解密客戶端发來的经过证书公钥加密的随机数信息，是 HTTPS 加密通讯过程非常重要的文件，在配置 HTTPS 的時候要用到
  使用 OpenSSl 命令可以在系统当前目录生成 example.key 和 example.csr 文件：
  openssl req -new -newkey rsa:2048 -sha256 -nodes -out example_com.csr -keyout example_com.key -subj "/C=CN/ST=ShangHai/L=ShangHai/O=Example Inc./OU=Web Security/CN=13.76.198.223"
- C：Country ，单位所在国家，为两位数的国家缩写，如： CN 就是中国
- ST 字段： State/Province ，单位所在州或省
- L 字段： Locality ，单位所在城市 / 或县区
- O 字段： Organization ，此网站的单位名称;
- OU 字段： Organization Unit，下属部门名称;也常常用于显示其他证书相关信息，如证书类型，证书产品名称或身份验证类型或验证内容等;
- CN 字段： Common Name ，网站的域名;
  https://www.zhihu.com/question/19578422

## let's encrypt

```
yum install certbot
certbot certonly --standalone -d video4us.top --register-unsafely-without-email
```

nginx 配置

```
server_name video4us.top;
listen 443;
ssl on;
ssl_certificate /etc/letsencrypt/live/video4us.top/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/video4us.top/privkey.pem;

```

- privkey.pem 私钥
- cert.pem 公钥
- chain.pem 给公钥签名的 CA 的证书。
- fullchain.pem: cert.pem + chain.pem

如何续期？如何加长时间？

certbot --nginx --nginx-server-root=/usr/local/nginx/conf/ -d video4us.top

```

```
