# Stream
参考 stream-handbook

```js
const server = http.createServer((req, res) => {
  const stream = fs.createReadStream('path.txt');
  // stream.pipe(res);
  stream.pipe(oppressor(req)).pipe(res);
})
```
## readable streams
可以生产数据的stream

```js
const Readable = require('stream').Readable;
var rs = new Readable;
rs.push('foo ');
rs.push('bar\n');
rs.push(null);
rs.pipe(process.stdout);
```

可以使用_read方法来按需push数据

```js
rs._read = () => {
  rs.push(String.fromCharCode(c++));
  if (c > 'z'.charCodeAt(0)) rs.push(null);
}
```

消费readable

```js
// process.stdin是一个readable stream,当stdin有可读数据时，readable事件被触发。
process.stdin.on('readable', () => {
  const buf = process.stdin.read();
  console.dir(buf);
});
```

## writable streams
只能 pipe to 不能 pipe from

```js
const Writable = require('stream').Writable;
const ws = Writable();
// chunk表示写入的数据,enc表示编码,next是回调函数，表示可以写入更多数据
ws._write = (chunk, enc, next) => {
  console.dir(chunk);
  next();
};
process.stdin.pipe(ws);

// 向一个writable写入数据的方法
process.stdout.write('foo bar\n');
// 告诉writable写入数据结束
process.stdout.end('bbb\n');
```

## transform stream
流的中间部分

## duplex流
双工流，可读可写

## classic流
Classic readable流只是一个事件发射器，当有数据消耗者出现时发射data事件，当输出数据完毕时发射end事件。

我们可以同构检查stream.readable来检查一个classic流对象是否可读。

为了从一个classic readable流中读取数据，你可以注册data和end监听器。

```js
process.stdin.on('data', function (buf) {
    console.log(buf);
});
process.stdin.on('end', function () {
    console.log('__END__');
});
```

# Buffer
http://javascript.ruanyifeng.com/nodejs/buffer.html

```js
const bytes = new Buffer(256);
for (var i = 0; i < bytes.length; i++) {
  bytes[i] = i;
}
var more = new Buffer(4);
bytes.copy(more, 0, 4, 8);
```

## 构造buffer

```js
var hello = new Buffer(5);

// 参数是数组，数组成员必须是整数值
var hello = new Buffer([0x48, 0x65, 0x6c, 0x6c, 0x6f]);
hello.toString() // 'Hello'

// 参数是字符串（默认为utf8编码）
var hello = new Buffer('Hello');
hello.length // 5
hello.toString() // "Hello"

// 参数是字符串（不省略编码）
var hello = new Buffer('Hello', 'utf8');

// 参数是另一个Buffer实例，等同于拷贝后者
var hello1 = new Buffer('Hello');
var hello2 = new Buffer(hello1);
```

## 类方法

```js
Buffer.isEncoding('utf8')
Buffer.isBuffer(buff)
Buffer.byteLength('hello', 'utf8')   // 5

var i1 = new Buffer('Hello');
var i2 = new Buffer(' ');
var i3 = new Buffer('World');
Buffer.concat([i1, i2, i3]).toString()  // 合并buffer  'Hello World'
```

## 实例属性

```js
buf = new Buffer(1234);
buf.length // 1234
```

## 实例方法

```js
buf.write('He');
var chunk = buf.slice(5, 9);
buff.toString();
```


