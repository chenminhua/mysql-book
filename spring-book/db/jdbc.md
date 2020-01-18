```xml
    <dependency>
			<groupId>com.h2database</groupId>
			<artifactId>h2</artifactId>
			<scope>runtime</scope>
		</dependency>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-test</artifactId>
			<scope>test</scope>
		</dependency>
```

### DataSource

```java
  @Autowired private DataSource dataSource;

	private void showConnection() throws SQLException {
		System.out.println(dataSource.toString());
		Connection conn = dataSource.getConnection();
		System.out.println(conn.toString());
		conn.close();
	}
```

### JdbcTemplate

```
@Autowired private JdbcTemplate jdbcTemplate;
jdbcTemplate.queryForList("select * from t1").forEach(row -> System.out.println(row.toString()));
```

数据源相关的 Bean: DataSource，根据选择的连接池实现决定

事务相关的 Bean: PlatformTransactionManager, DataSourceTransactionManager, TransactionTemplate

操作相关的 Bean: JdbcTemplate

### spring boot 替我们做了啥

通过 DataSourceAutoConfiguration 配置了 DataSource
通过 DataSourceTransactionManagerAutoConfiguration 配置了 DataSourceTransactionManager
通过 JdbcTemplateAutoConfiguration 配置了 JdbcTemplate

符合条件时才进行配置，如果你已经自己配置了一个 datasource，spring boot 就不给你配了。

### 数据源相关配置

```
spring.datasource.url=jdbc:mysql://localhost/test
spring.datasource.username=root
spring.datasource.password=dbpass
spring.datasource.driver-class-name=com.mysql.jdbc.Driver
```

### 多数据源
