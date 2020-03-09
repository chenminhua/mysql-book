second "10 minutes a day plan"

hello spring, I hate you.

## reference

## todo list (想到啥就写啥咯)

如何换掉 servlet
jvm 那些乱七八糟的东西

## spring 有哪些模块

spring 架构

core, bean, context, jdbc, orm, jms, transaction, web, web-servlet, aop 等等。

核心容器（ApplicationContext）。BeanFactory 是 Spring 的核心。BeanFactory 实现是 XmlBeanFactory 类。BeanFactory 提供了 IOC。

ApplicationContext 通常的实现是什么?

- FileSystemXmlApplicationContext：此容器从一个 XML 文件中加载 beans 的定义，XMLBean 配置文件的全路径名必须提供给它的构造函数。
- ClassPathXmlApplicationContext：此容器也从一个 XML 文件中加载 beans 的定义，这里，你需要正确设置 classpath 因为这个容器将在 classpath 里找 bean 配置。
- WebXmlApplicationContext：此容器加载一个 XML 文件，此文件定义了一个 WEB 应用的所有 bean。

Bean 工厂和 Applicationcontexts 有什么区别？
Applicationcontexts 提供一种方法处理文本消息，一个通常的做法是加载文件资源（比如镜像），它们可以向注册为监听器的 bean 发布事件。另外，在容器或容器内的对象上执行的那些不得不由 bean 工厂以程序化方式处理的操作，可以在 Applicationcontexts 中以声明的方式处理。Applicationcontexts 实现了 MessageSource 接口，该接口的实现以可插拔的方式提供获取本地化消息的方法。

你怎样定义类的作用域?
当定义一个<bean>在 Spring 里，我们还能给这个 bean 声明一个作用域。它可以通过 bean 定义中的 scope 属性来定义。如，当 Spring 要在需要的时候每次生产一个新的 bean 实例，bean 的 scope 属性被指定为 prototype。另一方面，一个 bean 每次使用的时候必须返回同一个实例，这个 bean 的 scope 属性必须设为 singleton。

## bean 的生命周期。

- singleton:bean 在每个 Springioc 容器中只有一个实例。（默认声明周期）
- prototype：一个 bean 的定义可以有多个实例。
- request：每次 http 请求都会创建一个 bean，该作用域仅在基于 web 的 SpringApplicationContext 情形下有效。
- session：在一个 HTTPSession 中，一个 bean 定义对应一个实例。该作用域仅在基于 web 的 SpringApplicationContext 情形下有效。
- global-session：在一个全局的 HTTPSession 中，一个 bean 定义对应一个实例。仅在基于 web 的 SpringApplicationContext 情形下有效。
- 单例 bean 是线程安全的吗? 不。

实现

- Spring 容器从 XML 文件中读取 bean 的定义，并实例化 bean。
- Spring 根据 bean 的定义填充所有的属性。
- 如果 bean 实现了 BeanNameAware 接口，Spring 传递 bean 的 ID 到 setBeanName 方法。
- 如果 Bean 实现了 BeanFactoryAware 接口，Spring 传递 beanfactory 给 setBeanFactory 方法。
- 如果有任何与 bean 相关联的 BeanPostProcessors，Spring 会在 postProcesserBeforeInitialization()方法内调用它们。
- 如果 bean 实现 IntializingBean 了，调用它的 afterPropertySet 方法，如果 bean 声明了初始化方法，调用此初始化方法。
- 如果有 BeanPostProcessors 和 bean 关联，这些 bean 的 postProcessAfterInitialization()方法将被调用。
- 如果 bean 实现了 DisposableBean，它将调用 destroy()方法。

## 哪些是重要的 bean 生命周期方法？你能重载它们吗？

- 一个是 setup，它是在容器加载 bean 的时候被调用。
- 第二个方法是 teardown 它是在容器卸载类的时候被调用。
- 用它们你可以自己定制初始化和注销方法。它们也有相应的注解（@PostConstruct 和@PreDestroy）。

## @Required 注解

这个注解表明 bean 的属性必须在配置的时候设置，通过一个 bean 定义的显式的属性值或通过自动装配，若@Required 注解的 bean 属性未被设置，容器将抛出 BeanInitializationException。

## @Autowired 注解

@Autowired 注解提供了更细粒度的控制，包括在何处以及如何完成自动装配。它的用法和@Required 一样，修饰 setter 方法、构造器、属性或者具有任意名称和/或多个参数的 PN 方法。

## @Qualifier 注解

当有多个相同类型的 bean 却只有一个需要自动装配时，将@Qualifier 注解和@Autowire 注解结合使用以消除这种混淆，指定需要装配的确切的 bean。

## 异常处理

```java
// 1. 实现 HandlerExceptionResolver，然后配置一个 HandlerExceptionResolver
public class AppHandlerExceptionResolver implements HandlerExceptionResolver {
    @Override
     public ModelAndView resolveException(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        // ...
    }
}

@Bean
public AppHandlerExceptionResolver appHandlerExceptionResolver() {
    return new AppHandlerExceptionResolver();
}

// 2. 通过 @ControllerAdvice 和 @ExceptionHandler 注解。可以配置拦截指定的类或者包等
// @RestControllerAdvice 使 @ExceptionHandler 注解的方法默认具有 @ResponseBody 注解
@RestControllerAdvice(basePackageClasses = HelloWorldController.class)
public class AppExceptionHandlerAdvice {
    // 配置拦截的错误类型
    // 这里也可以返回 ModelAndView 导向错误视图
    @ExceptionHandler(Exception.class)
     public ResponseEntity<Object> responseEntity(Exception e) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON_UTF8);
        Map<String, Object> map = new HashMap<>();
        map.put("status", 400);
        map.put("message", e.getMessage());
        // 直接返回结果
        return new ResponseEntity<>(map, headers, HttpStatus.BAD_REQUEST);
    }
}
```

## DispatcherServlet

Spring 的 MVC 框架是围绕 DispatcherServlet 来设计的，它用来处理所有的 HTTP 请求和响应。

## WebApplicationContext

WebApplicationContext 继承了 ApplicationContext 并增加了一些 WEB 应用必备的特有功能，它不同于一般的 ApplicationContext，因为它能处理主题，并找到被关联的 servlet。
