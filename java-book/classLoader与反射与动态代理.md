# 类加载

类的加载指的是将类读入到内存中，将其放在 Jvm 的方法区内，然后在堆创建一个 java.lang.Class 对象，用来封装类在方法区内的数据结构。类的加载的最终产品是位于堆中的 Class 对象，Class 对象封装了类在方法区内的数据结构，并且向 Java 程序员提供了访问方法区内的数据结构的接口。

类加载器负责在运行时动态加载 java 类。

```java
// BootstrapLoader搜寻 System.getProperty("sun.boot.library.path”)中的类，
// ExtLoader搜寻 System.getProperty("java.ext.dirs”)中指定的类。
// AppClassLoader搜索 classpath, System.getProperty(“java.class.path”)
MyClassLoader.class.getClassLoader(); // AppClassLoader
Logging.class.getClassLoader(); // ExtClassLoader
ArrayList.class.getClassLoader(); // null (BootstrapClassLoader)

ClassLoader loader = Thread.currentThread().getContextClassLoader();
// sun.misc.Launcher$AppClassLoader@18b4aac2   应用类加载器
System.out.println(loader);
// sun.misc.Launcher$ExtClassLoader@610455d6 扩展类加载器
System.out.println(loader.getParent());
// Bootstrap ClassLoader 启动类加载器(用 C 语言实现，所以此处返回 null)
System.out.println(loader.getParent().getParent());

```

- AppClassLoader 从 classpath 里的文件 load。
- ExtClassLoader 加载核心 java 类的 extension 类。通常是 JAVA_HOME/lib/ext 下的类。
- BootstrapClassLoader 是 native 的，不是 java class。
- BootstrapClassLoader 负责加载 ClassLoader 这个类，加载 JDK 内部的类，尤其是 rt.jar 以及其他在 JAVA_HOME/jre/lib 下的核心库。
- 子 classloader 加载的类可见父 classloader 加载的类，反之不行。所以通过 AppClassLoader 加载的类可见 ExtClassLoader 加载的类，反之不行。

java.lang.ClassLoader.loadClass() 负责加载类定义。如果这个类还没 Load，会委托其父 ClassLoader 来加载，如果父的类加载器找不到这个类，子的类加载器再来加载，如果子的类加载器也不能加载这个类，就会抛出 NoClassDefFoundError 或者 ClassNotFoundException. 使用委派模型的目的是避免重复加载 Java 类型。

全盘负责，当一个类加载器负责加载某个 Class 时，该 Class 所依赖的和引用的其他 Class 也将由该类加载器负责载入，除非显示使用另外一个类加载器来载入

## Custom ClassLoader

可用于修改已有的字节码，weaving agents，动态创建类等等。比如在 jdbc 中，切换不同的 driver 就是通过动态类加载实现的。

```java
class CustomClassLoader extends ClassLoader {
    @Override
    public Class findClass(String name) throws ClassNotFoundException {
        byte[] b = loadClassFromFile(name);
        return defineClass(name, b, 0, b.length);
    }

    private byte[] loadClassFromFile(String fileName) {
        InputStream inputStream = getClass().getClassLoader().getResourceAsStream(
            fileName.replace('.', File.separatorChar) + ".class");
        byte[] buffer;
        ByteArrayOutputStream byteStream = new ByteArrayOutputStream();
        int nextValue = 0;
        try {
            while ( (nextValue = inputStream.read()) != -1 ) {
                byteStream.write(nextValue);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        buffer = byteStream.toByteArray();
        return buffer;
    }
}

// 核心在于对字节码文件的获取，如果是加密的字节码则需要在该类中对文件进行解密。
public class MyClassLoader extends ClassLoader {
    // 存放字节码文件的目录
    private final File bytecodeFileDirectory;
    public MyClassLoader(File bytecodeFileDirectory) {
        this.bytecodeFileDirectory = bytecodeFileDirectory;
    }
    // 请实现一个自定义的类加载器，将当前目录中的字节码文件加载成为Class对象
    // 提示，一般来说，要实现自定义的类加载器，你需要覆盖以下方法，完成：
    // 1.如果类名对应的字节码文件存在，则将它读取成为字节数组
    //   1.1 调用ClassLoader.defineClass()方法将字节数组转化为Class对象
    // 2.如果类名对应的字节码文件不存在，则抛出ClassNotFoundException
    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        byte[] classData = getByteArrayFromFile(name);
        if (classData == null) {
            throw new ClassNotFoundException();
        }
        return defineClass(name, classData, 0, classData.length);
    }
    byte[] getByteArrayFromFile(String className) throws ClassNotFoundException {
        ByteArrayOutputStream bos = new ByteArrayOutputStream();
        File file = new File(bytecodeFileDirectory, className + ".class");
        int len = 0;
        try {
            byte[] bufferSize = new byte[1024];
            FileInputStream fis = new FileInputStream(file);
            while ((len = fis.read(bufferSize)) != -1) {
                bos.write(bufferSize, 0, len);
            }
        } catch (FileNotFoundException e) {
            throw new ClassNotFoundException();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return bos.toByteArray();
    }
    public static void main(String[] args) throws Exception {
        File projectRoot = new File(System.getProperty("basedir", System.getProperty("user.dir")));
        MyClassLoader myClassLoader = new MyClassLoader(projectRoot);
        Class testClass = myClassLoader.loadClass("com.github.hcsp.MyTestClass");
        Object testClassInstance = testClass.getConstructor().newInstance();
        String message = (String) testClass.getMethod("sayHello").invoke(testClassInstance);
        System.out.println(message);
    }
}
```

