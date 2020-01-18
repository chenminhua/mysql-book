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
