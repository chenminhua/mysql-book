```java
class Foo implements InitializingBean, DisposableBean {
    public Bar bar;
    public Foo() { }
    public void setBar(Bar bar) {
        this.bar = bar;
    }

    @PostConstruct
    public void init() {
        System.out.println("------post construct------");
    }

    @PreDestroy
    public void destory() {
        System.out.println("------pre destroy------");
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        //Assert.notNull(this.bar, "bar can't be null");
        System.out.println("------after properties set------");
    }

    @Override
    public void destroy() throws Exception {
        this.bar = null;
    }
}

@Component
public class TestSmartLifecycle implements SmartLifecycle {
    private boolean isRunning = false;

    // 我们主要在该方法中启动任务或者其他异步服务，比如开启MQ接收消息。
    // 当上下文被刷新（所有对象已被实例化和初始化之后）时，将调用该方法。
    // 默认检查isAutoStartup()方法返回的布尔值为true,才调用此方法。
    @Override
    public void start() {
        System.out.println("start");
        // 执行完其他业务后，可以修改 isRunning = true
        isRunning = true;
    }


    // 如有多个实现类，start()的执行顺序按getPhase()从小到大执行。
    @Override
    public int getPhase() {
        // 默认为0
        return 0;
    }

    // 控制start方法是否自动执行
    @Override
    public boolean isAutoStartup() {
        // 默认为false
        return true;
    }

    @Override
    public boolean isRunning() {
        // 默认返回false
        return isRunning;
    }

    @Override
    public void stop(Runnable callback) {
        System.out.println("stop(Runnable)");
        callback.run();
        isRunning = false;
    }


    // 方法stop()和方法stop(Runnable callback)的区别只在于，后者是SmartLifecycle子类的专属。
    @Override
    public void stop() {
        System.out.println("stop");

        isRunning = false;
    }

}
```

```java
public interface Boom {}
public static class Boom1 implements Boom {}
public static class Boom2 implements Boom {}

@Bean
BoomFactoryBean boom() {
    return new BoomFactoryBean();
}

public static class BoomFactoryBean implements FactoryBean<Boom> {

    private boolean preferOne = true;
    public void setPreferOne(boolean preferOne) {
        this.preferOne = preferOne;
    }

    @Override
    public Boom getObject() throws Exception {
        return this.preferOne ? new Boom1() : new Boom2();
    }

    @Override
    public Class<?> getObjectType() {
        return null;
    }

    @Override
    public boolean isSingleton() {
        return false;
    }
}

```
