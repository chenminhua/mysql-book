## java 提供了哪些 io 方式？

- BIO, NIO, AIO
- java.io,基于流模型，提供了 File 抽象，输入输出流等等。同步阻塞。
- java.nio,提供了 Channel, Selector, Buffer 等抽象。
- java.nio 支持多路复用，同步非阻塞 IO 程序。
- JAVA7 引入了异步非阻塞 IO 方式（AIO），异步 IO 基于事件和回调机制。

异步往往和回调联系在一起。

```java
File

RandomAccessFile

InputStream: FileInputStream, BufferInputStream, ByteArrayInputStream, ObjectInputStream, PiepInputStream...

OutputStream: FileOutputStream, BufferOutputStream, ByteArrayOutputStream, ObjectOutputStream, PiepOutputStream...

Reader: InputStreamReader, FileReader, BufferedReader, PipeReader...

Writer: OutputStreamWriter, FileWriter, BufferedWriter, PipedWriter...
```

- InputStream, OutputStream 是用来读取或写入字节的，如操作图片。
- Reader, Writer 则是操作字符的，适用于从文件读取或写入文本信息。
- BufferedOutputStream 等带缓冲的实现，可避免频繁的磁盘读写，提高 IO 效率。

## NIO

- Buffer 是高效的数据容器。
- Channel 类似 Linux 上的文件描述符，用来支持批量 IO 的操作。
- Selector 是实现多路复用的基础，可以检测到注册在 selector 上的多个 channel 中，是否有 channel 处于就绪状态，进而实现了单线程对多 channel 的高效管理。Linux 上的 Selector 依赖于 epoll.

File 或者 Socket 是比较高层次的抽象，而 Channel 则是更加操作系统底层的一种抽象，这也使得 NIO 得以充分利用现代操作系统底层机制，获得特定场景的性能优化，例如，DMA（Direct Memory Access）等。不同层次的抽象是相互关联的，我们可以通过 Socket 获取 Channel，反之亦然。

```java

public class DemoServer extends Thread {
    private ServerSocket serverSocket;

    public int getPort() {
        return  serverSocket.getLocalPort();
    }

    public void run() {
        try {
            serverSocket = new ServerSocket(0);
            executor = Executors.newFixedThreadPool(8);
            while (true) {
                Socket socket = serverSocket.accept();
                RequestHandler requestHandler = new RequestHandler(socket);
                executor.execute(requestHandler);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (serverSocket != null) {
                try {
                    serverSocket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                ;
            }
        }
    }

    public static void main(String[] args) throws IOException {
        DemoServer server = new DemoServer();
        server.start();
        try (Socket client = new Socket(InetAddress.getLocalHost(), server.getPort())) {
            BufferedReader bufferedReader = new BufferedReader(new                   InputStreamReader(client.getInputStream()));
            bufferedReader.lines().forEach(s -> System.out.println(s));
        }
    }
 }
// 简化实现，不做读取，直接发送字符串
class RequestHandler extends Thread {
    private Socket socket;
    RequestHandler(Socket socket) {
        this.socket = socket;
    }
    @Override
    public void run() {
        try (PrintWriter out = new PrintWriter(socket.getOutputStream());) {
            out.println("Hello world!");
            out.flush();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

NIO 版本

```java