```java
java.lang.ClassLoader
public Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {}
protected final Class<?> defineClass(String name, byte[] b, int off, int len) throws ClassFormatError
protected Class<?> findClass(String name) throws ClassNotFoundException
public final ClassLoader getParent()
public URL getResource(String name)

protected synchronized Class<?> loadClass(String name, boolean resolve)throws ClassNotFoundException {
    // 首先判断该类型是否已经被加载
    Class c = findLoadedClass(name);
    if (c == null) {
        //如果没有被加载，就委托给父类加载或者委派给启动类加载器加载
        try {
            if (parent != null) {
                //如果存在父类加载器，就委派给父类加载器加载
                c = parent.loadClass(name, false);
            } else {
                //如果不存在父类加载器，就检查是否是由启动类加载器加载的类，通过调用本地方法native Class findBootstrapClass(String name)
                c = findBootstrapClass0(name);
            }
        } catch (ClassNotFoundException e) {
                //如果父类加载器和启动类加载器都不能完成加载任务，才调用自身的加载功能
                c = findClass(name);
            }
        }
    if (resolve) {
        resolveClass(c);
    }
    return c;
}
```

- 类加载过程分为三个步骤：加载、链接、初始化。Loading, Linking, Initialization
- 加载阶段：将字节码从不同数据源读取到 JVM 中，并映射为 Class 对象。用户可以自定义类加载器来实现类加载过程。
- 链接阶段：又分为验证、准备、解析。这是类加载的关键步骤，比如创建静态变量并赋值，将常量池中的符号引用替换为直接引用等。
- 初始化阶段：真正执行类初始化逻辑，包括静态字段赋值操作，以及执行类定义中的静态初始化块内的逻辑。父类型的初始化逻辑优先于当前类型的逻辑执行。

通过指定名称，找到其二进制实现，这里往往就是自定义类加载器会“定制”的部分，例如，在特定数据源根据名字获取字节码，或者修改或生成字节码。
然后，创建 Class 对象，并完成类加载过程。二进制信息到 Class 对象的转换，通常就依赖 defineClass，我们无需自己实现，它是 final 方法。有了 Class 对象，后续完成加载过程就顺理成章了。

### 类加载的三种方式

- 应用启动时初始化加载。
- 通过 Class.forName()加载。
- 通过 ClassLoader.loadClass()加载。

Class.forName 和 ClassLoader.loadClass 的区别在于前者默认会执行类的 static 块等，而 loadClass 只负责把类加载到堆上。

```java
try {
    Class c = Class.forName("java.util.ArrayList");
    Object list = c.newInstance();
    c.getDeclaredMethod("add", Object.class).invoke(list, 100);
    System.out.println(c.getDeclaredMethod("get", int.class).invoke(list, 0));
} catch (Exception e) {
    e.printStackTrace();
}

```

### Class 对象

加载和连接过程的结果是一个 Class 对象。Class 对象可以和反射 API 一起实现对方法，域，构造方法等类成员的间接访问。

```java
Class c1 = String.class;
Class c2 = "hello".getClass();
```

##### 依赖注入中的类加载器 （spring 的玩法）

第一阶段由 application classLoader 加载主类以及其直接引用的类，但是由于我们使用了依赖注入，很多类都没有被引用到，因此也没有机会加载；因此第二阶段就由框架定制的 ClassLoader 按照配置文件加载类，并创建 Bean。

# 反射

**从 Class 对象中获取信息**

