start.spring.io 是一个可以用于快速生成项目骨架的网站

```java
@SpringBootApplication
@RestController
public class HelloSpringApplication {
  public static void main(String[] args) {
    SpringApplication.run(HelloSpringApplication.class, args);
  }

  @RequestMapping("/hello")
  public String hello() {
    return "Hello Spring";
  }
}
```

## spring 是如何解决循环依赖的

Spring 实例化 bean 是通过 ApplicationContext.getBean()方法来进行的。如果要获取的对象依赖了另一个对象，那么其首先会创建当前对象，然后通过递归的调用 ApplicationContext.getBean()方法来获取所依赖的对象，最后将获取到的对象注入到当前对象中。

- 首先尝试通过 getBean()方法获取 A 的实例，由于容器中还没有 A 对象实例，因而会创建一个 A 对象。
- 然后发现其依赖了 B 对象，因而会尝试递归的通过 getBean()方法获取 B 对象的实例。
- 但是 Spring 容器中此时也没有 B 对象的实例，因而其还是会先创建一个 B 对象的实例。
- 此时 A,B 对象都已经创建在 Spring 容器中了，只不过 A 对象的属性 b 和 B 对象的属性 a 都还没有设置。
- 创建 B 对象之后，发现 B 对象依赖了属性 A，还是会尝试递归的调用 getBean()方法获取 A 对象的实例。
- 因为已经有一个 A 实例，虽然只是半成品，但其也还是目标 bean，因而会将该 A 对象的实例返回。
- 此时，B 对象的属性 a 就设置进去了，然后就会将该 B 实例设置到 A 对象的属性 b 中。