public class NIOServer extends Thread {
    public void run() {
        try (Selector selector = Selector.open();
            ServerSocketChannel serverSocket = ServerSocketChannel.open();) {// 创建Selector和Channel
            serverSocket.bind(new InetSocketAddress(InetAddress.getLocalHost(), 8888));
            serverSocket.configureBlocking(false);
            // 注册到Selector，并说明关注点
            serverSocket.register(selector, SelectionKey.OP_ACCEPT);
            while (true) {
                selector.select();// 阻塞等待就绪的Channel，这是关键点之一
                Set<SelectionKey> selectedKeys = selector.selectedKeys();
                Iterator<SelectionKey> iter = selectedKeys.iterator();
                while (iter.hasNext()) {
                    SelectionKey key = iter.next();
                    // 生产系统中一般会额外进行就绪状态检查
                    sayHelloWorld((ServerSocketChannel) key.channel());
                    iter.remove();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    private void sayHelloWorld(ServerSocketChannel server) throws IOException {
        try (SocketChannel client = server.accept();) {          client.write(Charset.defaultCharset().encode("Hello world!"));
        }
    }
   // 省略了与前面类似的main
}
```

- 通过 Selector.open()创建一个 Selector，作为类似调度员的角色。
- 然后创建 ServerSocketChannel，向 Selector 注册并指定 SelectionKey.OP_ACCEPT，表明其关注新的连接。
- Selector 阻塞在 select 操作，当有 Channel 接入请求，就会被唤醒。
- 通过 SocketChannel 和 Buffer 进行数据操作

### AIO

```java

AsynchronousServerSocketChannel serverSock =        AsynchronousServerSocketChannel.open().bind(sockAddr);
serverSock.accept(serverSock, new CompletionHandler<>() { //为异步操作指定CompletionHandler回调函数
    @Override
    public void completed(AsynchronousSocketChannel sockChannel, AsynchronousServerSocketChannel serverSock) {
        serverSock.accept(serverSock, this);
        // 另外一个 write（sock，CompletionHandler{}）
        sayHelloWorld(sockChannel, Charset.defaultCharset().encode
                ("Hello World!"));
    }
  // 省略其他路径处理方法...
});
```

### 文件拷贝

```java
public static void copyFileByStream(File source, File dest) throws
        IOException {
    try (InputStream is = new FileInputStream(source);
         OutputStream os = new FileOutputStream(dest);){
        byte[] buffer = new byte[1024];
        int length;
        while ((length = is.read(buffer)) > 0) {
            os.write(buffer, 0, length);
        }
    }
}

public static void copyFileByChannel(File source, File dest) throws
        IOException {
    try (FileChannel sourceChannel = new FileInputStream(source)
            .getChannel();
         FileChannel targetChannel = new FileOutputStream(dest).getChannel
                 ();){
        for (long count = sourceChannel.size() ;count>0 ;) {
            long transferred = sourceChannel.transferTo(
                    sourceChannel.position(), count, targetChannel);            sourceChannel.position(sourceChannel.position() + transferred);
            count -= transferred;
        }
    }
}
```

对于 Copy 的效率，这个其实与操作系统和配置等情况相关，总体上来说，NIO transferTo/From 的方式可能更快，因为它更能利用现代操作系统底层机制，避免不必要拷贝和上下文切换。

- 在程序中，使用缓存等机制，合理减少 IO 次数。
- 使用 transferTo 等机制，减少上下文切换和额外 IO 操作。
- 尽量减少不必要的转换过程，比如编解码；对象序列化和反序列化，比如操作文本文件或者网络通信，如果不是过程中需要使用文本信息，可以考虑不要将二进制信息转换成字符串，直接传输二进制信息。

### NIO Buffer

Buffer 是 NIO 操作数据的基本工具，java 为每种原始数据类型都提供了相应的 buffer 实现。

```java
ByteBuffer, MappedByteBuffer
CharBuffer
DoubleBuffer
FloatBuffer
IntBuffer
LongBuffer
ShortBuffer
```

Buffer 基本属性

```java
capacity
position: 要操作的数据起始位置。
limit: 相当于操作的限额。在读取或者写入时，limit 的意义很明显是不一样的。
mark: 记录上一次position的位置，默认为0。
```

Buffer 用法

- 创建 ByteBuffer，capacity 是缓冲区大小，position 就是 0，limit 默认等于 capacity。
- 写入数据时，position 会升高，但不会超过 limit。
- 如果想把写入的数据读出来，需调用 flip 方法，将 limit 设为 position，position 设置为 0。
- 如果还想从头再读一遍，可以调用 rewind，让 limit 不变，position 再次设置为 0。

http://tutorials.jenkov.com/java-nio/buffers.html

### Direct Buffer 和垃圾收集

Direct Buffer 是堆外内存。在实际使用中 java 会尽量对 direct buffer 仅做本地 IO 操作。使用 Direct Buffer，我们需要清楚它对内存和 JVM 参数的影响。首先，因为它不在堆上，所以 Xmx 之类参数，其实并不能影响 Direct Buffer 等堆外成员所使用的内存额度，我们可以使用下面参数设置大小

```java
-XX:MaxDirectMemorySize=512M
```

### MappedByteBuffer