```java
Class c = Class.forName(args[0]); // 比如输入 java.util.ArrayList
System.out.println("包信息 package:" + c.getPackage());
System.out.println("类修饰符 modifier:" + c.getModifiers());
System.out.println("构造方法 constructor:");
Arrays.stream(c.getDeclaredConstructors()).forEach(System.out::println);
System.out.println("成员变量 fields:");
Arrays.stream(c.getDeclaredFields()).forEach(System.out::println);

String name = "hello";
Class stringClass = name.getClass();
System.out.println("类的名称:" + stringClass.getName());
System.out.println("是否为接口:" + stringClass.isInterface());
System.out.println("是否为基本类型:" + stringClass.isPrimitive());
System.out.println("是否为数组:" + stringClass.isArray());
System.out.println("父类名称:" + stringClass.getSuperclass().getName());
Class stringClass = String.class;

Class c = Class.forName(args[0]);   // 指定全限定名
ClassLoader loader = Thread.currentThread().getContextClassLoader();
// Class.forName() 加载类 默认会执行初始化块
Class.forName("Test2");
// Class.forName() 加载类 第二个参数 可以控制是否执行初始化块
Class.forName("Test2", false, loader);
class Test2 {
    static {
        System.out.println("静态初始化块执行了!");
    }
}
```

# 动态代理

**通过使用动态代理可以让调用者和实现者之间解耦**。比如进行 RPC 调用，框架内部的寻址、序列化、反序列化等，对于调用者往往是没有太大意义的。

基于 jdk： 实现原理就是反射，代码实现更简单。缺点是只能代理接口。实现方式：首先实现对应的 InvocationHandler; 然后以需要被代理的接口为纽带，为被调用目标构建代理对象。

基于 cglib ：可以处理没有接口的情况。实现方式： 创建目标类的子类。

```java
public class MyDynamicProxy {
    public static  void main (String[] args) {
        HelloImpl hello = new HelloImpl();
        MyInvocationHandler handler = new MyInvocationHandler(hello);
        // 构造代码实例
        Hello proxyHello = (Hello) Proxy.newProxyInstance(HelloImpl.class.getClassLoader(), HelloImpl.class.getInterfaces(), handler);
        // 调用代理方法
        proxyHello.sayHello();
    }
}
interface Hello {
    void sayHello();
}

class HelloImpl implements  Hello {
    @Override
    public void sayHello() {
        System.out.println("Hello World");
    }
}

class MyInvocationHandler implements InvocationHandler {
    private Object target;
    public MyInvocationHandler(Object target) {
        this.target = target;
    }
    @Override
    public Object invoke(Object proxy, Method method, Object[] args)
            throws Throwable {
        System.out.println("Invoking sayHello");
        Object result = method.invoke(target, args);
        return result;
    }
}
```

从 API 设计和实现的角度，这种实现仍然有局限性，因为它是以接口为中心的，相当于添加了一种对于被调用者没有太大意义的限制。我们实例化的是 Proxy 对象，而不是真正的被调用类型，这在实践中还是可能带来各种不便和能力退化。

如果被调用者没有实现接口，而我们还是希望利用动态代理机制，那么可以考虑其他方式。我们知道 Spring AOP 支持两种模式的动态代理，JDK Proxy 或者 cglib，如果我们选择 cglib 方式，你会发现对接口的依赖被克服了。

### 如何直接生成字节码然后交给类加载器去加载？

Java Compiler API, 字节码操纵工具 ASM, Javassist, cglib
classLoader 里面的 defineClass 方法就是用来从字节码转换到 Class 对象的。

```java
protected final Class<?> defineClass(String name, byte[] b, int off, int len, ProtectionDomain protectionDomain)
protected final Class<?> defineClass(String name, java.nio.ByteBuffer b, ProtectionDomain protectionDomain)
```

Jdk 提供的 defineClass 方法，最终都是本地代码实现的。

```java
static native Class<?> defineClass1(ClassLoader loader, String name, byte[] b, int off, int len, ProtectionDomain pd, String source);

static native Class<?> defineClass2(ClassLoader loader, String name, java.nio.ByteBuffer b, int off, int len, ProtectionDomain pd, String source);
```

JDK 动态代理中对应逻辑是实现在 ProxyBuilder 这个静态内部类中的。ProxyGenerator 生成字节码，并以 byte[]保存，然后通过调用 Unsafe 提供的 defineClass 入口。

```java
byte[] proxyClassFile = ProxyGenerator.generateProxyClass(proxyName, interfaces.toArray(EMPTY_CLASS_ARRAY), accessFlags);
try {
    Class<?> pc = UNSAFE.defineClass(proxyName, proxyClassFile,0, proxyClassFile.length, loader, null);
    reverseProxyCache.sub(pc).putIfAbsent(loader, Boolean.TRUE);
    return pc;
} catch (ClassFormatError e) {}
```

### 如何实现动态代理

从相对实用的角度思考一下，实现一个简单的动态代理，都要做什么？如何使用字节码操纵技术，走通这个过程呢？对于一个普通的 Java 动态代理，其实现过程可以简化成为：

- 一个基础接口作为被调类型（com.mycorp.HelloImpl）和代理类之间的统一入口，如 com.mycorp.Hello。
- 实现 InvocationHandler，对代理对象方法的调用，会被分派到其 invoke 方法来真正实现动作。
- 通过 Proxy 类，调用其 newProxyInstance 方法，生成一个实现了相应基础接口的代理类实例。
