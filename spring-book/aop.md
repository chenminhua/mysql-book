# 代理技术 Proxy

## 静态代理

在 AOP(面向切面编程)中，我们需要定义一个切面类来编写需要横切业务逻辑的代码。此外，我们需要通过一个条件来匹配想要拦截的类，这个条件在 AOP 中被称为切点。

```java
public interface Hello{
	void say(String name);
}

public class HelloImpl implements Hello{
    public void say(String name) {
        System.out.println("hello" + name);
    }
}
```

如果我们想再 println 前面和后面分别加一点逻辑，直接把代码写入方法中吗？太不优雅了。

我们要使用代理模式。

写一个 HelloProxy 类
让它去调用 HelloImpl 的 say 方法，在调用前后加入逻辑。

````java
public class HelloProxy implements Hello{
    private Hello hello;

    public HelloProxy(){
        hello =  new HelloImpl();
    }

    public void say(String name){
        before();
        hello.say(name);
        after();
    }

    private void before(){
        System.out.println("before");
    }

    private void after(){
        System.out.println("after");
    }
}
```

## jdk动态代理

```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

public class DynamicProxy implements InvocationHandler {
    private Object target;
    public DynamicProxy(Object target){
        this.target = target;
    }

    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        before();
        Object result = method.invoke(target, args);
        after();
        return result;
    }

    private void before(){
        System.out.println(" before");
    }

    private void after(){
        System.out.println(" after");
    }

    public static void main(String[] args){
        Hello hello = new HelloImpl();
        DynamicProxy dynamicProxy = new DynamicProxy(hello);

        Hello helloProxy = (Hello) Proxy.newProxyInstance(
            hello.getClass().getClassLoader(),
            hello.getClass().getInterfaces(),
            dynamicProxy
        );

        helloProxy.say("jack");
    }
}
````

定义了一个 Object 类型的 target 变量，它就是被代理的目标。
我们在 main 函数中，**通过 DynamicProxy 类去包装 HelloImpl 实例**，然后再通过 Proxy 类的工厂方法 newProxyInstance 来动态创建一个 Hello 接口的代理类。

但是这个地方有点难用。我们来改进一下

```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

/**
 * Created by chenminhua on 11/16/15.
 */
public class DynamicProxy implements InvocationHandler {
    private Object target;
    public DynamicProxy(Object target){
        this.target = target;
    }

    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        before();
        Object result = method.invoke(target, args);
        after();
        return result;
    }

    @SuppressWarnings("unchecked")
    public <T> T getProxy(){
        return (T) Proxy.newProxyInstance(
                target.getClass().getClassLoader(),
                target.getClass().getInterfaces(),
                this
        );
    }

    private void before(){
        System.out.println(" before");
    }

    private void after(){
        System.out.println(" after");
    }

    public static void main(String[] args){
        Hello hello = new HelloImpl();
        DynamicProxy dynamicProxy = new DynamicProxy(hello);
        Hello helloProxy = dynamicProxy.getProxy();
        helloProxy.say("jack");
    }
}
```

这个动态代理的好处还是很明显的，接口变了，动态代理类是不用动的。

## CGlib 动态代理

```java
import net.sf.cglib.proxy.Enhancer;
import net.sf.cglib.proxy.MethodInterceptor;
import net.sf.cglib.proxy.MethodProxy;

import java.lang.reflect.Method;

public class CGLibProxy implements MethodInterceptor {
    public <T> T getProxy(Class<T> cls){
        return (T) Enhancer.create(cls, this);
    }

    public Object intercept(Object o, Method method, Object[] objects, MethodProxy methodProxy) throws Throwable {
        before();
        Object result = methodProxy.invokeSuper(o, objects);
        after();
        return result;
    }

    private void before(){
        System.out.println(" before");
    }

    private void after(){
        System.out.println(" after");
    }

    public static void main(String[] args){
        CGLibProxy cgLibProxy = new CGLibProxy();
        Hello helloProxy = cgLibProxy.getProxy(HelloImpl.class);
        helloProxy.say("jack");
    }
}
```

我们需要实现 CGLib 给我们提供的 MethodInterceptor 实现类，并填充 intercept 方法，方法最后一个 MethodProxy 类型的参数 methodProxy 值得注意。
CGLib 提供的是**方法级别的代理.**
也可以理解为对方法的拦截。
我们直接调用 invokeSuper，将被代理的对象以及方法参数传入其中。

**与 jdk 动态代理不同，这里不需要任何接口，对谁都可以生成动态对象**

```java
@Retention(AnnotationRetention.RUNTIME)
@Target(AnnotationTarget.FUNCTION, AnnotationTarget.TYPE_PARAMETER)
annotation class LimitingAnnotation(
        val intervalTime: Int = 60000,  // 默认 1 分钟 100 次
        val maxCount: Int = 100
)

data class Counter(
        val count: AtomicInteger,
        val lastResetTime: Long
)

// @Aspect注解 实现切面
@Aspect
@Component
class LimitingAop{

    val counterMap: ConcurrentHashMap<String, Counter> = ConcurrentHashMap()

    fun parseAnnotation(pjp: ProceedingJoinPoint): LimitingAnnotation {
        val method = (pjp.signature as MethodSignature).method
        return method.getAnnotation(LimitingAnnotation::class.java)
    }

    fun resetCounter(requestPath: String) {
        counterMap.put(requestPath, Counter(AtomicInteger(1), Date().time))
    }

    fun getRequestPath(request: HttpServletRequest): String {
        val uri = request.getAttribute(HandlerMapping.BEST_MATCHING_PATTERN_ATTRIBUTE) as String
        return "${uri}@[${request.method}]"

    }

    // 切点
    @Pointcut("@annotation(tech.blacklake.dev.manufacture.aop.LimitingAnnotation)")
    fun annotationPointCut(){}

    // 连接点
    @Around(value = "annotationPointCut()")
    fun hander(pjp: ProceedingJoinPoint): Any?{
        val request = (RequestContextHolder.getRequestAttributes() as ServletRequestAttributes).request
        val requestPath = getRequestPath(request)
        val annotation = parseAnnotation(pjp)
        val intervalTime = annotation.intervalTime
        val maxCount = annotation.maxCount

        val counter = counterMap.get(requestPath)
        if (counter == null) {
            resetCounter(requestPath)
        } else {
            val now = Date().time
            val lastTime = counter.lastResetTime
            val count = counter.count
            val diffTime = now - lastTime
            if (diffTime > intervalTime) {
                resetCounter(requestPath)
            } else {
                count.incrementAndGet()
                if (count.get() > maxCount) {
                    //println("exception $requestPath $count")
                    throw TooManyRequests(I18n.turnTo("manufacture388", arrayOf("$requestPath")))
                }
            }
        }

        return pjp.proceed()
    }
}
```
